# Registre NO-GO

## Statuts

Statuts de cause : `OPEN`, `CONTINUE`, `ATTRIBUTION_BLOCKED`, `REDUCE_SCOPE`, `STOP`, `RESOLVED`. Statuts d'occurrence : `ATTRIBUTED`, `UNATTRIBUTED`. `UNKNOWN` est un classement de relation causale, pas un statut terminal. Une absence d'entrée ne signifie jamais qu'un critère a été testé.

## Registre

La source machine autoritaire est [`NO_GO_CYCLE_REGISTRY.json`](NO_GO_CYCLE_REGISTRY.json). Ce tableau Markdown est une projection humaine et ne peut ajouter ni retirer un cycle. Le contrôleur valide le schéma, recalcule chaque `causal_payload_sha256`, vérifie la séquence des `occurrence_id` et recompose les unions uniquement depuis ce JSON versionné.

Le registre est append-only entre deux révisions Git. Pour une évaluation au commit `E`, le commit candidat `C` est l'unique sortie de `git rev-list --first-parent --max-count=1 E -- docs/fusion/NO_GO_CYCLE_REGISTRY.json` : il s'agit donc du dernier ancêtre de première parenté qui a effectivement modifié le fichier, et non nécessairement de `E`. Pour un `C` non-genesis, le parent autoritaire est l'unique sortie de `git rev-list --first-parent --max-count=1 "C^1" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json`. `parent_registry_commit` doit lui être égal et `previous_blob_sha256` doit égaler le SHA-256 de son blob. Une sortie vide est autorisée uniquement si `C` est exactement la genesis normative et porte `parent_registry_commit: null`, `previous_blob_sha256: null` et tous les tableaux vides; elle est interdite autrement. Un commit `E` qui ne modifie pas le registre valide ainsi le dernier `C` sans créer une fausse révision.

Pour chaque merge `M` rencontré sur la première parenté depuis la genesis normative
(exclue) jusqu'à `E` (inclus), le contrôleur compare le blob du registre de chacun des
parents au blob du premier parent; l'absence du fichier est une valeur distincte. Il exige
aussi que le blob porté par `M` soit identique à celui du premier parent. Toute divergence,
y compris dans le second parent d'un merge transparent `-s ours` que `rev-list ... --
<fichier>` ne retournerait pas comme révision, produit `MERGE_REGISTRY_CONFLICT`. Un merge
ne peut donc modifier ni réconcilier le registre. La réconciliation exige un commit
linéaire ultérieur, une décision versionnée et l'union exhaustive validée. Ainsi la
première-parenté fixe l'ordre sans effacer silencieusement une branche.

Les ensembles d'identités des `cycles`, `occurrences`, `groups` et `supersessions` du parent sont des sous-ensembles obligatoires du nouveau blob; une entrée existante reste octet-pour-octet identique. Parent/hash absent ou divergent, saut d'une révision, suppression ou mutation produit `NON_TESTABLE` avec `REGISTRY_HISTORY_VIOLATION`. Mutants obligatoires : traiter un commit non-révision comme `C`, saut vers genesis, résultat vide hors genesis, merge aux parents divergents, merge modifiant le registre et merge transparent `-s ours` dont un parent secondaire porte un blob divergent; tous échouent. Sur la chaîne actuelle, `E=3876fce` résout `C=7039476`, puis son prédécesseur `P=6867a2d`; le blob porté sans modification par `3876fce` ne produit donc pas de violation.

La genesis normative est le blob au commit `930b0f9292c18d74b99a3daabc53f1af2b7fba68`, SHA-256 `4ff3bef1ba8d0005dcacdc0dd381d523e821a1c9d28549ebc847a74f6db046fb`. Le fichier vide créé à `f14546f` est une pré-genesis documentaire sans données et ne peut servir d'ancêtre autoritaire. Le premier successeur cite cette genesis dans `genesis_commit`, `parent_registry_commit` et `previous_blob_sha256`.

`schema_version` est immuable dans une chaîne. Toute migration crée un nouveau fichier versionné, un manifeste de migration revu reliant genesis source et cible, et prouve la conservation exhaustive des identités, y compris `supersessions`; elle ne réinitialise jamais la chaîne existante.

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

Le seuil du groupe candidat est exactement trois cycles bloqués, identique au seuil familial. Tout résultat `NON_TESTABLE`, notamment `INVALID_CAUSAL_ID_STATE`, compte comme cycle bloqué de sa famille et de son groupe candidat. Au troisième cycle, attribution/scission ou `STOP` devient obligatoire; répéter un ID non actif ne remet ni compteur ni échéance à zéro.

Créer, fusionner, scinder ou renommer un groupe ne remet jamais son compteur à zéro. Un nouveau `RCG-NNN` couvrant au moins une cause déjà comptée hérite de l'union de tous les `cycle_id` bloqués de ces causes et de leurs groupes antérieurs. Le compteur est la cardinalité de cette union : un même `cycle_id` n'est compté qu'une fois. L'entrée machine enregistre `predecessor_group_ids`, `member_cause_ids`, `inherited_cycle_ids` et `history_sha256` de leur JSON canonique. Omettre un prédécesseur ou un cycle présent dans la source machine produit `NON_TESTABLE` avec raison `INCOMPLETE_GROUP_HISTORY` et compte comme cycle bloqué; l'opérateur ne peut pas substituer un compteur manuel.
