# Registre NO-GO

## Statuts

Statuts de cause : `OPEN`, `CONTINUE`, `ATTRIBUTION_BLOCKED`, `REDUCE_SCOPE`, `STOP`, `RESOLVED`. Statuts d'occurrence : `ATTRIBUTED`, `UNATTRIBUTED`. `UNKNOWN` est un classement de relation causale, pas un statut terminal. Une absence d'entrée ne signifie jamais qu'un critère a été testé.

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

Une occurrence encore non diagnostiquée reçoit `UNATTRIBUTED` sous la famille. Elle ne compte pas comme répétition d'une cause précise, mais compte dans le compteur de cycles bloqués de la **famille**. Au troisième cycle familial comportant une occurrence non attribuée, le statut devient obligatoirement `ATTRIBUTION_BLOCKED` : aucun quatrième cycle, `CONTINUE` ou `REDUCE_SCOPE` n'est permis. L'opérateur attribue/scinde rétroactivement les occurrences avec liens historiques, ou choisit immédiatement `STOP` si l'attribution reste impossible.

Les identifiants stables proviennent de [`CAUSAL_ID_REGISTRY.md`](CAUSAL_ID_REGISTRY.md). Une même cause racine observée sur plusieurs composants reçoit un `root_cause_group_id`; le seuil de répétition est évalué également sur ce groupe. Au plus tard au troisième cycle d'une famille, l'opérateur recherche obligatoirement les signatures partageant preuves ou dépendance causale et décide leur fusion, séparation ou classement `UNKNOWN`, sans effacer leurs clés. `UNKNOWN` compte toujours comme cycle bloqué de la famille et du groupe candidat; il ne suspend aucun compteur ni obligation. Seuls `RESOLVED` et `STOP` clôturent. Toute fusion, scission ou requalification exige une décision versionnée.
