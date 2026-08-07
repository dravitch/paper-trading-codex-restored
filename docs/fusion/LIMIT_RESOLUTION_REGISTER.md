# Consolidation Producteur des limites L1–L12

## Règle

`RESOLVED_SPEC` signifie que l'ambiguïté documentaire est supprimée, pas que le futur code passe son gate. `OPEN_PROOF` exige encore une exécution ou une revue indépendante. La source contradictoire reste `CONTRADICTOIRE_FEASIBILITY.md` et n'est jamais réécrite.

## Registre

| Limite | Décision Producteur | Modification | Preuve restante | Statut |
|---|---|---|---|---|
| L1 | liquidation = contrainte dure au MVP | O2 donne un attendu unique : `FailureMap`, hors Pareto | test O2 et mutation politique | `RESOLVED_SPEC` |
| L2 | clé sémantique fixée | tuple canonique, JSON trié, déduplication, SHA-256 dans O7 | implémentation et permutation | `RESOLVED_SPEC` |
| L3 | cas Pareto manquants oraculés | O8–O11 : zéro, non-fini, axe unique, objectifs contradictoires | tests exécutables | `RESOLVED_SPEC` |
| L4 | voisinage O4 opérationnalisé | rayon 1, bornes, rendement et drawdown fixés | mutation rayon/seuil | `RESOLVED_SPEC` |
| L5 | hash et tolérance séparés | hash exact dans environnement verrouillé; tolérance = assertion seulement | sérialiseur canonique et parité P2 | `RESOLVED_SPEC` |
| L6 | mutations centrales ajoutées | P1 réintroduit `now()`; P3 injecte provider | mutation testing réel | `RESOLVED_SPEC` |
| L7 | règlement des frais déclaré | devise USD, base, moment et compte dans `ReferenceSpec` | modèle de ledger P1 | `RESOLVED_SPEC` |
| L8 | NO-GO défini | sept conditions d'arrêt en §12.1 | application lors des gates | `RESOLVED_SPEC` |
| L9 | licence avant portage | registre créé; commit Bitget figé; aucune licence trouvée; copie interdite | clarification du titulaire ou licence explicite | `BLOCKED_LICENSE` |
| L10 | nom canonique unique | `IsolatedLinearShortAccountModel`; discriminant versionné distinct | schéma P1 | `RESOLVED_SPEC` |
| L11 | résultats historiques non reproduits | environnement Nix restauré réexécuté : 68 tests, 87,07 %, Ruff 0 | baseline Bitget reste à exécuter séparément | `RESOLVED_RESTORED_ONLY` |
| L12 | oracles définitionnels sous revue | O2/O4/O7 explicitement non acceptés avant Contradictoire | revue du présent delta | `OPEN_PROOF` |

## Objections Critique supplémentaires

| ID | Constat | Action | Statut |
|---|---|---|---|
| C1 | erreur Bitget Demo `40099` présentée comme permanente | cause historique retirée des contrats et docstrings; endpoints privés restent interdits par conception | `RESOLVED_DOC` |
| C2 | retour possible du faux « plafond Sell & Hold » | mutation documentaire ajoutée à P7 : réintroduire cette égalité sans hypothèse doit échouer | `RESOLVED_SPEC` |
| C3 | calendrier canadien précis non authentifié | restriction générale sourcée; dates privées restent `UNKNOWN` et hors architecture du moteur | `RESOLVED_SCOPE` |

## Verdict Producteur

Neuf limites sont résolues au niveau spécification ou preuve du dépôt restauré. L9 et L12 restent `OPEN_PROOF`; la partie Bitget de L11 et les mutations exécutables L6 restent ouvertes. Aucun gate ne passe par cette consolidation. Le delta doit être revu avant retour dans `fusion/controlled-merger`.

## Reproduction Nix du dépôt restauré

Commande exécutée le 2026-08-06 :

```bash
nix develop --no-write-lock-file -c bash -lc \
  'pytest -q --cov=paper_trading_codex --cov-report=term-missing && ruff check .'
```

Résultat : exit code `0`; Python `3.12.12`; `68 passed in 2.26s`; couverture totale `87.07%`; seuil 70 % atteint; `All checks passed!` pour Ruff. Le warning Git dirty était attendu sur la branche de correction et n'affecte pas le calcul. Ces résultats ne décrivent pas le dépôt Bitget source.

## Limites résiduelles R1–R8

| Limite | Intégration Producteur | Statut après intégration |
|---|---|---|
| R1 | clé O7 étendue à tous objectifs/contraintes mandatés; résultats divergents = conflit | `RESOLVED_SPEC_PENDING_REVIEW` |
| R2 | `reference_hash = SHA-256(canonical_json(ReferenceSpec))` | `RESOLVED_SPEC_PENDING_REVIEW` |
| R3 | mutation `now()` limitée aux futurs modules `domain/` et `replay/`; legacy déclaré | `RESOLVED_SPEC_PENDING_P1` |
| R4 | statut et révision ajoutés par oracle; O7 repasse pending après modification | `RECORDED` |
| R5 | écart de type de commit reconnu; aucun calcul métier n'avait changé | `RECORDED_PROCESS_DEBT` |
| R6 | statuts attendus des cinq points O4 explicités | `RESOLVED_SPEC_PENDING_REVIEW` |
| R7 | détection pré-sérialisation et anomalie finie définies | `RESOLVED_SPEC_PENDING_REVIEW` |
| R8 | cycle, opérateur et registre NO-GO définis | `RESOLVED_SPEC_PENDING_USE` |

Le verdict source reste `ACCEPT_WITH_LIMITS`. Cette table décrit la réponse Producteur, pas la fermeture indépendante des limites.

## Constats F1–F5 sur la réponse R1–R8

| Constat | Réponse Producteur | Statut |
|---|---|---|
| F1 | points 1 et 2 O4 corrigés en `ROBUST`, conformément à la règle | `RESOLVED_SPEC_PENDING_REVIEW` |
| F2 | contrôle AST interdit imports/appels temporels directs et alias dans les modules canoniques | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| F3 | `cause_key` dérivée du gate, critère, invariant et mutation; preuves exclues de l'identité | `RESOLVED_SPEC_PENDING_USE` |
| F4 | conflit comparé sur projection sémantique complète du `RiskPoint` | `RESOLVED_SPEC_PENDING_REVIEW` |
| F5 | O4 marqué `SUPERSEDED_PENDING_REVIEW` | `RECORDED` |

Les artefacts source `CONTRADICTOIRE_DELTA_8335AB0.md` et `HEARTBEAT_CONTRADICTOIRE_DELTA_8335AB0.md` ont été admis explicitement au commit `a1e9892` et sont suivis. Leur admission ne transforme pas les réponses Producteur en fermeture indépendante.

## Constats G1–G4 sur la réponse F1–F5

| Constat | Réponse Producteur | Statut |
|---|---|---|
| G1 | analyse AST par provenance, imports dynamiques/stat temporel interdits, onze mutants | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| G2 | `cause_family_key` + signature stable + `cause_key`; occurrences inconnues hors compteur | `RESOLVED_SPEC_PENDING_USE` |
| G3 | vocabulaire fermé et transitions des statuts d'oracle | `RESOLVED_DOC_PENDING_REVIEW` |
| G4 | note remplacée par l'admission au commit `a1e9892` | `RESOLVED_DOC` |

## Constats H1–H5 sur la réponse G1–G4

| Constat | Réponse Producteur | Statut |
|---|---|---|
| H1 | allowlist P1 v1 explicite, imports transitifs contrôlés, NumPy/Pandas interdits | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| H2 | P6 exige mécaniquement O2/O4/O7 en `REVIEWED_ACCEPT*` courant | `RESOLVED_SPEC_PENDING_REVIEW` |
| H3 | `REVIEWED_NON_TESTABLE` et transitions depuis superseded ajoutés | `RESOLVED_DOC_PENDING_REVIEW` |
| H4 | troisième cycle familial non attribué force `ATTRIBUTION_BLOCKED` | `RESOLVED_SPEC_PENDING_USE` |
| H5 | registre d'IDs stables et groupe de cause racine ajoutés | `RESOLVED_SPEC_PENDING_USE` |

## Constats J1–J5 sur la réponse H1–H5

| Constat | Réponse Producteur | Statut |
|---|---|---|
| J1 | contrat `Clock`, `InstantNs`, emplacement et implémentations autorisées définis | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| J2 | preuve P6 lie statut, commit, rapport, hash et verdict; mutations d'élévation ajoutées | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| J3 | `ATTRIBUTION_BLOCKED` et statuts d'occurrence ajoutés au vocabulaire | `RESOLVED_DOC_PENDING_REVIEW` |
| J4 | `UNKNOWN` compte dans les seuils; seuls `RESOLVED`/`STOP` clôturent | `RESOLVED_SPEC_PENDING_USE` |
| J5 | cycle `RESERVED→ACTIVE→DEPRECATED→RETIRED` et autorités alignées | `RESOLVED_SPEC_PENDING_REVIEW` |

## Constats K1–K5 sur la réponse J1–J5

| Constat | Réponse Producteur | Statut |
|---|---|---|
| K1 | hash recalculé depuis le blob du commit d'admission distinct et ancêtre | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| K2 | mutants construction implicite et déplacement `SystemClock` ajoutés à P1 | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| K3 | usages nouveaux RESERVED/DEPRECATED/RETIRED → `NON_TESTABLE INVALID_CAUSAL_ID_STATE` | `RESOLVED_SPEC_PENDING_REVIEW` |
| K4 | seuil du groupe candidat fixé à trois cycles bloqués | `RESOLVED_DOC_PENDING_USE` |
| K5 | tout `NON_TESTABLE` compte comme cycle bloqué, sans remise à zéro | `RESOLVED_SPEC_PENDING_USE` |

## Constats L1–L4 sur la réponse K1–K5

| Constat | Réponse Producteur | Statut |
|---|---|---|
| L1 | `Oracle scope` indexé et marqueur normatif vérifié dans le blob admis | `RESOLVED_SPEC_PENDING_REVIEW` |
| L2 | occurrence historique définie par identité et ascendance Git, sans temps mural | `RESOLVED_SPEC_PENDING_REVIEW` |
| L3 | nouveau groupe hérite de l'union dédupliquée des cycles de ses membres/prédécesseurs | `RESOLVED_SPEC_PENDING_REVIEW` |
| L4 | preuve de protection distante ou archive signée obligatoire avant P6 | `RESOLVED_SPEC_OPEN_PROOF_EXTERNAL` |

Les contre-exemples et tests de non-régression attendus sont consignés dans [`REV06.md`](../../REV06.md). Cette réponse Producteur ne ferme pas la revue Contradictoire et ne franchit aucun gate.

## Constats M1–M4 sur la réponse L1–L4

| Constat | Réponse Producteur | Statut |
|---|---|---|
| M1 | ligne `Oracle-Review` unique, ancrée, syntaxe et verdict fermés | `RESOLVED_SPEC_PENDING_REVIEW` |
| M2 | hash canonique des champs causaux comparé au premier enregistrement | `RESOLVED_SPEC_PENDING_REVIEW` |
| M3 | registre JSON versionné déclaré source autoritaire des cycles | `RESOLVED_SPEC_PENDING_IMPLEMENTATION` |
| M4 | espace `OCC-NNNNNN` et codes de raison fermés | `RESOLVED_SPEC_PENDING_REVIEW` |

La preuve externe d'immuabilité demeure ouverte. Voir [`REV07.md`](../../REV07.md).

## Constats N1–N4 sur la réponse M1–M4

| Constat | Réponse Producteur | Statut |
|---|---|---|
| N1 | politique LF/CR et table autoritaire des verdicts d'oracles | `RESOLVED_SPEC_PENDING_REVIEW` |
| N2 | JSON canonique récursif avec vecteur SHA-256 | `RESOLVED_SPEC_PENDING_REVIEW` |
| N3 | registre append-only, chaîne du blob parent et supersession | `RESOLVED_SPEC_PENDING_REVIEW` |
| N4 | regex, domaine et allocation contiguë exclusive des occurrences | `RESOLVED_SPEC_PENDING_REVIEW` |

Voir [`REV08.md`](../../REV08.md). Aucun contrôleur n'est implémenté.

## Constats O1–O4 sur la réponse N1–N4

| Constat | Réponse Producteur | Statut |
|---|---|---|
| O1 | candidate exacte et blob historique du registre des verdicts ancré | `RESOLVED_SPEC_PENDING_REVIEW` |
| O2 | NFC, échappements exhaustifs et vecteur Unicode | `RESOLVED_SPEC_PENDING_REVIEW` |
| O3 | genesis/parent/hash explicites et migration sans remise à zéro | `RESOLVED_SPEC_PENDING_REVIEW` |
| O4 | supersession append-only avec nouvel ID contigu | `RESOLVED_SPEC_PENDING_REVIEW` |

Voir [`REV09.md`](../../REV09.md). Aucun contrôleur n'est implémenté.

## Constats P1–P4 sur la réponse O1–O4

| Constat | Réponse Producteur | Statut |
|---|---|---|
| P1 | grammaire/hash/mutants de la ligne machine `Oracle-Admission` | `RESOLVED_SPEC_PENDING_REVIEW` |
| P2 | vecteur Unicode/contrôles et fixtures de rejet | `RESOLVED_SPEC_PENDING_REVIEW` |
| P3 | parent fixé à la révision first-parent immédiatement précédente | `RESOLVED_SPEC_PENDING_REVIEW` |
| P4 | schéma append-only `supersessions` et invariants de chaîne | `RESOLVED_SPEC_PENDING_REVIEW` |

La source admise est `REV09bis`; `REV09` reste `SUPERSEDED_PROCEDURAL`. Voir [`REV10.md`](../../REV10.md).
