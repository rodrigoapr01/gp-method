/* GP METHOD — bozza "Giorgia ti guida". */

const WHATSAPP = '393935896994'; // same constant as ../main.js (root site)

/* Frame numbers (f_###.webp) where each gesture is clearly readable.
   The whole scroll choreography hangs on these: a new video only needs new numbers. */
const BEATS = { hello: 4, one: 48, two: 98, three: 126, point: 172 };
const FRAME_COUNT = 193;
const LEAD = 8; // a card arrives this many frames before its gesture peaks

const root = document.documentElement;
const reduceMotion = !root.classList.contains('scrub');
const frameUrl = (n) => `assets/seq/f_${String(n).padStart(3, '0')}.webp`;

/* ---------- WhatsApp: one constant, a pre-filled message per link ---------- */

document.querySelectorAll('[data-wa]').forEach((link) => {
  link.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(link.dataset.wa)}`;
  link.target = '_blank';
  link.rel = 'noopener';
});

/* ---------- Frames: up to BEATS.one first (that is what the preloader counts), the rest after ---------- */

const frames = new Array(FRAME_COUNT + 1);

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
    while (next <= to) {
      const n = next++;
      await loadFrame(n);
      onEach?.();
    }
  };
  await Promise.all(Array.from({ length: concurrency }, worker));
}

/* ---------- Preloader ---------- */

const preloader = document.querySelector('.preloader');
const preloaderBar = document.querySelector('.preloader-line span');
let preloaderClosed = false;

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
  preloader.classList.add('is-lighting');   // two flickers, 340ms
  setTimeout(finish, 360);                  // then a 360ms fade: < 900ms in total
}

document.querySelector('.preloader-skip')?.addEventListener('click', closePreloader);

/* ---------- Canvas: draw only when the frame changes ---------- */

const guide = document.querySelector('.guide');
const canvas = document.querySelector('.guide-canvas');
const ctx = canvas?.getContext('2d');
const desktop = window.matchMedia('(min-width: 1024px)');
let currentFrame = 0;
let layout = null;

function measure() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(h * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.imageSmoothingQuality = 'high';
  const ratio = 480 / 854;
  const fh = desktop.matches ? h * 0.98 : h * 0.9;
  const fw = fh * ratio;
  const cx = desktop.matches ? w * 0.72 : w / 2;
  layout = { w, h, x: cx - fw / 2, y: h * 0.03, fw, fh };
  currentFrame = 0; // force a redraw
}

function nearestLoaded(n) {
  for (let i = n; i >= 1; i--) if (frames[i]) return i;
  for (let i = n + 1; i <= FRAME_COUNT; i++) if (frames[i]) return i;
  return 0;
}

function draw(n) {
  const k = nearestLoaded(n);
  if (!k || k === currentFrame) return;
  currentFrame = k;
  ctx.clearRect(0, 0, layout.w, layout.h);
  ctx.drawImage(frames[k], layout.x, layout.y, layout.fw, layout.fh);
}

/* ---------- Choreography: which beats are on for a frame ---------- */

const beatEls = {
  hello: document.querySelector('[data-beat="hello"]'),
  one: document.querySelector('[data-beat="one"]'),
  two: document.querySelector('[data-beat="two"]'),
  three: document.querySelector('[data-beat="three"]'),
  point: document.querySelector('[data-beat="point"]'),
};
const lanes = document.querySelector('.lanes');

function setBeats(frame) {
  const reached = (k) => frame >= BEATS[k] - LEAD;
  const lanesOn = reached('one');
  // Phone: the lockup gives the lower third to the lanes. Desktop: it stays.
  beatEls.hello.classList.toggle('is-on', desktop.matches || !lanesOn);
  beatEls.one.classList.toggle('is-on', lanesOn);
  beatEls.two.classList.toggle('is-on', reached('two'));
  beatEls.three.classList.toggle('is-on', reached('three'));
  beatEls.point.classList.toggle('is-on', reached('point'));
  lanes.classList.toggle('has-on', lanesOn);
}

function frameForScroll() {
  const rect = guide.getBoundingClientRect();
  const travel = guide.offsetHeight - window.innerHeight;
  const p = Math.min(Math.max(-rect.top / travel, 0), 1);
  return 1 + Math.round(p * (FRAME_COUNT - 1));
}

/* ---------- Method: the three words drift sideways with the scroll ---------- */

const method = document.querySelector('.method');
const driftWords = [...document.querySelectorAll('[data-drift]')];

function driftShift() {
  // read: where the method section sits (null when off-screen)
  const r = method.getBoundingClientRect();
  if (r.bottom < 0 || r.top > window.innerHeight) return null;
  const p = (window.innerHeight - r.top) / (window.innerHeight + r.height); // 0..1 across the viewport
  return (p - 0.5) * 6; // vw, at most ±3vw
}

function applyDrift(shift) {
  // write: transforms only
  driftWords.forEach((el) => {
    el.style.transform = `translate3d(${shift * Number(el.dataset.drift)}vw, 0, 0)`;
  });
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
}

/* ---------- Weal House neon: lights up once when the panel comes into view ---------- */

const weal = document.querySelector('.weal');
if ('IntersectionObserver' in window && weal) {
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) { weal.classList.add('is-lit'); io.disconnect(); }
  }, { threshold: 0.35 });
  io.observe(weal);
} else {
  weal?.classList.add('is-lit');
}

/* ---------- WhatsApp fixed button: after the guide, out of the way at the footer ---------- */

const fab = document.querySelector('.fab');
const footer = document.querySelector('.foot');
function fabWanted() {
  if (!fab || !guide) return false;
  const afterGuide = guide.getBoundingClientRect().bottom < window.innerHeight * 0.5;
  const atFooter = footer.getBoundingClientRect().top < window.innerHeight;
  return afterGuide && !atFooter;
}

/* ---------- Smooth scroll (Lenis), off with reduced motion ---------- */

let lenis = null;
if (!reduceMotion && window.Lenis) {
  lenis = new window.Lenis({ lerp: 0.12, anchors: true });
  if (!guide) { const loop = (t) => { lenis.raf(t); requestAnimationFrame(loop); }; requestAnimationFrame(loop); }
}

/* ---------- Boot ---------- */

let lastBeatFrame = 0;
let lastShift = null;
let fabOn = false;

function tick(time) {
  lenis?.raf(time);
  // 1. reads (layout) first
  const scrub = !reduceMotion && layout;
  const f = scrub ? frameForScroll() : 0;
  const shift = scrub ? driftShift() : null;
  const wantFab = fabWanted();
  // 2. then writes, and only when something changed
  if (scrub) {
    draw(f);
    if (f !== lastBeatFrame) { setBeats(f); lastBeatFrame = f; }
    if (shift !== null && shift !== lastShift) { applyDrift(shift); lastShift = shift; }
  }
  if (wantFab !== fabOn) { fab.classList.toggle('is-visible', wantFab); fabOn = wantFab; }
  requestAnimationFrame(tick);
}

async function boot() {
  window.GP_READY = true;
  if (document.fonts?.ready) await document.fonts.ready;
  fitLockups();
  window.addEventListener('resize', () => { fitLockups(); if (layout) measure(); });
  if (!guide) return; // placeholder pages: lockup, WhatsApp links and Lenis only

  if (reduceMotion) {
    // Static Giorgia (the <img> of the hello frame), cards in a normal column.
    await loadFrame(BEATS.hello);
    closePreloader();
    requestAnimationFrame(tick);
    return;
  }

  root.classList.add('is-loading');
  lenis?.stop();
  let loaded = 0;
  const first = BEATS.one;
  await loadRange(1, first, () => {
    loaded += 1;
    preloaderBar?.style.setProperty('--p', (loaded / first).toFixed(3));
  });
  measure();
  draw(1);
  setBeats(1);
  closePreloader();
  requestAnimationFrame(tick);
  loadRange(first + 1, FRAME_COUNT, null, 4); // background
}

boot();
