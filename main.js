const WHATSAPP = '393935896994';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

/* Skip link is a keyboard action: jump instantly, no smooth scroll. */
document.querySelector('.skip')?.addEventListener('click', (event) => {
  const target = document.querySelector(event.currentTarget.hash);
  if (!target) return;
  event.preventDefault();
  target.scrollIntoView({ behavior: 'instant' });
  target.focus({ preventScroll: true });
});

/* Every [data-wa] link opens WhatsApp with its own pre-filled message. */
document.querySelectorAll('[data-wa]').forEach((link) => {
  link.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(link.dataset.wa)}`;
  link.target = '_blank';
  link.rel = 'noopener';
});

/* "Cosa include": height + opacity, interruptible (always starts from the current height). */
document.querySelectorAll('.include-btn').forEach((button) => {
  const panel = document.getElementById(button.getAttribute('aria-controls'));

  panel.addEventListener('transitionend', (event) => {
    if (event.target !== panel || event.propertyName !== 'height') return;
    if (button.getAttribute('aria-expanded') === 'true') {
      panel.style.height = 'auto';
    } else {
      panel.style.visibility = 'hidden';
    }
  });

  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));

    if (reduceMotion.matches) {
      panel.style.height = open ? 'auto' : '0px';
      panel.style.opacity = open ? '1' : '0';
      panel.style.visibility = open ? 'visible' : 'hidden';
      return;
    }

    const from = panel.getBoundingClientRect().height;
    panel.style.visibility = 'visible';
    panel.style.height = `${from}px`;
    panel.getBoundingClientRect(); // commit the start height
    panel.style.height = open ? `${panel.scrollHeight}px` : '0px';
    panel.style.opacity = open ? '1' : '0';
  });
});

/* Mobile WhatsApp button: only after the hero; steps aside when another WhatsApp button is on screen. */
const fab = document.querySelector('.fab');
const hero = document.querySelector('.hero');
const closing = document.querySelector('.closing');
const footer = document.querySelector('.foot');

if (fab && 'IntersectionObserver' in window) {
  const inView = new Map();
  const update = () => {
    const show = [...inView.values()].every((visible) => !visible);
    fab.classList.toggle('is-visible', show);
  };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => inView.set(entry.target, entry.isIntersecting));
    update();
  }, { threshold: 0 });
  const levelButtons = document.querySelectorAll('.level .btn');
  [hero, closing, footer, ...levelButtons].forEach((el) => {
    inView.set(el, el === hero);
    observer.observe(el);
  });
}
