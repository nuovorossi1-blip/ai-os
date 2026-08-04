# Istruzioni per l'AI

Questo repository è **AI-OS**, un framework per creare e riprendere progetti
software tramite LLM.

**Prima di rispondere a qualsiasi richiesta dell'utente, leggi
[`AIOS_PROTOCOL.md`](./AIOS_PROTOCOL.md).** Quel file contiene la procedura
da eseguire e ha priorità su ogni altro documento di questo repository.

Comandi riconosciuti:

- `/ai-os new` — crea un progetto nuovo da zero
- `/handoff <nome-progetto>` — recupera un progetto esistente, ne ricostruisce
  lo stato, riferisce e **si ferma** aspettando istruzioni

L'utente non è un tecnico. Parla italiano, fai una domanda alla volta, e dopo
ogni passaggio dichiara sempre se deve fare qualcosa lui o se fai tutto tu.
