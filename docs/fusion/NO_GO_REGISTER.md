# Registre NO-GO

## Statuts

`OPEN`, `CONTINUE`, `REDUCE_SCOPE`, `STOP`, `RESOLVED`. Une absence d'entrée ne signifie jamais qu'un critère a été testé.

## Registre

| Cause ID | Critère §12.1 | Gate | Cycle | Révision Producteur | Verdict Contradictoire | Décision opérateur | Statut |
|---|---|---|---:|---|---|---|---|
| — | aucun critère déclenché à ce jour | — | — | — | — | — | — |

## Règle d'application

Une même cause conserve son `Cause ID` à travers les cycles. Au troisième cycle bloqué visé par le critère 6, le statut ne peut rester `OPEN` : l'opérateur choisit `REDUCE_SCOPE` ou `STOP`, avec justification versionnée. Un changement d'étiquette sans changement causal ne remet pas le compteur à zéro.
