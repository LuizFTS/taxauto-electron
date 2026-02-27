const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = require('electron-is-dev');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 750,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Carrega a ponte
      nodeIntegration: false,    // Segurança: Desativado
      contextIsolation: true     // Segurança: Ativado
    }
  });

  // Se estiver em dev, carrega o localhost do Angular. Se for prod, o arquivo dist.
  const startUrl = isDev
    ? 'http://localhost:4200'
    : `file://${path.join(__dirname, 'app-desktop/dist/app-desktop/browser/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools(); // Abre o console automaticamente em dev
  }

  mainWindow.on('closed', () => mainWindow = null);
}

// --- Lógica para Executar Python ---
ipcMain.handle('run-python-script', async (event, dados) => {
  return new Promise((resolve, reject) => {
    // Caminho para o script (ajuste conforme sua pasta)
    const scriptPath = path.join(__dirname, 'resources/scripts/bot_automacao.py');

    // Comando: python resources/scripts/bot_automacao.py '{"param": "valor"}'
    // Dica: Se usar venv, troque 'python' pelo caminho do executável do venv
    const pythonProcess = spawn('python', [scriptPath, JSON.stringify(dados)]);

    let result = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
      // Opcional: Enviar logs em tempo real para o Angular
      mainWindow.webContents.send('python-log', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          resolve(JSON.parse(result)); // Devolve o JSON do Python para o Angular
        } catch (e) {
          resolve({ status: 'sucesso', raw: result });
        }
      } else {
        reject(`Erro no Python (Código ${code}): ${errorOutput}`);
      }
    });
  });
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});