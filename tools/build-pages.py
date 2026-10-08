"""Writes index.html, livelli.html and chi-sono.html (static output, committed).
Shared header, menu and footer live here once; the official logo files are used as they are. Run: python3 tools/build-pages.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://rodrigoapr01.github.io/gp-method/"
# link preview (WhatsApp, Instagram, Facebook): the metal logo; bump ?v= when the image changes, WhatsApp caches hard
OG_IMAGE = f"{BASE}assets/og/og-gp-method.jpg?v=2"

WA_ICON = ('<svg class="i-wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
           '<path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" '
           'd="M20.5 11.7a8.4 8.4 0 0 1-12.4 7.4L3.5 20.5l1.4-4.4a8.4 8.4 0 1 1 15.6-4.4z"/>'
           '<path fill="currentColor" d="M9.1 7.9c.2-.4.4-.4.6-.4h.5c.2 0 .4 0 .5.3l.7 1.7c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5a5.6 5.6 0 0 0 2.6 2.3c.2.1.4.1.5-.1l.7-.8c.2-.2.3-.2.5-.1l1.6.8c.2.1.3.2.3.3v.5c0 .5-.4 1.1-1 1.3-.6.3-1.6.3-3-.3a8.6 8.6 0 0 1-3.7-3.5c-.7-1.2-.6-2.3-.2-3.2z"/></svg>')


# official logo: the round metal logo without background (assets/brand): the light metal on the dark pages,
# the dark metal on /chiaro/ (swapped in write_chiaro). The flat files in assets/brand/lineare stay for print only.
LOGO_ROUND = "assets/brand/GP-logo-metallo-chiaro"
LOGO_DARK = "assets/brand/GP-logo-metallo-scuro"
FAVICON = "assets/brand/favicon"


def logo_round(cls, size, eager=False):
    """The round metal logo (transparent) as WebP (160/320/640) with the PNG as fallback; size = the largest CSS width it is shown at."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" sizes="{size}px" '
            f'srcset="{LOGO_ROUND}-160.webp 160w, {LOGO_ROUND}-320.webp 320w, {LOGO_ROUND}-640.webp 640w">'
            f'<img class="{cls}" src="{LOGO_ROUND}.png" width="{size}" height="{size}" alt="GP METHOD" {load} decoding="async"></picture>')


def pic(name, alt, w=1086, h=1448, cls="", eager=False, sizes="100vw"):
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="assets/palestra/{name}.webp" sizes="{sizes}">'
            f'<img{c} src="assets/palestra/{name}.jpg" width="{w}" height="{h}" alt="{alt}" {lazy} decoding="async"></picture>')


def wa_btn(msg, label, cls="btn btn--primary"):
    return f'<a class="{cls}" data-wa="{msg}" href="#contatti">{WA_ICON}<span>{label}</span></a>'


# ---------------------------------------------------------------- preloader (first visit of the session only)
# The flat circle logo from assets/brand/lineare, inline so it can be drawn: GP in one continuous stroke
# (G arc -> bar -> P stem -> belly -> stem), the ring clockwise from the top like a stopwatch hand, then METHOD and
# the tagline. Everything lives in the <head> (style + script) so it never waits for the network.
# No JS: never shown. Reduced motion: the finished logo, still, for 400ms, then the fade.
def _preloader_svg():
    import re
    src = (ROOT / "assets/brand/lineare/svg/GP-METHOD-lineare_con-cerchio_trasparente-chiaro.svg").read_text()
    src = re.sub(r"<metadata>.*?</metadata>", "", src, flags=re.S)
    paths = re.findall(r'<path d="([^"]*)"', src)
    r1 = lambda d: re.sub(r"-?\d+\.\d+", lambda m: ("%.1f" % float(m.group())).rstrip("0").rstrip("."), d)
    method, tagline = r1(paths[1]), r1(paths[2])
    rule = re.search(r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)"', src).groups()
    # the monogram path, rewritten as ONE subpath: after the G's bar it runs back along the bar (invisible) into the P
    gp = ("M538.1,341.2 A128,128 0 1 0 565.3,420 L459,420 L565.3,420 L565.3,292 "
          "L626.7,292 A64,64 0 0 1 626.7,420 L565.3,420 L565.3,598")
    ring = "M500,100 A400,400 0 1 1 500,900 A400,400 0 1 1 500,100"
    return f"""<div class="pl" id="preloader" aria-hidden="true">
    <svg class="pl-logo" viewBox="90 90 820 820" focusable="false">
      <defs><linearGradient id="pl-g" x1="200" y1="150" x2="800" y2="850" gradientUnits="userSpaceOnUse"><stop offset="0" class="pl-a"/><stop offset="1" class="pl-b"/></linearGradient></defs>
      <path class="pl-ring" d="{ring}" pathLength="1"/>
      <path class="pl-gp" d="{gp}" pathLength="1"/>
      <g class="pl-text"><circle cx="565.3" cy="420" r="5.6"/><path d="{method}"/><rect x="{rule[0]}" y="{rule[1]}" width="{rule[2]}" height="{rule[3]}"/><path d="{tagline}"/></g>
    </svg>
  </div>"""


PRELOADER_SVG = _preloader_svg()

PRELOADER_HEAD = """  <style>
    :root { --pl-bg: #191716; --pl-a: #F7EAD6; --pl-b: #B08A64; }
    .pl { display: none; }
    html.pl-on { overflow: hidden; scrollbar-gutter: stable; }  /* scroll locked, no jump when the scrollbar returns */
    html.pl-on .pl { position: fixed; inset: 0; z-index: 100; display: grid; place-items: center; background: var(--pl-bg); touch-action: none;
      transition: opacity 400ms cubic-bezier(0.23, 1, 0.32, 1); }
    .pl-logo { width: 140px; height: auto; overflow: visible; transition: transform 400ms cubic-bezier(0.23, 1, 0.32, 1); }
    @media (min-width: 900px) { .pl-logo { width: 180px; } }
    .pl-a { stop-color: var(--pl-a); } .pl-b { stop-color: var(--pl-b); }
    .pl-gp, .pl-ring { fill: none; stroke: url(#pl-g); stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
    .pl-gp { stroke-width: 7; animation: pl-draw 700ms cubic-bezier(0.77, 0, 0.175, 1) both; }
    .pl-ring { stroke-width: 3.5; animation: pl-draw 500ms cubic-bezier(0.77, 0, 0.175, 1) 500ms both; }
    .pl-text { fill: url(#pl-g); opacity: 0; transform: translateY(6px); transform-box: fill-box;
      animation: pl-rise 300ms cubic-bezier(0.23, 1, 0.32, 1) 900ms both; }
    @keyframes pl-draw { to { stroke-dashoffset: 0; } }
    @keyframes pl-rise { to { opacity: 1; transform: none; } }
    html.pl-out .pl { opacity: 0; }
    html.pl-out .pl-logo { transform: scale(0.96); }
    @media (prefers-reduced-motion: reduce) {
      .pl-gp, .pl-ring, .pl-text { animation: none; stroke-dashoffset: 0; opacity: 1; transform: none; }
      html.pl-out .pl-logo { transform: none; }
    }
  </style>
  <script>
    /* preloader: once per session; 1.6s in all (800ms with reduced motion), held until the page is parsed, never past 3s; skippable */
    (function () {
      try { if (sessionStorage.getItem('gp-pl')) return; sessionStorage.setItem('gp-pl', '1'); } catch (e) { return; }
      var d = document.documentElement, t0 = Date.now();
      var hold = matchMedia('(prefers-reduced-motion: reduce)').matches ? 400 : 1200, fade = 400, cap = 3000;
      d.classList.add('pl-on');
      var done = false;
      function finish() {
        if (done) return; done = true;
        d.classList.add('pl-out');
        setTimeout(function () { var p = document.getElementById('preloader'); if (p) p.remove(); d.classList.remove('pl-on', 'pl-out'); }, fade);
      }
      function check() {
        if (document.readyState !== 'loading' || Date.now() - t0 >= cap - fade) finish(); else setTimeout(check, 50);
      }
      setTimeout(check, hold);
      // a tap, a click or a key skips it: it is a welcome, it should never hold anyone up
      addEventListener('pointerdown', finish, { once: true });
      addEventListener('keydown', finish, { once: true });
    })();
  </script>
"""


# ---------------------------------------------------------------- /chiaro/ (light preview for the client)
# Same pages, same assets, same texts, same logo: only the colours change (chiaro/css/tema-chiaro.css).
# noindex + canonical to the main site, since it is only a preview.


def write_chiaro(file, html):
    import re
    if file == "index.html":
        # home header: over the photo on phones (light metal), over avorio from 900px (dark metal)
        a = html.index('<header class="top">'); b = html.index('</header>', a)
        head = html[a:b].replace('<picture><source type="image/webp"',
                                 '<picture><source media="(min-width: 900px)" type="image/webp" sizes="80px" srcset="'
                                 f'{LOGO_DARK}-160.webp 160w, {LOGO_DARK}-320.webp 320w, {LOGO_DARK}-640.webp 640w"><source type="image/webp"', 1)
        html = html[:a] + head.replace("GP-logo-metallo-chiaro", "@@KEEP@@") + html[b:]
    html = html.replace("GP-logo-metallo-chiaro", "GP-logo-metallo-scuro")  # dark metal on avorio
    html = html.replace("@@KEEP@@", "GP-logo-metallo-chiaro")
    html = html.replace("--pl-bg: #191716; --pl-a: #F7EAD6; --pl-b: #B08A64;", "--pl-bg: #EFE9E2; --pl-a: #8A6E58; --pl-b: #2E2620;")
    html = re.sub(r'(?<=["\s,])assets/', '../assets/', html)  # every local asset, srcset entries included
    html = html.replace('href="styles.css">', 'href="../styles.css">\n  <link rel="stylesheet" href="css/tema-chiaro.css">')
    html = html.replace('src="main.js"', 'src="../main.js"')
    html = html.replace('<meta name="theme-color" content="#191716">', '<meta name="theme-color" content="#EFE9E2">')
    html = html.replace('<meta name="color-scheme" content="dark">', '<meta name="color-scheme" content="light">\n  <meta name="robots" content="noindex">')
    (ROOT / "chiaro").mkdir(exist_ok=True)
    (ROOT / "chiaro" / file).write_text(html)


def page(file, title, desc, body, wa_msg, extra_head="", home=False):
    nav = [("index.html#metodo", "Metodo"), ("livelli.html", "Livelli"), ("chi-sono.html", "Chi sono")]
    current = {"livelli.html": "Livelli", "chi-sono.html": "Chi sono"}.get(file)
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if t == current else ""}>{t}</a>' for h, t in nav)
    html = f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#191716">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{BASE}{'' if file == 'index.html' else file}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:site_name" content="GP METHOD">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{BASE}{'' if file == 'index.html' else file}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Logo GP METHOD">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="icon" href="{FAVICON}/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="{FAVICON}/favicon-512.png" sizes="512x512" type="image/png">
  <link rel="apple-touch-icon" href="{FAVICON}/favicon-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@300;400;500;600&display=swap">
{PRELOADER_HEAD}  <link rel="stylesheet" href="styles.css">
  <script>document.documentElement.classList.add('js')</script>
  <script src="main.js" defer></script>
{extra_head}</head>
<body class="{'is-home' if home else 'is-inner'}">
  {PRELOADER_SVG}
  <a class="skip" href="#main">Vai al contenuto</a>
  <header class="top">
    <a class="brand" href="index.html">{logo_round('brand-logo', 80, eager=True)}</a>
    <nav class="top-nav" aria-label="Principale">{links}</nav>
    {wa_btn(wa_msg, 'Scrivimi', 'btn btn--secondary btn--sm top-wa')}
    <button class="menu-btn" type="button" aria-haspopup="dialog" aria-controls="menu" aria-label="Apri il menu"><span></span><span></span></button>
  </header>

  <dialog class="menu" id="menu" aria-label="Menu">
    <a class="menu-logo" href="index.html">{logo_round('menu-logo-img', 72)}</a>
    <button class="menu-close" type="button" aria-label="Chiudi il menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
    <nav aria-label="Menu">{links}</nav>
    {wa_btn(wa_msg, 'Scrivimi su WhatsApp')}
  </dialog>

  <main id="main">
{body}
  </main>

  <footer class="foot" id="contatti">
    <a class="foot-brand" href="index.html">{logo_round('foot-logo', 160)}</a>
    <nav class="foot-nav" aria-label="Pagine">{links}<a href="https://www.instagram.com/lapiras93/" target="_blank" rel="noopener">Instagram</a><a href="https://www.facebook.com/giorgia.piras.3" target="_blank" rel="noopener">Facebook</a></nav>
    <p class="foot-address">Weal House, Via Michele Amari 51, Roma</p>
    <p class="foot-credit">Sito realizzato da <a href="https://transiva.it" target="_blank" rel="noopener">Transiva</a></p>
  </footer>

  {wa_btn(wa_msg, 'Scrivimi', 'fab')}
</body>
</html>
"""
    (ROOT / file).write_text(html)
    write_chiaro(file, html)


# the four stages of a cycle; tapping one shows its line under the row.
# Lines only reuse facts already on the site (the path note and the "Cosa include" lists): to be confirmed by Giorgia.
STEPS = [
    ("Assess", "Livello, obiettivo, disponibilità, attrezzatura e capacità vengono valutati prima di costruire la programmazione."),
    ("Build", "La programmazione prende forma sulle tue giornate, con progressioni dalla Week 1 alla Week 6."),
    ("Perform", "Ti alleni con RPE e indicazioni sui carichi; con Coaching ed Elite arrivano anche check e analisi dei video."),
    ("Review", "A fine ciclo il check finale: Review con Coaching, GP Performance Review con Elite."),
]


def steps(cls="", uid="cycle"):
    lis = "".join(
        f'<li><button class="step" type="button" aria-pressed="{"true" if i == 1 else "false"}" aria-controls="{uid}-note" data-note="{note}">'
        f'<span class="step-n" aria-hidden="true">{i}</span><span class="step-w" lang="en">{w}</span></button></li>'
        for i, (w, note) in enumerate(STEPS, 1))
    return (f'<div class="steps-wrap" data-steps><ol class="steps {cls}">{lis}</ol>'
            f'<p class="step-note" id="{uid}-note" aria-live="polite">{STEPS[0][1]}</p></div>')


# Weal House on Google Maps: 5,0 out of 5 (22 reviews, checked 7 Oct 2026). Static: update by hand if the rating changes.
GOOGLE_PLACE = "https://www.google.com/maps?cid=5456743492543164649"
STAR = '<svg viewBox="0 0 24 24" focusable="false"><path d="M12 2.6l2.9 6 6.5.8-4.8 4.5 1.2 6.5L12 17.2l-5.8 3.2 1.2-6.5L2.6 9.4l6.5-.8z"/></svg>'


def reviews(page_key):
    return f'''    <section class="reviews light" aria-labelledby="reviews-{page_key}">
      <p class="stars" role="img" aria-label="5 stelle su 5">{STAR * 5}</p>
      <h2 id="reviews-{page_key}" class="title">5 su 5 su Google.</h2>
      <p class="reviews-sub">Le recensioni di Weal House, la palestra dove nasce GP METHOD.</p>
      <p class="reviews-ask">Ti alleni con Giorgia? Lascia la tua recensione.</p>
      <div class="reviews-actions">
        <a class="btn btn--dark" href="{GOOGLE_PLACE}" target="_blank" rel="noopener">Lascia una recensione</a>
        <a class="text-link" href="{GOOGLE_PLACE}" target="_blank" rel="noopener">Leggi le recensioni</a>
      </div>
    </section>'''


# ---------------------------------------------------------------- home
# Detail lines reuse what the levels already include (warm-up, video library, Week 1-6, RPE, conditioning, cardio): to be confirmed by Giorgia.
PILLARS = [
    ("shape", "Shape", "Costruzione muscolare e proporzioni",
     "Lavoro mirato per costruire muscolo e migliorare le proporzioni, con warm-up specifici e i video degli esercizi per eseguirli bene."),
    ("strength", "Strength", "Forza e progressioni",
     "Progressioni dalla Week 1 alla Week 6, con RPE e indicazioni sui carichi: sai sempre quanto spingere e quando aumentare."),
    ("performance", "Performance", "Running, conditioning, Hybrid/HYROX",
     "Conditioning e linee guida cardio dentro la stessa programmazione, per allenare anche fiato e capacità di lavoro."),
]
pillars = "".join(
    f'<li><button class="pillar-btn" type="button" aria-expanded="false" aria-controls="m-{key}">'
    f'<span class="pillar-word" lang="en">{word}</span><span class="pillar-line">{line}<span class="plus" aria-hidden="true"></span></span></button>'
    f'<div class="more-panel" id="m-{key}"><div><p>{detail}</p></div></div></li>'
    for key, word, line, detail in PILLARS)


home = f"""    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-copy">
        <p class="kicker" lang="en">Online coaching</p>
        <h1 id="hero-title" class="hero-name">Giorgia Piras<span class="hero-role">Personal trainer a Roma</span></h1>
        <span class="hero-rule" aria-hidden="true"></span>
        <p class="hero-line">Non allenarti solo per cambiare il tuo corpo. Allenalo per renderlo forte, performante e capace.</p>
        <div class="hero-actions">
          {wa_btn('Ciao Giorgia, vorrei informazioni su GP METHOD.', 'Scrivimi su WhatsApp')}
          <a class="text-link" href="#metodo">Scopri il metodo</a>
        </div>
        <p class="hero-proof"><span class="nowrap">Co-fondatrice</span> di <strong>Weal House</strong> · Via Michele Amari 51, Roma</p>
      </div>
      <figure class="hero-photo">
        <picture>
          <source media="(max-width: 767px)" type="image/webp" srcset="assets/hero/GP_hero_giorgia_mobile_studio-900.webp?v=8 900w, assets/hero/GP_hero_giorgia_mobile_studio-1280.webp?v=8 1280w, assets/hero/GP_hero_giorgia_mobile_studio.webp?v=8 1920w" sizes="100vw" width="1920" height="3124">
          <source media="(max-width: 767px)" srcset="assets/hero/GP_hero_giorgia_mobile_studio.jpg?v=8" width="1920" height="3124">
          <source type="image/webp" srcset="assets/hero/GP_hero_giorgia_desktop_studio-1280.webp?v=8 1280w, assets/hero/GP_hero_giorgia_desktop_studio.webp?v=8 1920w" sizes="100vw" width="1920" height="1086">
          <img src="assets/hero/GP_hero_giorgia_desktop_studio.jpg?v=8" width="1920" height="1086" alt="Giorgia Piras, personal trainer" fetchpriority="high" decoding="async">
        </picture>
      </figure>
    </section>

    <section class="usp" aria-labelledby="usp-title">
      <h2 id="usp-title" class="neon" data-neon>
        <span class="neon-line neon-line--white" data-text="Non devi scegliere">Non devi scegliere</span>
        <span class="neon-line neon-line--red" data-text="tra estetica">tra estetica</span>
        <span class="neon-line neon-line--white" data-text="e performance.">e performance.</span>
      </h2>
    </section>

    <section class="method light" id="metodo" aria-labelledby="method-title">
      <h2 id="method-title" class="sr-only">Il metodo</h2>
      <ul class="pillars" role="list">{pillars}</ul>
      <p class="method-close">Ogni percorso parte da te.</p>
    </section>

    <section class="cycle" aria-labelledby="cycle-title">
      <h2 id="cycle-title" class="title">Un ciclo di 6 settimane.</h2>
      {steps()}
    </section>

    <section class="preview light" aria-labelledby="preview-title">
      <h2 id="preview-title" class="sr-only">I livelli</h2>
      <ul class="rows" role="list">
        <li><a class="row" href="livelli.html#essential"><span class="row-name">Essential</span><span class="row-price"><strong>€149</strong> <span>/ 6 settimane</span></span></a></li>
        <li><a class="row" href="livelli.html#coaching"><span class="row-name">Coaching <span class="badge">Consigliato</span></span><span class="row-price"><strong>€249</strong> <span>/ 6 settimane</span></span></a></li>
        <li><a class="row" href="livelli.html#elite"><span class="row-name">Elite</span><span class="row-price"><strong>€399</strong> <span>/ 6 settimane</span></span></a></li>
      </ul>
      <div class="preview-actions">
        <a class="btn btn--dark" href="livelli.html">Scegli il tuo livello</a>
        <a class="text-link" href="livelli.html#faq">Domande frequenti</a>
      </div>
    </section>

    <section class="place" aria-labelledby="place-title">
      <div class="strip">
        {pic('sala-pista-sled', 'Sala della palestra con la pista da sled, la scritta START e i numeri a terra', 1058, 1411, sizes='(min-width: 900px) 33vw, 70vw')}
        {pic('manubri', 'Rastrelliera di manubri esagonali neri', sizes='(min-width: 900px) 33vw, 70vw')}
        {pic('neon-weal-house', 'Insegna al neon Weal House sul muro a doghe di legno', sizes='(min-width: 900px) 33vw, 70vw')}
      </div>
      <div class="place-copy">
        <h2 id="place-title" class="title">Dove nasce il metodo.</h2>
        <a class="text-link" href="chi-sono.html">Chi sono</a>
      </div>
    </section>

{reviews('home')}

    <section class="close" aria-labelledby="close-title">
      <h2 id="close-title" class="title">Iniziamo?</h2>
      {wa_btn('Ciao Giorgia, vorrei iniziare GP METHOD.', 'Scrivimi su WhatsApp')}
    </section>"""

page("index.html", "GP METHOD | Coaching online di Giorgia Piras",
     "Coaching online di Giorgia Piras, personal trainer a Roma: shape, strength e performance in cicli di 6 settimane. Tre livelli, da €149.",
     home, "Ciao Giorgia, vorrei informazioni su GP METHOD.", home=True)

# ---------------------------------------------------------------- livelli
LEVELS = [
    ("essential", "Essential", "€149", None, "Per chi vuole una programmazione strutturata senza assistenza continua.",
     "START YOUR METHOD.", "Inizia con Essential", "Ciao Giorgia, vorrei iniziare GP METHOD | ESSENTIAL.",
     ["Programmazione personalizzata, 3-4 giorni", "Progressioni Week 1–6", "RPE e indicazioni sui carichi", "Warm-up specifici",
      "Lavoro Shape, Strength e Performance", "Conditioning", "Video exercise library", "Linee guida cardio", "Check finale"]),
    ("coaching", "Coaching", "€249", "Consigliato", "Programma costruito su di te dopo assessment e video call.",
     "DON'T JUST FOLLOW A PROGRAM. BE COACHED.", "Scegli Coaching", "Ciao Giorgia, vorrei iniziare GP METHOD | COACHING.",
     ["3-5 giorni di allenamento", "Check ogni 2 settimane", "Analisi tecnica dei video", "Adattamenti della programmazione",
      "Gestione cardio e conditioning",
      "Indicazioni generali su alimentazione sportiva e integrazione, nell'ambito delle competenze di un personal trainer",
      "Supporto diretto", "Review finale"]),
    ("elite", "Elite", "€399", "Posti limitati", "Il livello più alto del coaching GP.",
     "THE HIGHEST LEVEL OF GP COACHING.", "Candidati a Elite", "Ciao Giorgia, vorrei candidarmi a GP METHOD | ELITE.",
     ["Assessment 1:1 approfondito", "Programmazione completamente individuale", "Check settimanale", "Feedback video prioritario",
      "Adattamenti continui", "Strategia performance e recupero", "Due call 1:1", "Gestione dei giorni ON/OFF", "GP Performance Review finale"]),
]
cards = []
for key, name, price, badge, line, sign, cta, msg, items in LEVELS:
    b = f'<span class="badge">{badge}</span>' if badge else '<span class="badge-slot" aria-hidden="true"></span>'
    lis = "".join(f"<li>{i}</li>" for i in items)
    btn = "btn btn--primary" if key == "coaching" else "btn btn--secondary"
    cards.append(f"""        <article class="card card--{key}" id="{key}" aria-labelledby="t-{key}">
          {b}
          <h2 class="card-name" id="t-{key}"><span class="card-brand">GP METHOD |</span> {name}</h2>
          <p class="card-price"><strong>{price}</strong> <span>/ 6 settimane</span></p>
          <p class="card-line">{line}</p>
          <p class="card-sign" lang="en">{sign}</p>
          <div class="include">
            <button class="include-btn" type="button" aria-expanded="false" aria-controls="inc-{key}">Cosa include<span class="plus" aria-hidden="true"></span></button>
            <div class="include-panel" id="inc-{key}"><ul role="list">{lis}</ul></div>
          </div>
          {wa_btn(msg, cta, btn)}
        </article>""")
# Questions and answers, in Giorgia's voice. Only facts already on the site (prices, level contents, the path).
FAQ_START = ('Come si inizia?',
             'Scrivimi su WhatsApp dicendomi il livello che ti interessa: partiamo dall\'assessment.')
FAQ = [
    ("Quanto costa?", "Essential €149, Coaching €249, Elite €399. Il prezzo è per un ciclo di 6 settimane."),
    ("Che differenza c'è tra i livelli?",
     "Essential è una programmazione strutturata senza assistenza continua, 3-4 giorni a settimana. "
     "Con Coaching costruisco il programma su di te dopo assessment e video call: 3-5 giorni, con check ogni 2 settimane. "
     "Elite è il livello più alto: programmazione completamente individuale, check settimanale e due call 1:1."),
    ("Quale livello scelgo?",
     "Se vuoi seguire una programmazione in autonomia, Essential. Se vuoi che ti segua da vicino, Coaching: è quello che consiglio. "
     "Se vuoi il massimo del supporto, anche su performance e recupero, Elite. Se hai dubbi, lo scegliamo insieme."),
    ("Quanto dura un percorso?",
     "Un ciclo dura 6 settimane e si chiude con un check finale (Essential), una review (Coaching) o la GP Performance Review (Elite)."),
    ("Sono all'inizio: va bene lo stesso?",
     "Sì. Prima di costruire la programmazione valuto livello, obiettivo, disponibilità, attrezzatura e capacità: ogni percorso parte da te."),
    ("Mi alleno online o in palestra?",
     "Il coaching è online: ricevi la programmazione e ti alleni dove ti alleni di solito. L'attrezzatura che hai a disposizione è una delle cose che valuto all'inizio."),
    ("Dai indicazioni sull'alimentazione?",
     "Con Coaching sì: indicazioni generali su alimentazione sportiva e integrazione, nell'ambito delle competenze di un personal trainer."),
]


def faq_item(i, q, a_html):
    return (f'<li><h3 class="faq-q"><button class="faq-btn" type="button" aria-expanded="false" aria-controls="faq-{i}">'
            f'{q}<span class="plus" aria-hidden="true"></span></button></h3>'
            f'<div class="more-panel" id="faq-{i}"><div><p>{a_html}</p></div></div></li>')


faq_items = "".join(faq_item(i, q, a) for i, (q, a) in enumerate(FAQ, 1))
faq_items += faq_item(len(FAQ) + 1, FAQ_START[0],
                      FAQ_START[1])
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ + [FAQ_START]]},
    ensure_ascii=False)

livelli = f"""    <section class="intro" aria-labelledby="levels-title">
      <h1 id="levels-title">Scegli il tuo livello.</h1>
      <p class="lead">Stessa filosofia, tre livelli di assistenza. Ogni ciclo dura 6 settimane.</p>
    </section>

    <section class="cards" aria-label="I tre livelli">
{chr(10).join(cards)}
    </section>

    <section class="path light" aria-labelledby="path-title">
      <h2 id="path-title" class="title">Il percorso</h2>
      {steps('steps--dark', uid='path')}
    </section>

    <section class="faq" id="faq" aria-labelledby="faq-title">
      <h2 id="faq-title" class="title">Domande frequenti</h2>
      <ul class="faq-list" role="list">{faq_items}</ul>
    </section>

    <section class="close" aria-labelledby="close-title">
      <h2 id="close-title" class="title">Iniziamo?</h2>
      {wa_btn('Ciao Giorgia, vorrei informazioni sui livelli di GP METHOD.', 'Scrivimi su WhatsApp')}
    </section>"""
page("livelli.html", "Livelli e prezzi | GP METHOD, coaching online",
     "Essential €149, Coaching €249, Elite €399: tre livelli di coaching online GP METHOD con Giorgia Piras, ogni ciclo dura 6 settimane.",
     livelli, "Ciao Giorgia, vorrei informazioni sui livelli di GP METHOD.",
     extra_head=f'  <script type="application/ld+json">{faq_ld}</script>\n')

# ---------------------------------------------------------------- chi sono
gallery = [("neon-weal-house", "Insegna al neon Weal House sul muro a doghe di legno", 1086, 1448),
           ("sala-pista-sled", "Sala con la pista da sled, la scritta START e i numeri a terra", 1058, 1411),
           ("neon-stronger-panca", "Insegna al neon Be stronger than your excuses sopra la panca e i dischi", 1086, 1448),
           ("manubri", "Rastrelliera di manubri esagonali neri", 1086, 1448)]
tiles = "".join(f'<li><button class="tile" type="button" data-full="assets/palestra/{n}.webp" data-alt="{a}" aria-label="Apri la foto: {a}">'
                f'{pic(n, a, w, h, sizes="(min-width: 900px) 33vw, 50vw")}</button></li>' for n, a, w, h in gallery)
jsonld = """  <script type="application/ld+json">
  {"@context": "https://schema.org", "@graph": [
    {"@type": "Person", "name": "Giorgia Piras", "jobTitle": "Personal trainer",
     "url": "https://rodrigoapr01.github.io/gp-method/chi-sono.html",
     "sameAs": ["https://www.instagram.com/lapiras93/", "https://www.facebook.com/giorgia.piras.3"],
     "worksFor": {"@id": "#wealhouse"}},
    {"@type": "LocalBusiness", "@id": "#wealhouse", "name": "Weal House",
     "address": {"@type": "PostalAddress", "streetAddress": "Via Michele Amari 51", "addressLocality": "Roma", "addressCountry": "IT"},
     "image": "https://rodrigoapr01.github.io/gp-method/assets/palestra/neon-weal-house.jpg"}
  ]}
  </script>
"""
chi = f"""    <section class="intro" aria-labelledby="about-title">
      <h1 id="about-title">GP METHOD nasce dall'unione di tre mondi: costruzione muscolare, forza e performance.</h1>
      <p class="lead">Un percorso di coaching online pensato per chi vuole un fisico più atletico senza scegliere tra estetica e prestazione.</p>
    </section>

    <section class="who light" aria-labelledby="who-title">
      <figure class="who-photo">
        <picture>
          <source type="image/webp" srcset="assets/chi-sono/GP_chi_sono_giorgia_4x5-900.webp 900w, assets/chi-sono/GP_chi_sono_giorgia_4x5.webp 1920w" sizes="(min-width: 900px) 45vw, 100vw">
          <img src="assets/chi-sono/GP_chi_sono_giorgia_4x5.jpg" width="1920" height="2400" alt="Giorgia Piras, personal trainer, seduta nella palestra Weal House a Roma" decoding="async">
        </picture>
      </figure>
      <div class="who-copy">
      <h2 id="who-title" class="title">Giorgia Piras, personal trainer a Roma. <span class="nowrap">Co-fondatrice</span> di Weal House.</h2>
      <p class="who-social">
        <a class="text-link text-link--dark" href="https://www.instagram.com/lapiras93/" target="_blank" rel="noopener">Instagram @lapiras93</a>
        <a class="text-link text-link--dark" href="https://www.facebook.com/giorgia.piras.3" target="_blank" rel="noopener">Facebook</a>
      </p>
      </div>
    </section>

    <section class="gallery-sec" aria-labelledby="gallery-title">
      <h2 id="gallery-title" class="title">La palestra</h2>
      <ul class="gallery" role="list">{tiles}</ul>
    </section>

    <section class="map" aria-labelledby="map-title">
      <h2 id="map-title" class="title">Weal House</h2>
      <p class="map-address">Via Michele Amari 51, Roma</p>
      <div class="map-frame"><iframe title="Mappa: Weal House, Via Michele Amari 51, Roma" src="https://www.google.com/maps?q=Via+Michele+Amari+51+Roma&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
      <a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query=Via+Michele+Amari+51+Roma" target="_blank" rel="noopener">Apri in Maps</a>
    </section>

{reviews('chi')}

    <section class="close" aria-labelledby="close-title">
      <h2 id="close-title" class="title">Iniziamo?</h2>
      {wa_btn('Ciao Giorgia, ti scrivo dalla pagina Chi sono di GP METHOD.', 'Scrivimi su WhatsApp')}
    </section>

    <dialog class="lightbox" aria-label="Foto della palestra">
      <button class="lightbox-close" type="button" aria-label="Chiudi la foto"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
      <img class="lightbox-img" src="" alt="">
    </dialog>"""
page("chi-sono.html", "Chi sono | Giorgia Piras, GP METHOD",
     "Giorgia Piras, personal trainer a Roma. Co-fondatrice di Weal House. La palestra di Via Michele Amari 51 dove nasce GP METHOD.",
     chi, "Ciao Giorgia, ti scrivo dalla pagina Chi sono di GP METHOD.", extra_head=jsonld)
print("pages written")
