# P0 Contract Scope Decision — Rescoping de l'immuabilité distante

**Date** : 2026-08-17
**Auteur** : Big Pickle (opencode), sur directive de l'opérateur
**Type** : Décision normative de rescoping

## Constat

L'audit P0 a révélé une contradiction interne dans les artefacts de clôture :

- `P0_CONTRACT_MAP.md` établit que la preuve d'immuabilité distante fait partie des critères de sortie de P0 et la marque `ABSENT`, en concluant : « P0 ne peut pas passer au sens strict du protocole ».
- `P0_CLOSURE_DECISION.md` affirme ensuite que cette même preuve « ne bloque pas P0 » et prononce `P0_CLOSE_WITH_DEBT`.

Ces deux affirmations sont incompatibles. La raison en est que le contrat P0原始 (défini dans `06_FUSION_GATES.md` et `REVIEW_ADMISSION_REGISTRY.md`) plaçait effectivement l'immuabilité distante dans les critères de P0. Mais l'audit a démontré que cette exigence était mal scopée.

## Analyse

L'immuabilité distante (protection anti force-push ou archive signée) est nécessaire pour :

1. **P6** : les preuves de revue d'oracle doivent être infalsifiables. Si un commit d'admission peut être réécrit, la chaîne de preuve P6 est rompue.
2. **P7** : la publication ne peut pas revendiquer des résultats reproductibles si l'historique peut être modifié.

Mais l'immuabilité distante **n'est pas nécessaire pour** :

1. **L'exécution des baselines** : les tests tournent, les hashes sont reproductibles, indépendamment de ce que GitHub garantit sur la branche.
2. **La reproductibilité** : le `result_sha256` est identique entre exécutions sous Nix.
3. **La provenance et la licence** : les SHA-256 des artefacts sont vérifiables localement.
4. **Les revues Critique et Contradictoire** : les rapports sont admis et indexés, leur contenu est auditable.

Autrement dit : l'immuabilité distante protège la **valeur probatoire** des commits, pas leur **exécutabilité**. P0 porte sur l'exécutabilité et la reproductibilité. P6 porte sur la valeur probatoire.

## Décision

Déplacer l'exigence d'immuabilité distante du périmètre de P0 vers P6/P7.

### Règle ancienne

```text
remote immutability → required for P0
```

### Règle nouvelle

```text
remote immutability → required for P6/P7
                      non-blocking for P0
```

### Justification

L'audit a démontré que les affirmations fondamentales de P0 (les deux baselines sont exécutables, leurs résultats reproductibles, leurs provenances établies) sont étayées par des preuves réelles et reproduites indépendamment. L'absence de protection distante ne contredit aucune de ces affirmations. Elle les affaiblit sur le plan de l'inférence à long terme (un commit pourrait être modifié), mais ne les invalide pas au moment de l'observation.

### Conséquences

- `P0_CONTRACT_MAP.md` : la section "Critères de sortie" doit être mise à jour
- `P0_DEBT_REGISTER.md` : D01 doit être reclassée de "bloque P0" à "bloque P6/P7 uniquement"
- `P0_CLOSURE_DECISION.md` : `P0_CLOSE_WITH_DEBT` devient cohérent après rescoping
- Le statut P0 dans `PROGRESSION.md` peut passer à `CLOSED_WITH_DEBT`

### Ce que cette décision ne change pas

- Les dettes D01 et D02 restent ouvertes et doivent être résolues avant P6
- Cette décision ne constitue pas une validation de P6 ou P7
- La prochaine branche (`hypothesis/HNNN-*`) ne doit pas supposer que l'immuabilité est résolue
