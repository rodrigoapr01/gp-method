/* GP METHOD bozza v2: Giorgia guida tutta la pagina. */

const WHATSAPP = '393935896994'; // same constant as ../main.js (root site)

/* ======================================================================
   GUIDE CONFIG: the only place to touch when the video changes.
   BEATS: frame number (f_###.webp) where each gesture reads clearly.
   null = this gesture is not in the current video: FALLBACK says which beat stands in.
   SCENES: page order; each section hangs on its beats (a scene with several beats is
   scrubbed from the first to the last as the section passes the middle of the screen).
   ====================================================================== */
const GUIDE = {
  frameCount: 193,
  lead: 8, // a card arrives this many frames before its gesture peaks
  BEATS: {
    hello: 4, present: null, pointUp: null, pointMid: null,
    one: 48, two: 98, three: 126, pointDown: 172, thumbsUp: null,
  },
  FALLBACK: { present: 'hello', pointUp: 'hello', pointMid: 'hello', thumbsUp: 'hello' },
  SCENES: [
    { el: '#hero', beats: ['hello', 'present'] },
    { el: '#livelli', beats: ['one', 'two', 'three', 'pointDown'] },
    { el: '#metodo', beats: ['pointUp', 'pointMid'] },
    { el: '#weal-house', beats: ['present'] },
    { el: '#chi-e-giorgia', beats: ['pointMid'] },
    { el: '#mappa', beats: ['pointDown'] },
    { el: '#fine', beats: ['thumbsUp'] },
  ],
};

/* Level details: the approved texts of the current site (../index.html). */
const LEVELS = {
  essential: {
    n: 1, name: 'Essential', price: '€149', badge: null,
    pitch: 'Il tuo programma, in autonomia.',
    items: ['Programmazione personalizzata, 3-4 giorni', 'Progressioni Week 1–6', 'RPE e indicazioni sui carichi',
      'Warm-up specifici', 'Lavoro Shape, Strength e Performance', 'Conditioning', 'Video exercise library',
      'Linee guida cardio', 'Check finale'],
    wa: 'Ciao Giorgia, vorrei iniziare GP METHOD | ESSENTIAL.', cta: 'Inizia con Essential',
  },
  coaching: {
    n: 2, name: 'Coaching', price: '€249', badge: ['Consigliato', 'badge--red'],
    pitch: 'Programma su misura e Giorgia che ti segue.',
    items: ['Programma costruito dopo assessment e video call', '3-5 giorni di allenamento', 'Check ogni 2 settimane',
      'Analisi tecnica dei video', 'Adattamenti della programmazione', 'Gestione cardio e conditioning',
      "Indicazioni generali su alimentazione sportiva e integrazione, nell'ambito delle competenze di un personal trainer",
      'Supporto diretto', 'Review finale'],
    wa: 'Ciao Giorgia, vorrei iniziare GP METHOD | COACHING.', cta: 'Scegli Coaching',
  },
  elite: {
    n: 3, name: 'Elite', price: '€399', badge: ['Posti limitati', ''],
    pitch: 'Il livello più alto: Giorgia, a distanza.',
    items: ['Assessment 1:1 approfondito', 'Programmazione completamente individuale', 'Check settimanale',
      'Feedback video prioritario', 'Adattamenti continui', 'Strategia performance e recupero', 'Due call 1:1',
      'Gestione dei giorni ON/OFF', 'GP Performance Review finale'],
    wa: 'Ciao Giorgia, vorrei candidarmi a GP METHOD | ELITE.', cta: 'Candidati a Elite',
  },
};

const root = document.documentElement;
const reduceMotion = !root.classList.contains('scrub');
const waUrl = (msg) => `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`;
const frameUrl = (n) => `assets/seq/f_${String(n).padStart(3, '0')}.webp`;

/* ---------- WhatsApp: one constant, a pre-filled message per link ---------- */

function wireWhatsApp(scope = document) {
  scope.querySelectorAll('[data-wa]').forEach((link) => {
    link.href = waUrl(link.dataset.wa);
    link.target = '_blank';
    link.rel = 'noopener';
  });
}
wireWhatsApp();

/* ---------- Beats ---------- */

function beatFrame(name) {
  const f = GUIDE.BEATS[name];
  if (f != null) return f;
  const stand = GUIDE.FALLBACK[name];
  return stand ? beatFrame(stand) : 1;
}

/* ---------- Frames ---------- */

const frames = new Array(GUIDE.frameCount + 1);
function loadFrame(n) {
  return new Promise((resolve) => {
    const img = new Image();
    img.decoding = 'async';
    img.onload = () => { frames[n] = img; resolve(); };
    img.onerror = () => resolve();
    img.src = frameUrl(n);
  });
}
async function loadRange(from, to, onEach, concurrency = 6) {
  let next = from;
  const worker = async () => {
    while (next <= to) { const n = next++; await loadFrame(n); onEach?.(); }
  };
  await Promise.all(Array.from({ length: concurrency }, worker));
}

/* ---------- Preloader ---------- */

const preloader = document.querySelector('.preloader');
const preloaderBar = document.querySelector('.preloader-line span');
let preloaderClosed = false;
let lenis = null;

function closePreloader() {
  if (preloaderClosed || !preloader) return;
  preloaderClosed = true;
  const finish = () => {
    preloader.classList.add('is-done');
    root.classList.remove('is-loading');
    setTimeout(() => preloader.classList.add('is-gone'), 380);
    lenis?.start();
  };
  if (reduceMotion) { finish(); return; }
  preloader.classList.add('is-lighting'); // two flickers, 340ms
  setTimeout(finish, 360);                // then a 360ms fade: < 900ms in total
}
document.querySelector('.preloader-skip')?.addEventListener('click', closePreloader);

/* ---------- Canvas: draw only when the frame changes ---------- */

const guideEl = document.querySelector('.guide');
const canvas = document.querySelector('.guide-canvas');
const ctx = canvas?.getContext('2d');
let currentFrame = 0;
let box = null;

function measure() {
  if (!canvas) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(h * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.imageSmoothingQuality = 'high';
  box = { w, h };
  currentFrame = 0;
}
function nearestLoaded(n) {
  for (let i = n; i >= 1; i--) if (frames[i]) return i;
  for (let i = n + 1; i <= GUIDE.frameCount; i++) if (frames[i]) return i;
  return 0;
}
function draw(n) {
  const k = nearestLoaded(n);
  if (!k || k === currentFrame || !box) return;
  currentFrame = k;
  ctx.clearRect(0, 0, box.w, box.h);
  ctx.drawImage(frames[k], 0, 0, box.w, box.h);
}

/* ---------- Scenes: which frame for the current scroll ---------- */

const scenes = GUIDE.SCENES
  .map((s) => ({ ...s, node: document.querySelector(s.el), frames: s.beats.map(beatFrame) }))
  .filter((s) => s.node);

function sceneFrame() {
  const focus = window.innerHeight * 0.5;
  let scene = null;
  let rect = null;
  for (const s of scenes) {
    const r = s.node.getBoundingClientRect();
    if (r.top <= focus && r.bottom > focus) { scene = s; rect = r; break; }
  }
  if (!scene) return null;
  const p = Math.min(Math.max((focus - rect.top) / rect.height, 0), 1);
  let a = Math.min(...scene.frames);
  let b = Math.max(...scene.frames);
  if (a === b) { a = Math.max(1, a - 3); b = Math.min(GUIDE.frameCount, b + 10); } // a held gesture still breathes
  if (scene.el === '#livelli') a = Math.max(1, a - GUIDE.lead);
  return Math.round(a + (b - a) * p);
}

/* Level cards follow her fingers */
const beatEls = [...document.querySelectorAll('.beat[data-beat]')];
function setBeats(frame) {
  beatEls.forEach((el) => el.classList.toggle('is-on', frame >= beatFrame(el.dataset.beat) - GUIDE.lead));
}

/* ---------- Method accordions ---------- */

document.querySelectorAll('.pillar-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    btn.setAttribute('aria-expanded', String(btn.getAttribute('aria-expanded') !== 'true'));
  });
});
// open the pillar named in the URL (#shape, #strength, #performance)
if (/^#[a-z-]+$/.test(location.hash)) {
  document.querySelector(`${location.hash} > .pillar-btn`)?.setAttribute('aria-expanded', 'true');
}

/* ---------- Lockups: every line set to the same width ---------- */

function fitLockups() {
  document.querySelectorAll('[data-fit]').forEach((lockup) => {
    const width = lockup.clientWidth;
    if (!width) return;
    lockup.querySelectorAll(':scope > span:not(.sr-only)').forEach((line) => {
      line.style.fontSize = '100px';
      const natural = line.scrollWidth;
      if (natural) line.style.fontSize = `${(100 * width) / natural}px`;
    });
    lockup.classList.add('is-fitted');
  });
  // Method words: each one justified to the column width (like the lockup lines), max 80px
  document.querySelectorAll('.pillar-word').forEach((word) => {
    const avail = word.closest('.pillar-btn').clientWidth - 26;
    word.style.fontSize = '100px';
    word.style.fontSize = `${Math.min(80, (100 * avail) / word.scrollWidth).toFixed(1)}px`;
  });
}

/* ---------- Weal House neon: switches on once when the section comes into view ---------- */

const weal = document.querySelector('.weal');
if (weal && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) { weal.classList.add('is-lit'); io.disconnect(); }
  }, { threshold: 0.3 });
  io.observe(weal);
} else {
  weal?.classList.add('is-lit');
}

/* ---------- Level sheet: bottom sheet (phone) / side panel (desktop) ---------- */

const sheet = document.getElementById('level-sheet');
const sheetBody = sheet?.querySelector('.sheet-body');
const sheetInner = sheet?.querySelector('.sheet-inner');
let sheetOpener = null;

function fillSheet(key) {
  const l = LEVELS[key];
  const badge = l.badge ? `<span class="badge ${l.badge[1]}">${l.badge[0]}</span>` : '';
  sheetBody.innerHTML = `
    <div class="sheet-head">
      <h2 class="sheet-title" id="sheet-title">${l.name}</h2>
      ${badge}
      <p class="sheet-price"><strong>${l.price}</strong> <span>/ 6 settimane</span></p>
    </div>
    <p>${l.pitch}</p>
    <div><h3>Durata</h3><p>6 settimane</p></div>
    <div><h3>A chi è adatto</h3><p class="tbc">[TESTO DA CONFERMARE]</p></div>
    <div><h3>Cosa include</h3><ul class="sheet-list">${l.items.map((i) => `<li>${i}</li>`).join('')}</ul></div>
    <div class="sheet-actions">
      <a class="btn btn--ink" data-wa="${l.wa}" href="programmi.html#${key}">
        <svg class="wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-wa"/></svg>
        ${l.cta}
      </a>
      <a class="btn btn--ghost" href="programmi.html#${key}">Vedi tutti i dettagli</a>
    </div>`;
  wireWhatsApp(sheetBody);
  sheetBody.scrollTop = 0;
}

function openSheet(key, opener) {
  if (!sheet?.showModal) { location.href = `programmi.html#${key}`; return; }
  sheetOpener = opener;
  fillSheet(key);
  sheet.showModal();
  lenis?.stop();
  sheet.getBoundingClientRect(); // commit the closed position, then animate in
  sheet.classList.add('is-open');
  sheet.querySelector('.sheet-close').focus();
}

function closeSheet() {
  if (!sheet?.open || sheet.classList.contains('is-closing')) return;
  sheet.classList.add('is-closing');
  sheet.classList.remove('is-open');
  sheetInner.style.transform = '';
  const done = () => {
    sheet.classList.remove('is-closing');
    sheet.close();
    lenis?.start();
    sheetOpener?.focus(); // focus returns to the card
  };
  if (reduceMotion) done(); else setTimeout(done, 270);
}

document.querySelectorAll('.lane-btn').forEach((btn) => {
  btn.addEventListener('click', () => openSheet(btn.dataset.level, btn));
});
sheet?.querySelector('.sheet-close').addEventListener('click', closeSheet);
sheet?.addEventListener('cancel', (e) => { e.preventDefault(); closeSheet(); }); // Esc
sheet?.addEventListener('click', (e) => { if (e.target === sheet) closeSheet(); }); // backdrop

/* Swipe down to close (phone): from the grab bar or the sheet header */
(function swipe() {
  if (!sheet) return;
  const phone = window.matchMedia('(max-width: 1023px)');
  let startY = 0; let startT = 0; let dy = 0; let dragging = false;
  sheet.addEventListener('pointerdown', (e) => {
    if (!phone.matches || dragging) return;
    if (!e.target.closest('.sheet-grab, .sheet-head')) return;
    dragging = true; startY = e.clientY; startT = performance.now(); dy = 0;
    sheet.classList.add('is-dragging');
    e.target.setPointerCapture?.(e.pointerId);
  });
  sheet.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const raw = e.clientY - startY;
    dy = raw >= 0 ? raw : raw * 0.15; // dragging up: friction, not a wall
    sheetInner.style.transform = `translateY(${dy}px)`;
  });
  const end = () => {
    if (!dragging) return;
    dragging = false;
    sheet.classList.remove('is-dragging');
    const velocity = dy / (performance.now() - startT);
    if (dy > sheetInner.offsetHeight * 0.25 || velocity > 0.11) closeSheet();
    else sheetInner.style.transform = '';
  };
  sheet.addEventListener('pointerup', end);
  sheet.addEventListener('pointercancel', end);
})();

/* ---------- WhatsApp fixed button: never in the hero, never next to another WhatsApp button ---------- */

const fab = document.querySelector('.fab');
const hero = document.querySelector('#hero');
const footer = document.querySelector('.foot');
const ctaRow = document.querySelector('.cta-row');
const pageButtons = [...document.querySelectorAll('main .btn, main .lane-btn')];
function fabWanted() {
  if (!fab || !hero) return false;
  const vh = window.innerHeight;
  const pastHero = hero.getBoundingClientRect().bottom < vh * 0.4;
  const atFooter = footer.getBoundingClientRect().top < vh;
  const ctaRect = ctaRow?.getBoundingClientRect();
  const ctaOn = ctaRow && (reduceMotion || ctaRow.classList.contains('is-on')) && ctaRect.top < vh && ctaRect.bottom > 0;
  // step aside whenever another button sits where the fixed one would cover it
  const covering = pageButtons.some((b) => { const r = b.getBoundingClientRect(); return r.bottom > vh - 84 && r.top < vh; });
  return pastHero && !atFooter && !ctaOn && !covering;
}

/* ---------- Smooth scroll (Lenis), off with reduced motion ---------- */

if (!reduceMotion && window.Lenis) lenis = new window.Lenis({ lerp: 0.12, anchors: true });

/* In-page links: smooth for taps and clicks, an instant jump for keyboard activation
   (event.detail === 0). Focus follows the jump. */
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (event.detail !== 0 || link.hash.length < 2) return;
    const target = document.querySelector(link.hash);
    if (!target) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    if (lenis) lenis.scrollTo(target, { immediate: true, force: true }); else target.scrollIntoView({ behavior: 'instant' });
    target.focus({ preventScroll: true });
  }, { capture: true });
});

/* ---------- Loop: reads first, then writes, only on change ---------- */

let lastFrame = 0;
let fabOn = false;
function tick(time) {
  lenis?.raf(time);
  const f = !reduceMotion && box ? sceneFrame() : null;
  const wantFab = fabWanted();
  if (f !== null && f !== lastFrame) { draw(f); setBeats(f); lastFrame = f; }
  if (wantFab !== fabOn) { fab.classList.toggle('is-visible', wantFab); fabOn = wantFab; }
  requestAnimationFrame(tick);
}

async function boot() {
  window.GP_READY = true;
  if (document.fonts?.ready) await document.fonts.ready;
  fitLockups();
  window.addEventListener('resize', () => { fitLockups(); if (box) { measure(); lastFrame = 0; } });

  if (!canvas) { requestAnimationFrame(tick); return; } // inner pages

  if (reduceMotion) {
    // Giorgia stays still on the hello frame; every card is visible in a normal column.
    await loadFrame(beatFrame('hello'));
    measure();
    draw(beatFrame('hello'));
    closePreloader();
    requestAnimationFrame(tick);
    return;
  }

  root.classList.add('is-loading');
  lenis?.stop();
  const first = beatFrame('one');
  let loaded = 0;
  await loadRange(1, first, () => {
    loaded += 1;
    preloaderBar?.style.setProperty('--p', (loaded / first).toFixed(3));
  });
  measure();
  draw(beatFrame('hello'));
  closePreloader();
  requestAnimationFrame(tick);
  loadRange(first + 1, GUIDE.frameCount, null, 4); // the rest in the background
}

boot();
