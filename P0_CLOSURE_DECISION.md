# P0 Closure Decision

**Date** : 2026-08-17
**Auditeur** : Big Pickle (opencode)
**Commit P0 candidate** : `3a3b2678b957e86768ec05584bbba5a8e90f629e`

## Contexte normatif

L'audit a révélé que le contrat P0原始 plaçait l'immuabilité distante parmi ses critères de sortie, mais que cette exigence était mal scopée. Le `P0_CONTRACT_SCOPE_DECISION.md` formalise le rescoping : l'immuabilité distante est déplacée de P0 vers P6/P7. La présente décision est cohérente avec ce rescoping.

## Trois décisions possibles

| Décision | Signification |
|---|---|
| `P0_CLOSE` | Tout ce que P0 exigeait est démontré |
| `P0_CLOSE_WITH_DEBT` | Dettes connues mais ne falsifient pas les revendications P0 |
| `P0_KEEP_OPEN` | Preuve manquante ou contradictoire empêche d'affirmer ce que P0 prétend |

## Évaluation

### Ce que P0 rescopé établit

1. Les deux baselines sont exécutables et leurs résultats reproductibles
2. La provenance et la licence sont documentées
3. Des revues Critique et Contradictoire séparées et aveugles au premier verdict ont été produites et admises

### Ce qui est démontré

| Revendication | Preuve | Statut |
|---|---|---|
| Restored 68/68, 87.07%, Ruff 0 | Exécuté sous Nix (cet audit), exit 0 | **DÉMONTRÉ** |
| Bitget 9/9, 38% | Démontré par preuves antérieures admises et reproductions Critique/Contradictoire ; non rejoué dans le présent audit | **DÉMONTRÉ** (preuves antérieures) |
| `result_sha256` reproductible | `fc3531b6...` identique entre exécutions | **DÉMONTRÉ** |
| Licence MIT Bitget | SHA-256 `dd10b10e...` reproduit | **DÉMONTRÉ** |
| Revues admises | Commit `804002f`, deux verdicts `ACCEPT_WITH_LIMITS` | **DÉMONTRÉ** |
| Concordance distante | `git ls-remote` ponctuel | **OBSERVÉ** (pas de protection prouvée — rescopée vers P6/P7) |

### Ce qui n'est PAS démontré (hors périmètre P0 rescopé)

| Revendication | Statut | Effet |
|---|---|---|
| Immuabilité distante | **ABSENT** | Rescopée vers P6/P7 — ne bloque pas P0 |
| Oracles O2/O4/O7 revus | **ABSENT** | Scope P6 — ne bloque pas P0 |
| Contrôleurs implémentés | **ABSENT** | Hors périmètre P0 |

### Dette identifiée

12 dettes documentées dans `P0_DEBT_REGISTER.md`. **Aucune ne bloque P0** au sens rescopé du protocole. Les deux dettes bloquantes (D01, D02) concernent P6/P7.

## Décision

### `P0_CLOSE_WITH_DEBT`

**Justification** :

1. Les revendications fondamentales de P0 rescopé (exécution, reproductibilité, revues) sont démontrées par des preuves réelles et reproduites séparément.

2. L'absence de preuve d'immuabilité distante est une **dette structurelle**, pas une contradiction. Le rescoping (voir `P0_CONTRACT_SCOPE_DECISION.md`) la déplace vers P6/P7 parce que l'audit a démontré qu'elle protège la valeur probatoire, pas l'exécutabilité.

3. Les 12 dettes sont documentées, classées par scope, et n'affectent pas les résultats de baseline.

4. La capacité de paper trading est fonctionnellement démontrée (comptabilité, PnL, frais, liquidation, grid, métriques) — cf. `P0_PAPER_TRADING_CAPABILITY_MAP.md`.

5. La reproductibilité est prouvée : même SHA-256 sous Nix, tests identiques, couverture identique.

6. Bitget n'a pas été rejoué dans cet audit. Ses preuves reposent sur les exécutions antérieures (VM 140) et les reproductions Critique/Contradictoire, toutes admises dans le commit `804002f`.

**Conditions de cette clôture** :

- Les dettes D01 et D02 restent ouvertes et doivent être résolues avant P6
- Le statut P0 dans `PROGRESSION.md` doit être mis à jour en `CLOSED_WITH_DEBT`
- Les artefacts d'audit restent dans la branche comme documentation permanente
- La prochaine branche (hypothèse HNNN) ne doit pas supposer que P0 a validé P6

## Ce que P0 ne prouve PAS (rappel)

- Que la stratégie est rentable ou prédictive
- Que le simulateur reproduit un exchange réel
- Que les résultats sont significatifs statistiquement
- Que le code est prêt pour le trading en direct
- Aucune promesse de performance financière
