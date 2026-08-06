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
