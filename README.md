# AI-OS

**Un modo per non dover mai più rispiegare un progetto a un'intelligenza
artificiale.**

---

## A cosa serve

Quando lavori a un'applicazione con l'aiuto di un'AI e poi chiudi la chat,
tutto quello che vi eravate detti sparisce. La volta dopo — magari con un'AI
diversa — devi ricominciare da capo: cos'è il progetto, cosa funziona, cosa
si era rotto, dove eravate arrivati.

AI-OS risolve questo. Fa in modo che ogni progetto **si porti dentro la
propria memoria**, scritta in un formato che qualsiasi AI sa leggere.

---

## Come si usa

Colleghi una qualsiasi AI (Claude, ChatGPT, Gemini, altre) al tuo GitHub, e
usi **due comandi soltanto**.

### `/ai-os new`

Crea un'applicazione nuova da zero.

L'AI ti fa le domande una alla volta — come si chiama, cosa deve fare, dove
deve stare online, se deve ricordare dei dati — poi ti chiede le credenziali
che le servono, spiegandoti dove si prendono, e infine scrive il codice, lo
mette su GitHub e lo pubblica. Alla fine ti dà un link che funziona.

### `/handoff <nome-progetto>`

Riprende un progetto che esiste già.

L'AI apre il progetto, capisce da sola a che punto è, e ti presenta un
riepilogo: obiettivo, cosa funziona, problemi aperti, problemi già risolti,
dove si era fermato chi ci ha lavorato prima, prossimi passi. **Poi si ferma
e aspetta che tu decida cosa fare.**

Funziona anche su progetti che non sono mai stati creati con AI-OS: la prima
volta l'AI ti chiede il link di questo repository, poi sistema tutto da sola
e non te lo chiede mai più.

Non esistono altri comandi. Non devi ricordarti di salvare niente: la memoria
del progetto si aggiorna da sola ogni volta che un'AI finisce un lavoro.

---

## Cosa c'è in questo repository

| File | Cosa contiene |
|---|---|
| `AIOS_PROTOCOL.md` | Il protocollo vero e proprio: la procedura che l'AI deve seguire |
| `AGENTS.md` | Rimando al protocollo, letto in automatico da molti strumenti |
| `.aios/templates/` | I due file di memoria che vengono creati dentro ogni progetto |

Sono file di testo, non un programma. Non c'è niente da installare, niente da
eseguire, nessun terminale da aprire.

---

## Per l'AI che sta leggendo

Leggi [`AIOS_PROTOCOL.md`](./AIOS_PROTOCOL.md) prima di rispondere
all'utente. Ha priorità su ogni altro file di questo repository.

---

## Licenza

MIT — vedi [LICENSE](./LICENSE).
