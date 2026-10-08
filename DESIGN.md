# GP METHOD v4 — Design

Rifatto da zero (ottobre 2026). La versione precedente è salvata nel tag `proposta-giorgia-animata`.
Bocciature da non ripetere: troppo testo, poco intuitivo, figura animata di Giorgia finta. Qui: niente figure di Giorgia; protagoniste la palestra (foto) e le scritte LED ricreate in CSS.

## 1. Perché NUA 2.0 funziona (branch `nua-2.0`, file `NuaHome.tsx`, `NuaHeader.tsx`, `NuaBottomSheet.tsx`, `NuaFooter.tsx`, `nua-2.0.css`)

| Aspetto | NUA 2.0 | Cosa ne prendo |
| --- | --- | --- |
| Sezioni | 6 in home: hero, intro, banner corsi, promo, listino (3 tile), recensioni | 7 in home, una idea ciascuna |
| Parole per sezione | 5-25; il blocco più lungo (recensioni) arriva a ~25 | massimo ~25 per sezione |
| Hero | Una sola immagine a tutto schermo, nessun paragrafo: la foto è il messaggio | foto neon della palestra a 100svh, H1 + una riga + un bottone |
| Navigazione | logo a sinistra, 3 link + pillola "Prenota"; su mobile menu a tutto schermo | logo, Metodo / Livelli / Chi sono, "Scrivimi"; menu a tutto schermo su mobile |
| Rimandi tra pagine | la home mostra un'anteprima e rimanda alla pagina completa ("Tutto il listino", "Scopri i corsi") | anteprima dei livelli → livelli.html; atmosfera → chi-sono.html |
| Dettaglio | mai liste lunghe in pagina: il listino si apre in un bottom sheet al tocco | "Cosa include" si apre al tocco |
| CTA | una sola azione, WhatsApp, con messaggio precompilato del servizio | idem, messaggio per livello o pagina |
| Footer | dove, orari, contatti, mappa, legali, credito Transiva, tutto centrato e piccolo | logo, 3 link, Instagram, indirizzo, WhatsApp, credito |
| Ritmo | gutter 20/48px, sezioni 48-80px, lo spazio separa | gutter 20/56px, sezioni 72-128px |

Non copio testi, colori né immagini di NUA. Non ne prendo nemmeno gli eyebrow maiuscoli sopra ogni titolo né la parola in corsivo colorato nei titoli.

## 2. Token

| Token | Hex | Uso | Contrasto |
| --- | --- | --- | --- |
| `--nero` | #191716 | sfondo principale | — |
| `--pietra` | #E0E2DB | testo su nero; sfondo delle sezioni chiare | 13.7:1 |
| `--bronzo` | #8A6E58 | logo, filetti, numeri, prezzi, bordi, anello di focus | 3.8:1 su nero, 3.6:1 su pietra → solo ≥24px o grassetto ≥19px, mai testo piccolo né testo dei bottoni |

Testo secondario: pietra al 75% su nero (8.1:1), nero al 75% su pietra (6.8:1). Nessun altro colore d'interfaccia.
Luce neon (solo nelle scritte LED): rosso #FF3B2F, bianco #F4F7F6, resa con `text-shadow` a più livelli.

Tipografia: **Cormorant Garamond** 500 per titoli e numeri (è il carattere di METHOD nel logo), **Jost** 300-600 per testo, interfaccia e neon. Corpo 17px, etichette 13px maiuscole.
Forma: bottoni a pillola 52px (primario pietra/nero, secondario bordo bronzo/testo pietra); card e foto con raggio 14px; filetti 1px bronzo.
Motion: accensione dei neon USP (~600ms, una volta), poi la riga rossa "ronza" (tre cali ogni 4,5s, mai spenta) e fa un glitch di 1s al passaggio del mouse, al tocco e, sui telefoni, ogni volta che entra nello schermo (max 3 lampi/s, WCAG 2.3.1); i pilastri del metodo si aprono come "Cosa include" (stessa transizione 220ms); le tappe del ciclo mostrano una riga sotto (nessuna animazione), "Cosa include" (altezza + opacità, 220ms, `cubic-bezier(0.23,1,0.32,1)`), `scale(0.97)` su :active (160ms). Nessuno scroll-reveal; tutto il testo visibile senza JS.

## 2a. Hero (ottobre 2026)
Foto di Giorgia a Weal House (`assets/hero/`): 5:4 sotto 768px, 4:3 da 768px; WebP q82 con versioni leggere (900w / 1280w), JPG di riserva, `fetchpriority="high"` (è l'LCP).
- Sotto 900px: header pieno #191716, foto subito sotto a tutta larghezza, sfumata in nero (12% sopra, 20% sotto), poi testo.
- Da 900px: foto a tutta larghezza dell'hero (`object-position: 70% 20%`), Giorgia a destra, testo a sinistra su gradiente scuro.
Testo: "Giorgia Piras", "Personal trainer a Roma", filetto bronzo, una frase, un bottone, riga Weal House.

## 2b. Logo ufficiale: tondo in metallo (ottobre 2026)
`assets/brand/GP-logo-metallo-tondo.png` (trasparente) + WebP 160/320/640 con srcset, su tutte le pagine (anche /chiaro/), alt "GP METHOD", width/height espliciti.
- Header: solo il logo tondo, 64px mobile / 80px desktop, `fetchpriority="high"`; l'header non si compatta allo scroll.
- Menu mobile aperto: logo tondo 72px in alto.
- Footer: logo tondo 140px mobile / 160px desktop.
- Favicon (`assets/brand/favicon/`): favicon-32 trasparente; favicon-180 (apple-touch-icon) e favicon-512 sul fondo #E2D9D0, perché i telefoni riempiono di nero la trasparenza.
- I loghi piatti in `assets/brand/lineare/` restano per la stampa, ma non sono usati nelle pagine.
- Anteprima dei link (og:image e twitter:image, tutte le pagine anche /chiaro/): `assets/og/og-gp-method.jpg?v=2`, logo in metallo alto 600px su #E2D9D0, 1200×630 (`tools/build-assets.py`). Se cambia l'immagine, alzare `?v=` in `OG_IMAGE`.
- Home (scura e chiara): fascia avorio #EFE9E2 con il logo in metallo (`assets/chiaro/logo-metallo-900.*`, bordi sfumati), min(80vw, 420px), prima di "Iniziamo?".

## 2c. Approfondimenti (ottobre 2026)
- Metodo: ogni pilastro (Shape, Strength, Performance) è un bottone che apre una riga di dettaglio.
- Ciclo di 6 settimane (home) e Il percorso (livelli): ogni tappa è un bottone; la riga sotto cambia. Su livelli la riga di Assess sostituisce la vecchia nota.
- I testi riusano solo fatti già sul sito (nota sul percorso e liste "Cosa include"): da far confermare a Giorgia.

## 2d. WhatsApp e recensioni (ottobre 2026)
- WhatsApp (5 punti): "Scrivimi" nell'header, voce nel menu mobile, bottone nell'hero, "Iniziamo?" in chiusura, bottone fisso compatto solo su mobile (sotto 768px, in basso a destra, 48px, dopo l'hero, si nasconde quando un bottone o un link passa sotto di lui). In Livelli restano anche i bottoni delle tre card. Niente WhatsApp nel footer né sotto il ciclo.
- Recensioni: blocco chiaro in home (dopo "Dove nasce il metodo") e in Chi sono (dopo la mappa): 5 stelle, "5 su 5 su Google", invito "Ti alleni con Giorgia? Lascia la tua recensione." e link alla scheda Google di Weal House (cid 5456743492543164649). Il voto (5,0, 22 recensioni al 7/10/2026) è scritto a mano: aggiornarlo se cambia.

## 2e. Voce e domande frequenti (ottobre 2026)
- I bottoni WhatsApp parlano in prima persona (Giorgia): "Scrivimi", "Scrivimi su WhatsApp".
- Livelli: sezione "Domande frequenti" (#faq) dopo Il percorso, 8 domande in prima persona con prezzi, differenze tra livelli, durata, principianti, online/palestra, alimentazione, come iniziare. Stessa apertura di "Cosa include". JSON-LD FAQPage. In home, link "Domande frequenti" accanto a "Scegli il tuo livello".
- Le risposte usano solo fatti già sul sito: da far confermare a Giorgia.

## 2f. Chi sono: foto di Giorgia (ottobre 2026)
Nella sezione di presentazione (`.who`): foto 4:5 seduta davanti all'insegna "Be stronger than your excuses" (`assets/chi-sono/`, WebP q82 900w/1920w + JPG), angoli 14px, `object-position: 50% 20%`. Mobile: a tutta larghezza sopra il testo, caricata subito (è nella prima schermata). Desktop: colonne 45/55, testo centrato in verticale.

## 2g. Anteprima chiara (/chiaro/, ottobre 2026)
Generata da `tools/build-pages.py` (funzione `write_chiaro`) a partire dalle stesse pagine: stessi testi, foto e struttura, asset con `../`, `noindex` e canonical verso la versione principale. Colori in `chiaro/css/tema-chiaro.css`, caricato dopo `styles.css`: avorio #EFE9E2, sezioni #E4DCD3, testo espresso #2E2620 (secondario #6B5E54), bronzo #8A6E58, linee champagne #B9A796. La fascia neon resta #191716. Loghi scuri (monogramma nero, cerchio trasparente-scuro). La versione scura non cambia.

## 3. Elemento firma: il neon
Dalle foto `neon-stronger-*`: parole bianche sottili (Jost 300, bagliore freddo) alternate a parole rosse piene (Jost 500 maiuscolo, #FF3B2F, bagliore rosso con text-shadow a più livelli; niente text-stroke, che disegnava linee dove i tratti delle lettere si sovrappongono). Un solo punto: la USP della home, che dall'ottobre 2026 è solo la frase "Non devi scegliere / tra estetica / e performance." resa come l'insegna "Be stronger than your excuses" (bianco, rosso a tubo, bianco), centrata; le tre righe inglesi BUILD/DEVELOP/ELEVATE sono state tolte. Il testo è sempre acceso senza JS; con JS il bagliore parte spento e si accende con due micro-tremolii quando la sezione entra in vista. "JUST DO IT" non è usato (marchio Nike; la foto è esclusa dal sito).

## 4. Wireframe

### Home (390px)
```
[GP logo]                [≡]      header su foto
┌──────────────────────────────┐
│ foto neon + velo nero 100svh │
│ ONLINE COACHING BY G. PIRAS  │
│ Non allenarti solo per       │
│ cambiare il tuo corpo.       │  H1 Cormorant
│ Allenalo per renderlo forte… │
│ [ Scopri il metodo ]         │
└──────────────────────────────┘
 Non devi scegliere tra          USP (nero)
 estetica e performance.
   BUILD YOUR SHAPE.     ← bianco sottile
   DEVELOP YOUR STRENGTH. ← rosso contornato
   ELEVATE YOUR PERFORMANCE.
═══ pietra ════════════════════  Il metodo
 SHAPE        Costruzione…
 STRENGTH     Forza e…
 PERFORMANCE  Running, …
 Ogni percorso parte da te.
═══ nero ══════════════════════  Come funziona
 Un ciclo di 6 settimane.
 1 Assess │ 2 Build │ 3 Perform │ 4 Review (filetto bronzo)
═══ pietra ════════════════════  Livelli (anteprima)
 Essential   €149 / 6 settimane
 Coaching    €249  [Consigliato]
 Elite       €399
 [ Scegli il tuo livello ]
═══ nero ══════════════════════  Atmosfera
 [foto][foto][foto]  (scorrono)
 Dove nasce il metodo.  Chi sono →
 Iniziamo?  [ Scrivimi su WhatsApp ]
 footer
```
### Home (1440px)
Hero: testo in basso a sinistra su foto a tutto schermo. USP: titolo a sinistra, neon a destra. Metodo: tre colonne. Come funziona: 4 tappe in linea su un filetto. Livelli: tre righe a tutta larghezza. Atmosfera: tre foto affiancate.

### Livelli (390 / 1440)
```
 Scegli il tuo livello.          intro (nero)
 Stessa filosofia, tre livelli…
 ┌ COACHING [Consigliato] ┐      prima su mobile, bordo bronzo
 │ €249 / 6 settimane     │
 │ riga · firma           │
 │ Cosa include      [+]  │
 │ [ Scegli Coaching ]    │
 └────────────────────────┘
 ┌ ESSENTIAL ┐ ┌ ELITE [Posti limitati] ┐
 Desktop: Essential · Coaching · Elite in 3 colonne, CTA allineate
 ASSESS → BUILD → PERFORM → REVIEW + una frase
 [ Scrivimi su WhatsApp ]
```
### Chi sono (390 / 1440)
```
 GP METHOD nasce dall'unione…    intro
 Giorgia Piras, … co-fondatrice di Weal House.  @lapiras93
 Galleria 2 col (mobile) / 3 col (desktop), tocco = vista grande
 Mappa Weal House + Apri in Maps
 [ Scrivimi su WhatsApp ]
```

## 5. Conteggio parole (visibili; prezzi e nomi esclusi)

| Pagina · sezione | Parole |
| --- | --- |
| Home · hero | 4 + 7 + 7 + 3 = 21 |
| Home · USP | 7 (solo neon) |
| Home · metodo | 4 + 3 + 6 + 4 = 17 |
| Home · come funziona | 5 + 4 = 9 |
| Home · livelli | 6 ("/ 6 settimane" ×3 escluso come prezzo) + 1 badge + 4 bottone = 11 |
| Home · atmosfera | 4 + 2 = 6 |
| Home · chiusura | 1 + 3 = 4 |
| Livelli · intro | 4 + 13 = 17 |
| Livelli · ogni card | riga 6-10 + firma 3-7 + bottone 3 + "Cosa include" 2 ≈ 16-20 (le voci incluse sono chiuse) |
| Livelli · percorso | 4 + 15 = 19 |
| Chi sono · intro | 12 + 18 = 30 → due frasi del brief, leggermente sopra 25 |
| Chi sono · Giorgia | 12 |
| Chi sono · palestra | 2 (titolo) |

## 6. Revisione contro i default generici
| Rischio | Scelta |
| --- | --- |
| "Nero + un accento neon" è un look da template | il neon non è un accento d'interfaccia: vive solo nelle foto e in una sezione, ed è copiato dai LED veri della palestra |
| Tre card uguali | sulla home i livelli sono righe tipografiche, non card; le card sono solo nella pagina di vendita, con Coaching distinta dal bordo bronzo |
| Eyebrow sopra ogni titolo | un solo "piccolo" nella hero (richiesto dal brief); nessun altro |
| Numeri 01/02/03 decorativi | numeri solo sulle 4 tappe, che sono una sequenza vera |
| Scroll-reveal | nessuno |
| Galleria a griglia identica | una foto grande + tre piccole su desktop |
