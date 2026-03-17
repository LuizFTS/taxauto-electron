const { app, dialog } = require('electron');

const { createLoadingWindow, createMainWindow, getWindow, closeLoading } = require('./window');
const { startBackend, stopBackend, killOldBackends, killPort } = require('./backend');
const waitBackend = require('../utils/waitBackend');
const registerWindowIPC = require('./ipc/window.ipc');

let backendPort = null;

const gotLock = app.requestSingleInstanceLock();

if (!gotLock) {

  app.quit();

} else {

  app.on('second-instance', () => {

    const win = getWindow();

    if (win) {
      if (win.isMinimized()) win.restore();
      win.focus();
    }

  });

}


app.whenReady().then(async () => {

  createLoadingWindow();
  console.log("Starting TaxAuto backend...");


  try {
    await killOldBackends();
    killPort(8000);

    await new Promise(resolve => setTimeout(resolve, 500));

    backendPort = await startBackend();
    if (!backendPort) {
      throw new Error("Backend did not return port");
    }

    const ready = await waitBackend(backendPort);

    if (!ready) {
      throw new Error("Backend startup timeout");
    }

    closeLoading();

    createMainWindow(backendPort);

    registerWindowIPC();

  } catch (error) {
    console.error(error);

    dialog.showErrorBox(
      "Startup Error",
      "Failed to start backend service."
    );

    app.quit();

  }

});


app.on('before-quit', () => {

  stopBackend();

});


app.on('window-all-closed', () => {

  stopBackend();

  if (process.platform !== 'darwin') {
    app.quit();
  }

});


app.on('quit', () => {

  stopBackend();
  process.exit(0);

});