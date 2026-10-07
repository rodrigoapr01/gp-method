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
Motion (solo 3): accensione dei neon USP (~600ms, una volta), "Cosa include" (altezza + opacità, 220ms, `cubic-bezier(0.23,1,0.32,1)`), `scale(0.97)` su :active (160ms). Nessuno scroll-reveal; tutto il testo visibile senza JS.

## 2a. Hero (ottobre 2026)
Foto di Giorgia a Weal House (`assets/hero/`): 5:4 sotto 768px, 4:3 da 768px; WebP q82 con versioni leggere (900w / 1280w), JPG di riserva, `fetchpriority="high"` (è l'LCP).
- Sotto 900px: header pieno #191716, foto subito sotto a tutta larghezza, sfumata in nero (12% sopra, 20% sotto), poi testo.
- Da 900px: foto a tutta larghezza dell'hero (`object-position: 70% 20%`), Giorgia a destra, testo a sinistra su gradiente scuro.
Testo: "Giorgia Piras", "Personal trainer a Roma", filetto bronzo, una frase, un bottone, riga Weal House.

## 2b. Logo ufficiale (assets/brand/lineare, approvato dalla cliente)
File usati così come sono, mai ridisegnati né ricolorati.
- Header (tutte le pagine): monogramma `svg/GP-monogramma-lineare_pietra.svg` alto 36px + "GP METHOD"; sotto 360px solo il monogramma.
- Footer: stesso logo con cerchio, 180px.
- Regola: il logo con cerchio mai sotto i 160px; sotto si usa il monogramma.
- Favicon: `svg/favicon.svg`, `png/favicon-32.png`, `png/favicon-180.png`. OG: `png/GP-METHOD-lineare_con-cerchio_scuro.png` centrato su #191716 (`tools/build-assets.py`).

## 3. Elemento firma: il neon
Dalle foto `neon-stronger-*`: parole bianche sottili (Jost 300, riempite, bagliore freddo) alternate a parole rosse spesse e contornate (Jost 600 maiuscolo, `-webkit-text-stroke`, riempimento trasparente, bagliore rosso). Un solo punto: la USP della home. Il testo è sempre acceso senza JS; con JS il bagliore parte spento e si accende con due micro-tremolii quando la sezione entra in vista. "JUST DO IT" non è usato (marchio Nike; la foto è esclusa dal sito).

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
| Home · USP | 7 + 9 (neon) = 16 |
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
