const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const Database = require('better-sqlite3');

const DB_PATH = path.join(__dirname, 'kernel_finance_pro_js.db');
let db;

const CATEGORIES = [
  'Food',
  'Transport',
  'Monthly Bills',
  'Stationary',
  'Party',
  'Shopping',
  'Others'
];

function hashText(value) {
  return crypto.createHash('sha256').update(String(value || ''), 'utf8').digest('hex');
}

function normUsername(username) {
  return String(username || '').trim().toLowerCase();
}

function normAnswer(answer) {
  return String(answer || '').trim().toLowerCase();
}

function nowIso() {
  return new Date().toISOString().slice(0, 19);
}

function openDb() {
  db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username_display TEXT NOT NULL,
      username_norm TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      security_answer_hash TEXT NOT NULL,
      currency TEXT NOT NULL DEFAULT 'INR',
      theme TEXT NOT NULL DEFAULT 'dark',
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      amount REAL NOT NULL,
      category TEXT NOT NULL,
      remark TEXT,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
  `);

  const cols = db.prepare("PRAGMA table_info(users)").all().map((r) => r.name);
  if (!cols.includes('currency')) db.exec("ALTER TABLE users ADD COLUMN currency TEXT NOT NULL DEFAULT 'INR'");
  if (!cols.includes('theme')) db.exec("ALTER TABLE users ADD COLUMN theme TEXT NOT NULL DEFAULT 'dark'");
}

function userById(id) {
  return db.prepare('SELECT * FROM users WHERE id = ?').get(id);
}

function userByUsername(username) {
  return db.prepare('SELECT * FROM users WHERE username_norm = ?').get(normUsername(username));
}

function safeUser(user) {
  if (!user) return null;
  return {
    id: user.id,
    usernameDisplay: user.username_display,
    currency: user.currency || 'INR',
    theme: user.theme || 'dark'
  };
}

function monthTotal(userId) {
  const now = new Date();
  const y = now.getFullYear();
  const m = now.getMonth() + 1;
  const rows = db.prepare('SELECT amount, created_at FROM transactions WHERE user_id = ?').all(userId);
  return rows.reduce((acc, r) => {
    const d = new Date(r.created_at);
    if (d.getFullYear() === y && d.getMonth() + 1 === m) return acc + Number(r.amount || 0);
    return acc;
  }, 0);
}

function monthlyCategoryTotals(userId) {
  const now = new Date();
  const y = now.getFullYear();
  const m = now.getMonth() + 1;
  const rows = db.prepare('SELECT amount, category, created_at FROM transactions WHERE user_id = ?').all(userId);
  const out = {};
  for (const c of CATEGORIES) out[c] = 0;
  for (const r of rows) {
    const d = new Date(r.created_at);
    if (d.getFullYear() === y && d.getMonth() + 1 === m) {
      if (!Object.prototype.hasOwnProperty.call(out, r.category)) out[r.category] = 0;
      out[r.category] += Number(r.amount || 0);
    }
  }
  return out;
}

function compareData(userId, mode, yearContext) {
  const rows = db.prepare('SELECT amount, created_at FROM transactions WHERE user_id = ?').all(userId);
  const now = new Date();

  if (mode === 'weekly') {
    const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const values = [0, 0, 0, 0, 0, 0, 0];
    const day = now.getDay();
    const monday = new Date(now);
    monday.setDate(now.getDate() - ((day + 6) % 7));
    monday.setHours(0, 0, 0, 0);
    for (const r of rows) {
      const d = new Date(r.created_at);
      const delta = Math.floor((d - monday) / 86400000);
      if (delta >= 0 && delta <= 6) values[delta] += Number(r.amount || 0);
    }
    return { labels, values };
  }

  if (mode === 'monthly') {
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const values = new Array(12).fill(0);
    for (const r of rows) {
      const d = new Date(r.created_at);
      if (d.getFullYear() === now.getFullYear()) values[d.getMonth()] += Number(r.amount || 0);
    }
    return { labels, values };
  }

  if (mode === 'yearly') {
    const map = new Map();
    for (const r of rows) {
      const y = new Date(r.created_at).getFullYear();
      map.set(y, (map.get(y) || 0) + Number(r.amount || 0));
    }
    const years = [...map.keys()].sort((a, b) => a - b);
    return { labels: years.map(String), values: years.map((y) => map.get(y)) };
  }

  if (mode === 'year-month') {
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const values = new Array(12).fill(0);
    const yr = Number(yearContext);
    for (const r of rows) {
      const d = new Date(r.created_at);
      if (d.getFullYear() === yr) values[d.getMonth()] += Number(r.amount || 0);
    }
    return { labels, values };
  }

  return { labels: [], values: [] };
}

function parseDate(value) {
  if (!value) return null;
  const d = new Date(value + 'T00:00:00');
  if (Number.isNaN(d.getTime())) return null;
  return d;
}

function filteredTransactions(userId, filters = {}) {
  const rows = db.prepare('SELECT id, amount, category, remark, created_at FROM transactions WHERE user_id = ? ORDER BY datetime(created_at) DESC').all(userId);
  const now = new Date();
  const fromDate = parseDate(filters.fromDate || '');
  const toDate = parseDate(filters.toDate || '');
  const minAmount = filters.minAmount === '' || filters.minAmount == null ? null : Number(filters.minAmount);
  const maxAmount = filters.maxAmount === '' || filters.maxAmount == null ? null : Number(filters.maxAmount);
  const remarkNeedle = String(filters.remark || '').trim().toLowerCase();
  const category = filters.category || null;
  const monthOnly = Boolean(filters.monthOnly);

  return rows.filter((r) => {
    const d = new Date(r.created_at);
    const dayDate = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    if (monthOnly && (d.getFullYear() !== now.getFullYear() || d.getMonth() !== now.getMonth())) return false;
    if (category && r.category !== category) return false;
    if (fromDate && dayDate < fromDate) return false;
    if (toDate && dayDate > toDate) return false;
    if (minAmount != null && Number(r.amount) < minAmount) return false;
    if (maxAmount != null && Number(r.amount) > maxAmount) return false;
    if (remarkNeedle && !String(r.remark || '').toLowerCase().includes(remarkNeedle)) return false;
    return true;
  });
}

function simplePdfBuffer(title, lines) {
  function esc(t) {
    return String(t).replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
  }
  const pageLines = 42;
  const pages = [];
  for (let i = 0; i < lines.length; i += pageLines) pages.push(lines.slice(i, i + pageLines));
  if (!pages.length) pages.push([]);

  const objects = [];
  let id = 1;
  const catalogId = id++;
  const pagesId = id++;
  const fontId = id++;
  const pageIds = [];
  const contentIds = [];
  for (let i = 0; i < pages.length; i++) {
    pageIds.push(id++);
    contentIds.push(id++);
  }

  objects.push([catalogId, `<< /Type /Catalog /Pages ${pagesId} 0 R >>`]);
  objects.push([pagesId, `<< /Type /Pages /Kids [${pageIds.map((p) => `${p} 0 R`).join(' ')}] /Count ${pageIds.length} >>`]);
  objects.push([fontId, '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']);

  for (let i = 0; i < pages.length; i++) {
    const pageObj = `<< /Type /Page /Parent ${pagesId} 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 ${fontId} 0 R >> >> /Contents ${contentIds[i]} 0 R >>`;
    objects.push([pageIds[i], pageObj]);
    let y = 800;
    const cmds = [];
    cmds.push(`BT /F1 14 Tf 50 ${y} Td (${esc(i === 0 ? title : `${title} (Page ${i + 1})`)}) Tj ET`);
    y -= 26;
    for (const line of pages[i]) {
      cmds.push(`BT /F1 11 Tf 50 ${y} Td (${esc(line)}) Tj ET`);
      y -= 18;
    }
    const stream = cmds.join('\n');
    objects.push([contentIds[i], `<< /Length ${Buffer.byteLength(stream, 'latin1')} >>\nstream\n${stream}\nendstream`]);
  }

  objects.sort((a, b) => a[0] - b[0]);
  const parts = [];
  parts.push(Buffer.from('%PDF-1.4\n%\xE2\xE3\xCF\xD3\n', 'binary'));
  const offsets = [0];
  let current = parts[0].length;

  for (const [objId, body] of objects) {
    offsets.push(current);
    const chunk = Buffer.from(`${objId} 0 obj\n${body}\nendobj\n`, 'latin1');
    parts.push(chunk);
    current += chunk.length;
  }

  const xrefPos = current;
  const xrefHeader = Buffer.from(`xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`, 'latin1');
  parts.push(xrefHeader);
  current += xrefHeader.length;
  for (let i = 1; i < offsets.length; i++) {
    const ln = Buffer.from(`${String(offsets[i]).padStart(10, '0')} 00000 n \n`, 'latin1');
    parts.push(ln);
    current += ln.length;
  }
  const trailer = Buffer.from(`trailer\n<< /Size ${objects.length + 1} /Root ${catalogId} 0 R >>\nstartxref\n${xrefPos}\n%%EOF\n`, 'latin1');
  parts.push(trailer);
  return Buffer.concat(parts);
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 760,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

function setupIpc() {
  ipcMain.handle('auth:createAccount', (_e, payload) => {
    const usernameDisplay = String(payload.username || '').trim();
    const usernameNorm = normUsername(payload.username);
    const password = String(payload.password || '');
    const answer = String(payload.securityAnswer || '').trim();
    if (!usernameDisplay || !usernameNorm) return { ok: false, error: 'Username cannot be empty.' };
    if (!password) return { ok: false, error: 'Password cannot be empty.' };
    if (!answer) return { ok: false, error: 'Security answer cannot be empty.' };

    try {
      db.prepare(`INSERT INTO users (username_display, username_norm, password_hash, security_answer_hash, currency, theme, created_at)
                  VALUES (?, ?, ?, ?, 'INR', 'dark', ?)`).run(usernameDisplay, usernameNorm, hashText(password), hashText(normAnswer(answer)), nowIso());
      return { ok: true };
    } catch (err) {
      if (String(err.message || '').toLowerCase().includes('unique')) return { ok: false, error: 'Username taken' };
      return { ok: false, error: 'Failed to create account.' };
    }
  });

  ipcMain.handle('auth:login', (_e, payload) => {
    const user = userByUsername(payload.username);
    if (!user) return { ok: false, error: 'Invalid username or password.' };
    if (user.password_hash !== hashText(payload.password || '')) return { ok: false, error: 'Invalid username or password.' };
    return { ok: true, user: safeUser(user), monthTotal: monthTotal(user.id) };
  });

  ipcMain.handle('auth:resetPassword', (_e, payload) => {
    const user = userByUsername(payload.username);
    if (!user) return { ok: false, error: 'Username or security answer is incorrect.' };
    if (user.security_answer_hash !== hashText(normAnswer(payload.securityAnswer || ''))) {
      return { ok: false, error: 'Username or security answer is incorrect.' };
    }
    if (!String(payload.newPassword || '')) return { ok: false, error: 'Password cannot be empty.' };
    db.prepare('UPDATE users SET password_hash = ? WHERE id = ?').run(hashText(payload.newPassword), user.id);
    return { ok: true };
  });

  ipcMain.handle('user:updateCurrency', (_e, payload) => {
    db.prepare('UPDATE users SET currency = ? WHERE id = ?').run(payload.currency, payload.userId);
    const user = userById(payload.userId);
    return { ok: true, user: safeUser(user), monthTotal: monthTotal(payload.userId) };
  });

  ipcMain.handle('user:updateTheme', (_e, payload) => {
    db.prepare('UPDATE users SET theme = ? WHERE id = ?').run(payload.theme, payload.userId);
    const user = userById(payload.userId);
    return { ok: true, user: safeUser(user) };
  });

  ipcMain.handle('user:updateProfile', (_e, payload) => {
    const usernameDisplay = String(payload.username || '').trim();
    const usernameNorm = normUsername(payload.username);
    if (!usernameDisplay || !usernameNorm) return { ok: false, error: 'Username cannot be empty.' };

    const existing = db.prepare('SELECT id FROM users WHERE username_norm = ?').get(usernameNorm);
    if (existing && existing.id !== payload.userId) return { ok: false, error: 'Username taken' };

    db.prepare('UPDATE users SET username_display = ?, username_norm = ? WHERE id = ?').run(usernameDisplay, usernameNorm, payload.userId);
    if (String(payload.newPassword || '').trim()) {
      db.prepare('UPDATE users SET password_hash = ? WHERE id = ?').run(hashText(payload.newPassword), payload.userId);
    }
    if (String(payload.securityAnswer || '').trim()) {
      db.prepare('UPDATE users SET security_answer_hash = ? WHERE id = ?').run(hashText(normAnswer(payload.securityAnswer)), payload.userId);
    }
    return { ok: true, user: safeUser(userById(payload.userId)) };
  });

  ipcMain.handle('tx:add', (_e, payload) => {
    const amount = Number(payload.amount);
    if (!Number.isFinite(amount) || amount <= 0) return { ok: false, error: 'Invalid amount.' };
    db.prepare('INSERT INTO transactions (user_id, amount, category, remark, created_at) VALUES (?, ?, ?, ?, ?)')
      .run(payload.userId, amount, payload.category, String(payload.remark || '').trim(), nowIso());
    return { ok: true, monthTotal: monthTotal(payload.userId) };
  });

  ipcMain.handle('tx:update', (_e, payload) => {
    const amount = Number(payload.amount);
    if (!Number.isFinite(amount) || amount <= 0) return { ok: false, error: 'Invalid amount.' };
    db.prepare('UPDATE transactions SET amount = ?, category = ?, remark = ? WHERE id = ? AND user_id = ?')
      .run(amount, payload.category, String(payload.remark || '').trim(), payload.txId, payload.userId);
    return { ok: true, monthTotal: monthTotal(payload.userId) };
  });

  ipcMain.handle('tx:delete', (_e, payload) => {
    db.prepare('DELETE FROM transactions WHERE id = ? AND user_id = ?').run(payload.txId, payload.userId);
    return { ok: true, monthTotal: monthTotal(payload.userId) };
  });

  ipcMain.handle('tx:list', (_e, payload) => {
    const rows = filteredTransactions(payload.userId, payload.filters || {});
    return { ok: true, rows };
  });

  ipcMain.handle('stats:monthTotal', (_e, userId) => ({ ok: true, value: monthTotal(userId) }));
  ipcMain.handle('stats:monthlyCategoryTotals', (_e, userId) => ({ ok: true, totals: monthlyCategoryTotals(userId) }));
  ipcMain.handle('stats:compare', (_e, payload) => ({ ok: true, ...compareData(payload.userId, payload.mode, payload.yearContext) }));

  ipcMain.handle('report:exportPdf', async (_e, payload) => {
    const rows = filteredTransactions(payload.userId, payload.filters || {});
    const { canceled, filePath } = await dialog.showSaveDialog({
      title: 'Export PDF',
      defaultPath: `kernelfinance_history_${Date.now()}.pdf`,
      filters: [{ name: 'PDF', extensions: ['pdf'] }]
    });
    if (canceled || !filePath) return { ok: false, canceled: true };
    const lines = rows.map((r) => `ID ${r.id} | ${String(r.created_at).slice(0, 10)} | ${r.category} | ${r.remark || '-'} | ${Number(r.amount).toFixed(2)}`);
    fs.writeFileSync(filePath, simplePdfBuffer(payload.title || 'KernelFinance Report', lines));
    return { ok: true, filePath };
  });

  ipcMain.handle('data:backup', async () => {
    const { canceled, filePath } = await dialog.showSaveDialog({
      title: 'Backup Database',
      defaultPath: `kernelfinance_backup_${Date.now()}.db`,
      filters: [{ name: 'DB', extensions: ['db'] }]
    });
    if (canceled || !filePath) return { ok: false, canceled: true };
    db.pragma('wal_checkpoint(FULL)');
    db.close();
    fs.copyFileSync(DB_PATH, filePath);
    openDb();
    return { ok: true, filePath };
  });

  ipcMain.handle('data:restore', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      title: 'Restore Database',
      properties: ['openFile'],
      filters: [{ name: 'DB', extensions: ['db'] }]
    });
    if (canceled || !filePaths || !filePaths[0]) return { ok: false, canceled: true };
    db.close();
    fs.copyFileSync(filePaths[0], DB_PATH);
    openDb();
    return { ok: true };
  });
}

app.whenReady().then(() => {
  openDb();
  setupIpc();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
