/* GP METHOD v4 */

const WHATSAPP = '393935896994';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- WhatsApp: one number, every button names its level or page ---------- */

document.querySelectorAll('[data-wa]').forEach((link) => {
  link.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(link.dataset.wa)}`;
  link.target = '_blank';
  link.rel = 'noopener';
});

/* ---------- Full-screen menu (phones): a modal dialog = focus trap + Esc for free ---------- */

const menu = document.getElementById('menu');
const menuBtn = document.querySelector('.menu-btn');
if (menu && menuBtn) {
  menuBtn.addEventListener('click', () => {
    menu.showModal();
    menuBtn.setAttribute('aria-expanded', 'true');
  });
  menu.addEventListener('close', () => {
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.focus();
  });
  menu.querySelector('.menu-close').addEventListener('click', () => menu.close());
  // a link to a section of this page: close the menu first so the page can scroll
  menu.querySelectorAll('nav a').forEach((a) => a.addEventListener('click', () => menu.close()));
}

/* ---------- "Cosa include", the method pillars and the FAQ: the button owns the state, CSS animates the panel ---------- */

document.querySelectorAll('.include-btn, .pillar-btn, .faq-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    btn.setAttribute('aria-expanded', String(btn.getAttribute('aria-expanded') !== 'true'));
  });
});

/* ---------- The cycle: tap a stage, its line shows under the row ---------- */

document.querySelectorAll('[data-steps]').forEach((wrap) => {
  const note = wrap.querySelector('.step-note');
  wrap.querySelectorAll('.step').forEach((step) => {
    step.addEventListener('click', () => {
      wrap.querySelectorAll('.step').forEach((s) => s.setAttribute('aria-pressed', String(s === step)));
      note.textContent = step.dataset.note;
    });
  });
});

/* ---------- Neon: the glow switches on once when the USP comes into view.
   Only the glow layer flickers; the words are readable from the start. ---------- */

const neon = document.querySelector('[data-neon]');
if (neon && !reduceMotion && 'IntersectionObserver' in window) {
  neon.classList.add('neon-wait');
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) {
      neon.classList.add('is-lit');
      io.disconnect();
    }
  }, { threshold: 0.5 });
  io.observe(neon);
}

// the red tube glitches when the pointer passes over the sign or a finger taps it (once per second at most)
const redTube = neon && neon.querySelector('.neon-line--red');
if (redTube && !reduceMotion) {
  const glitch = () => {
    if (redTube.classList.contains('is-glitch')) return;
    redTube.classList.add('is-glitch');
    setTimeout(() => redTube.classList.remove('is-glitch'), 1000);
  };
  neon.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') glitch(); });
  neon.addEventListener('pointerdown', glitch, { passive: true });
  // phones have no hover: the sign glitches by itself each time it scrolls into view
  if (window.matchMedia('(hover: none)').matches && 'IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) setTimeout(glitch, 900);
    }, { threshold: 0.6 }).observe(neon);
  }
}

/* ---------- Gallery: tap = large view; close with X, Esc, tap outside or swipe down ---------- */

const lightbox = document.querySelector('.lightbox');
if (lightbox) {
  const img = lightbox.querySelector('.lightbox-img');
  let opener = null;
  document.querySelectorAll('.tile').forEach((tile) => {
    tile.addEventListener('click', () => {
      opener = tile;
      img.src = tile.dataset.full;
      img.alt = tile.dataset.alt;
      img.style.transform = '';
      lightbox.showModal();
    });
  });
  lightbox.addEventListener('close', () => opener?.focus());
  lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox) lightbox.close(); });

  // swipe down: the photo follows the finger; past 120px or a fast flick it closes
  let startY = null; let startT = 0; let dy = 0;
  img.addEventListener('pointerdown', (e) => {
    if (startY !== null) return; // ignore a second finger
    startY = e.clientY; startT = performance.now(); dy = 0;
    img.setPointerCapture(e.pointerId);
  });
  img.addEventListener('pointermove', (e) => {
    if (startY === null) return;
    dy = e.clientY - startY;
    img.style.transform = `translateY(${dy > 0 ? dy : dy * 0.2}px)`; // upwards: friction, not a wall
  });
  const end = () => {
    if (startY === null) return;
    const velocity = Math.abs(dy) / (performance.now() - startT);
    startY = null;
    if (dy > 120 || (dy > 20 && velocity > 0.11)) lightbox.close();
    img.style.transform = '';
  };
  img.addEventListener('pointerup', end);
  img.addEventListener('pointercancel', end);
}

/* ---------- WhatsApp fixed button (phones; hidden by CSS from 768px): after the hero, never next to
   another WhatsApp button, and out of the way when any button or link reaches the bottom strip it sits in ---------- */

const fab = document.querySelector('.fab');
if (fab && 'IntersectionObserver' in window) {
  const first = document.querySelector('.hero, .intro');
  const others = [...document.querySelectorAll('main [data-wa], .foot')];
  const state = new Map([[first, true], ...others.map((el) => [el, false])]);
  const covered = new Set();  // controls currently inside the bottom strip
  const update = () => fab.classList.toggle('is-visible', covered.size === 0 && [...state.values()].every((v) => !v));
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => state.set(e.target, e.isIntersecting));
    update();
  });
  [first, ...others].forEach((el) => el && io.observe(el));

  const controls = [...document.querySelectorAll('main .btn, main .text-link, main .row, main .faq-btn, main .include-btn')];
  let strip = null;
  const watchStrip = () => {
    if (strip) strip.disconnect();
    covered.clear();
    // only the bottom 84px of the screen count: that is where the button lives
    strip = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? covered.add(e.target) : covered.delete(e.target)));
      update();
    }, { rootMargin: `-${Math.max(0, window.innerHeight - 84)}px 0px 0px 0px` });
    controls.forEach((el) => strip.observe(el));
  };
  watchStrip();
  let t = 0;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(watchStrip, 200); });
}
