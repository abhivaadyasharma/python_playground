const CATEGORIES = ['Food', 'Transport', 'Monthly Bills', 'Stationary', 'Party', 'Shopping', 'Others'];
const CATEGORY_COLORS = {
  Food: '#ff5e5b',
  Transport: '#4aa3ff',
  'Monthly Bills': '#ffd166',
  Stationary: '#56f39a',
  Party: '#c084fc',
  Shopping: '#ff9f1c',
  Others: '#94a3b8'
};
const CURRENCIES = [['INR', '₹'], ['USD', '$'], ['EUR', '€'], ['GBP', '£'], ['JPY', '¥'], ['AED', 'د.إ']];

const state = {
  user: null,
  monthTotal: 0,
  authMode: 'login',
  screen: 'dashboard',
  message: '',
  error: '',
  txRows: [],
  selectedTxId: null,
  pieCategoryRows: [],
  selectedPieCategory: null,
  compareMode: 'monthly',
  compareYear: null,
  barMeta: []
};

const appEl = document.getElementById('app');

function symbolFor(currency) {
  const f = CURRENCIES.find(([c]) => c === currency);
  return f ? f[1] : '₹';
}
function fmtAmount(v) { return `${symbolFor(state.user?.currency || 'INR')} ${Number(v || 0).toFixed(2)}`; }
function esc(s) { return String(s ?? '').replace(/[&<>"]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m])); }
function setMsg(msg = '', err = '') { state.message = msg; state.error = err; }

function applyTheme() {
  const root = document.documentElement;
  const dark = {
    '--bg': '#1e1f22', '--panel': '#24262b', '--panel-alt': '#2c2f36', '--text': '#39ff14', '--muted': '#8ce88a',
    '--danger': '#ff7373', '--btn-bg': '#2d3a2d', '--btn-active': '#3d4f3d', '--entry-bg': '#121315', '--entry-fg': '#d7ffd1'
  };
  const light = {
    '--bg': '#f2f5f3', '--panel': '#e1e8e3', '--panel-alt': '#d4dfd8', '--text': '#0f6b2b', '--muted': '#2f7f45',
    '--danger': '#b73333', '--btn-bg': '#b8cdbd', '--btn-active': '#a8c0ae', '--entry-bg': '#fbfdfb', '--entry-fg': '#194e2a'
  };
  const theme = state.user?.theme === 'light' ? light : dark;
  Object.entries(theme).forEach(([k, v]) => root.style.setProperty(k, v));
}

function render() {
  applyTheme();
  if (!state.user) return renderAuth();
  renderApp();
}

function logoHtml() {
  return `<img class="logo" src="../../assets/logo.png" onerror="this.style.display='none'" alt="logo">`;
}
function smallLogoHtml() {
  return `<img class="small-logo" src="../../assets/logo.png" onerror="this.style.display='none'" alt="logo">`;
}

function renderAuth() {
  const isLogin = state.authMode === 'login';
  const isCreate = state.authMode === 'create';
  const isForgot = state.authMode === 'forgot';

  appEl.innerHTML = `
    <div class="auth">
      <div class="card">
        <div class="logo-row">${logoHtml()}</div>
        <h1>${isLogin ? 'KernelFinance Pro' : isCreate ? 'Create Account' : 'Reset Password'}</h1>
        ${isLogin ? loginFormHtml() : ''}
        ${isCreate ? createFormHtml() : ''}
        ${isForgot ? forgotFormHtml() : ''}
        ${state.message ? `<div class="notice">${esc(state.message)}</div>` : ''}
        ${state.error ? `<div class="error">${esc(state.error)}</div>` : ''}
      </div>
    </div>
  `;

  if (isLogin) bindLogin();
  if (isCreate) bindCreate();
  if (isForgot) bindForgot();
}

function loginFormHtml() {
  return `
    <div class="field"><label>Username</label><input id="login-username"></div>
    <div class="field"><label>Password</label><input id="login-password" type="password"></div>
    <button class="btn" id="btn-login">Login</button>
    <button class="btn" id="btn-to-create">New? Create Account</button>
    <button class="btn" id="btn-to-forgot">Forgot Password?</button>
  `;
}
function createFormHtml() {
  return `
    <div class="field"><label>Username</label><input id="create-username"></div>
    <div class="field"><label>Password</label><input id="create-password" type="password"></div>
    <div class="field"><label>Confirm Password</label><input id="create-confirm" type="password"></div>
    <div class="field"><label>Security Answer</label><input id="create-security"></div>
    <button class="btn" id="btn-create">Create Account</button>
    <button class="btn" id="btn-create-back">Back to Login</button>
  `;
}
function forgotFormHtml() {
  return `
    <div class="field"><label>Username</label><input id="forgot-username"></div>
    <div class="field"><label>Security Answer</label><input id="forgot-security"></div>
    <div class="field"><label>New Password</label><input id="forgot-password" type="password"></div>
    <div class="field"><label>Confirm New Password</label><input id="forgot-confirm" type="password"></div>
    <button class="btn" id="btn-forgot">Reset Password</button>
    <button class="btn" id="btn-forgot-back">Back to Login</button>
  `;
}

function bindLogin() {
  document.getElementById('btn-to-create').onclick = () => { setMsg(); state.authMode = 'create'; render(); };
  document.getElementById('btn-to-forgot').onclick = () => { setMsg(); state.authMode = 'forgot'; render(); };
  document.getElementById('btn-login').onclick = async () => {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const res = await window.kernelApi.login({ username, password });
    if (!res.ok) return (setMsg('', res.error), render());
    state.user = res.user;
    state.monthTotal = res.monthTotal;
    setMsg();
    state.screen = 'dashboard';
    render();
  };
}
function bindCreate() {
  document.getElementById('btn-create-back').onclick = () => { setMsg(); state.authMode = 'login'; render(); };
  document.getElementById('btn-create').onclick = async () => {
    const username = document.getElementById('create-username').value;
    const password = document.getElementById('create-password').value;
    const confirm = document.getElementById('create-confirm').value;
    const securityAnswer = document.getElementById('create-security').value;
    if (password !== confirm) return (setMsg('', 'Password and confirm password do not match.'), render());
    const res = await window.kernelApi.createAccount({ username, password, securityAnswer });
    if (!res.ok) return (setMsg('', res.error), render());
    state.authMode = 'login';
    setMsg('Account created. Please login.', '');
    render();
  };
}
function bindForgot() {
  document.getElementById('btn-forgot-back').onclick = () => { setMsg(); state.authMode = 'login'; render(); };
  document.getElementById('btn-forgot').onclick = async () => {
    const username = document.getElementById('forgot-username').value;
    const securityAnswer = document.getElementById('forgot-security').value;
    const newPassword = document.getElementById('forgot-password').value;
    const confirm = document.getElementById('forgot-confirm').value;
    if (newPassword !== confirm) return (setMsg('', 'New password and confirm password do not match.'), render());
    const res = await window.kernelApi.resetPassword({ username, securityAnswer, newPassword });
    if (!res.ok) return (setMsg('', res.error), render());
    state.authMode = 'login';
    setMsg('Password reset successful. Please login.', '');
    render();
  };
}

function headerHtml(back = false) {
  const cOptions = CURRENCIES.map(([c, s]) => `<option value="${c}" ${state.user.currency === c ? 'selected' : ''}>${c} (${s})</option>`).join('');
  const tOptions = ['dark', 'light'].map((t) => `<option value="${t}" ${state.user.theme === t ? 'selected' : ''}>${t[0].toUpperCase() + t.slice(1)}</option>`).join('');
  return `
    <div class="header">
      <div class="left">${smallLogoHtml()}<h2>Hello ${esc(state.user.usernameDisplay)}</h2>${back ? '<button class="btn back-btn" id="btn-back">Back</button>' : ''}</div>
      <div class="center"><h3>Total Expenditure (This Month): ${fmtAmount(state.monthTotal)}</h3></div>
      <div class="right">
        <label>Currency:</label>
        <select id="sel-currency" class="header-select">${cOptions}</select>
        <label>Theme:</label>
        <select id="sel-theme" class="header-select">${tOptions}</select>
      </div>
    </div>
  `;
}

function renderApp() {
  const withBack = state.screen !== 'dashboard';
  let content = '';
  if (state.screen === 'dashboard') content = dashboardHtml();
  if (state.screen === 'add') content = addHtml();
  if (state.screen === 'history') content = historyHtml();
  if (state.screen === 'pie') content = pieHtml();
  if (state.screen === 'compare') content = compareHtml();
  if (state.screen === 'profile') content = profileHtml();
  if (state.screen === 'data') content = dataToolsHtml();

  appEl.innerHTML = `<div class="page">${headerHtml(withBack)}<div class="panel">${content}</div><div class="logout-wrap"><button class="btn" id="btn-logout">Logout</button></div></div>`;

  bindHeader();
  document.getElementById('btn-logout').onclick = () => {
    state.user = null;
    state.screen = 'dashboard';
    state.authMode = 'login';
    setMsg();
    render();
  };

  if (state.screen === 'dashboard') bindDashboard();
  if (state.screen === 'add') bindAdd();
  if (state.screen === 'history') bindHistory();
  if (state.screen === 'pie') bindPie();
  if (state.screen === 'compare') bindCompare();
  if (state.screen === 'profile') bindProfile();
  if (state.screen === 'data') bindDataTools();
}

function bindHeader() {
  const back = document.getElementById('btn-back');
  if (back) back.onclick = () => { state.screen = 'dashboard'; setMsg(); render(); };

  document.getElementById('sel-currency').onchange = async (e) => {
    const res = await window.kernelApi.updateCurrency({ userId: state.user.id, currency: e.target.value });
    if (res.ok) {
      state.user = res.user;
      state.monthTotal = res.monthTotal;
      render();
    }
  };

  document.getElementById('sel-theme').onchange = async (e) => {
    const res = await window.kernelApi.updateTheme({ userId: state.user.id, theme: e.target.value });
    if (res.ok) {
      state.user = res.user;
      render();
    }
  };
}

function dashboardHtml() {
  const item = (id, title, desc) => `<div class="menu-item"><button class="btn" id="${id}">${title}</button><p>${desc}</p></div>`;
  return `
    <h2>Dashboard Menu</h2>
    ${item('go-add', 'Add Transaction', 'Add a new expense with value, category, and remark.')}
    ${item('go-history', 'View Transaction History', 'See all transactions with filters, edit/delete and PDF export.')}
    ${item('go-pie', 'Monthly Expenditure Pie Chart', 'View monthly category split and category-wise monthly history below.')}
    ${item('go-compare', 'Compare Your Expenditure In Bargraphs', 'Compare weekly/monthly/yearly values with drill-down.')}
    ${item('go-profile', 'Edit Profile', 'Change username, password and security answer.')}
    ${item('go-data', 'Backup / Restore Database', 'Backup database and restore from file.')}
  `;
}
function bindDashboard() {
  document.getElementById('go-add').onclick = () => { state.screen = 'add'; setMsg(); render(); };
  document.getElementById('go-history').onclick = async () => { state.screen = 'history'; await loadHistory(); render(); };
  document.getElementById('go-pie').onclick = async () => { state.screen = 'pie'; await loadPieData(); render(); };
  document.getElementById('go-compare').onclick = async () => { state.screen = 'compare'; state.compareMode = 'monthly'; state.compareYear = null; render(); };
  document.getElementById('go-profile').onclick = () => { state.screen = 'profile'; setMsg(); render(); };
  document.getElementById('go-data').onclick = () => { state.screen = 'data'; setMsg(); render(); };
}

function addHtml() {
  return `
    <h2>${state.editTx ? 'Edit Transaction' : 'Add Transaction'}</h2>
    <div class="form-grid">
      <div class="field"><label>Value</label><input id="add-value" type="number" step="0.01" value="${state.editTx ? esc(Number(state.editTx.amount).toFixed(2)) : ''}"></div>
      <div class="field"><label>Category</label><select id="add-category">${CATEGORIES.map((c) => `<option ${state.editTx?.category === c ? 'selected' : ''}>${c}</option>`).join('')}</select></div>
      <div class="field"><label>Remark</label><input id="add-remark" value="${esc(state.editTx?.remark || '')}"></div>
      <button class="btn" id="btn-save-add">${state.editTx ? 'Save Changes' : 'Register Transaction'}</button>
      ${state.message ? `<div class="notice">${esc(state.message)}</div>` : ''}
      ${state.error ? `<div class="error">${esc(state.error)}</div>` : ''}
    </div>
  `;
}
function bindAdd() {
  document.getElementById('add-value').focus();
  document.getElementById('btn-save-add').onclick = async () => {
    const amount = Number(document.getElementById('add-value').value);
    const category = document.getElementById('add-category').value;
    const remark = document.getElementById('add-remark').value;
    let res;
    if (state.editTx) {
      res = await window.kernelApi.updateTx({ userId: state.user.id, txId: state.editTx.id, amount, category, remark });
    } else {
      res = await window.kernelApi.addTx({ userId: state.user.id, amount, category, remark });
    }
    if (!res.ok) return (setMsg('', res.error || 'Failed.'), render());
    state.monthTotal = res.monthTotal;
    state.editTx = null;
    setMsg(state.editTx ? 'Transaction updated.' : 'Transaction registered.', '');
    state.screen = 'dashboard';
    render();
  };
}

function historyHtml() {
  const rows = state.txRows.map((r) => `
    <tr data-id="${r.id}" class="${state.selectedTxId === r.id ? 'selected' : ''}">
      <td>${r.id}</td>
      <td>${esc(String(r.created_at).slice(0, 10))}</td>
      <td>${esc(r.category)}</td>
      <td>${esc(r.remark || '-')}</td>
      <td>${fmtAmount(r.amount)}</td>
    </tr>
  `).join('');

  return `
    <h2>Transaction History</h2>
    <div class="row">
      <div class="field"><label>From Date (YYYY-MM-DD)</label><input id="f-from" value="${esc(state.filters?.fromDate || '')}"></div>
      <div class="field"><label>To Date (YYYY-MM-DD)</label><input id="f-to" value="${esc(state.filters?.toDate || '')}"></div>
      <div class="field"><label>Min Amount</label><input id="f-min" value="${esc(state.filters?.minAmount || '')}"></div>
      <div class="field"><label>Max Amount</label><input id="f-max" value="${esc(state.filters?.maxAmount || '')}"></div>
      <div class="field"><label>Remark Contains</label><input id="f-remark" value="${esc(state.filters?.remark || '')}"></div>
      <button class="btn" id="btn-filter">Apply Filters</button>
      <button class="btn" id="btn-reset">Reset</button>
      <button class="btn" id="btn-export">Export PDF</button>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>ID</th><th>Date</th><th>Category</th><th>Remark</th><th>Value</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
    <div class="row" style="margin-top:8px">
      <button class="btn" id="btn-edit">Edit Selected</button>
      <button class="btn" id="btn-delete">Delete Selected</button>
    </div>
    ${state.message ? `<div class="notice">${esc(state.message)}</div>` : ''}
    ${state.error ? `<div class="error">${esc(state.error)}</div>` : ''}
  `;
}

async function loadHistory(extra = {}) {
  state.filters = { ...(state.filters || {}), ...extra };
  const res = await window.kernelApi.listTx({ userId: state.user.id, filters: state.filters });
  if (res.ok) state.txRows = res.rows;
}
function bindHistory() {
  appEl.querySelectorAll('tbody tr').forEach((tr) => {
    tr.onclick = () => { state.selectedTxId = Number(tr.dataset.id); render(); };
  });

  document.getElementById('btn-filter').onclick = async () => {
    await loadHistory({
      fromDate: document.getElementById('f-from').value.trim(),
      toDate: document.getElementById('f-to').value.trim(),
      minAmount: document.getElementById('f-min').value.trim(),
      maxAmount: document.getElementById('f-max').value.trim(),
      remark: document.getElementById('f-remark').value.trim()
    });
    render();
  };
  document.getElementById('btn-reset').onclick = async () => {
    state.filters = {};
    state.selectedTxId = null;
    await loadHistory({});
    render();
  };
  document.getElementById('btn-export').onclick = async () => {
    const res = await window.kernelApi.exportPdf({ userId: state.user.id, filters: state.filters || {}, title: 'KernelFinance Transaction History' });
    if (res.ok) setMsg(`PDF saved at ${res.filePath}`, ''); else if (!res.canceled) setMsg('', 'PDF export failed.');
    render();
  };
  document.getElementById('btn-edit').onclick = () => {
    if (!state.selectedTxId) return alert('Select a transaction first.');
    const tx = state.txRows.find((r) => r.id === state.selectedTxId);
    if (!tx) return;
    state.editTx = tx;
    state.screen = 'add';
    render();
  };
  document.getElementById('btn-delete').onclick = async () => {
    if (!state.selectedTxId) return alert('Select a transaction first.');
    if (!confirm('Delete this transaction?')) return;
    const res = await window.kernelApi.deleteTx({ userId: state.user.id, txId: state.selectedTxId });
    if (!res.ok) return alert('Delete failed.');
    state.monthTotal = res.monthTotal;
    state.selectedTxId = null;
    await loadHistory({});
    setMsg('Transaction deleted.', '');
    render();
  };
}

function pieHtml() {
  return `
    <h2>This Month Category Split</h2>
    <div class="notice">Click a pie slice to view that category's history for this month below.</div>
    <div class="canvas-wrap">
      <canvas id="pie-canvas" width="460" height="340"></canvas>
      <div style="min-width:320px; flex:1">
        <div class="legend" id="pie-legend"></div>
      </div>
    </div>
    <h3 style="margin-top:12px">Category History (Current Month): ${esc(state.selectedPieCategory || 'Click a slice')}</h3>
    <div class="table-wrap" style="max-height:280px">
      <table>
        <thead><tr><th>Date</th><th>Remark</th><th>Value</th></tr></thead>
        <tbody>
          ${(state.pieCategoryRows.length ? state.pieCategoryRows : []).map((r) => `<tr><td>${esc(String(r.created_at).slice(0, 10))}</td><td>${esc(r.remark || '-')}</td><td>${fmtAmount(r.amount)}</td></tr>`).join('') || '<tr><td colspan="3">No rows</td></tr>'}
        </tbody>
      </table>
    </div>
  `;
}

async function loadPieData() {
  const totalsRes = await window.kernelApi.monthlyCategoryTotals(state.user.id);
  state.pieTotals = totalsRes.ok ? totalsRes.totals : {};
  if (state.selectedPieCategory) await loadPieCategoryRows(state.selectedPieCategory);
}
async function loadPieCategoryRows(cat) {
  const rows = await window.kernelApi.listTx({ userId: state.user.id, filters: { category: cat, monthOnly: true } });
  state.pieCategoryRows = rows.ok ? rows.rows : [];
}
function bindPie() {
  drawPie();
}
function drawPie() {
  const canvas = document.getElementById('pie-canvas');
  const legend = document.getElementById('pie-legend');
  if (!canvas || !legend) return;
  legend.innerHTML = '';

  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const totals = state.pieTotals || {};
  const entries = Object.entries(totals).filter(([, v]) => Number(v) > 0);
  const total = entries.reduce((a, [, v]) => a + Number(v), 0);
  const cx = 180, cy = 170, r = 115;
  state.pieMeta = [];

  if (!total) {
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--muted');
    ctx.font = 'bold 16px Helvetica';
    ctx.fillText('No transactions for this month', 70, 180);
    return;
  }

  let start = -Math.PI / 2;
  for (const [cat, valRaw] of entries) {
    const val = Number(valRaw);
    const angle = (val / total) * Math.PI * 2;
    const color = CATEGORY_COLORS[cat] || '#94a3b8';

    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, r, start, start + angle);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = '#121315';
    ctx.stroke();

    const mid = start + angle / 2;
    const tx = cx + Math.cos(mid) * (r + 24);
    const ty = cy + Math.sin(mid) * (r + 24);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--entry-fg');
    ctx.font = 'bold 12px Helvetica';
    ctx.fillText(`${Math.round((val / total) * 100)}%`, tx - 12, ty);

    state.pieMeta.push({ cat, start, end: start + angle });
    start += angle;

    legend.insertAdjacentHTML('beforeend', `<div class="legend-item"><span class="swatch" style="background:${color}"></span>${esc(cat)}</div>`);
  }

  canvas.onclick = async (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left - cx;
    const y = e.clientY - rect.top - cy;
    const dist = Math.sqrt(x * x + y * y);
    if (dist > r) return;
    let a = Math.atan2(y, x);
    if (a < -Math.PI / 2) a += Math.PI * 2;
    for (const m of state.pieMeta) {
      if (a >= m.start && a <= m.end) {
        state.selectedPieCategory = m.cat;
        await loadPieCategoryRows(m.cat);
        render();
        return;
      }
    }
  };
}

function compareHtml() {
  return `
    <h2>Compare Your Expenditure</h2>
    <div class="row">
      <button class="btn" id="cmp-weekly">Weekly</button>
      <button class="btn" id="cmp-monthly">Monthly</button>
      <button class="btn" id="cmp-yearly">Yearly</button>
      <div class="notice" id="cmp-title"></div>
    </div>
    <canvas id="bar-canvas" width="960" height="470"></canvas>
  `;
}
function bindCompare() {
  document.getElementById('cmp-weekly').onclick = () => { state.compareMode = 'weekly'; state.compareYear = null; drawCompare(); };
  document.getElementById('cmp-monthly').onclick = () => { state.compareMode = 'monthly'; state.compareYear = null; drawCompare(); };
  document.getElementById('cmp-yearly').onclick = () => { state.compareMode = 'yearly'; state.compareYear = null; drawCompare(); };
  drawCompare();
}
async function drawCompare() {
  const mode = state.compareYear ? 'year-month' : state.compareMode;
  const title = state.compareYear ? `Monthly Comparison (${state.compareYear})` : `${state.compareMode[0].toUpperCase()}${state.compareMode.slice(1)} Comparison`;
  document.getElementById('cmp-title').textContent = title;

  const res = await window.kernelApi.compareStats({ userId: state.user.id, mode, yearContext: state.compareYear });
  const labels = res.labels || [];
  const values = res.values || [];

  const canvas = document.getElementById('bar-canvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  state.barMeta = [];

  if (!labels.length) {
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--muted');
    ctx.font = 'bold 16px Helvetica';
    ctx.fillText('No data to compare', 380, 230);
    return;
  }

  const w = canvas.width, h = canvas.height;
  const padL = 60, padR = 30, padT = 20, padB = 55;
  const pw = w - padL - padR;
  const ph = h - padT - padB;
  const max = Math.max(...values, 1);
  const n = labels.length;
  const gap = n > 8 ? 8 : 14;
  const bw = Math.max(14, (pw - gap * (n + 1)) / n);

  ctx.strokeStyle = '#5a6b5a';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(padL, h - padB); ctx.lineTo(w - padR, h - padB);
  ctx.moveTo(padL, padT); ctx.lineTo(padL, h - padB);
  ctx.stroke();

  let x = padL + gap;
  labels.forEach((lab, i) => {
    const v = Number(values[i] || 0);
    const bh = (v / max) * (ph - 10);
    const x0 = x, x1 = x + bw, y0 = h - padB - bh, y1 = h - padB;
    let color = '#39ff14';
    if (mode === 'yearly') color = '#4aa3ff';
    if (mode === 'year-month') color = '#ffd166';

    ctx.fillStyle = color;
    ctx.fillRect(x0, y0, bw, bh);
    ctx.strokeStyle = '#0e120e';
    ctx.strokeRect(x0, y0, bw, bh);

    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--entry-fg');
    ctx.font = '11px Helvetica';
    ctx.fillText(`${symbolFor(state.user.currency)}${Math.round(v)}`, x0 + 2, y0 - 6);
    ctx.fillText(String(lab), x0 + 2, y1 + 14);

    state.barMeta.push({ x0, x1, y0, y1, label: String(lab), mode });
    x += bw + gap;
  });

  if (mode === 'yearly') {
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--muted');
    ctx.fillText('Click a year bar to view that year month-wise', 320, h - 20);
  }

  canvas.onclick = (e) => {
    if (mode !== 'yearly') return;
    const rect = canvas.getBoundingClientRect();
    const xClick = e.clientX - rect.left;
    const yClick = e.clientY - rect.top;
    const hit = state.barMeta.find((m) => xClick >= m.x0 && xClick <= m.x1 && yClick >= m.y0 && yClick <= m.y1);
    if (hit) {
      state.compareYear = Number(hit.label);
      drawCompare();
    }
  };
}

function profileHtml() {
  return `
    <h2>Edit Profile</h2>
    <div class="form-grid">
      <div class="field"><label>Username</label><input id="p-username" value="${esc(state.user.usernameDisplay)}"></div>
      <div class="field"><label>New Password (optional)</label><input id="p-password" type="password"></div>
      <div class="field"><label>Confirm New Password</label><input id="p-confirm" type="password"></div>
      <div class="field"><label>New Security Answer (optional)</label><input id="p-security"></div>
      <button class="btn" id="btn-profile-save">Save Profile</button>
      ${state.message ? `<div class="notice">${esc(state.message)}</div>` : ''}
      ${state.error ? `<div class="error">${esc(state.error)}</div>` : ''}
    </div>
  `;
}
function bindProfile() {
  document.getElementById('btn-profile-save').onclick = async () => {
    const username = document.getElementById('p-username').value;
    const newPassword = document.getElementById('p-password').value;
    const confirm = document.getElementById('p-confirm').value;
    const securityAnswer = document.getElementById('p-security').value;
    if (newPassword !== confirm) return (setMsg('', 'New password and confirm password do not match.'), render());
    const res = await window.kernelApi.updateProfile({ userId: state.user.id, username, newPassword, securityAnswer });
    if (!res.ok) return (setMsg('', res.error), render());
    state.user = res.user;
    setMsg('Profile updated.', '');
    render();
  };
}

function dataToolsHtml() {
  return `
    <h2>Backup & Restore</h2>
    <div class="notice">Backup saves complete database. Restore replaces current database with selected file.</div>
    <button class="btn" id="btn-backup">Backup Database</button>
    <button class="btn" id="btn-restore">Restore Database</button>
    ${state.message ? `<div class="notice">${esc(state.message)}</div>` : ''}
    ${state.error ? `<div class="error">${esc(state.error)}</div>` : ''}
  `;
}
function bindDataTools() {
  document.getElementById('btn-backup').onclick = async () => {
    const res = await window.kernelApi.backupDb();
    if (res.ok) setMsg(`Backup saved at ${res.filePath}`, '');
    else if (!res.canceled) setMsg('', 'Backup failed.');
    render();
  };
  document.getElementById('btn-restore').onclick = async () => {
    if (!confirm('Restore will replace current database. Continue?')) return;
    const res = await window.kernelApi.restoreDb();
    if (res.ok) {
      state.user = null;
      state.authMode = 'login';
      setMsg('Database restored. Please login again.', '');
      render();
    } else if (!res.canceled) {
      setMsg('', 'Restore failed.');
      render();
    }
  };
}

async function bootstrap() {
  setMsg('', '');
  render();
}

bootstrap();
