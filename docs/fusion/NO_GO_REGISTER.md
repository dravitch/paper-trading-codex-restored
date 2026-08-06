# Registre NO-GO

## Statuts

`OPEN`, `CONTINUE`, `REDUCE_SCOPE`, `STOP`, `RESOLVED`. Une absence d'entrée ne signifie jamais qu'un critère a été testé.

## Registre

| Cause ID | Family key | Failure signature | Cause key | Critère §12.1 | Gate | Cycle | Décision opérateur | Statut |
|---|---|---|---|---|---|---:|---|---|
| — | — | — | — | aucun critère déclenché à ce jour | — | — | — | — |

## Règle d'application

Une même cause conserve son `Cause ID` à travers les cycles. Au troisième cycle bloqué visé par le critère 6, le statut ne peut rester `OPEN` : l'opérateur choisit `REDUCE_SCOPE` ou `STOP`, avec justification versionnée. Un changement d'étiquette sans changement causal ne remet pas le compteur à zéro.

L'identité mécanique possède deux niveaux :

```text
cause_family_key = SHA-256(canonical_json({
  gate_id,
  no_go_criterion_id,
  violated_invariant_id,
  failing_mutation_id
}))

failure_signature = {
  component_id,
  symbol_id,
  failure_mode_id
}

cause_key = SHA-256(canonical_json({
  cause_family_key,
  failure_signature
}))
```

La signature utilise des identifiants stables préenregistrés : jamais texte libre, numéro de ligne, traceback, révision ou hash de preuve. Deux défauts distincts observés dans une exécution créent deux causes sous la même famille. Les descriptions, révisions, verdicts et hashes de preuves sont enregistrés dans un journal annexe par cycle mais exclus de l'identité.

Une occurrence encore non diagnostiquée reçoit `UNATTRIBUTED` sous la famille et ne compte pas pour le seuil des trois cycles. Avant `REDUCE_SCOPE` ou `STOP`, l'opérateur doit l'attribuer ou la scinder rétroactivement, avec liens vers les anciennes occurrences. Toute fusion, scission ou requalification exige une décision versionnée et conserve les anciennes clés.
