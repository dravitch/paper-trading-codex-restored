# P0 L1–L12 Forensic Audit

**Date** : 2026-08-17
**Auditeur** : Big Pickle (opencode)
**P0_EVIDENCE_COMMIT** : `3a3b2678b957e86768ec05584bbba5a8e90f629e`
**P0_CLOSURE_COMMIT** : `0a11672`

## Méthodologie

Pour chaque L, les 5 questions :
- **A.** Qu'est-ce qui était faux/incomplet ?
- **B.** Quelle résolution a été décidée ?
- **C.** Où est-elle matérialisée ?
- **D.** Quelle preuve ?
- **E.** La dette contamine-t-elle P0 ? (grille `status × impact × scope`)

---

## L1 — Liquidation = contrainte dure au MVP

| Dimension | Détail |
|---|---|
| **A. Problème** | Le seuil de liquidation n'était pas défini comme contrainte dure ; risque de le traiter comme un paramètre optionnel |
| **B. Décision** | La liquidation est une contrainte dure au MVP ; O2 donne un attendu unique (`FailureMap`), hors Pareto |
| **C. Matérialisation** | `strategies/grid_bot.py` : `_calculate_liquidation_price()` — formule dérivée dans `METHODS.md` §4 ; `test_grid_bot.py` : `test_liquidation_price_formula` (H3) |
| **D. Preuve** | Test exécutable ; formule algebraïque vérifiable dans METHODS.md |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: MVP` — concerne la capacitéfuture O2/P6, pas la baseline actuelle |

**Verdict** : Résolu au niveau spécification + test. Ne bloque pas P0.

---

## L2 — Clé sémantique fixée

| Dimension | Détail |
|---|---|
| **A. Problème** | Pas de clé canonique pour les artefacts ; risque de collision ou d'ambiguïté |
| **B. Décision** | Tuple canonique, JSON trié, déduplication, SHA-256 dans O7 |
| **C. Matérialisation** | `docs/fusion/CAUSAL_ID_REGISTRY.md` : sérialisation canonique définie ; `METHODS.md` §6 : JSON trié, compact, UTF-8 |
| **D. Preuve** | Spécification documentée ; pas de contrôleur implémenté pour valider |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P6` — n'affecte pas la baseline P0 |

**Verdict** : Résoluspec. Ne bloque pas P0.

---

## L3 — Cas Pareto manquants oraculés

| Dimension | Détail |
|---|---|
| **A. Problème** | Frontière de Pareto incomplète : zéro, non-fini, axe unique, objectifs contradictoires |
| **B. Décision** | O8–O11 définis pour ces cas limites |
| **C. Matérialisation** | `HYPOTHESIS.md` (H1–H6) ; `docs/fusion/05_RISKMAP_ORACLES.md` |
| **D. Preuve** | Tests H1–H6 exécutables ; oracles O8–O11 sont documentaires |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P6` |

**Verdict** : Résolu spec. Ne bloque pas P0.

---

## L4 — Voisinage O4 opérationnalisé

| Dimension | Détail |
|---|---|
| **A. Problème** | Voisinage pour l'optimisation non défini |
| **B. Décision** | Rayon 1, bornes, rendement et drawdown fixés |
| **C. Matérialisation** | Spécification documentée ; pas d'implémentation exécutable |
| **D. Preuve** | Spec uniquement ; mutation rayon/seuil prévue |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P6` |

**Verdict** : Résolu spec. Ne bloque pas P0.

---

## L5 — Hash et tolérance séparés

| Dimension | Détail |
|---|---|
| **A. Problème** | Hash exact et tolérance d'assertion mélangés |
| **B. Décision** | Hash exact dans environnement verrouillé ; tolérance = assertion seulement |
| **C. Matérialisation** | `METHODS.md` §6 : sérialisation canonique ; `REPRODUCIBILITY_MANIFEST.json` : `result_sha256` |
| **D. Preuve** | Manifeste présent ; `result_sha256 = fc3531b6...` vérifiable |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P2` |

**Verdict** : Résolu. Ne bloque pas P0.

---

## L6 — Mutations centrales ajoutées

| Dimension | Détail |
|---|---|
| **A. Problème** | Mutations testant les mécanismes centraux (frais, position size, liquidation) pas systématiques |
| **B. Décision** | P1 réintroduit `now()` ; P3 injecte provider ; mutations réelles attendues |
| **C. Matérialisation** | `HYPOTHESIS.md` H1–H6 avec critères de réfutation ; `test_grid_bot.py`, `test_contracts.py` |
| **D. Preuve** | Tests existants couvrent les invariants ; mutations complètes = P1 |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P1` |

**Verdict** : Résolu spec. Ne bloque pas P0.

---

## L7 — Règlement des frais déclaré

| Dimension | Détail |
|---|---|
| **A. Problème** | Frais non déclarés avec devise, base, moment et compte |
| **B. Décision** | Devise USD, base, moment et compte dans `ReferenceSpec` |
| **C. Matérialisation** | `METHODS.md` §2–3 : frais en USD, commission_rate déclaré |
| **D. Preuve** | `HYPOTHESIS.md` H1 : test de conservation comptable |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P1` |

**Verdict** : Résolu. Ne bloque pas P0.

---

## L8 — NO-GO défini

| Dimension | Détail |
|---|---|
| **A. Problème** | Pas de conditions d'arrêt formalisées |
| **B. Décision** | Sept conditions d'arrêt en §12.1 |
| **C. Matérialisation** | `docs/fusion/NO_GO_REGISTER.md` ; registre vide = aucune condition déclenchée |
| **D. Preuve** | Registre vide = zéro NO-GO constaté ; pas de violation |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P1` |

**Verdict** : Résolu. Ne bloque pas P0.

---

## L9 — Licence avant portage

| Dimension | Détail |
|---|---|
| **A. Problème** | Licence Bitget inconnue sur l'ancien commit `adc1d275...` |
| **B. Décision** | MIT ajoutée au commit `f2e41890...` ; portage interdit avant clarification |
| **C. Matérialisation** | `LICENSE` (MIT) dans bitget-paper-trading ; `COMPONENT_PROVENANCE.md` |
| **D. Preuve** | SHA-256 `dd10b10e...` reproduit par Critique et Contradictoire |
| **E. Dette P0** | `status: RESOLVED_LICENSE_PENDING_REVIEW`, `impact: NON_BLOCKING`, `scope: P3` — licence observée mais chaque portage reste soumis à revue |

**Verdict** : Résolu pour P0. Portage = P3.

---

## L10 — Nom canonique unique

| Dimension | Détail |
|---|---|
| **A. Problème** | Pas de nom unique pour le modèle comptable |
| **B. Décision** | `IsolatedLinearShortAccountModel` ; discriminant versionné distinct |
| **C. Matérialisation** | `METHODS.md` : modèle documenté ; `HYPOTHESIS.md` : hypothèses nommées H1–H6 |
| **D. Preuve** | Spec uniquement ; schéma P1 attendu |
| **E. Dette P0** | `status: RESOLVED_SPEC`, `impact: NON_BLOCKING`, `scope: P1` |

**Verdict** : Résolu spec. Ne bloque pas P0.

---

## L11 — Résultats historiques non reproduits

| Dimension | Détail |
|---|---|
| **A. Problème** | Les deux baselines n'avaient pas été exécutées et reproduites indépendamment |
| **B. Décision** | VM NixOS dédiée, exécution hors réseau, deux revues séparées et aveugles au premier verdict |
| **C. Matérialisation** | `P0_BASELINE_EVIDENCE.md` : restored 68/68, 87.07% sous Nix ; bitget 9/9, 38% ; revues Critique et Contradictoire |
| **D. Preuve** | Restored : 68 tests, exit 0, Ruff 0 (reproduit sous Nix) ; Bitget : 9/9, exit 0 (reproduit sur VM 140) ; couverture Bitget 38% `--cov=paper_trading` (reproduit) |
| **E. Dette P0** | `status: RESOLVED_BASELINES_REVIEWED`, `impact: NON_BLOCKING`, `scope: P0` — la couverture Bitget 38% < 70% n'est pas exigée par P0 |

**Verdict** : Résolu. Ne bloque pas P0.

---

## L12 — Oracles définitionnels sous revue

| Dimension | Détail |
|---|---|
| **A. Problème** | Les oracles O2, O4, O7 n'ont pas reçu de revue Contradictoire séparée et aveugle au premier verdict avant utilisation |
| **B. Décision** | O2/O4/O7 explicitement non acceptés avant Contradictoire ; revue du présent delta attendue |
| **C. Matérialisation** | `REVIEW_ADMISSION_REGISTRY.md` : table "Admissions d'oracles" = **vide** (aucune admission) |
| **D. Preuve** | Aucune admission d'oracle ; le registre est vide |
| **E. Dette P0** | `status: OPEN_PROOF`, `impact: BLOCKING`, `scope: P6` — P6 exige mécaniquement O2/O4/O7 en `REVIEWED_ACCEPT*` ; P0 ne peut pas clore cette dette |

**Verdict** : **BLOQUANT pour P6**, mais P0 ne prétend pas valider P6. La question est : est-ce que cette dette contamine P0 lui-même ?

**Analyse de contamination** : P0 porte sur les baselines, leur exécution et leur reproductibilité. Les oracles O2/O4/O7 sont des oracles de RiskMap (P6). P0 n'utilise pas ces oracles pour établir ses résultats. Les tests H1–H6 utilisent des oracles à formules algébriques, séries écrites à la main. **L12 ne contamine pas P0** car P0 ne revendique rien qui dépende de O2/O4/O7.

---

## Synthèse

| Limite | Statut | Bloque P0 ? | Dette résiduelle |
|---|---|---|---|
| L1 | `RESOLVED_SPEC` | non | — |
| L2 | `RESOLVED_SPEC` | non | — |
| L3 | `RESOLVED_SPEC` | non | — |
| L4 | `RESOLVED_SPEC` | non | — |
| L5 | `RESOLVED_SPEC` | non | — |
| L6 | `RESOLVED_SPEC` | non | P1 mutations |
| L7 | `RESOLVED_SPEC` | non | — |
| L8 | `RESOLVED_SPEC` | non | — |
| L9 | `RESOLVED_LICENSE_PENDING_REVIEW` | non | P3 portage |
| L10 | `RESOLVED_SPEC` | non | P1 schéma |
| L11 | `RESOLVED_BASELINES_REVIEWED` | non | — |
| L12 | `OPEN_PROOF` | **non pour P0** | P6 oracles |

**Aucune des 12 limites ne bloque P0 au sens strict.** L12 est `OPEN_PROOF` mais ne concerne que P6.

### Limites R1–R8 et cycles supersérieurs

Toutes en `RESOLVED_SPEC_PENDING_REVIEW` ou `RESOLVED_SPEC_PENDING_IMPLEMENTATION`. Aucune n'est `OPEN_PROOF`. Elles ne bloquent pas P0 mais ne sont pas non plus fermées indépendamment — leur fermeture dépend de P1+.

### Objections Critique (C1–C3)

| ID | Statut | Effet P0 |
|---|---|---|
| C1 | `RESOLVED_DOC` | aucune |
| C2 | `RESOLVED_SPEC` | aucune |
| C3 | `RESOLVED_SCOPE` | aucune |
