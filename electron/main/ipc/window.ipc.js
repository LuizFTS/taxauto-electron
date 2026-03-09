const { ipcMain, app } = require('electron');
const { getWindow } = require('../window');

function registerWindowIPC() {

  ipcMain.on('window-minimize', () => {
    getWindow().minimize();
  });

  ipcMain.on('window-maximize', () => {
    const win = getWindow();

    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
    }
  });

  ipcMain.on('window-close', () => {
    app.quit();
  });

}

module.exports = registerWindowIPC;