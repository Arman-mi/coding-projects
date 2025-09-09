/* app.js - tiny client for EMT Simulation API (mounted at /web) */
const el = (sel) => document.querySelector(sel);
const apiBase = ""; // same-origin

let runId = null;
let scenarios = [];

async function fetchJSON(path, opts = {}) {
  const res = await fetch(apiBase + path, {
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    ...opts,
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`HTTP ${res.status}: ${msg}`);
  }
  return res.json();
}

function addMessage(role, text) {
  const wrap = document.createElement('div');
  wrap.className = `message ${role}`;
  wrap.innerHTML = `<div class="role">${role}</div><div class="bubble">${text}</div>`;
  el('#messages').appendChild(wrap);
  el('#messages').scrollTop = el('#messages').scrollHeight;
}

function setParsed(parsed) {
  el('#parsedPanel').classList.remove('hidden');
  el('#parsedJson').textContent = JSON.stringify(parsed, null, 2);
}

function setRunId(id) {
  runId = id;
  el('#runIdBadge').textContent = id ? `run: ${id}` : '';
  el('#sendBtn').disabled = !id;
  el('#gradeBtn').disabled = !id;
}

async function loadScenarios() {
  const sel = el('#scenarioSelect');
  sel.innerHTML = `<option value="" disabled selected>Loading scenarios…</option>`;
  try {
    scenarios = await fetchJSON('/scenarios');
    if (!Array.isArray(scenarios) || scenarios.length === 0) {
      sel.innerHTML = `<option value="" disabled selected>No scenarios found</option>`;
      addMessage('system', 'No scenarios were returned by the API.');
      return;
    }
    sel.innerHTML = '';
    scenarios.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.id;
      opt.textContent = `#${s.id} • ${s.title}`;
      sel.appendChild(opt);
    });
  } catch (err) {
    sel.innerHTML = `<option value="" disabled selected>Failed to load scenarios</option>`;
    addMessage('system', `Error loading scenarios: ${err.message}`);
    console.error(err);
  }
}

async function startRun() {
  setRunId(null);
  const sel = el('#scenarioSelect');
  const val = sel.value;
  if (!val) {
    addMessage('system', 'Please pick a scenario first.');
    return;
  }
  const sid = Number(val);
  const body = sid ? { scenario_id: sid } : {};
  const data = await fetchJSON('/run/start', { method: 'POST', body: JSON.stringify(body)});
  setRunId(data.run_id);
  addMessage('system', `Started: ${data.scenario.title} (disease_id=${data.scenario.disease_id})`);
}

async function sendTurn() {
  const text = el('#userInput').value.trim();
  if (!text || !runId) return;
  addMessage('user', text);
  el('#userInput').value = '';

  try {
    const data = await fetchJSON('/run/step', { method: 'POST', body: JSON.stringify({ run_id: runId, text })});
    setParsed(data.parsed);
    const reply = data.reply?.reply_text || JSON.stringify(data.reply);
    addMessage('patient', reply);
  } catch (err) {
    addMessage('system', `Error: ${err.message}`);
    console.error(err);
  }
}

async function gradeRun() {
  if (!runId) return;
  try {
    const report = await fetchJSON(`/run/${runId}/grade`);
    el('#gradePanel').classList.remove('hidden');

    const fmt = (x, fallback = '—') => {
      const n = Number(x);
      return Number.isFinite(n) ? n.toFixed(1) : fallback;
    };
    const pct = Number.isFinite(Number(report.percent))
      ? Number(report.percent).toFixed(1)
      : '0.0';

    el('#scoreHeader').textContent =
      `Disease: ${report.disease || '—'} • ` +
      `Score: ${fmt(report.score, '0.0')} / ${fmt(report.max_score, '0.0')} ` +
      `(${pct}%)`;

    const tbody = el('#gradeTable tbody');
    tbody.innerHTML = '';

    const details = Array.isArray(report.details) ? report.details : [];
    for (const d of details) {
      const metSymbol = d.met === null ? '—' : (d.met ? '✔' : '✘');
      const metClass  = d.met === null ? ''   : (d.met ? 'met' : 'miss');
      const awarded   = fmt(d.awarded);
      const weight    = fmt(d.weight);
      const rationale = d.rationale || (d.met === null ? 'Not applicable' : '');

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${d.code ?? '—'}</td>
        <td class="${metClass}">${metSymbol}</td>
        <td>${awarded}</td>
        <td>${weight}</td>
        <td>${rationale}</td>
      `;
      tbody.appendChild(tr);
    }

    el('#narrative').textContent = report.narrative || '';
  } catch (err) {
    addMessage('system', `Error getting grade: ${err.message}`);
    console.error(err);
  }
}













window.addEventListener('DOMContentLoaded', async () => {
  el('#apiBase').textContent = location.origin;
  await loadScenarios();
  el('#startBtn').addEventListener('click', startRun);
  el('#sendBtn').addEventListener('click', sendTurn);
  el('#userInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendTurn();
  });
  el('#gradeBtn').addEventListener('click', gradeRun);
});
