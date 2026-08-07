# REV11 — Réponse Producteur Q1–Q4

## Portée

Réponse au rapport Contradictoire `CONTRADICTOIRE_DELTA_REV10.md`, admis au commit `ae5eb92`. Spécification seulement; aucun gate franchi.

| Constat | Correction | Test falsifiable |
|---|---|---|
| Q1 | source dédiée `ORACLE_ADMISSIONS.json`, ordre O2/O4/O7 et unicité | Markdown/fence ignoré; doublon, hors-ordre ou oracle inconnu invalide le fichier |
| Q2 | `NON_CANONICAL_CAUSAL_JSON` devient rejet pré-validation sans occurrence/cycle | fixture NFD ne modifie aucun compteur; corruption d'une entrée existante devient `REGISTRY_HISTORY_VIOLATION` |
| Q3 | commande first-parent épinglée; genesis vide seule exemptée; merges divergents interdits | résultat vide hors genesis et merge divergent produisent un échec déterministe |
| Q4 | regex/domaine/séquence/allocation SUP, raisons fermées et décision ancestrale | SUP-000000, trou, doublon, raison inconnue ou commit absent/non-ancêtre échoue |

`ORACLE_ADMISSIONS.json` et les tableaux du registre sont vides. La preuve externe d'immuabilité manque toujours; P6 reste bloqué.
