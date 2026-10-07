"""Writes index.html, livelli.html and chi-sono.html (static output, committed).
Shared header, menu and footer live here once; the official logo files are used as they are. Run: python3 tools/build-pages.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://rodrigoapr01.github.io/gp-method/"

WA_ICON = ('<svg class="i-wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
           '<path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" '
           'd="M20.5 11.7a8.4 8.4 0 0 1-12.4 7.4L3.5 20.5l1.4-4.4a8.4 8.4 0 1 1 15.6-4.4z"/>'
           '<path fill="currentColor" d="M9.1 7.9c.2-.4.4-.4.6-.4h.5c.2 0 .4 0 .5.3l.7 1.7c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5a5.6 5.6 0 0 0 2.6 2.3c.2.1.4.1.5-.1l.7-.8c.2-.2.3-.2.5-.1l1.6.8c.2.1.3.2.3.3v.5c0 .5-.4 1.1-1 1.3-.6.3-1.6.3-3-.3a8.6 8.6 0 0 1-3.7-3.5c-.7-1.2-.6-2.3-.2-3.2z"/></svg>')


# official logo (assets/brand/lineare), never redrawn or recoloured.
# The full logo with the circle is only used at 160px or wider: below that its small lettering is unreadable.
BRAND = "assets/brand/lineare"
LOGO_FULL = f"{BRAND}/svg/GP-METHOD-lineare_con-cerchio_trasparente-chiaro.svg"


def logo_full(cls, size, eager=False):
    load = "" if eager else ' loading="lazy"'
    return f'<img class="{cls}" src="{LOGO_FULL}" width="{size}" height="{size}" alt="GP METHOD"{load} decoding="async">'


def pic(name, alt, w=1086, h=1448, cls="", eager=False, sizes="100vw"):
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="assets/palestra/{name}.webp" sizes="{sizes}">'
            f'<img{c} src="assets/palestra/{name}.jpg" width="{w}" height="{h}" alt="{alt}" {lazy} decoding="async"></picture>')


def wa_btn(msg, label, cls="btn btn--primary"):
    return f'<a class="{cls}" data-wa="{msg}" href="#contatti">{WA_ICON}<span>{label}</span></a>'


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
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{BASE}{'' if file == 'index.html' else file}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:site_name" content="GP METHOD">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{BASE}{'' if file == 'index.html' else file}">
  <meta property="og:image" content="{BASE}assets/img/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="GP METHOD">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{BRAND}/svg/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{BRAND}/png/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{BRAND}/png/favicon-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@300;400;500;600&display=swap">
  <link rel="stylesheet" href="styles.css">
  <script>document.documentElement.classList.add('js')</script>
  <script src="main.js" defer></script>
{extra_head}</head>
<body class="{'is-home' if home else 'is-inner'}">
  <a class="skip" href="#main">Vai al contenuto</a>
  <header class="top">
    <a class="brand" href="index.html" aria-label="GP METHOD">{logo_full('brand-logo', 160, eager=True)}</a>
    <nav class="top-nav" aria-label="Principale">{links}</nav>
    {wa_btn(wa_msg, 'Scrivimi', 'btn btn--secondary btn--sm top-wa')}
    <button class="menu-btn" type="button" aria-haspopup="dialog" aria-controls="menu" aria-label="Apri il menu"><span></span><span></span></button>
  </header>

  <dialog class="menu" id="menu" aria-label="Menu">
    <button class="menu-close" type="button" aria-label="Chiudi il menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
    <nav aria-label="Menu">{links}</nav>
    {wa_btn(wa_msg, 'Scrivimi su WhatsApp')}
  </dialog>

  <main id="main">
{body}
  </main>

  <footer class="foot" id="contatti">
    <a class="foot-brand" href="index.html" aria-label="GP METHOD">{logo_full('foot-logo', 180)}</a>
    <nav class="foot-nav" aria-label="Pagine">{links}<a href="https://www.instagram.com/lapiras93/" target="_blank" rel="noopener">Instagram</a></nav>
    <p class="foot-address">Weal House, Via Michele Amari 51, Roma</p>
    {wa_btn(wa_msg, 'Scrivimi su WhatsApp', 'btn btn--secondary')}
    <p class="foot-credit">Sito realizzato da <a href="https://transiva.it" target="_blank" rel="noopener">Transiva</a></p>
  </footer>

  {wa_btn(wa_msg, 'Scrivi a Giorgia', 'fab')}
</body>
</html>
"""
    (ROOT / file).write_text(html)


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
          {wa_btn('Ciao Giorgia, vorrei informazioni su GP METHOD.', 'Scrivi a Giorgia')}
          <a class="text-link" href="#metodo">Scopri il metodo</a>
        </div>
        <p class="hero-proof">Co-fondatrice di <strong>Weal House</strong> · Via Michele Amari 51, Roma</p>
      </div>
      <figure class="hero-photo">
        <picture>
          <source media="(max-width: 767px)" type="image/webp" srcset="assets/hero/GP_hero_giorgia_mobile_5x4-900.webp 900w, assets/hero/GP_hero_giorgia_mobile_5x4.webp 1791w" sizes="100vw" width="1791" height="1433">
          <source media="(max-width: 767px)" srcset="assets/hero/GP_hero_giorgia_mobile_5x4.jpg" width="1791" height="1433">
          <source type="image/webp" srcset="assets/hero/GP_hero_giorgia_4x3-1280.webp 1280w, assets/hero/GP_hero_giorgia_4x3.webp 1920w" sizes="100vw" width="1920" height="1433">
          <img src="assets/hero/GP_hero_giorgia_4x3.jpg" width="1920" height="1433" alt="Giorgia Piras, personal trainer, nella palestra Weal House a Roma" fetchpriority="high" decoding="async">
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
      <div class="ask">
        <p class="ask-q">Non sai da dove partire?</p>
        {wa_btn('Ciao Giorgia, non so quale livello di GP METHOD fa per me.', 'Chiedi a Giorgia', 'btn btn--secondary')}
      </div>
    </section>

    <section class="preview light" aria-labelledby="preview-title">
      <h2 id="preview-title" class="sr-only">I livelli</h2>
      <ul class="rows" role="list">
        <li><a class="row" href="livelli.html#essential"><span class="row-name">Essential</span><span class="row-price"><strong>€149</strong> <span>/ 6 settimane</span></span></a></li>
        <li><a class="row" href="livelli.html#coaching"><span class="row-name">Coaching <span class="badge">Consigliato</span></span><span class="row-price"><strong>€249</strong> <span>/ 6 settimane</span></span></a></li>
        <li><a class="row" href="livelli.html#elite"><span class="row-name">Elite</span><span class="row-price"><strong>€399</strong> <span>/ 6 settimane</span></span></a></li>
      </ul>
      <a class="btn btn--dark" href="livelli.html">Scegli il tuo livello</a>
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

    <section class="close" aria-labelledby="close-title">
      <h2 id="close-title" class="title">Iniziamo?</h2>
      {wa_btn('Ciao Giorgia, vorrei informazioni sui livelli di GP METHOD.', 'Scrivimi su WhatsApp')}
    </section>"""
page("livelli.html", "Livelli e prezzi | GP METHOD, coaching online",
     "Essential €149, Coaching €249, Elite €399: tre livelli di coaching online GP METHOD con Giorgia Piras, ogni ciclo dura 6 settimane.",
     livelli, "Ciao Giorgia, vorrei informazioni sui livelli di GP METHOD.")

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
     "sameAs": ["https://www.instagram.com/lapiras93/"],
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
      <h2 id="who-title" class="title">Giorgia Piras, personal trainer a Roma e co-fondatrice di Weal House.</h2>
      <a class="text-link text-link--dark" href="https://www.instagram.com/lapiras93/" target="_blank" rel="noopener">@lapiras93</a>
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
     "Giorgia Piras, personal trainer a Roma e co-fondatrice di Weal House. La palestra di Via Michele Amari 51 dove nasce GP METHOD.",
     chi, "Ciao Giorgia, ti scrivo dalla pagina Chi sono di GP METHOD.", extra_head=jsonld)
print("pages written")
