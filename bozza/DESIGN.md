# GP METHOD — bozza "Giorgia ti guida"

Bozza navigabile in `/bozza/`. Il sito in root non cambia. Descrive ciò che è stato costruito (ottobre 2026).

## Concetto
Giorgia è l'interfaccia. Un video scorre fotogramma per fotogramma con lo scroll: saluta, conta 1-2-3 con le dita mentre arrivano i tre livelli come corsie di una pista, poi indica in basso "Scopri i programmi". Gli elementi della palestra Weal House (doghe di legno, insegna neon, pista con START e numeri) sono ricostruiti in CSS.

## Token
| Token | Valore | Uso |
| --- | --- | --- |
| `--bg` | #D7C9B8 | campionato dallo sfondo del video (`tools/extract-seq.py`) |
| `--ink` | #111111 | testi (11.6:1 su `--bg`) |
| `--ink-soft` | #3B3129 | testo secondario (7.8:1) |
| `--neon-red` | #FF3B3B | badge "Consigliato", neon piccolo. Poco |
| `--neon-white` / `--glow` | #F4FFFD / #7FF3E3 | insegna, solo sul pannello scuro |
| `--lime` | #9BD43A | solo i segni laterali delle corsie |
| `--bronze` | #B08A5B | monogramma GP nel footer |
| legno | #6E4B2F / #62422A / #73502F, giunti #3A2717 | doghe in `repeating-linear-gradient` + velo scuro |

## Tipografia
- **Lockup** (solo 3 punti: hero, Weal House, chiusura): Fraunces corsivo 400 + tondo 800 maiuscolo, opsz 144, interlinea 0.86, ogni riga portata alla stessa larghezza da `fitLockups()` in `main.js`; riga sans Archivo 125% maiuscola sotto.
- **Testo**: Archivo, corpo 17px (min 16), etichette 13px maiuscole con tracking; nomi livelli e titoli di sezione in Archivo 125%.

## Componenti
- **Corsia** (`.lane`): nero, numero bianco 46px, segni lime sul bordo esterno, linea di partenza bianca a sinistra, "START" verticale sulla prima.
- **Canvas di Giorgia**: fotogrammi normalizzati (sfondo = bianco) disegnati con `mix-blend-mode: multiply` sopra `--bg`; maschera ovale + dissolvenza prima del terzo basso. Lo stage sticky ha `background: var(--bg)` perché il multiply fonda con la pagina.
- **Neon**: `text-shadow` a più livelli; accensione una volta sola (sfarfallio in opacità) quando il pannello entra in vista.
- **Bottoni**: pillola 52px, nero o bordo nero; sul legno bianco neon.

## Coreografia (main.js)
- `BEATS = { hello: 4, one: 48, two: 98, three: 126, point: 172 }`, `LEAD = 8`: ogni card arriva 8 fotogrammi prima del gesto.
- Card: opacity + translateY(14px), 260ms, `cubic-bezier(0.23,1,0.32,1)`, transizioni (si invertono scorrendo indietro).
- Preloader: linea = quota reale dei fotogrammi 1..`BEATS.one`; poi due sfarfallii (340ms) e dissolvenza (360ms). Tasto "Salta".
- Metodo: parole che scorrono di ±3vw. Lenis (lerp 0.12) per lo scroll morbido.
- `prefers-reduced-motion`: niente scrub, niente Lenis, niente sfarfallio; Giorgia ferma sul fotogramma "hello", card in colonna.
- Senza JS: pagina statica completa (rete di sicurezza a 6s se `main.js` non parte).

## Cambiare video
1. `python3 bozza/tools/extract-seq.py <video.mp4> [fps] [larghezza]`
2. Copia il `--bg` stampato in `styles.css` e in `theme-color`.
3. Aggiorna `BEATS` e `FRAME_COUNT` in `main.js` (guarda i fotogrammi).

## Provenienza raster
- `assets/seq/f_001…193.webp`: dal video `giorgia-guida.mp4` (bozza 480p, fornito dal cliente), estratti a 24 fps, normalizzati sul colore di sfondo, WebP q78. Il video sorgente resta in `gp-method-media/` (non versionato).
- Nessuna foto della palestra: legno, neon e pista sono CSS.
