# STILE GRAFICO — l'aspetto standard delle app AI-OS

> Modulo referenziato da `AIOS_PROTOCOL.md`. **Ogni app nuova nasce con questo
> aspetto**, salvo che l'utente chieda esplicitamente qualcos'altro.
> Scelta dell'utente del 29/10/2026: *"mi piace lo stile, la grafica e i font usati"*.
>
> **È verificato e in produzione**: NutriTrack PRO (React + Tailwind, commit 5c83846), PronoBlast (`nuovorossi1-blip/PronoBlast-app`,
> commit 8031276, React Native Web/Expo) e Jupiter (`nuovorossi1-blip/Jupiter`,
> commit b90e2e9, HTML/CSS puro). Se lì cambia, questo file va riallineato al
> codice vero.

Il pacchetto pronto da copiare sta in [`stile/`](./stile):

| File | Cosa contiene |
|---|---|
| `stile/tokens.css` | colori, font, riquadri a vetro, pulsanti, barra in basso, schermata d'avvio |
| `stile/fonts/*.woff2` | Manrope (testi) e Barlow Condensed 600-900 (titoli) |
| `stile/fonts/OFL-*.txt` | licenze dei font (SIL Open Font License: uso libero, anche commerciale) |

---

## Il carattere in una riga

Scuro grafite, un solo colore d'accento (oro, con un riflesso corallo nei
gradienti), riquadri "a vetro" con bordi sottili, testi puliti in **Manrope** e
titoli/numeri grandi in **Barlow Condensed** maiuscolo. Poche cose per
schermata, ben distanziate.

## Colori

| Ruolo | Valore | Dove |
|---|---|---|
| Sfondo | `#1A1A1A` | pagina, barra di stato del telefono (`theme-color`), manifest, avvio |
| Riquadro | `#242424` | card, pulsanti normali, giorni del calendario |
| Riquadro alto | `#2D2D2D` | hover, riquadri dentro riquadri |
| Vetro | `rgba(36,36,36,.72)` + `blur(20px)` | barra in basso, intestazioni |
| Bordo | `rgba(255,255,255,.08)` (forte `.16`) | tutti i contorni |
| Testo | `#FFFFFF` · secondario `#A1A1AA` · spento `#71717A` | |
| **Oro** | `#F5A623` | voce attiva, etichette, pronostico in evidenza |
| Gradiente | `#FFC15E → #F5A623 → #FF6B6B` (135°) | pulsante principale, giorno/filtro selezionato |
| Alone | `0 0 24px rgba(245,166,35,.45)` | icona attiva, nome nella schermata d'avvio |

**Colori con un significato** — verde `#10B981` (vinto/ok), giallo `#F59E0B`
(attenzione/candidato), rosso `#EF4444` (perso/errore, anche i badge con i
numeri), blu `#60A5FA` (AI/informazione). Non si usano per decorare e, quando
si rifà la grafica di un'app esistente, **i colori che hanno già un significato
in quell'app restano quelli**.

## Font

- **Manrope** 400-800 per tutto il testo.
- **Barlow Condensed** 800-900, maiuscolo, spaziatura `.5-1px`, per: nome
  dell'app, titoli di pagina, nomi delle squadre in grande, numeri dei giorni,
  il valore principale di una card (pronostico, risultato, prezzo).
- I font si **mettono dentro l'app** (cartella `/fonts`), non si caricano da
  Google: funzionano offline, sono più veloci e non vengono bloccati dalle
  regole di sicurezza della pagina (CSP con `default-src 'self'`).
- Precarica solo `manrope-latin.woff2` (`<link rel="preload" as="font" crossorigin>`).

## Forme e componenti

- Raggi: 8 · 12 · 16 · 24 px; pillole e pulsanti tondi (`999px`).
- **Card**: vetro o `#242424`, bordo `.08`, raggio 16-24.
- **Pulsante principale**: gradiente, testo `#1A1A1A` grassetto, ombra oro
  leggera. Uno per schermata.
- **Etichette di sezione**: 11 px, maiuscolo, spaziatura 1.5 px, oro.
- **Barra in basso (telefono)**: piena larghezza, vetro, bordo superiore
  sottile; icone 20-22 px; etichette 10 px maiuscole; voce attiva in oro con
  alone; badge rossi.

## Come si apre sul telefono

1. `theme-color` e `background_color` del manifest = `#1A1A1A`, `display: standalone`,
   `orientation: portrait`.
2. **Schermata d'avvio** (in `tokens.css`, `#avvio`): sfondo grafite, icona
   dell'app con alone oro, nome in Barlow Condensed oro, cerchio che gira. Sta
   nell'HTML (si vede subito, prima del JavaScript) e si **sfuma quando i dati
   della prima schermata sono pronti**, restando almeno 0,8 s; dopo 6 s sparisce
   comunque. Se la pagina ha una CSP senza `'unsafe-inline'` per gli script, il
   codice che la toglie va in un file `.js` separato.
3. App Android con guscio (Capacitor): barra di navigazione di sistema `#1A1A1A`,
   pulsanti chiari.

## Ricette per tecnologia

**HTML/CSS puro** — copia `stile/tokens.css` e `stile/fonts/` nella cartella
pubblica, collega `tokens.css` prima del CSS dell'app. Per un'app esistente: un
foglio in più caricato **per ultimo** che sovrascrive solo l'aspetto (come
`public/grafica.css` di Jupiter). Se i file hanno `?v=` per la cache, cambia la
versione a ogni modifica.

**React Native Web / Expo** — tema in un file solo (`src/theme.ts`: `colors`,
`fonts.heading = "Barlow Condensed"`), titoli con `fontFamily: fonts.heading`.
Per dare Manrope a **tutto** il testo senza toccare le icone: dichiarare Manrope
anche col nome `"-apple-system"` (`@font-face { font-family: "-apple-system"; … }`),
perché React Native Web scrive il testo con la pila `-apple-system, …` mentre le
icone hanno un font loro. Vedi `frontend/scripts/inject-pwa-head.js` di PronoBlast.

**React + Tailwind** — in `tailwind.config`: `colors.bg #1A1A1A`, `surface #242424`,
`gold #F5A623`, `coral #FF6B6B`; `fontFamily.sans ['Manrope', …]`,
`fontFamily.titoli ['"Barlow Condensed"', …]`; `@font-face` da `tokens.css`.
Per un'app Tailwind esistente (NutriTrack PRO): invece di cambiare le classi nei
componenti, ridefinisci nel config le scure di `neutral` (700 `#3A3A3A`, 800
`#2D2D2D`, 900 `#242424`, 950 `#1A1A1A`) e la scala del colore d'accento
(es. `blue`) con le tonalità dell'oro; il pulsante principale prende il
gradiente e il testo grafite con una regola CSS. Lascia scritti a mano i
colori che hanno un significato (macro, vinto/perso).

## Cosa non fare

- Non cambiare **calcoli, logica o navigazione** quando si rifà la grafica di
  un'app esistente: solo aspetto. Se l'app ha un modo suo di muoversi (es. il
  menu laterale di Jupiter), resta com'è.
- Non copiare loghi, nomi, immagini o codice di altre app: lo stile è ispirato,
  i file sono nostri.
- Non salvare file di testo dalla PowerShell 5.1 con `Get-Content`/`Set-Content`:
  rovina le lettere accentate (successo il 29/10/2026 su Jupiter). Usare
  l'editor, `node` o `[IO.File]::WriteAllText(..., UTF8 senza BOM)`.
- Verifica sempre con foto da telefono (larghezza 412 px), non solo con la build.
