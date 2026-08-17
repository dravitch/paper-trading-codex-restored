# P0 Contract Map — Cartographie du contrat P0

**Commit P0 candidate** : `3a3b2678b957e86768ec05584bbba5a8e90f629e`
**Date d'audit** : 2026-08-17
**Branche** : `correction/reconcile-l1-l12`

## 1. Objectif déclaré de P0

P0 est le gate "Baselines". Il établit :
- que les deux dépôts sources (`paper-trading-codex-restored` et `bitget-paper-trading`) sont exécutables et que leurs résultats sont reproductibles;
- que la provenance, la licence et les limites de chaque dépôt sont documentées;
- que des revues Critique et Contradictoire séparées et aveugles au premier verdict ont été produites et admises.

**P0 ne prouve pas** : rentabilité, fidélité au marché, validité scientifique du moteur, performance future, ni validité d'une stratégie de trading.

## 2. Éléments qui doivent exister (selon `06_FUSION_GATES.md`)

| Critère | Source | Statut |
|---|---|---|
| hashes, versions | `REPRODUCIBILITY_MANIFEST.json`, `P0_BASELINE_EVIDENCE.md` | PRÉSENT |
| limites | `LIMIT_RESOLUTION_REGISTER.md`, `HYPOTHESIS.md`, `LIMITATIONS.md` | PRÉSENT |
| provenance/licence | `COMPONENT_PROVENANCE.md`, `LICENSE` (MIT) | PRÉSENT |
| résultats reproduits | Tests exécutés sous Nix (68/68 restored, 9/9 bitget) | DOCUMENTÉ |
| revue Critique | `CRITIQUE_P0_BASELINE.md` | ADMISE (commit `804002f`) |
| revue Contradictoire | `CONTRADICTOIRE_P0_BASELINE.md` | ADMISE (commit `804002f`) |

## 3. Éléments explicitement hors P0

- Schémas exécutables de contrôleur (P1+)
- Replay déterministe du moteur (P2+)
- Portage de stratégies Bitget (P3+)
- Adaptateurs fournisseurs (P4+)
- Persistance / live (P5+)
- RiskMap et chaîne probatoire (P6+)
- Publication CI/wheel/docs (P7+)

## 4. Critères de sortie déclarés

Selon `P0_BASELINE_EVIDENCE.md` et les revues, **après rescoping** (voir `P0_CONTRACT_SCOPE_DECISION.md`) :

1. Deux baselines exécutées séparément avec résultats documentés
2. Provenance et licence établies
3. Revues Critique et Contradictoire séparées et aveugles au premier verdict, produites et admises
4. ~~Preuve d'immuabilité distante~~ → déplacée vers P6/P7 (décision de rescoping)
5. Concordance ponctuelle des branches distantes observée

## 5. Décisions L1–L12 applicables

Voir `LIMIT_RESOLUTION_REGISTER.md`. Résumé :

| Limite | Décision | Statut | Bloque P0 ? |
|---|---|---|---|
| L1 | liquidation = contrainte dure MVP | `RESOLVED_SPEC` | non |
| L2 | clé sémantique fixée | `RESOLVED_SPEC` | non |
| L3 | cas Pareto manquants oraculés | `RESOLVED_SPEC` | non |
| L4 | voisinage O4 opérationnalisé | `RESOLVED_SPEC` | non |
| L5 | hash et tolérance séparés | `RESOLVED_SPEC` | non |
| L6 | mutations centrales ajoutées | `RESOLVED_SPEC` | non |
| L7 | règlement des frais déclaré | `RESOLVED_SPEC` | non |
| L8 | NO-GO défini | `RESOLVED_SPEC` | non |
| L9 | licence avant portage | `RESOLVED_LICENSE_PENDING_REVIEW` | non |
| L10 | nom canonique unique | `RESOLVED_SPEC` | non |
| L11 | résultats historiques non reproduits | `RESOLVED_BASELINES_REVIEWED` | non |
| L12 | oracles définitionnels sous revue | `OPEN_PROOF` | non — scope P6 |

Limites R1–R8, F1–F5, G1–G4, H1–H5, J1–J5, K1–K5, L1–L4, M1–M4, N1–N4, O1–O4, P1–P4, Q1–Q4, S1–S4 : toutes en `RESOLVED_SPEC_PENDING_REVIEW` ou `RESOLVED_SPEC_PENDING_IMPLEMENTATION`. Aucune n'est `OPEN_PROOF` sauf L12 (oracles définitionnels, scope P6).

## 6. Dette autorisée après P0

| Dette | Source | Appartient à |
|---|---|---|
| Schémas contrôleur non implémentés | `REV12.md` | P1+ |
| `ORACLE_ADMISSIONS.json` et `OPERATOR_SUPERSESSION_DECISIONS.json` vides | `REV12.md` | P6+ |
| Protection distante non prouvée | `P0_BASELINE_EVIDENCE.md` | P6, P7 (rescopée depuis P0) |
| Couverture Bitget 38% < 70% | `P0_BASELINE_EVIDENCE.md` | Hors portée P0 |
| Quatre fallbacks temporels legacy | `06_FUSION_GATES.md` | P1 |
| Portage/licence Bitget non finalisé | `COMPONENT_PROVENANCE.md` | P3 |

## 7. Revues admises

| Revue | Verdict | Commit d'admission | SHA-256 |
|---|---|---|---|
| Critique P0 | `ACCEPT_WITH_LIMITS` | `804002f` | `5a5df6466d...` |
| Contradictoire P0 | `ACCEPT_WITH_LIMITS` | `804002f` | `c444e7e8c3...` |

## 8. Blocages identifiés

| Blocage | Gravité | Source |
|---|---|---|
| Preuve d'immuabilité distante absente | **non bloquante P0** — rescopée vers P6/P7 | `P0_CONTRACT_SCOPE_DECISION.md` |
| L12 oracles définitionnels non revus | **non bloquante P0** — scope P6 | `LIMIT_RESOLUTION_REGISTER.md` |
| Aucun contrôleur implémenté | non bloquante P0 | `REV12.md` |
| Artefacts hors dépôt non vérifiables | non bloquante P0 | `CRITIQUE_P0_BASELINE.md` O3 |

## 9. Verdict du contrat P0

Le contrat P0原始 exigeait une preuve d'immuabilité distante. L'audit a démontré que cette exigence était mal scopée : elle protège la valeur probatoire (P6/P7), pas l'exécutabilité (P0). Le rescoping (voir `P0_CONTRACT_SCOPE_DECISION.md`) la déplace vers P6/P7.

Les critères de sortie de P0 rescopé sont :
1. Deux baselines exécutées — **DÉMONTRÉ** (restored : exécuté dans cet audit ; Bitget : démontré par preuves antérieures admises et reproductions Critique/Contradictoire, non rejoué dans le présent audit)
2. Provenance et licence — **DÉMONTRÉ**
3. Revues Critique et Contradictoire séparées et aveugles au premier verdict — **DÉMONTRÉ** (commit `804002f`)

**Conséquence** : P0 peut passer au sens rescopé du protocole. `P0_CLOSE_WITH_DEBT` est cohérent.
