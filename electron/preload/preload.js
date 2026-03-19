const { contextBridge, ipcRenderer, webUtils } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  send: (channel, data) => ipcRenderer.send(channel, data),
  invoke: (channel, data) => ipcRenderer.invoke(channel, data),

  getPort: async () => {
    return await ipcRenderer.invoke('get-backend-port');
  },

  focusWindow: () => {
    ipcRenderer.send('window-focus');
  },

  getFilePath: (file) => {
    return webUtils.getPathForFile(file);
  }
});