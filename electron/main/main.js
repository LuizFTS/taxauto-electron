const { app, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { autoUpdater } = require('electron-updater');

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

function copiarPastasIniciais() {
  const isDev = !app.isPackaged;

  // 1. Define os caminhos de ORIGEM (onde os arquivos estão após o build)
  const srcNazm = isDev
    ? path.join(app.getAppPath(), 'data', 'nazm')
    : path.join(process.resourcesPath, 'data', 'nazm');

  const srcTaxauto = isDev
    ? path.join(app.getAppPath(), 'data', 'taxauto')
    : path.join(process.resourcesPath, 'data', 'taxauto');

  // 2. Define os caminhos de DESTINO (%appdata%/TaxAuto)
  // app.getPath('userData') aponta automaticamente para %appdata%/TaxAuto no Windows
  const appDataPath = app.getPath('appData');
  const destNazm = path.join(appDataPath, 'nazm');
  const destTaxauto = path.join(appDataPath, 'taxauto');

  // Função auxiliar para copiar de forma recursiva (nativo do Node.js)
  /**
   * Copia arquivos de forma recursiva complementando o destino,
   * sem sobrescrever arquivos que já existem.
   */
  const copiarComplementando = (origem, destino) => {
    if (!fs.existsSync(origem)) {
      console.warn(`Aviso: Pasta de origem não encontrada em ${origem}`);
      return;
    }

    // Garante que a pasta de destino exista
    if (!fs.existsSync(destino)) {
      fs.mkdirSync(destino, { recursive: true });
    }

    // Lê todos os arquivos e subpastas da origem
    const itens = fs.readdirSync(origem);

    for (const item of itens) {
      const caminhoOrigem = path.join(origem, item);
      const caminhoDestino = path.join(destino, item);
      const stat = fs.statSync(caminhoOrigem);

      if (stat.isDirectory()) {
        // Se for uma pasta, chama a função recursivamente para ela
        copiarComplementando(caminhoOrigem, caminhoDestino);
      } else {
        // Se for um arquivo, só copia se ele NÃO existir no destino
        if (!fs.existsSync(caminhoDestino)) {
          fs.copyFileSync(caminhoOrigem, caminhoDestino);
          console.log(`Copiado (novo): ${item} -> ${caminhoDestino}`);
        } else {
          console.log(`Pulado (já existe): ${item}`);
        }
      }
    }
  };

  // Executa a cópia
  console.log("Iniciando sincronização de arquivos para o %appdata%...");
  copiarComplementando(srcNazm, destNazm);
  copiarComplementando(srcTaxauto, destTaxauto);
  console.log("Sincronização concluída!");
}

app.whenReady().then(async () => {
  copiarPastasIniciais();


  createLoadingWindow();
  console.log("Starting TaxAuto backend...");
  autoUpdater.checkForUpdatesAndNotify();

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


autoUpdater.on('update-available', (info) => {
  console.log('Update available: ', info.version);
});

autoUpdater.on('update-not-available', () => {
  console.log('Você já está na versão mais recente.');
});

autoUpdater.on('download-progress', (progress) => {
  console.log(`Baixando: ${Math.round(progress.percent)}%`);
});

autoUpdater.on('update-downloaded', (info) => {
  autoUpdater.quitAndInstall();
});

autoUpdater.on('error', (err) => {
  console.error('Erro no auto-update:', err);
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