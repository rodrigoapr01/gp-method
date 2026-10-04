import re, html
idx=open('index.html').read()
sym=re.search(r'<svg width="0" height="0".*?</svg>',idx,re.S).group(0)
head_common='''<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title} | GP METHOD (bozza)</title>
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#D7C9B8">
  <link rel="icon" href="assets/logo/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/logo/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&display=swap">
  <link rel="stylesheet" href="styles.css">
  <script>document.documentElement.classList.add('js')</script>
  <script src="main.js" defer></script>
</head>
<body class="page">
  <header class="top">
    <a class="brand" href="./" aria-label="GP METHOD, home"><img src="assets/logo/gp-method-monogram.svg" width="36" height="37" alt=""></a>
    <nav class="top-nav" aria-label="Principale">
      <a class="top-link" href="programmi.html">Programmi</a>
      <a class="top-link top-link--wide" href="chi-sono.html">Chi sono</a>
      <a class="top-wa" data-wa="Ciao Giorgia, vorrei informazioni su GP METHOD." href="./" aria-label="Scrivimi su WhatsApp">
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-wa"/></svg>
      </a>
    </nav>
  </header>
  <main class="page-main">
'''
foot='''  </main>
  <footer class="page-foot">
    <img class="foot-logo" src="assets/logo/gp-method-logo.svg" width="150" height="150" alt="GP METHOD: Shape, Strength, Performance" loading="lazy">
    <a class="text-link" href="./">Torna alla home</a>
    <p class="foot-credit">Sito realizzato da <a href="https://transiva.it" target="_blank" rel="noopener">Transiva</a></p>
  </footer>
  {sym}
</body>
</html>
'''
def page(fn,title,it,ro,body):
    # the Fraunces lockup lives only in the home's 3 places; inner pages get a plain Archivo title
    open(fn,'w').write(head_common.format(title=title)+f'''    <h1 class="page-title">{title}</h1>
{body}
'''+foot.format(sym=sym))

js=open('main.js').read()
levels={}
for key in ['essential','coaching','elite']:
    blk=js[js.index(f'  {key}: {{'):]
    blk=blk[:blk.index('\n  },')]
    g=lambda f: re.search(rf"{f}: '([^']*)'",blk).group(1)
    i0=blk.index('items: ['); seg=blk[i0:blk.index('],', i0)]
    items=[a or b for a,b in re.findall(r"'([^']*)'|\"([^\"]*)\"", seg)]
    badge=re.search(r"badge: \['([^']*)', '([^']*)'\]",blk)
    levels[key]=dict(n=re.search(r'n: (\d)',blk).group(1),name=g('name'),price=g('price'),pitch=g('pitch'),
                     items=items,wa=g('wa'),cta=g('cta'),badge=badge.groups() if badge else None)
secs=[]
for key,l in levels.items():
    b=f' <span class="badge {l["badge"][1]}">{l["badge"][0]}</span>' if l['badge'] else ''
    lis=''.join(f'<li>{html.escape(i)}</li>' for i in l['items'])
    secs.append(f'''    <section class="level-full" id="{key}" aria-labelledby="h-{key}">
      <h2 class="sheet-title" id="h-{key}">{l["name"]}{b}</h2>
      <p class="sheet-price"><strong>{l["price"]}</strong> <span>/ 6 settimane</span></p>
      <p>{l["pitch"]}</p>
      <div><h3 class="label">Durata</h3><p>6 settimane</p></div>
      <div><h3 class="label">A chi è adatto</h3><p class="tbc">[TESTO DA CONFERMARE]</p></div>
      <div><h3 class="label">Cosa include</h3><ul class="sheet-list">{lis}</ul></div>
      <a class="btn btn--ink" data-wa="{l["wa"]}" href="./"><svg class="wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-wa"/></svg> {l["cta"]}</a>
    </section>''')
NA='<span aria-label="non incluso">-</span>'
rows=[('Programmazione','Personalizzata, 3-4 giorni','Costruita dopo assessment e video call, 3-5 giorni','Completamente individuale, dopo assessment 1:1 approfondito'),
      ('Check','Check finale','Ogni 2 settimane','Settimanale'),
      ('Video','Video exercise library','Analisi tecnica dei video','Feedback video prioritario'),
      ('Call con Giorgia',None,'Video call iniziale','Due call 1:1'),
      ('Adattamenti',None,'Adattamenti della programmazione','Adattamenti continui'),
      ('Cardio e conditioning','Linee guida cardio, conditioning','Gestione cardio e conditioning','Strategia performance e recupero'),
      ('Supporto',None,'Supporto diretto','Gestione dei giorni ON/OFF'),
      ('Chiusura del ciclo','Check finale','Review finale','GP Performance Review finale')]
trs=''.join('<tr><th scope="row">'+r[0]+'</th>'+''.join('<td>'+(c if c else NA)+'</td>' for c in r[1:])+'</tr>' for r in rows)
compare=f'''    <section class="compare" id="confronto" aria-labelledby="h-compare">
      <h2 class="label" id="h-compare">Confronto</h2>
      <div class="compare-scroll" tabindex="0" role="region" aria-label="Tabella di confronto">
        <table>
          <thead><tr><th scope="col"><span class="sr-only">Voce</span></th><th scope="col">Essential<br><span>€149</span></th><th scope="col">Coaching<br><span>€249</span></th><th scope="col">Elite<br><span>€399</span></th></tr></thead>
          <tbody>{trs}</tbody>
        </table>
      </div>
      <p class="tbc">Il confronto riassume solo le voci di "Cosa include".</p>
    </section>'''
nav='    <nav class="level-nav" aria-label="Livelli"><a href="#essential">Essential</a><a href="#coaching">Coaching</a><a href="#elite">Elite</a><a href="#confronto">Confronto</a></nav>'
page('programmi.html','Programmi','I tre','Programmi',nav+'\n'+'\n'.join(secs)+'\n'+compare)

def block(t, body): return f'    <section class="about-block"><h2 class="label">{t}</h2>{body}</section>'
tbc='<p class="tbc">[TESTO DA CONFERMARE]</p>'
chi='\n'.join([
 '''    <div class="about-intro">
      <picture>
        <source type="image/avif" srcset="../assets/img/giorgia-800.avif">
        <source type="image/webp" srcset="../assets/img/giorgia-800.webp">
        <img class="about-photo" src="../assets/img/giorgia-800.jpg" width="800" height="1000" alt="Giorgia Piras in tuta nera con profili dorati">
      </picture>
      <p class="about-line">Sono Giorgia Piras, personal trainer a Roma e cofondatrice di Weal&nbsp;House.</p>
    </div>''',
 block('La mia storia',tbc), block('Da quanto alleno','<p class="tbc">[DA CONFERMARE: anni di esperienza]</p>'),
 block('Cosa faccio','<p>Coaching online sui tre assi del metodo: Shape (costruzione muscolare e proporzioni), Strength (forza e progressioni), Performance (running, conditioning, Hybrid/HYROX).</p><p class="tbc">[DA CONFERMARE: specializzazioni]</p>'),
 block('Cosa NON faccio','<p>Le indicazioni su alimentazione sportiva e integrazione restano nell\'ambito delle competenze di un personal trainer.</p><p class="tbc">[TESTO DA CONFERMARE]</p>'),
 block('Le mie priorità con chi alleno',tbc),
 block('Weal House','<p>Cofondatrice di Weal House, Via Michele Amari 51, Roma.</p><a class="text-link" href="./#weal-house">Vedi Weal House</a>'),
 block('Formazione e certificazioni','<p class="tbc">[DA CONFERMARE: titoli e certificazioni]</p>'),
 '''    <section class="about-block about-cta"><h2 class="label">Scrivimi</h2>
      <a class="btn btn--ink" data-wa="Ciao Giorgia, vorrei informazioni su GP METHOD." href="./"><svg class="wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-wa"/></svg> Scrivimi su WhatsApp</a>
      <a class="text-link" href="https://www.instagram.com/lapiras93/" target="_blank" rel="noopener">Instagram @lapiras93</a>
    </section>'''])
page('chi-sono.html','Chi sono','Chi è','Giorgia',chi)
page('privacy.html','Privacy','Informativa','Privacy','    <p class="tbc">[TESTO DA CONFERMARE] Qui andrà l\'informativa privacy e cookie (necessaria anche per la mappa Google incorporata).</p>')
print('ok', {k:len(v['items']) for k,v in levels.items()})
