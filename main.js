const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;

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

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});