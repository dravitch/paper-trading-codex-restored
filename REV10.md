# REV10 — Réponse Producteur P1–P4

## Portée

Réponse à `CONTRADICTOIRE_DELTA_REV09BIS.md` et son addendum, admis au commit `4f281b7`. Spécification seulement; aucun gate franchi.

| Constat | Correction | Preuve ou mutant |
|---|---|---|
| P1 | ligne `Oracle-Admission` en JSON canonique, grammaire fermée et hash vectorisé | vecteur `7dcf17…067`; toute mutation d'octet/clé/champ bloque P6 |
| P2 | vecteur avec clé Unicode et contrôles; fixtures NFD/surrogate/duplicat | vecteur `5ab872…feee`; rejets sans hash avec `NON_CANONICAL_CAUSAL_JSON` |
| P3 | parent = dernière révision first-parent du fichier | mutant sautant une révision vers genesis doit produire `REGISTRY_HISTORY_VIOLATION` |
| P4 | tableau machine `supersessions` avec identités, références et invariants | suppression, branche, cycle, absence ou réutilisation d'ID doit échouer |

Le JSON courant chaîne le dernier blob modifié à `6867a2d` (`a7ad22…322c1`). Les tableaux métier restent vides. P6 reste `BLOCKED_IMMUTABILITY`.
