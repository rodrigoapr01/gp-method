const WHATSAPP = '393935896994';

/* In-page links: smooth scroll for taps and clicks (CSS), an instant jump for keyboard
   activation (event.detail === 0) and for the skip link. Focus follows the jump. */
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = link.hash.length > 1 && document.querySelector(link.hash);
    if (!target || (event.detail !== 0 && !link.classList.contains('skip'))) return;
    event.preventDefault();
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.scrollIntoView({ behavior: 'instant' });
    target.focus({ preventScroll: true });
    history.replaceState(null, '', link.hash);
  });
});

/* Every [data-wa] link opens WhatsApp with its own pre-filled message. */
document.querySelectorAll('[data-wa]').forEach((link) => {
  link.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(link.dataset.wa)}`;
  link.target = '_blank';
  link.rel = 'noopener';
});

/* "Cosa include": the button owns the state; CSS animates the panel (grid row 0fr -> 1fr). */
document.querySelectorAll('.include-btn').forEach((button) => {
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
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
