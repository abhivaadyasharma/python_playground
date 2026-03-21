const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('kernelApi', {
  createAccount: (payload) => ipcRenderer.invoke('auth:createAccount', payload),
  login: (payload) => ipcRenderer.invoke('auth:login', payload),
  resetPassword: (payload) => ipcRenderer.invoke('auth:resetPassword', payload),
  updateCurrency: (payload) => ipcRenderer.invoke('user:updateCurrency', payload),
  updateTheme: (payload) => ipcRenderer.invoke('user:updateTheme', payload),
  updateProfile: (payload) => ipcRenderer.invoke('user:updateProfile', payload),

  addTx: (payload) => ipcRenderer.invoke('tx:add', payload),
  updateTx: (payload) => ipcRenderer.invoke('tx:update', payload),
  deleteTx: (payload) => ipcRenderer.invoke('tx:delete', payload),
  listTx: (payload) => ipcRenderer.invoke('tx:list', payload),

  monthTotal: (userId) => ipcRenderer.invoke('stats:monthTotal', userId),
  monthlyCategoryTotals: (userId) => ipcRenderer.invoke('stats:monthlyCategoryTotals', userId),
  compareStats: (payload) => ipcRenderer.invoke('stats:compare', payload),

  exportPdf: (payload) => ipcRenderer.invoke('report:exportPdf', payload),
  backupDb: () => ipcRenderer.invoke('data:backup'),
  restoreDb: () => ipcRenderer.invoke('data:restore')
});
