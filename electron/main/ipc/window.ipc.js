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

  ipcMain.handle('select-directory', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory']
    });

    if (result.canceled) {
      return null;
    } else {
      return result.filePaths[0];
    }
  })

}

module.exports = registerWindowIPC;