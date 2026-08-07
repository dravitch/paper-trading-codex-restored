# REV09 — Réponse Producteur O1–O4

## Portée

Réponse au rapport `CONTRADICTOIRE_DELTA_REV08.md`, admis au commit `a7c8a69`. Spécification seulement; aucun gate franchi.

| Constat | Correction | Oracle falsifiable |
|---|---|---|
| O1 | candidate = préfixe exact à l'octet 0; commit et hash du registre des verdicts ancrés | préfixe cité ignoré; deux candidates ou changement de registre bloquent P6 |
| O2 | NFC exigé, surrogates rejetés, échappements exhaustifs et vecteur Unicode | vecteur étendu ⇒ `eacf3f…7563`; NFD/slash échappé divergent et doit être rejeté |
| O3 | genesis fixée à `930b0f9`/`4ff3be…`, parent explicite, migrations séparées | blob courant doit chaîner exactement la genesis; suppression reste interdite |
| O4 | supersession référence un ancien ID et alloue un nouvel ID contigu | ancien ID conservé dans la longueur; réutilisation ou remplacement sans nouvel ID rejeté |

La table d'oracles et le registre de cycles restent vides. La protection externe requise pour P6 reste absente.
