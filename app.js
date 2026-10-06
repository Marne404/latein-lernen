(() => {
'use strict';

/* =====================================================================
   Konstanten & Hilfsfunktionen
   ===================================================================== */
const MIN = 60000, DAY = 86400000;
// Leitner-Boxen: Wartezeit bis zur nächsten Wiederholung je Box
const INTERVALS = [0, 10 * MIN, DAY, 3 * DAY, 7 * DAY, 16 * DAY, 35 * DAY];
const MAX_BOX = INTERVALS.length - 1;
const MASTERED = 4;            // ab Box 4 gilt ein Wort als "sicher"
const DAILY_GOAL = 20;
const REVIEW_CAP = 25;
const KEY = 'latein-lernen-v1';
const PACKS = PACK_TITLES.length;

const $app = document.getElementById('app');
const $toast = document.getElementById('toast');
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.random() * (i + 1) | 0; [a[i], a[j]] = [a[j], a[i]]; } return a; };
const rnd = n => Math.random() * n | 0;
const todayStr = (d = new Date()) => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
let toastTimer;
function toast(msg) {
  $toast.textContent = msg; $toast.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => $toast.classList.remove('show'), 2200);
}

/* =====================================================================
   Speicher
   ===================================================================== */
const defaults = () => ({
  cards: {},
  settings: { mode: 'smart', batch: 10, vibrate: true },
  streak: { days: 0, last: null },
  daily: { date: null, n: 0 },
});
let S = load();
function load() {
  try {
    const r = JSON.parse(localStorage.getItem(KEY));
    if (r && r.cards) {
      const d = defaults();
      return { ...d, ...r, settings: { ...d.settings, ...r.settings }, streak: { ...d.streak, ...r.streak }, daily: { ...d.daily, ...r.daily } };
    }
  } catch (e) { /* ignorieren */ }
  return defaults();
}
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* ignorieren */ } }
function vibrate(p) { if (S.settings.vibrate && navigator.vibrate) { try { navigator.vibrate(p); } catch (e) { /* */ } } }

/* =====================================================================
   Karten, Statistik
   ===================================================================== */
const card = id => S.cards[id] || { box: 0, due: 0, seen: 0, ok: 0, bad: 0 };
const isDue = id => { const c = S.cards[id]; return !!c && c.box > 0 && c.due <= Date.now(); };
const packIds = p => WORDS.filter(w => w.pack === p).map(w => w.id);
const newIds = ids => ids.filter(id => card(id).box === 0);
const dueIds = ids => ids.filter(isDue).sort((a, b) => S.cards[a].due - S.cards[b].due);

function stats(ids) {
  let neu = 0, learning = 0, mastered = 0, due = 0, score = 0;
  for (const id of ids) {
    const c = card(id);
    if (c.box === 0) neu++; else if (c.box >= MASTERED) mastered++; else learning++;
    if (isDue(id)) due++;
    score += c.box / MAX_BOX;
  }
  return { total: ids.length, neu, learning, mastered, due, pct: Math.round(100 * score / ids.length) };
}
const allIds = WORDS.map(w => w.id);

function dailyCount() { return S.daily.date === todayStr() ? S.daily.n : 0; }
function streakDays() {
  const l = S.streak.last; if (!l) return 0;
  const t = todayStr(), y = todayStr(new Date(Date.now() - DAY));
  return (l === t || l === y) ? S.streak.days : 0;
}
function bumpDay() {
  const t = todayStr();
  if (S.streak.last === t) return;
  S.streak.days = S.streak.last === todayStr(new Date(Date.now() - DAY)) ? S.streak.days + 1 : 1;
  S.streak.last = t;
}

/* =====================================================================
   Routing  (#/ , #/pack/N , #/lernen)
   ===================================================================== */
let sess = null;
function go(hash) { if (location.hash === hash) render(); else location.hash = hash; }
window.addEventListener('hashchange', render);

function render() {
  const h = location.hash || '#/';
  const m = h.match(/^#\/pack\/(\d+)$/);
  if (h === '#/lernen' && sess) return renderStep();
  if (h === '#/ende' && sess && sess.finished) return renderSummary();
  sess = null;
  if (m && +m[1] < PACKS) return renderPack(+m[1]);
  if (h !== '#/') { history.replaceState(null, '', '#/'); }
  renderHome();
  window.scrollTo(0, 0);
}

/* =====================================================================
   Startseite
   ===================================================================== */
function ring(pctM, pctL) {
  const r = 40, c = 2 * Math.PI * r;
  const m = c * pctM / 100, l = c * (pctM + pctL) / 100;
  return `<svg viewBox="0 0 100 100" aria-hidden="true">
    <circle class="bg" cx="50" cy="50" r="${r}" fill="none" stroke-width="11"/>
    <circle class="fg2" cx="50" cy="50" r="${r}" fill="none" stroke-width="11" stroke-linecap="round" stroke-dasharray="${l} ${c}"/>
    <circle class="fg" cx="50" cy="50" r="${r}" fill="none" stroke-width="11" stroke-linecap="round" stroke-dasharray="${m} ${c}"/>
  </svg>`;
}

function renderHome() {
  const st = stats(allIds);
  const mPct = 100 * st.mastered / st.total, lPct = 100 * st.learning / st.total;
  const dn = Math.min(dailyCount(), DAILY_GOAL);
  const firstOpen = [...Array(PACKS).keys()].find(p => newIds(packIds(p)).length);
  let cta;
  if (st.due) {
    cta = `<button class="cta" data-act="review-all">Wiederholen<small>${st.due} Wörter fällig</small></button>`;
  } else if (firstOpen !== undefined) {
    cta = `<button class="cta" data-act="learn" data-pack="${firstOpen}">Weiter lernen<small>Pack ${firstOpen + 1} · ${PACK_TITLES[firstOpen]}</small></button>`;
  } else {
    cta = `<button class="cta alt" disabled>🏛️ Alle 500 Wörter gelernt – nichts fällig</button>`;
  }
  const tiles = [...Array(PACKS).keys()].map(p => {
    const s = stats(packIds(p));
    const done = s.mastered === s.total;
    return `<button class="tile${done ? ' done' : ''}" data-act="open" data-pack="${p}">
      ${s.due ? `<span class="badge" title="fällig">${s.due}</span>` : done ? '<span class="crown">👑</span>' : ''}
      <span class="n">${p + 1}</span>
      <span class="t">${esc(PACK_TITLES[p])}</span>
      <span class="bar"><i class="m" style="width:${100 * s.mastered / s.total}%"></i><i class="l" style="width:${100 * s.learning / s.total}%"></i></span>
      <span class="meta">${s.mastered}/${s.total} sicher · ${s.pct}%</span>
    </button>`;
  }).join('');
  $app.innerHTML = `
    <div class="top"><div class="brand">Latein<span>lernen</span></div>
      <button class="icon-btn" data-act="settings" aria-label="Einstellungen">⚙️</button></div>
    <section class="hero">
      <div class="ring">${ring(mPct, lPct)}<div class="num"><div>${Math.round(st.pct)}%<small>gelernt</small></div></div></div>
      <div class="stats">
        <div class="stat"><b>${st.mastered}<span> /500</span></b><span>sicher</span></div>
        <div class="stat"><b>${st.learning}</b><span>in Arbeit</span></div>
        <div class="stat"><b>${st.due}</b><span>fällig</span></div>
        <div class="stat"><b>${streakDays()} 🔥</b><span>Tage am Stück</span></div>
        <div class="goal"><span class="stat"><span>Tagesziel: ${dn}/${DAILY_GOAL} Wörter</span></span>
          <div class="bar goalbar"><i class="m" style="width:${100 * dn / DAILY_GOAL}%"></i></div></div>
      </div>
    </section>
    ${cta}
    <h2 class="sec">25er-Packs</h2>
    <div class="grid">${tiles}</div>`;
}

/* =====================================================================
   Pack-Ansicht
   ===================================================================== */
function renderPack(p) {
  const ids = packIds(p), s = stats(ids), nNew = newIds(ids).length, nDue = s.due;
  const batch = Math.min(S.settings.batch, nNew);
  const list = ids.map(id => {
    const w = WORDS[id], c = card(id);
    const boxes = Array.from({ length: MAX_BOX }, (_, i) => `<i class="${i < c.box ? 'on' : ''}"></i>`).join('');
    return `<div class="w"><div class="txt"><div class="la">${esc(w.la)}</div><div class="fo">${esc(w.forms)}</div>
      <div class="de ${c.box === 0 && listHidden ? 'hide' : ''}">${esc(w.de)}</div></div>
      <div class="boxes ${c.box >= MASTERED ? 'mast' : ''}" title="Box ${c.box}/${MAX_BOX}">${boxes}</div></div>`;
  }).join('');
  $app.innerHTML = `
    <div class="top"><button class="back" data-act="home">‹ Zurück</button>
      <button class="icon-btn" data-act="settings" aria-label="Einstellungen">⚙️</button></div>
    <section class="packhead">
      <h1>Pack ${p + 1}</h1><div class="sub">${esc(PACK_TITLES[p])} · Wörter ${p * PACK_SIZE + 1}–${p * PACK_SIZE + ids.length}</div>
      <div class="bar"><i class="m" style="width:${100 * s.mastered / s.total}%"></i><i class="l" style="width:${100 * s.learning / s.total}%"></i></div>
      <div class="legend"><span><span class="dot m"></span><b>${s.mastered}</b> sicher</span><span><span class="dot l"></span><b>${s.learning}</b> in Arbeit</span><span><span class="dot"></span><b>${s.neu}</b> neu</span><span><b>${s.pct}%</b> Fortschritt</span></div>
    </section>
    <div class="btnrow">
      <button class="btn primary" data-act="learn" data-pack="${p}" ${nNew ? '' : 'disabled'}>Neue Wörter lernen<small>${nNew ? `${batch} von ${nNew} neuen Wörtern` : 'alle Wörter schon gesehen'}</small></button>
      <button class="btn" data-act="review-pack" data-pack="${p}" ${nDue ? '' : 'disabled'}>Fällige wiederholen<small>${nDue ? `${nDue} fällig` : 'nichts fällig'}</small></button>
      <button class="btn" data-act="drill" data-pack="${p}">Alle 25 durchüben<small>Schnelltest – ändert den Lernplan nicht</small></button>
    </div>
    <h2 class="sec">Wortliste</h2>
    <div class="row" style="margin-bottom:10px"><button class="btn" data-act="togglehide">${listHidden ? 'Übersetzungen neuer Wörter zeigen' : 'Übersetzungen neuer Wörter verbergen'}</button></div>
    <div class="words">${list}</div>`;
  window.scrollTo(0, 0);
}
let listHidden = false;

/* =====================================================================
   Lern-Sitzung
   ===================================================================== */
function startSession(ids, opts = {}) {
  if (!ids.length) { toast('Keine Wörter für diese Runde'); return; }
  const items = ids.map(id => {
    const isNew = card(id).box === 0 && !opts.drill;
    return { id, isNew, reps: 0, need: isNew ? 2 : 1, errors: 0, introDone: !isNew, finished: false };
  });
  sess = {
    items, queue: [...items], cur: null, awaiting: false, revealed: false, mcDir: 'ld',
    ok: 0, bad: 0, newLearned: 0, hard: new Map(), drill: !!opts.drill, back: opts.back || '#/', startedAt: Date.now(), finished: false,
  };
  bumpDay();
  go('#/lernen');
}

function stepType(it) {
  if (it.isNew && !it.introDone) return 'intro';
  const m = S.settings.mode;
  if (m === 'cards') return 'flip';
  if (m === 'type') return 'type';
  if (m === 'choice') return 'mc';
  // smart: neu → erst Auswahl, dann Selbstabfrage; Fehler → wieder leichter; Wiederholung → Selbstabfrage
  if (it.isNew || it.errors > 0) return it.reps === 0 ? 'mc' : 'flip';
  return 'flip';
}

function progressOf() {
  const t = sess.items.length;
  const s = sess.items.reduce((a, it) => a + (it.finished ? 1 : Math.min(it.reps, it.need) / it.need * 0.9 + (it.introDone && it.isNew ? 0.05 : 0)), 0);
  return { pct: 100 * s / t, done: sess.items.filter(i => i.finished).length, total: t };
}

function renderStep() {
  if (!sess.queue.length) return finishSession();
  const it = sess.cur = sess.queue.shift();
  sess.awaiting = false; sess.revealed = false;
  const w = WORDS[it.id], type = it.type = stepType(it);
  const pr = progressOf();
  let tag = '', body = '';
  if (it.isNew && !it.introDone) tag = '<span class="tag new">Neues Wort</span>';
  else if (it.errors) tag = '<span class="tag again">Nochmal</span>';
  else if (it.isNew) tag = '<span class="tag">Festigen</span>';
  else tag = '<span class="tag">Wiederholung</span>';

  if (type === 'intro') {
    body = `<div class="card">
        <div class="lat">${esc(w.la)}</div>${formsHtml(w)}<div class="sep"></div>
        <div class="de">${esc(w.de)}</div></div>
      <button class="revealbtn" data-act="intro-ok">Merken & weiter</button>
      <button class="skip" data-act="intro-known">Kenne ich schon</button>`;
  } else if (type === 'flip') {
    body = `<div class="card" id="card" data-act="reveal">
        <span class="stamp l">NOCH NICHT</span><span class="stamp r">GEWUSST</span>
        <div class="lat ${w.la.length > 12 ? 'sm' : ''}">${esc(w.la)}</div>${formsHtml(w)}
        <div id="back"><div class="hint">Antwort überlegen, dann antippen</div></div></div>
      <div id="flipbtns"><button class="revealbtn" data-act="reveal">Antwort zeigen</button></div>`;
  } else if (type === 'mc') {
    // Richtung wechselt: Latein→Deutsch, bei 2. Durchgang Deutsch→Latein
    const dir = it.reps % 2 === 0 ? 'ld' : 'dl';
    sess.mcDir = dir;
    const opts = pickOptions(w);
    const label = o => dir === 'ld' ? esc(o.de) : esc(o.forms);
    body = `<div class="card">${dir === 'ld'
        ? `<div class="lat ${w.la.length > 12 ? 'sm' : ''}">${esc(w.la)}</div>${formsHtml(w)}`
        : `<div class="de">${esc(w.de)}</div><div class="hint">Welches lateinische Wort?</div>`}</div>
      <div class="opts">${opts.map((o, i) => `<button class="opt ${dir === 'dl' ? 'la' : ''}" data-act="pick" data-id="${o.id}"><span class="k">${i + 1}</span><span>${label(o)}</span></button>`).join('')}</div>`;
  } else if (type === 'type') {
    body = `<div class="card"><div class="lat ${w.la.length > 12 ? 'sm' : ''}">${esc(w.la)}</div>${formsHtml(w)}
        <div id="back"><div class="hint">Deutsche Bedeutung eintippen</div></div></div>
      <form class="typebox" id="typeform" autocomplete="off"><input id="ans" type="text" enterkeyhint="done" autocapitalize="none" autocorrect="off" spellcheck="false" placeholder="Bedeutung …"><button type="submit">OK</button></form>
      <button class="skip" data-act="type-giveup">Weiß ich nicht</button>`;
  }
  $app.innerHTML = `<div class="session">
    <div class="sbar"><button class="x" data-act="quit" aria-label="Beenden">✕</button>
      <div class="bar"><i class="m" style="width:${pr.pct}%"></i></div><div class="cnt">${pr.done}/${pr.total}</div></div>
    <div class="stage">${tag}${body}</div></div>`;
  window.scrollTo(0, 0);
  if (type === 'flip') bindSwipe();
  if (type === 'type') {
    document.getElementById('typeform').addEventListener('submit', e => { e.preventDefault(); checkTyped(); });
    setTimeout(() => { const a = document.getElementById('ans'); a && a.focus(); }, 60);
  }
}

/* ---- Auswahl-Antworten -------------------------------------------- */
function pickOptions(w) {
  const sameCls = WORDS.filter(x => x.id !== w.id && x.cls === w.cls && x.de !== w.de && x.la !== w.la);
  const other = WORDS.filter(x => x.id !== w.id && x.cls !== w.cls && x.de !== w.de);
  // Nachbarpacks bevorzugen: ähnlich genug, um zu fordern, aber nicht zu ähnlich
  const near = sameCls.filter(x => Math.abs(x.pack - w.pack) <= 3);
  const pool = shuffle([...shuffle([...near]), ...shuffle([...sameCls.filter(x => !near.includes(x))]), ...shuffle(other)]);
  const picked = [];
  for (const x of pool) { if (picked.length >= 3) break; if (!picked.some(y => y.de === x.de || y.forms === x.forms)) picked.push(x); }
  return shuffle([w, ...picked]);
}

function pick(btn) {
  if (sess.awaiting) return;
  const it = sess.cur, w = WORDS[it.id], ok = +btn.dataset.id === it.id;
  sess.awaiting = true;
  document.querySelectorAll('.opt').forEach(b => {
    b.disabled = true;
    if (+b.dataset.id === it.id) b.classList.add('right');
    else if (b === btn) b.classList.add('wrong'); else b.classList.add('dim');
  });
  if (!ok) {
    // vollständige Lösung zeigen
    const c = document.querySelector('.card');
    c.insertAdjacentHTML('beforeend', `<div class="sep"></div><div class="de" style="font-size:18px">${esc(sess.mcDir === 'ld' ? w.de : w.forms)}</div>`);
  }
  grade(ok);
  if (ok) setTimeout(() => { if (sess && sess.cur === it) renderStep(); }, 650);
  else showNext();
}

function showNext() {
  const stage = document.querySelector('.stage');
  stage.insertAdjacentHTML('beforeend', `<button class="revealbtn" data-act="next">Weiter</button>`);
  const b = stage.lastElementChild; b.focus({ preventScroll: true });
}

/* ---- Selbstabfrage (Karte aufdecken, wischen) ----------------------- */
function reveal() {
  if (sess.revealed || sess.awaiting) return;
  sess.revealed = true;
  const w = WORDS[sess.cur.id];
  document.getElementById('back').innerHTML = `<div class="sep"></div><div class="de">${esc(w.de)}</div><div class="hint">← wischen: noch nicht &nbsp;·&nbsp; wischen: gewusst →</div>`;
  document.getElementById('flipbtns').innerHTML = `<div class="answerbtns">
    <button class="ab no" data-act="grade-no">✗ Nicht gewusst<small>nochmal üben</small></button>
    <button class="ab yes" data-act="grade-yes">✓ Gewusst<small>weiter</small></button></div>`;
}
function bindSwipe() {
  const el = document.getElementById('card'); if (!el) return;
  let x0 = null, dx = 0, moved = false;
  const sl = el.querySelector('.stamp.l'), sr = el.querySelector('.stamp.r');
  el.addEventListener('pointerdown', e => { if (!sess.revealed) return; x0 = e.clientX; dx = 0; moved = false; el.setPointerCapture(e.pointerId); el.classList.add('drag'); });
  el.addEventListener('pointermove', e => {
    if (x0 === null) return;
    dx = e.clientX - x0; if (Math.abs(dx) > 8) moved = true;
    el.style.transform = `translateX(${dx}px) rotate(${dx / 25}deg)`;
    sl.style.opacity = Math.min(1, Math.max(0, -dx / 90)); sr.style.opacity = Math.min(1, Math.max(0, dx / 90));
  });
  const end = () => {
    if (x0 === null) return; x0 = null; el.classList.remove('drag');
    if (moved && Math.abs(dx) > 90) {
      const ok = dx > 0; el.style.transform = `translateX(${ok ? 500 : -500}px) rotate(${ok ? 20 : -20}deg)`; el.style.opacity = 0;
      grade(ok); setTimeout(() => sess && renderStep(), 160);
    } else { el.style.transform = ''; sl.style.opacity = sr.style.opacity = 0; }
  };
  el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);
}

/* ---- Tippen --------------------------------------------------------- */
const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss').replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
function lev(a, b) {
  const m = a.length, n = b.length; let prev = Array.from({ length: n + 1 }, (_, j) => j);
  for (let i = 1; i <= m; i++) { const cur = [i]; for (let j = 1; j <= n; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); prev = cur; }
  return prev[n];
}
function acceptable(w) {
  const alts = new Set();
  w.de.replace(/\([^)]*\)/g, '').split(/[,;]/).forEach(p => {
    let a = norm(p); if (!a) return; alts.add(a);
    const s = a.replace(/^(sich|zu|der|die|das|ein|eine) /, ''); if (s) alts.add(s);
  });
  return [...alts];
}
function typedOk(input, w) {
  const parts = input.split(/[,;]/).map(norm).filter(Boolean);
  const alts = acceptable(w);
  return parts.some(p => alts.some(a => {
    const q = p.replace(/^(sich|zu|der|die|das|ein|eine) /, '');
    if (p === a || q === a) return true;
    const tol = a.length >= 9 ? 2 : a.length >= 5 ? 1 : 0;
    return tol > 0 && (lev(p, a) <= tol || lev(q, a) <= tol);
  }));
}
function checkTyped(giveUp) {
  if (sess.awaiting) return;
  const input = document.getElementById('ans').value, w = WORDS[sess.cur.id];
  if (!giveUp && !input.trim()) return;
  const ok = !giveUp && typedOk(input, w);
  sess.awaiting = true; sess.typedWrong = !ok;
  document.getElementById('typeform').remove();
  const sk = document.querySelector('.skip'); if (sk) sk.remove();
  document.getElementById('back').innerHTML = `<div class="sep"></div><div class="de">${esc(w.de)}</div>`;
  document.querySelector('.card').classList.add(ok ? 'good' : 'bad');
  const stage = document.querySelector('.stage');
  if (ok) {
    stage.insertAdjacentHTML('beforeend', `<div class="feedback good">✓ Richtig</div>`);
    grade(true); setTimeout(() => { if (sess && sess.cur && sess.awaiting) renderStep(); }, 900);
  } else {
    stage.insertAdjacentHTML('beforeend', `<div class="feedback bad">${giveUp ? 'Das war die Lösung' : '✗ Leider falsch – deine Antwort: „' + esc(input.trim()) + '“'}</div>
      ${giveUp ? '' : '<button class="skip" data-act="type-override">Doch richtig (Tippfehler / anderes Synonym)</button>'}`);
    grade(false); showNext();
  }
}

/* ---- Bewertung & Intervalle ----------------------------------------- */
function grade(ok) {
  const it = sess.cur;
  vibrate(ok ? 12 : [30, 40, 30]);
  if (ok) { sess.ok++; it.reps++; }
  else {
    sess.bad++; it.errors++; it.reps = 0;
    sess.hard.set(it.id, (sess.hard.get(it.id) || 0) + 1);
  }
  if (it.reps >= it.need) { it.finished = true; applySrs(it); }
  else {
    // später in der Runde wiederholen: Fehler schnell (3–4 Karten), Erfolg etwas später
    const gap = ok ? 4 + rnd(3) : 2 + rnd(2);
    sess.queue.splice(Math.min(gap, sess.queue.length), 0, it);
  }
}
function applySrs(it) {
  if (sess.drill) return;
  const c = { ...card(it.id) };
  if (it.isNew) { c.box = 1; sess.newLearned++; }
  else if (it.errors === 0) c.box = Math.min(MAX_BOX, Math.max(c.box, 1) + 1);
  else c.box = Math.max(1, c.box - 2);
  c.due = Date.now() + INTERVALS[c.box];
  c.seen = (c.seen || 0) + 1; c.ok = (c.ok || 0) + (it.errors ? 0 : 1); c.bad = (c.bad || 0) + it.errors;
  S.cards[it.id] = c;
  const t = todayStr(); if (S.daily.date !== t) S.daily = { date: t, n: 0 };
  S.daily.n++;
  save();
}

function finishSession() {
  sess.finished = true; save();
  go('#/ende');
}

function renderSummary() {
  const s = sess, total = s.items.length, errs = s.items.filter(i => i.errors).length;
  const acc = Math.round(100 * (total - errs) / total);
  const hard = [...s.hard.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  const msg = acc >= 90 ? ['🎉', 'Stark!'] : acc >= 70 ? ['👍', 'Gut gemacht!'] : ['💪', 'Dranbleiben!'];
  const left = s.back.startsWith('#/pack/') ? newIds(packIds(+s.back.split('/')[2])).length : 0;
  const dueNow = stats(allIds).due;
  $app.innerHTML = `<div class="summary">
    <div class="big">${msg[0]}</div><h1>${msg[1]}</h1>
    <div class="sub">${s.drill ? 'Durchlauf' : 'Runde'} abgeschlossen · ${Math.max(1, Math.round((Date.now() - s.startedAt) / 60000))} Min.</div>
    <div class="sumstats"><div><b>${total}</b><span>Wörter</span></div><div><b>${acc}%</b><span>auf Anhieb</span></div><div><b>${s.newLearned}</b><span>neu gelernt</span></div></div>
    ${hard.length ? `<div class="hard"><h3>Das braucht noch Übung</h3>${hard.map(([id, n]) => `<div class="w"><div class="txt"><div class="la">${esc(WORDS[id].la)}</div><div class="de">${esc(WORDS[id].de)}</div></div><span class="fo">${n}× falsch</span></div>`).join('')}</div>` : ''}
    <div class="btnrow">
      ${left ? `<button class="btn primary" data-act="learn" data-pack="${s.back.split('/')[2]}">Nächste Runde<small>noch ${left} neue Wörter in diesem Pack</small></button>` : ''}
      ${dueNow && !s.drill ? `<button class="btn ${left ? '' : 'primary'}" data-act="review-all">Fällige wiederholen<small>${dueNow} fällig</small></button>` : ''}
      <button class="btn" data-act="goback">Zurück</button>
    </div></div>`;
  window.scrollTo(0, 0);
}

/* =====================================================================
   Einstellungen
   ===================================================================== */
function openSettings() {
  const st = S.settings;
  const seg = (key, opts) => `<div class="seg">${opts.map(([v, l]) => `<button data-set="${key}" data-val="${v}" class="${String(st[key]) === String(v) ? 'on' : ''}">${l}</button>`).join('')}</div>`;
  const o = document.createElement('div'); o.className = 'overlay'; o.id = 'settings';
  o.innerHTML = `<div class="sheet" role="dialog" aria-label="Einstellungen">
    <h2>Einstellungen</h2>
    <div class="grp"><label>Lernmodus</label>${seg('mode', [['smart', 'Smart'], ['cards', 'Karten'], ['choice', 'Auswahl'], ['type', 'Tippen']])}
      <p><b>Smart</b>: neue Wörter erst per Auswahl, dann Selbstabfrage; Wiederholungen per Karte. Fehler kommen in der Runde bald wieder.</p></div>
    <div class="grp"><label>Neue Wörter pro Runde</label>${seg('batch', [[5, '5'], [10, '10'], [15, '15'], [25, '25']])}
      <p>Kleine Runden (10) sind meist effektiver – lieber öfter am Tag.</p></div>
    <div class="grp"><label>Vibration</label>${seg('vibrate', [['true', 'An'], ['false', 'Aus']])}</div>
    <div class="grp"><label>Fortschritt</label>
      <div class="row"><button class="btn" data-act="export">Sichern</button><button class="btn" data-act="import">Wiederherstellen</button></div>
      <div class="row" style="margin-top:10px"><button class="btn danger" data-act="reset">Alles zurücksetzen</button></div>
      <p>Der Fortschritt liegt nur in diesem Browser. „Sichern“ kopiert ihn als Text, den du auf einem anderen Gerät einfügen kannst.</p></div>
    <div class="grp"><button class="btn primary" data-act="close-settings" style="width:100%">Fertig</button></div></div>`;
  document.body.appendChild(o);
}
const formsHtml = w => w.forms === w.la ? '' : `<div class="forms">${esc(w.forms)}</div>`;
const closeSettings = () => { const o = document.getElementById('settings'); if (o) o.remove(); };

/* =====================================================================
   Ereignisse
   ===================================================================== */
document.addEventListener('click', e => {
  const set = e.target.closest('[data-set]');
  if (set) {
    const k = set.dataset.set; let v = set.dataset.val;
    S.settings[k] = k === 'batch' ? +v : k === 'vibrate' ? v === 'true' : v;
    save(); set.parentElement.querySelectorAll('button').forEach(b => b.classList.toggle('on', b === set));
    if (!sess) render();
    return;
  }
  if (e.target.id === 'settings') return closeSettings();
  const el = e.target.closest('[data-act]'); if (!el) return;
  const p = +el.dataset.pack;
  switch (el.dataset.act) {
    case 'open': go('#/pack/' + p); break;
    case 'home': go('#/'); break;
    case 'goback': go(sess && sess.back || '#/'); break;
    case 'settings': openSettings(); break;
    case 'close-settings': closeSettings(); render(); break;
    case 'togglehide': listHidden = !listHidden; renderPack(+location.hash.split('/')[2]); break;
    case 'learn': {
      const ids = newIds(packIds(p)).slice(0, S.settings.batch);
      // fällige Wörter dieses Packs gleich mitnehmen (vorneweg wiederholen)
      const due = dueIds(packIds(p)).slice(0, 8);
      startSession([...due, ...ids], { back: '#/pack/' + p }); break;
    }
    case 'review-pack': startSession(dueIds(packIds(p)).slice(0, REVIEW_CAP), { back: '#/pack/' + p }); break;
    case 'review-all': startSession(dueIds(allIds).slice(0, REVIEW_CAP), { back: '#/' }); break;
    case 'drill': startSession(shuffle(packIds(p)), { drill: true, back: '#/pack/' + p }); break;
    case 'intro-ok': { const it = sess.cur; it.introDone = true; sess.queue.splice(Math.min(1, sess.queue.length), 0, it); renderStep(); break; }
    case 'intro-known': {
      const it = sess.cur; it.finished = true; it.introDone = true; it.reps = it.need;
      S.cards[it.id] = { box: 3, due: Date.now() + INTERVALS[3], seen: 1, ok: 1, bad: 0 };
      const t = todayStr(); if (S.daily.date !== t) S.daily = { date: t, n: 0 }; S.daily.n++;
      sess.newLearned++; save(); renderStep(); break;
    }
    case 'reveal': reveal(); break;
    case 'grade-yes': grade(true); renderStep(); break;
    case 'grade-no': grade(false); renderStep(); break;
    case 'pick': pick(el); break;
    case 'next': renderStep(); break;
    case 'type-giveup': checkTyped(true); break;
    case 'type-override': { sess.cur.errors--; sess.cur.reps = 0; sess.bad--; { const n = (sess.hard.get(sess.cur.id) || 1) - 1; n > 0 ? sess.hard.set(sess.cur.id, n) : sess.hard.delete(sess.cur.id); }
      // zuvor eingetragenen Fehler zurücknehmen und als richtig werten
      sess.queue = sess.queue.filter(x => x !== sess.cur); sess.cur.finished = false; grade(true); renderStep(); break; }
    case 'quit': if (!sess.items.some(i => i.finished) || confirm('Runde beenden? Erledigte Wörter sind gespeichert.')) { const b = sess.back; sess = null; save(); go(b); } break;
    case 'export': {
      const txt = JSON.stringify(S);
      (navigator.clipboard ? navigator.clipboard.writeText(txt).then(() => toast('Fortschritt kopiert ✓')) : Promise.reject()).catch(() => prompt('Fortschritt kopieren:', txt));
      break; }
    case 'import': {
      const txt = prompt('Gesicherten Fortschritt hier einfügen:'); if (!txt) break;
      try { const r = JSON.parse(txt); if (!r.cards) throw 0; S = { ...defaults(), ...r }; save(); closeSettings(); render(); toast('Fortschritt wiederhergestellt ✓'); }
      catch (err) { toast('Das war kein gültiger Fortschritt'); }
      break; }
    case 'reset': if (confirm('Wirklich den gesamten Fortschritt löschen?')) { S = defaults(); save(); closeSettings(); go('#/'); render(); toast('Zurückgesetzt'); } break;
  }
});

// Tastatur (Desktop): Leertaste = aufdecken, ←/→ = bewerten, 1–4 = Auswahl, Enter = weiter
document.addEventListener('keydown', e => {
  if (!sess || location.hash !== '#/lernen' || document.getElementById('settings')) return;
  const typing = e.target && e.target.tagName === 'INPUT';
  if (typing) return;
  const it = sess.cur; if (!it) return;
  if (it.type === 'intro' && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); document.querySelector('[data-act=intro-ok]').click(); }
  else if (it.type === 'flip') {
    if (!sess.revealed && (e.key === ' ' || e.key === 'Enter')) { e.preventDefault(); reveal(); }
    else if (sess.revealed && e.key === 'ArrowRight') document.querySelector('[data-act=grade-yes]').click();
    else if (sess.revealed && e.key === 'ArrowLeft') document.querySelector('[data-act=grade-no]').click();
  } else if (it.type === 'mc' && /^[1-4]$/.test(e.key)) { const b = document.querySelectorAll('.opt')[+e.key - 1]; b && b.click(); }
  if (sess.awaiting && e.key === 'Enter') { const n = document.querySelector('[data-act=next]'); n && n.click(); }
});

window.addEventListener('pagehide', save);

if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
  navigator.serviceWorker.register('sw.js').catch(() => {});
}
render();
})();
