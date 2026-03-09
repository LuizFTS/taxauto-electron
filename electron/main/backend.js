const path = require('path');
const { spawn } = require('child_process');
const { app } = require('electron')
const { exec } = require('child_process');

const isDev = !app.isPackaged;
let backendProcess = null;
let backendPort = null;

function getBackendPath() {
  if (isDev) {
    return path.join(__dirname, '../../backend/.venv/Scripts/python.exe');
  }

  return path.join(process.resourcesPath, 'backend', 'backend.exe');
}

function startBackend() {

  return new Promise((resolve, reject) => {

    const backendPath = getBackendPath();

    if (backendProcess) {
      return resolve(backendPort);
    }

    backendProcess = isDev
      ? spawn(backendPath, ['main.py'], {
        cwd: path.join(__dirname, '../../backend'),
        stdio: 'pipe'
      })
      : spawn(backendPath, [], {
        stdio: 'pipe',
        windowsHide: true
      });

    backendProcess.stdout.on('data', (data) => {

      const text = data.toString();
      process.stdout.write(`[BACKEND] ${text}`);

      const match = text.match(/PORT=(\d+)/);

      if (match) {
        backendPort = parseInt(match[1], 10);
        resolve(backendPort);
      }

    });

    backendProcess.stderr.on('data', (data) => {
      process.stderr.write(`[BACKEND] ${data}`);
    });

    backendProcess.on('exit', (code) => {
      console.error(`Backend finalizado: ${code}`);
      backendProcess = null;
    });

    backendProcess.on('error', reject);

  });
}

function stopBackend() {
  if (!backendProcess) return;

  if (process.platform === 'win32') {

    exec(`taskkill /pid ${backendProcess.pid} /T /F`);

  } else {

    backendProcess.kill('SIGTERM');

  }
}

function killOldBackends() {
  if (process.platform === 'win32') {
    exec('taskkill /IM backend.exe /F /T', () => { });
  }
}

function killPort(port) {

  if (process.platform !== 'win32') return;

  exec(`for /f "tokens=5" %a in ('netstat -ano ^| findstr :${port}') do taskkill /PID %a /F`, () => { });

}

function closeLoading() {
  if (loadingWindow) {
    loadingWindow.close();
    loadingWindow = null;
  }
}


module.exports = {
  startBackend,
  stopBackend,
  closeLoading,
  killOldBackends,
  killPort
};