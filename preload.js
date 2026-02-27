const { contextBridge, ipcRenderer } = require('electron');

// Expondo APIs seguras para o Window do Angular
contextBridge.exposeInMainWorld('electronAPI', {
  // Função que o Angular vai chamar: window.electronAPI.executarAutomacao(dados)
  executarAutomacao: (dados) => ipcRenderer.invoke('run-python-script', dados),

  // Exemplo de log vindo do processo principal
  onLog: (callback) => ipcRenderer.on('python-log', (event, value) => callback(value))
});