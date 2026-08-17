# P0 Debt Register

**Date** : 2026-08-17
**P0_EVIDENCE_COMMIT** : `3a3b2678b957e86768ec05584bbba5a8e90f629e`
**P0_CLOSURE_COMMIT** : `0a11672`

## Dette identifiée pendant l'audit P0

| ID | Dette | Owner | Scope | Contamination | Resolution trigger | Bloque P0 ? |
|---|---|---|---|---|---|---|
| D01 | Preuve d'immuabilité distante absente (pas de protection anti force-push, pas d'archive signée) | Producteur | P6, P7 | `NON_BLOCKING` pour P0 (rescopée, voir `P0_CONTRACT_SCOPE_DECISION.md`), `BLOCKING` pour P6/P7 | Publication ou revendication P6 | **non** |
| D02 | L12 oracles O2/O4/O7 non revus (`OPEN_PROOF`) | Producteur | P6 | `BLOCKING` pour P6, `NON_BLOCKING` pour P0 | Revue Contradictoire des oracles | **non** (P0 n'utilise pas O2/O4/O7) |
| D03 | Aucun contrôleur implémenté (schémas JSON non validés mécaniquement) | Producteur | P1+ | `NON_BLOCKING` | Implémentation P1 | **non** |
| D04 | `ORACLE_ADMISSIONS.json` et `OPERATOR_SUPERSESSION_DECISIONS.json` vides | Producteur | P6 | `NON_BLOCKING` | Première admission oracle | **non** |
| D05 | Couverture Bitget 38% < 70% (seuil de publication) | Producteur | P7 | `NON_BLOCKING` | Tests additionnels Bitget | **non** (P0 n'exige pas 70% sur Bitget) |
| D06 | Artefacts hors dépôt non vérifiables (pip freeze, coverage.xml, VM KB) | Producteur | P0 | `NON_BLOCKING` | Commit des artefacts dans le dépôt | **non** (documenté dans P0_BASELINE_EVIDENCE.md) |
| D07 | Quatre fallbacks temporels legacy hors `domain/`/`replay/` | Producteur | P1 | `NON_BLOCKING` | Migration ou purging P1 | **non** |
| D08 | Portage/licence Bitget non finalisé (chaque composant = P3) | Producteur | P3 | `NON_BLOCKING` | Revue fichier par fichier | **non** |
| D09 | Adaptation timeframe sans test dédié (`adapt_config_to_timeframe`) | Producteur | P1 | `NON_BLOCKING` | Ajout de tests P1 | **non** |
| D10 | Exécution continue sans test (`continuous_paper_trading.py`) | Producteur | P5 | `NON_BLOCKING` | Tests d'intégration P5 | **non** |
| D11 | Configurations YAML sans validation automatique | Producteur | P1 | `NON_BLOCKING` | Schéma de validation P1 | **non** |
| D12 | Import avide de `core/__init__.py` (couplage transitif) | Producteur | P1 | `NON_BLOCKING` | Refactor P1 | **non** |

## Résumé

- **0 dette bloque P0** au sens rescopé du protocole (voir `P0_CONTRACT_SCOPE_DECISION.md`)
- **2 dettes bloquent P6/P7** (D01, D02) — hors périmètre P0
- **10 dettes NON_BLOCKING** — documentées, à résoudre dans les gates correspondants
