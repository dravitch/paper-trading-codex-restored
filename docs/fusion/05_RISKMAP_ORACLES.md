# Oracles indépendants de RiskMap

## Oracle O1 — Pareto manuel

Objectifs : maximiser rendement `G`, minimiser drawdown `D`. Tous les points ont zéro liquidation et le même référentiel.

| Point | G | D | Attendu |
|---|---:|---:|---|
| A | 4 | 2 | non dominé |
| B | 6 | 3 | non dominé |
| C | 5 | 4 | dominé par B |
| D | 8 | 8 | non dominé |
| E | 3 | 1 | non dominé |
| F | 6 | 3 | doublon sémantique de B |

Ensemble de Pareto par identifiant : `{A, B, D, E, F}`. Ensemble sémantique après déduplication : `{A, B, D, E}`.

Le classement par ratio `G/D` donnerait B/F avant A et pourrait masquer D; il ne répond donc pas à la même question.

## Oracle O2 — Liquidation

Ajouter L : rendement temporaire 20, drawdown 50, `liquidated=true`. Si la liquidation est une contrainte dure préenregistrée, L appartient à `FailureMap` et ne participe pas au Pareto admissible. Si elle est un objectif à minimiser, son axe vaut 1 et la politique doit être distincte.

## Oracle O3 — Référentiel incompatible

Ajouter U avec rendement 10 % en SOL alors que les autres sont en USD. L'agrégation doit échouer avant calcul de dominance.

## Oracle O4 — Pic fragile

Grille unidimensionnelle :

| paramètre | rendement | drawdown |
|---:|---:|---:|
| 1 | 2 | 2 |
| 2 | 3 | 2 |
| 3 | 20 | 2 |
| 4 | −8 | 20 |
| 5 | −10 | 30 |

Le point 3 est performant mais son voisinage droit échoue. Il est `PARETO_DESCRIPTIVE` et `FRAGILE`, jamais `ROBUST`.

## Oracle O5 — Mutation des frais

Un round-trip constant de 100 USD avec frais 0,1 % coûte 0,1999 USD. Muter le frais à zéro doit modifier PnL, equity, hash résultat et éventuellement dominance. Si le résultat ne change pas, le test doit échouer.

## Oracle O6 — Domaine cartésien

`leverage=[1,2]`, `fee=[0,0.001]`, `scenario=[flat,drop]` produit exactement 8 combinaisons. Chaque combinaison reçoit un statut terminal. La somme `PASS+FAIL+ERROR+CENSORED+NON_TESTABLE` vaut 8.

## Oracle O7 — Ordre invariant

La permutation des six points O1 ne change ni l'ensemble sémantique de Pareto ni son hash canonique. Le fichier JSON brut peut différer; le hash sémantique trie selon la clé canonique préalablement définie.

## Paysages de calibration

1. monotonie totale;
2. compromis convexe;
3. plateau et doublons;
4. pic fragile;
5. région liquidée;
6. région `NON_TESTABLE`;
7. bruit seedé;
8. inversion de lecture par changement de numéraire.

Ces oracles sont écrits avant le moteur et ne doivent jamais importer son implémentation.
