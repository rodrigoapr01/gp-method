# GP METHOD, bozza v2 "Giorgia ti guida"

Bozza navigabile in `/bozza/`. Il sito in root non cambia. Descrive ciò che è stato costruito (ottobre 2026).

## Concetto
Giorgia è la guida di tutta la home: resta fissa (in basso a destra su telefono, a destra su desktop) e il video avanza con lo scroll. Indica sempre alla sua destra, cioè il lato sinistro dello schermo, dove escono i contenuti. Conta 1-2-3 mentre arrivano i livelli come corsie di una pista, poi indica in basso i bottoni. Gli elementi della palestra Weal House (muro a doghe con l'insegna, muro nero col neon) sono ricostruiti fedelmente dalle foto.

Il metodo è per tutti: nessun testo rivolto solo a donne o solo a uomini.

## Logo (ufficiale, approvato il 2026-10-05)
- Monogramma GP e METHOD dai vettoriali del brand kit (`assets/brand/svg`), mai ridisegnati; finitura metallo lucido (gradiente).
- Sotto METHOD: linea sottile centrata (18% di METHOD) e tagline "SHAPE • STRENGTH • PERFORMANCE" in Jost Light convertito in tracciati (1.35x la larghezza di METHOD), come nel riferimento di Giorgia. Cerchio sottile in metallo.
- File: `assets/logo/gp-method-logo.svg` (+ `-light` per fondi scuri, + `@2x.png`), `gp-method-monogram.svg` (+ `-light`, `@2x.png`), favicon. Generati da `tools/build-logo.py`.
- Uso: monogramma nella nav, logo chiaro nel preloader, logo nel footer, favicon. Il logo non si modifica.

## Token
| Token | Valore | Uso |
| --- | --- | --- |
| `--bg` | #D7C9B8 | campionato dallo sfondo del video |
| `--paper` | #EFE8DF | pannello dei livelli, tabelle |
| `--ink` / `--ink-soft` | #111111 / #3B3129 | testi (11.6:1 / 7.8:1 su `--bg`) |
| `--neon-red` | #FF3B3B | badge "Consigliato", neon rosso |
| `--neon-white` | #F4FFFD | tubi bianchi, alone freddo leggero |
| `--lime` | #9BD43A | segni laterali delle corsie, trattini delle liste |
| `--track` / `--wall` | #111111 / #0B0A0A | corsie / muro nero |
| `--guide-w`, `--guide-body` | 44vw · 0.86 | larghezza di Giorgia e quota del frame occupata dal corpo (0.6 col video a corpo intero) |
| `--col` | calcolata | colonna dei contenuti: tutto ciò che sta a sinistra del corpo di Giorgia |

## Tipografia
- **Lockup** solo in 3 punti della home: hero, Weal House, chiusura ("Il tuo percorso / Iniziamo?"). Fraunces corsivo + tondo 800, righe giustificate alla stessa larghezza da `fitLockups()`, riga Archivo 125% sotto.
- **Archivo** per tutto il resto: corpo 17px (min 16), etichette 13px maiuscole; titoli delle pagine interne in Archivo 125% 800.
- **Metodo**: ogni parola (SHAPE, STRENGTH, PERFORMANCE) portata alla larghezza della colonna, come le righe del lockup.
- Il logo resta nel suo carattere, mai riscritto.

## Componenti
- **Guida** (`.guide`): canvas fisso sotto i contenuti, `mix-blend-mode: multiply` su `--bg`, maschera ovale. I muri di Weal House su telefono sono a tutta larghezza e le passano davanti.
- **Corsie** (`.lane-btn`): bottoni che aprono il dettaglio. Linea di partenza bianca, START sulla prima, segni lime.
- **Pannello livello** (`<dialog>`): bottom sheet a tutta altezza su telefono (chiusura con X, Esc, swipe giù con soglia di velocità 0.11), pannello laterale su desktop. `showModal()` = pagina inerte e focus intrappolato; il focus torna alla card. Contenuto: prezzo, durata, a chi è adatto [DA CONFERMARE], Cosa include (testi approvati del sito in root), WhatsApp del livello, "Vedi tutti i dettagli".
- **Metodo**: accordion sul posto (Cos'è, Per chi, Come si lavora, Esempio di settimana: [TESTO DA CONFERMARE]). `#shape`, `#strength`, `#performance` nell'URL lo aprono.
- **Muro a doghe**: texture rovere chiaro renderizzata una volta (`tools/wood-source.svg`, feTurbulence) in `assets/weal/wood.webp` (14 KB), luce dall'alto in CSS.
- **Insegna Weal House**: `assets/weal/weal-house-neon.svg`, tracciata dalla foto (soglia sui tubi bianchi, rimozione dei riflessi del plexiglass, potrace). Alone bianco freddo leggero.
- **Neon "BE STRONGER THAN YOUR EXCUSES"**: SVG inline, Archivo stretto al 62% e compresso all'80%, solo contorno = tubo a doppia linea; BE ed EXCUSES bianchi, STRONGER e THAN YOUR rossi.

## Coreografia (main.js, oggetto `GUIDE`)
- `BEATS`: hello 4, one 48, two 98, three 126, pointDown 172. `present`, `pointUp`, `pointMid`, `thumbsUp` sono `null` col video attuale (mezzo busto) e usano `FALLBACK` (hello).
- `SCENES`: hero → hello/present · livelli → one/two/three/pointDown (sezione fissa mentre conta) · metodo → pointUp/pointMid · Weal House → present · chi è Giorgia → pointMid · mappa → pointDown · fine → thumbsUp. Il fotogramma segue la sezione che passa a metà schermo.
- Card e bottoni del livello: opacity + translateY(12px), 260ms ease-out, transizioni (si invertono scorrendo indietro). Mai nascosti al focus da tastiera.
- Pannello: apertura 420ms `cubic-bezier(0.32,0.72,0,1)`, chiusura 260ms ease-out. Accordion 240ms. Bottoni scale 0.97 in 160ms; hover solo con mouse.
- Preloader: logo + linea = quota reale dei fotogrammi fino a `one`; due sfarfallii (340ms) e dissolvenza (360ms).
- Neon: accensione una volta sola all'ingresso in vista.
- Link interni: scorrimento morbido (Lenis) al tocco, salto istantaneo da tastiera.
- `prefers-reduced-motion`: niente scrub, Lenis, sfarfallio; Giorgia ferma, card in colonna, neon accesi.

## Arriva il video a corpo intero
1. Scarica in `gp-method-media/video/`, poi `python3 bozza/tools/extract-seq.py <video.mp4>`.
2. Copia il `--bg` stampato in `styles.css` e `theme-color`.
3. Guarda i fotogrammi e aggiorna solo `GUIDE.frameCount` e `GUIDE.BEATS` in `main.js` (togli i `null`).
4. Imposta `--guide-body` (quota del frame occupata dal corpo) in `styles.css`: la colonna dei contenuti si ricalcola da sola.

## Provenienza raster
- `assets/seq/f_*.webp`: dal video `giorgia-guida.mp4` (480p del cliente), 24 fps, normalizzati sul colore di sfondo, WebP q78.
- `assets/weal/weal-house-neon.svg`: tracciato dalla foto `rif-wealhouse-neon-legno.png` (non versionata).
- `assets/weal/wood.webp`: generato da `tools/wood-source.svg`.
- `assets/logo/*`: da `assets/brand/svg` + Jost Light (OFL), via `tools/build-logo.py`.
- Foto in "Chi è Giorgia": `../assets/img/giorgia-*` del sito in root.
