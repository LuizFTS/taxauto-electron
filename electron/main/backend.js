const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const { app } = require('electron');
const { exec } = require('child_process');

const isDev = !app.isPackaged;
let backendProcess = null;
let backendPort = null;

function getBackendPath() {
  if (isDev) {
    return path.join(__dirname, '../../local-backend/.venv/Scripts/python.exe');
  }
  return path.join(process.resourcesPath, 'backend', 'backend.exe');
}

function startBackend() {
  return new Promise((resolve, reject) => {
    const backendPath = getBackendPath();
    const cwd = isDev
      ? path.join(__dirname, '../../local-backend')
      : path.join(process.resourcesPath, 'backend');

    console.log(`[BACKEND] isDev: ${isDev}`);
    console.log(`[BACKEND] backendPath: ${backendPath}`);
    console.log(`[BACKEND] cwd: ${cwd}`);
    console.log(`[BACKEND] exe exists: ${fs.existsSync(backendPath)}`);
    console.log(`[BACKEND] cwd exists: ${fs.existsSync(cwd)}`);

    // Lista arquivos na pasta do backend para confirmar o que foi empacotado
    if (fs.existsSync(cwd)) {
      console.log(`[BACKEND] files in cwd: ${fs.readdirSync(cwd).join(', ')}`);
    }

    if (!fs.existsSync(backendPath)) {
      return reject(new Error(`backend.exe não encontrado: ${backendPath}`));
    }

    backendProcess = isDev
      ? spawn(backendPath, ['main.py'], { cwd, stdio: 'pipe' })
      : spawn(backendPath, [], { cwd, stdio: 'pipe', windowsHide: true });

    console.log(`[BACKEND] PID: ${backendProcess.pid}`);

    let resolved = false;

    function handleOutput(source, data) {
      const text = data.toString();
      console.log(`[BACKEND ${source}]: ${text.trim()}`);

      const match = text.match(/PORT=(\d+)/);
      if (match && !resolved) {
        resolved = true;
        backendPort = parseInt(match[1], 10);
        console.log(`[BACKEND] Porta capturada: ${backendPort}`);
        resolve(backendPort);
      }
    }

    backendProcess.stdout.on('data', (d) => handleOutput('STDOUT', d));
    backendProcess.stderr.on('data', (d) => handleOutput('STDERR', d));

    backendProcess.on('error', (err) => {
      console.error(`[BACKEND] Spawn error: ${err.message}`);
      reject(err);
    });

    backendProcess.on('exit', (code, signal) => {
      console.log(`[BACKEND] Exit — code: ${code}, signal: ${signal}`);
      backendProcess = null;
      if (!resolved) {
        reject(new Error(`Backend exited (code ${code}) before returning PORT`));
      }
    });

    // Timeout de segurança — se em 20s não resolver, rejeita
    setTimeout(() => {
      if (!resolved) {
        console.error(`[BACKEND] Timeout — PORT nunca recebido`);
        reject(new Error('Backend startup timeout (20s)'));
      }
    }, 60000);
  });
}

function stopBackend() {
  if (!backendProcess) return;
  console.log(`[BACKEND] Encerrando PID: ${backendProcess.pid}`);
  try {
    if (process.platform === 'win32') {
      exec(`taskkill /pid ${backendProcess.pid} /T /F`);
    } else {
      backendProcess.kill('SIGTERM');
    }
  } catch (error) {
    console.error('[BACKEND] Erro ao encerrar:', error);
  }
  backendProcess = null;
}

function killOldBackends() {
  return new Promise((resolve) => {
    if (process.platform !== 'win32') return resolve();

    console.log('[BACKEND] Matando instâncias antigas de backend.exe...');
    exec('taskkill /IM backend.exe /F /T', () => {
      // aguarda o taskkill terminar antes de resolver
      setTimeout(resolve, 300); // margem extra para o OS liberar
    });
  });
}

function killPort(port) {
  if (process.platform !== 'win32') return;
  console.log(`[BACKEND] Liberando porta ${port}...`);
  exec(
    `for /f "tokens=5" %a in ('netstat -ano ^| findstr :${port}') do taskkill /PID %a /F`,
    (err, stdout) => {
      if (stdout) console.log(`[BACKEND] killPort: ${stdout.trim()}`);
    }
  );
}

function getPort() {
  return backendPort;
}

module.exports = {
  startBackend,
  stopBackend,
  killOldBackends,
  killPort,
  getPort,
};