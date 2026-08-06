# REV08 — Réponse Producteur N1–N4

## Portée

Réponse au rapport `CONTRADICTOIRE_DELTA_F14546F.md`, admis au commit `cf6aa7a`. Spécification seulement; aucun gate franchi.

| Constat | Correction | Test falsifiable |
|---|---|---|
| N1 | LF seul, CR rejeté; verdict autoritaire dans une table d'admissions d'oracles | CRLF, doublon ou verdict absent de la table doit bloquer P6 |
| N2 | tri JSON récursif, types/encodage définis, vecteur SHA-256 fixé | le vecteur doit produire `51857e…75e6`; permuter l'objet imbriqué ne change pas le hash |
| N3 | registre append-only avec hash du blob parent et supersession | retirer ou modifier une entrée antérieure produit `REGISTRY_HISTORY_VIOLATION` |
| N4 | regex, domaine, séquence contiguë et allocation exclusive définis | `OCC-000000`, trou, doublon ou ID fourni par l'appelant est rejeté |

La table d'admissions d'oracles est vide et la preuve d'immuabilité externe reste absente. P6 demeure `BLOCKED_IMMUTABILITY`.
