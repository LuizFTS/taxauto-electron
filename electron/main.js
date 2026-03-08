const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const axios = require('axios');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;
const pythonPath = path.join(__dirname, '..', 'backend', '.venv', 'Scripts', 'python.exe');

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 750,
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Carrega a ponte
      nodeIntegration: false,    // Segurança: Desativado
      contextIsolation: true     // Segurança: Ativado
    }
  });

  ipcMain.on('window-minimize', () => {
    mainWindow.minimize();
  });

  ipcMain.on('window-maximize', () => {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  });

  ipcMain.on('window-close', () => {
    mainWindow.close();
  });

  // Se estiver em dev, carrega o localhost do Angular. Se for prod, o arquivo dist.
  const startUrl = isDev
    ? 'http://localhost:4200'
    : `file://${path.join(__dirname, 'app-desktop/dist/app-desktop/browser/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    //mainWindow.webContents.openDevTools(); // Abre o console automaticamente em dev
  }

  mainWindow.on('closed', () => mainWindow = null);
}

async function waitBackendReady(url, interval = 500) {
  let ready = false;
  while (!ready) {
    try {
      const res = await axios.get(url);
      if (res.status === 200) {
        ready = true;
        console.log("Backend está pronto!");
        break;
      }
    } catch (error) {
      // Backend ainda não subiu
      await new Promise((r) => setTimeout(r, interval));
    }
  }
}

app.whenReady().then(async () => {
  console.log('Starting TaxAuto backend...');

  backendProcess = spawn(pythonPath, ["main.py"], {
    cwd: path.join(__dirname, "../backend"),
    stdio: ["pipe", "pipe", "pipe"] // stdin, stdout, stderr
  });

  // Redireciona logs para o terminal principal
  backendProcess.stdout.on("data", (data) => {
    process.stdout.write(`[BACKEND] ${data}`);
  });

  backendProcess.stderr.on("data", (data) => {
    process.stderr.write(`[BACKEND] ${data}`);
  });

  // Aguarda o backend subir
  await waitBackendReady("http://localhost:8000/health");

  // Cria a janela depois que o backend estiver pronto
  createWindow();

});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on("quit", () => {
  if (backendProcess) backendProcess.kill();
});