/**
 * Task tracker API for the Sauna & Pool marketing dashboard.
 * Lives in: Ruchi – Leads & Website Task Tracker → Extensions → Apps Script.
 * Reading (GET) is open to anyone with the link. Saving (POST) needs a passcode;
 * the passcode decides whose name goes on the update.
 */
const PASSCODES = { 'CHANGE-ME-RUCHI': 'Ruchi', 'CHANGE-ME-AJAY': 'Ajay' };   // passcode → name
const TASKS_TAB = 'Tasks';
const LOG_TAB = 'Activity log';
const SOCIAL_TAB = 'Social log';
const TZ = 'Europe/London';

function doGet() {
  const ss = SpreadsheetApp.getActive();
  const t = ss.getSheetByName(TASKS_TAB).getDataRange().getDisplayValues();
  const head = t[0];
  const tasks = t.slice(1).filter((r) => r[0]).map((r) => {
    const o = {};
    head.forEach((h, i) => (o[h] = r[i]));
    return o;
  });
  const lg = ss.getSheetByName(LOG_TAB).getDataRange().getDisplayValues().slice(1)
    .filter((r) => r[0])
    .map((r) => ({ when: r[0], id: r[1], task: r[2], from: r[3], to: r[4], comment: r[5], by: r[6], minutes: Number(r[7]) || 0 }));
  let social = [];
  const ssh = ss.getSheetByName(SOCIAL_TAB);
  if (ssh) social = ssh.getDataRange().getDisplayValues().slice(1).filter((r) => r[0])
    .map((r) => ({ when: r[0], date: r[1], type: r[2], site: r[3], network: r[4], blog: r[5], link: r[6], comments: Number(r[7]) || 0, minutes: Number(r[8]) || 0, leads: Number(r[9]) || 0, notes: r[10], by: r[11] }));
  let pulse = null;
  const ps = ss.getSheetByName('Pulse');
  if (ps) { try { pulse = JSON.parse(ps.getRange('B1').getValue()); } catch (err) { pulse = null; } }
  return json({ ok: true, tasks: tasks, log: lg.slice(-500), social: social.slice(-500), pulse: pulse, at: now() });
}

function doPost(e) {
  let p;
  try { p = JSON.parse(e.postData.contents); } catch (err) { return json({ ok: false, error: 'bad request' }); }
  const by = p && PASSCODES[p.key];
  if (!by) return json({ ok: false, error: 'wrong passcode' });
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    if (p.kind === 'social') return logSocial(p, by);
    return updateTask(p, by);
  } finally {
    lock.releaseLock();
  }
}

function logSocial(p, by) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SOCIAL_TAB);
  const clip = (v, n) => String(v || '').slice(0, n).trim();
  const num = (v, max) => Math.max(0, Math.min(max, Math.round(Number(v) || 0)));
  const types = ['Post made', 'Post went live', 'Outreach (comments)', 'Replies to comments/messages', 'Lead passed to Kiana', 'Other'];
  const type = types.indexOf(p.type) !== -1 ? p.type : 'Other';
  sh.appendRow([now(), Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd'), type, clip(p.site, 20), clip(p.network, 40), clip(p.blog, 300),
    clip(p.link, 300), num(p.comments, 500), num(p.minutes, 600), num(p.leads, 50), clip(p.notes, 1000), by]);
  return json({ ok: true });
}

function updateTask(p, by) {
  const allowed = ['Not started', 'In progress', 'Done', 'Blocked', 'Needs Deepti'];
  const sh = SpreadsheetApp.getActive().getSheetByName(TASKS_TAB);
  const data = sh.getDataRange().getDisplayValues();
  const head = data[0];
  const col = (name) => head.indexOf(name) + 1;
  const cId = col('ID'), cTask = col('Task'), cStatus = col('Status'), cDone = col('Date done');
  const cNotes = head.findIndex((h) => h.indexOf('notes') !== -1) + 1;
  const cTime = col('Time spent (min)');
  const rowIdx = data.findIndex((r, i) => i > 0 && r[cId - 1] === String(p.id));
  if (rowIdx < 1) return json({ ok: false, error: 'task not found' });
  const row = rowIdx + 1;
  const old = data[rowIdx][cStatus - 1];
  let status = old;
  if (p.status && allowed.indexOf(p.status) !== -1) {
    status = p.status;
    sh.getRange(row, cStatus).setValue(status);
    if (status === 'Done' && !data[rowIdx][cDone - 1]) sh.getRange(row, cDone).setValue(new Date());
  }
  const comment = String(p.comment || '').slice(0, 1000).trim();
  const minutes = Math.max(0, Math.min(600, Math.round(Number(p.minutes) || 0)));
  if (minutes && cTime > 0) {
    const prevMin = Number(data[rowIdx][cTime - 1]) || 0;
    sh.getRange(row, cTime).setValue(prevMin + minutes);
  }
  if (comment && cNotes > 0) {
    const prev = data[rowIdx][cNotes - 1];
    const stamp = Utilities.formatDate(new Date(), TZ, 'dd/MM HH:mm');
    sh.getRange(row, cNotes).setValue((prev ? prev + '\n' : '') + stamp + ' ' + by + ': ' + comment);
  }
  if (status !== old || comment || minutes) {
    SpreadsheetApp.getActive().getSheetByName(LOG_TAB)
      .appendRow([now(), p.id, data[rowIdx][cTask - 1], old, status, comment, by, minutes || '']);
  }
  return json({ ok: true, id: p.id, status: status });
}

function now() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'); }
function json(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
