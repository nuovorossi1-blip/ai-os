# MODULO — App Android installabile e auto-aggiornante

> Modulo opzionale referenziato da `AIOS_PROTOCOL.md`. Si applica quando un progetto
> AI-OS deve offrire, oltre al sito/PWA normale, un'app Android che si installa con
> un'icona vera e si aggiorna da sola senza passare dal Play Store.
>
> **Non è una proposta teorica**: descrive un'implementazione reale, verificata e
> funzionante in produzione su GymBuilder (nuovorossi1-blip/gymbuilder) al 21/08/2026.
> Se in futuro qualcuno la modifica lì, questo file va riallineato al codice vero,
> non lasciato a descrivere una versione superata (stessa regola `[FACT]` di sempre:
> il codice è la prova, questo file è un indizio).

---

## Quando proporlo

Alla Fase 1 di `/ai-os new`, quando l'utente risponde sì a "Deve funzionare anche da
telefono?", fai una domanda di chiarimento in più (non automatica: chiedila):

> "Ti basta che il sito si apra bene da telefono, o vuoi anche una vera icona
> installabile che si aggiorna da sola ogni volta che pubblico una modifica, senza
> passare dal Play Store?"

Se la seconda, applica questo modulo nella Fase 4 (Creazione), oltre al resto.

---

## Come funziona, in breve

Il sito web normale (React/Vite o equivalente) viene impacchettato con **Capacitor**
dentro un guscio Android. L'app installata **non contiene il codice**: apre il sito
pubblicato online dentro quel guscio (come un browser dedicato senza barra indirizzi).
Un plugin nativo controlla, ad ogni apertura, se online è stata pubblicata una versione
più recente di quella installata; se sì, propone il download e l'installazione
dell'APK nuovo, che sovrascrive quello vecchio.

**Due metà**, una sul sito e una dentro l'app installata:

- Sul sito, un banner "Scarica app" — visibile SOLO se il sito gira in un browser
  normale, sparisce da solo dentro l'app installata — con un link diretto al file APK.
- Dentro l'app installata, un controllo a ogni apertura: versione installata (letta
  davvero dal sistema Android) contro versione pubblicata (un file `version.json`
  scaricato sempre fresco, mai dalla cache). Se la seconda è più alta, popup con le
  note di rilascio e un bottone "Aggiorna".

---

## Pezzi necessari

Nomi generici sotto — `<app>` è il nome del progetto, `<pacchetto>` è l'identificativo
Android (es. `app.gymbuilder.mobile`).

1. **Un file di versione pubblico**, servito staticamente dal sito
   (`public/version.json`):
   ```json
   {
     "version": "1.0.44",
     "versionCode": 44,
     "apkUrl": "https://<dominio-sito>/<app>.apk",
     "releaseUrl": "https://github.com/<org>/<app>/releases/latest",
     "notes": "Correzioni e miglioramenti.",
     "mandatory": false
   }
   ```

2. **Un confronto versioni lato JS** (`src/native/versioning.ts`): scarica
   `version.json` con `cache: 'no-store'` (mai una copia vecchia) e confronta
   `versionCode` numero per numero (non affidarsi a un confronto stringa semplice:
   `"1.0.9" > "1.0.10"` come stringhe darebbe il risultato sbagliato).

3. **Un plugin nativo Capacitor** (`ApkUpdaterPlugin`, Kotlin/Java in
   `android/app/src/main/java/<pacchetto>/`) con quattro metodi:
   - `getCurrentVersion()` — legge `versionName`/`versionCode` VERI dal
     `PackageManager` di Android, non un valore scritto a mano nel JS (altrimenti il
     confronto è finto e l'app non si accorgerebbe mai di essere vecchia).
   - `canInstallPackages()` — Android richiede un permesso esplicito ("Installa app
     sconosciute") per installare APK non provenienti dal Play Store.
   - `openInstallSettings()` — apre la schermata di sistema per concederlo.
   - `downloadAndInstall({ url, fileName })` — usa `DownloadManager` di Android per
     scaricare l'APK (validare lato nativo che l'URL sia `https://`, mai accettare
     altro), poi apre l'installer di sistema via
     `Intent(ACTION_VIEW, mimeType: "application/vnd.android.package-archive")`.
     **L'utente deve comunque confermare l'installazione a mano**: è una sicurezza di
     Android, non aggirabile e non va nemmeno tentato di aggirarla.

4. **Un componente React che controlla e propone l'aggiornamento**
   (`NativeUpdater.tsx`): gira SOLO su piattaforma nativa Android
   (`Capacitor.isNativePlatform() && Capacitor.getPlatform() === 'android'` — mai
   mostrarlo sul sito web, lì non esiste nulla da "aggiornare" in questo senso).
   Confronta le due versioni all'avvio, mostra un modal con le note di rilascio se
   c'è una versione più nuova, gestisce esplicitamente lo stato "permesso mancante"
   (apre le impostazioni e aspetta che l'utente torni) e lo stato "download fallito"
   (mai un errore silenzioso).

5. **Un banner "Scarica app" sul sito web** (`InstallBanner.tsx`): visibile SOLO
   quando l'app gira nel browser normale (`!Capacitor.isNativePlatform()`), con un
   link diretto al file APK pubblicato (`/<app>.apk`).

6. **Una pipeline che costruisce, versiona e pubblica l'APK a ogni modifica**
   (GitHub Actions, es. `build-apk.yml`):
   - si attiva su ogni push a `main`, **esclusi i file che lei stessa scrive**
     (`paths-ignore` su `public/<app>.apk`, `public/version.json`, il keystore di
     debug) — altrimenti loop infinito: la pipeline si ripubblica da sola all'infinito.
   - usa una **keystore di debug stabile**, generata una volta sola (se non esiste
     ancora nel repository) e riusata sempre. **Fondamentale**: Android rifiuta di
     sovrascrivere un'app già installata se la firma cambia — una keystore diversa a
     ogni build blocca silenziosamente tutti gli aggiornamenti futuri.
   - numera la versione in automatico (es. dal numero progressivo della pipeline
     stessa), nessun bump manuale per questo canale.
   - **rimuove l'APK della release precedente dagli asset bundlati PRIMA di
     costruire quella nuova**. Se non lo fai: l'APK dentro `public/` viene ricopiato
     negli asset dell'app Android a ogni build (`vite build` → `cap sync`), quindi
     ogni nuova APK si porta dentro anche quella precedente, che si portava dietro
     quella ancora prima — crescita illimitata a ogni release. **Bug reale osservato
     su GymBuilder**: build arrivate oltre i 95MB prima di questa correzione.
   - ricommitta `version.json` e l'APK nuovo su `main` (commit del bot, non
     dell'utente), poi pubblica il sito con l'APK nuovo incluso.

---

## Un secondo canale opzionale, separato: release firmata "vera"

Se in futuro serve un canale più ufficiale (Play Store, o distribuzione fuori da
questo meccanismo automatico), serve una **seconda pipeline separata** (in GymBuilder,
`android-release.yml`), attivata da un tag Git dedicato (es. `android-v1.2.0`), che usa
una keystore di **release** vera — mai la stessa di debug, **mai nel repository**:
solo nei secret di GitHub Actions (`ANDROID_KEYSTORE_BASE64`, `ANDROID_STORE_PASSWORD`,
`ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD`) — e pubblica l'APK come Release GitHub
invece che sul sito. In questo canale `versionCode`/`versionName` vanno aumentati a
mano prima di taggare: non è automatico come il canale principale.

Non attivare questo secondo canale di default: è per quando l'utente lo chiede
esplicitamente, non una parte necessaria del modulo base.

---

## Cosa serve dall'utente

**Canale automatico (quello che quasi tutti i progetti useranno)**: niente token o
credenziali — gira tutto dentro GitHub Actions con i permessi già presenti nel
repository, e pubblica sullo stesso hosting già collegato (Vercel/Netlify).

**Solo se si attiva anche il secondo canale** (release firmata): servono i quattro
secret della keystore di release, generati una volta sola. Vanno anche conservati in
un backup sicuro fuori da GitHub — perderli impedisce di aggiornare per sempre le
installazioni che hanno già quella firma, senza modo di recuperarle.

---

## Limiti da dichiarare sempre all'utente, senza che lo scopra da solo

- **Solo Android.** Su iOS non è possibile installare/aggiornare così — resta la PWA
  (Safari → Condividi → Aggiungi alla schermata Home). Dillo la prima volta che
  proponi questo modulo, non aspettare che l'utente lo scopra da un iPhone che non
  vede il banner.
- **L'utente deve comunque confermare ogni installazione a mano** (tocco su
  "Installa"): nessun meccanismo, di sistema o costruito da questo modulo, può
  renderlo silenzioso o automatico al 100%.
- **Ogni push a `main` che tocca il codice dell'app rifà una build e ripropone
  l'aggiornamento**, anche per modifiche piccole o solo di documentazione se non
  escluse esplicitamente dal `paths-ignore`. Non è un difetto da correggere di
  default: è il comportamento voluto (aggiornamenti frequenti), ma va spiegato
  all'utente la prima volta che succede, non lasciato a scoprirlo da solo chiedendosi
  perché l'app "continua a chiedere di aggiornarsi".
- **Non è mai verificabile end-to-end da un'AI**: nessun ambiente di lavoro di un LLM
  ha un vero telefono Android con un'app installata sopra. Chi applica questo modulo
  deve scriverlo esplicitamente come "non verificato in un browser/dispositivo reale"
  nel file di stato del progetto (vedi `SALVATAGGIO AUTOMATICO` in
  `AIOS_PROTOCOL.md`), e chiedere all'utente di riverificare lui sul proprio telefono
  dopo il primo deploy — mai dare per scontato che funzioni solo perché la build è
  verde.
