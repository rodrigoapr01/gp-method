# GP METHOD — Design

Proposta minimal per Giorgia Piras (coaching online). La versione precedente è stata bocciata: troppo testo, non si capiva cosa si compra. Il modello è NUA 2.0.

## 1. Perché NUA 2.0 funziona (analisi del branch `nua-2.0`, commit 91eba4e)

Fonte: `components/NuaHome.tsx`, `NuaHeader.tsx`, `NuaBottomSheet.tsx`, `NuaFooter.tsx`, `nua-2.0.css`.

| Aspetto | Cosa fa NUA 2.0 |
| --- | --- |
| Numero di sezioni | 6 in home: hero → intro → banner corsi → promo → listino (3 tile) → recensioni, più footer. |
| Parole per sezione | Hero ~5 (tre etichette + "Tocca 01·02·03"). Intro ~8 (H1 di 5 parole + 1 bottone). Banner corsi ~8. Ogni promo ~10 (nome, prezzo, bottone). Listino ~12 (nome + "da €"). Recensioni ~25: il blocco più lungo. |
| Hero | Un'immagine sola, a tutto schermo, con 3 punti toccabili. Niente paragrafi: la foto *è* il messaggio. |
| Servizi | 3 tile identiche: immagine, nome, prezzo "da". Tutto il dettaglio (righe di listino, note) sta in un **bottom sheet** che si apre al tocco. La home non mostra mai una lista lunga. |
| CTA | Una sola azione: WhatsApp. Pillola piena bronzo scuro, testo corto con verbo ("Prenota su WhatsApp", "Prenota la promo"). Ogni CTA ha il **messaggio precompilato** del servizio da cui parte. |
| Navigazione | Logo a sinistra, pillola "Prenota" a destra. Su mobile i link spariscono dietro un menu; il bottone di contatto resta sempre visibile. |
| Spaziature | Gutter 20px mobile / 48px desktop, max 1080px. Sezioni da 48–80px. Ritmo generoso: lo spazio vuoto separa, non le linee. |
| Interazioni | Pochissime e utili: aprire lo sheet, aprire la FAQ, premere il bottone. Il resto è statico. |
| Prezzi | Sempre visibili subito, cifre tabellari. Il prezzo è un'informazione, non un segreto da sbloccare. |

**La logica da replicare:** una domanda per blocco; il prezzo in vista; un solo tipo di azione (WhatsApp) ripetuto con il contesto giusto; il dettaglio nascosto dietro un tocco.

**Cosa NON replico:** il loader, il marquee, gli eyebrow maiuscoli sopra ogni titolo, la parola in corsivo colorato dentro i titoli, i punti pulsanti. Erano parte del linguaggio di NUA; qui sarebbero rumore (e sono le "firme" più comuni dei siti generati).

## 2. Token

### Colore
| Token | Hex | Uso | Contrasto su avorio |
| --- | --- | --- | --- |
| `--avorio` | #EFE9E2 | sfondo pagina | — |
| `--sabbia` | #E3D9CF | superfici secondarie (sezione livelli) | — |
| `--champagne` | #C9B8A6 | filetti, cerchio del ciclo, bordi | 1.6:1 → solo decorazione |
| `--bronzo` | #8A6E58 | testo grande (≥24px) e numeri del ciclo | 3.9:1 → solo testo grande |
| `--bronzo-scuro` | #5A4535 | CTA piene, testo secondario piccolo | 7.4:1 |
| `--espresso` | #2A2017 | testo, card Coaching | 13.2:1 |

Un solo elemento metallico: il logo dell'hero (gradiente champagne → bronzo → bronzo scuro). Tutto il resto è piatto.

### Tipografia
- **Cormorant Garamond** 400/500 — titoli, nomi dei livelli, prezzi, le tre parole del metodo. Ha lo stesso taglio a contrasto alto delle lettere del monogramma GP.
- **Jost** 400/500 — testo, bottoni, etichette. Geometrico come la scritta "METHOD" del logo.
- Scala (mobile → desktop): H1 32→60px, parole metodo 44→88px, H2 28→40px, testo 16px, piccolo 14px. Interlinea 1.1 sui titoli serif, 1.55 sul testo.
- Maiuscolo spaziato solo dove è il marchio: GP METHOD, SHAPE/STRENGTH/PERFORMANCE, ESSENTIAL/COACHING/ELITE.

### Forma e spazio
- Gutter 20px (mobile) / 48px (≥900px), contenuto max 1120px.
- Raggi: pillola 999px per i bottoni; 20px per le card dei livelli. Nessuna ombra.
- Sezioni 72px (mobile) / 120px (desktop).
- Aree di tocco ≥ 44px; CTA 52px.

### Motion
- `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`.
- Unico momento orchestrato: entrata del logo hero (cerchio + monogramma) al caricamento, CSS animation, opacity + transform.
- "Cosa include": altezza + opacità, 220ms, interrompibile (transition, non keyframes), "+" che ruota di 45°.
- Bottoni: `scale(0.97)` su `:active`, 160ms.
- Bottone WhatsApp mobile: entra/esce con translateY + opacity, 220ms.
- Nessuno scroll-reveal. Tutto il testo è visibile senza JS. `prefers-reduced-motion`: nessuna animazione.

## 3. L'idea che rende la pagina sua

Il **cerchio** del logo diventa il linguaggio della pagina:
1. Nell'hero è il logo metallico.
2. In "Come funziona" lo stesso cerchio, piatto e champagne, diventa il **ciclo di 6 settimane**: quattro parole sui quattro punti cardinali (Assess, Build, Perform, Review). È davvero un ciclo, quindi la forma circolare è informazione, non decorazione. Su mobile si legge in senso orario.
3. Nella foto di "Chi sono" il ritaglio è un arco (mezzo cerchio in alto).

Tutto il resto è quieto: niente card-kit, niente icone decorative, niente gradienti.

## 4. Wireframe

### Mobile (390px)
```
┌──────────────────────────────┐
│ (GP) GP METHOD   [◯ Scrivimi]│  header
│                              │
│          ╭──────╮            │
│        ╱   GP    ╲           │  logo metallico ~68vw
│        ╲  METHOD ╱           │
│          ╰──────╯            │
│  Non devi scegliere tra      │  H1 serif
│  estetica e performance.     │
│  Coaching online di G. Piras │  piccolo
│   [ Scegli il tuo livello ]  │  unico bottone
├──────────────────────────────┤ 100svh
│ Il metodo                    │
│ SHAPE                        │  parole enormi serif
│ Costruzione muscolare…       │
│ ──────────────────────────── │
│ STRENGTH                     │
│ Forza e progressioni         │
│ ──────────────────────────── │
│ PERFORMANCE                  │
│ Running, conditioning, …     │
├──────────────────────────────┤
│ Un ciclo di 6 settimane.     │
│            Assess            │
│        ╭────────────╮        │
│  Review│            │Build   │  cerchio champagne
│        ╰────────────╯        │
│            Perform           │
├──────────────────────────────┤  sfondo sabbia
│ Scegli il tuo livello        │
│ ┌──────────────────────────┐ │  COACHING (espresso, primo)
│ │ Consigliato              │ │
│ │ COACHING        €249     │ │
│ │ / 6 settimane            │ │
│ │ Programma su misura…     │ │
│ │ Cosa include          +  │ │  accordion
│ │ [    Scegli Coaching   ] │ │
│ └──────────────────────────┘ │
│ ┌ ESSENTIAL  €149 … ───────┐ │  bordo champagne
│ └──────────────────────────┘ │
│ ┌ ELITE  Posti limitati  … ┐ │
│ └──────────────────────────┘ │
├──────────────────────────────┤
│   ╭────╮                     │
│   │foto│  arco               │
│   └────┘                     │
│ Sono Giorgia Piras, …        │
│ @lapiras93                   │
├──────────────────────────────┤
│ Pronta a iniziare?           │
│ [ Scrivimi su WhatsApp ]     │
├──────────────────────────────┤
│ GP METHOD · Giorgia Piras    │  footer
│ Instagram · Sito: Transiva   │
└──────────────────────────────┘
 [◯ Scrivimi su WhatsApp]  ← fisso, solo dopo l'hero, sopra la safe area
```

### Desktop (1440px)
```
┌────────────────────────────────────────────────────────────┐
│ (GP) GP METHOD                               [◯ Scrivimi]   │
│                         ╭──────╮                            │
│                        │  GP   │   logo ~420px              │
│                         ╰──────╯                            │
│             Non devi scegliere tra estetica                 │
│                     e performance.                          │
│                Coaching online di Giorgia Piras             │
│                  [ Scegli il tuo livello ]                  │
├────────────────────────────────────────────────────────────┤
│ Il metodo                                                   │
│ SHAPE            │ STRENGTH          │ PERFORMANCE          │  3 colonne
│ Costruzione…     │ Forza e…          │ Running, …           │
├────────────────────────────────────────────────────────────┤
│ Un ciclo di           ╭──── Assess ────╮                    │
│ 6 settimane.     Review                Build                │
│                       ╰──── Perform ───╯                    │
├────────────────────────────────────────────────────────────┤
│ Scegli il tuo livello                                       │
│ ┌ ESSENTIAL ┐  ┌▓ COACHING ▓┐  ┌ ELITE ┐                     │  Coaching al centro, più alta
│ └───────────┘  └────────────┘  └───────┘                     │
├────────────────────────────────────────────────────────────┤
│ ╭─────╮                                                     │
│ │foto │   Sono Giorgia Piras, personal trainer a Roma …     │
│ └─────┘   @lapiras93                                        │
├────────────────────────────────────────────────────────────┤
│        Pronta a iniziare?   [ Scrivimi su WhatsApp ]        │
│ GP METHOD · Giorgia Piras        Instagram    Transiva      │
└────────────────────────────────────────────────────────────┘
```

Allineamento: hero e chiusura centrati (sono "manifesti"); metodo, ciclo, livelli e chi sono allineati a sinistra (si leggono).

## 5. Conteggio parole (visibili, prezzi e nomi esclusi)

| Sezione | Testo | Parole |
| --- | --- | --- |
| Header | "Scrivimi" | 1 |
| Hero | H1 (8) + "Coaching online di Giorgia Piras" (3, nome escluso) + "Scegli il tuo livello" (4) | 15 |
| Il metodo | "Il metodo" (2) + 3 righe (4 + 3 + 4); SHAPE/STRENGTH/PERFORMANCE sono nomi | 13 |
| Come funziona | "Un ciclo di 6 settimane." (5) + 4 tappe (4) | 9 |
| I livelli | titolo (4) + per card: riga (5–6) + "Cosa include" (2) + bottone (2–3) + badge (1–2) | 4 + ~12 per card |
| Chi sono | frase (12, nomi esclusi) + @lapiras93 (nome) | 12 |
| Chiusura | "Pronta a iniziare?" (3) + "Scrivimi su WhatsApp" (2) | 5 |
| Footer | "Instagram", "Sito realizzato da" | 4 |

**Nota onesta sui livelli:** i testi obbligatori del brief (tre righe, tre bottoni, tre badge/etichette) portano la sezione a ~40 parole visibili totali, ~12 per card. Il limite di 25 è rispettato **per card**, non per la sezione intera. Tutto il dettaglio (le 27 voci di "Cosa include") è chiuso dentro gli accordion. Per scendere sotto 25 bisognerebbe togliere testi che il brief richiede.

## 6. Revisione del piano contro i default generici

| Rischio template | Correzione |
| --- | --- |
| Crema + serif contrastato = il look "generato" n.1 | La palette è imposta dal brand; la differenzio con il **cerchio** come sistema (logo → ciclo → arco foto), non con un accento colorato. |
| Tre card uguali con ombra morbida | Niente ombre. Coaching è **espresso pieno** (un'altra materia, non una card "evidenziata"); Essential ed Elite sono solo un filetto champagne su sabbia. |
| Eyebrow maiuscolo sopra ogni titolo | Nessun eyebrow. Il titolo della sezione *è* la domanda. |
| Numeri 01/02/03 decorativi | Niente numeri: nel ciclo è la posizione sul cerchio (in senso orario) a dire l'ordine. |
| Freccia "→" nei bottoni, mono per etichette | Niente frecce, niente monospace. Icona solo dove dice qualcosa (WhatsApp, "+"). |
| Fade-up su ogni sezione | Vietato dal brief e dalla skill: un solo momento (il logo). |
