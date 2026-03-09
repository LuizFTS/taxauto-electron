const { BrowserWindow, app } = require('electron');
const path = require('path');

let mainWindow;
const isDev = !app.isPackaged;

function createLoadingWindow() {

  loadingWindow = new BrowserWindow({
    width: 420,
    height: 260,
    frame: false,
    resizable: false,
    transparent: false,
    center: true,
    show: false,
    backgroundColor: '#141b2b',
    webPreferences: {
      contextIsolation: true
    }
  });

  loadingWindow.loadFile(
    path.join(__dirname, '../renderer/loading.html')
  );

  loadingWindow.once('ready-to-show', () => {
    loadingWindow.show();
  });

  return loadingWindow;
}


function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 750,
    frame: false,
    icon: path.join(__dirname, '../../build/icon.ico'),
    webPreferences: {
      preload: path.join(__dirname, '../preload/preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true
    }
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:4200');
  } else {

    const indexPath = path.join(
      app.getAppPath(),
      'app-desktop',
      'dist',
      'app-desktop',
      'browser',
      'index.html'
    )

    console.log('Loading: ', indexPath)
    mainWindow.loadFile(indexPath);
  }

  mainWindow.on('closed', () => (mainWindow = null));

  return mainWindow;
}

function getWindow() {
  return mainWindow;
}

module.exports = {
  createMainWindow,
  createLoadingWindow,
  getWindow,
};