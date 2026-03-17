const { ipcMain, app, dialog } = require('electron');
const { getWindow, getFocusedWindow, getAllWindows } = require('../window');
const { getPort, stopBackend } = require('../backend');

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
    const win = getAllWindows()[0];

    if (win) {
      win.hide();
    }

    stopBackend();

    setTimeout(() => {
      app.quit();
    }, 200);

  });

  ipcMain.on('window-focus', () => {
    const win = getAllWindows()[0];

    if (!win) return;

    if (win.isMinimized()) {
      win.restore();
    }

    win.focus();
  });

  ipcMain.handle('select-directory', async () => {
    const focusedWindow = getFocusedWindow();

    const result = await dialog.showOpenDialog(focusedWindow, {
      title: 'Selecione a pasta de destino',
      buttonLabel: 'Selecionar pasta',
      properties: ['openDirectory', 'createDirectory', 'showHiddenFiles'],
      filters: [
        { name: 'Arquivos de Referência', extensions: ['csv', 'pdf'] }
      ]
    });

    return result.canceled ? null : result.filePaths[0]
  })

  ipcMain.handle('get-backend-port', async () => {
    return getPort();
  });


}

module.exports = registerWindowIPC;