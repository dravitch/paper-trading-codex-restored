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

Politique figée pour le noyau MVP : toute liquidation est une contrainte dure. Ajouter L : rendement temporaire 20, drawdown 50, `liquidated=true`. Attendu unique : L appartient à `FailureMap`, conserve toutes ses métriques descriptives et ne participe pas au Pareto admissible. Une étude où la liquidation devient un objectif appartient à un autre `HypothesisBundle` et ne peut réinterpréter cet oracle.

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

Règle figée : voisinage de rayon 1 sur l'index ordonné du paramètre, tronqué aux bornes du domaine. Une région est admissible si chaque point est non liquidé, a un rendement `>= 0` et un drawdown `<= 10`. Un point est `ROBUST` seulement si lui-même et tous ses voisins existants sont admissibles. Le point 3 a pour voisins 2 et 4; le point 4 viole les deux seuils. Attendu : point 3 = `PARETO_DESCRIPTIVE` et `FRAGILE`, jamais `ROBUST`.

| Point | Admissible | Voisins testés | Statut attendu |
|---|---:|---|---|
| 1 | oui | 2 | `ROBUST` |
| 2 | oui | 1, 3 | `ROBUST` |
| 3 | oui | 2, 4 | `PARETO_DESCRIPTIVE`, `FRAGILE` |
| 4 | non | 3, 5 | `FAIL_CONSTRAINT` |
| 5 | non | 4 | `FAIL_CONSTRAINT` |

## Oracle O5 — Mutation des frais

Un round-trip constant de 100 USD avec frais 0,1 % coûte 0,1999 USD. Muter le frais à zéro doit modifier PnL, equity, hash résultat et éventuellement dominance. Si le résultat ne change pas, le test doit échouer.

## Oracle O6 — Domaine cartésien

`leverage=[1,2]`, `fee=[0,0.001]`, `scenario=[flat,drop]` produit exactement 8 combinaisons. Chaque combinaison reçoit un statut terminal. La somme `PASS+FAIL+ERROR+CENSORED+NON_TESTABLE` vaut 8.

## Oracle O7 — Ordre invariant

La permutation des six points O1 ne change ni l'ensemble sémantique de Pareto ni son hash canonique. Le fichier JSON brut peut différer.

Clé canonique figée pour O1 : `(reference_hash, scenario_id, canonical_parameters, objective_vector, constraint_vector)`, avec `objective_vector={G,D}` et `constraint_vector={liquidated}`. Dans une autre expérience, les vecteurs contiennent **tous** les objectifs et contraintes préenregistrés dans le `HypothesisBundle` — par exemple expected shortfall ou turnover s'ils participent à la dominance — dans l'ordre canonique de leurs identifiants. Une métrique descriptive non mandatée ne participe pas à la dominance, mais reste dans le `RiskPoint`.

`reference_hash = SHA-256(canonical_json(ReferenceSpec))`. `canonical_parameters` et `canonical_json` utilisent des objets JSON aux clés triées, UTF-8, sans whitespace; les nombres suivent la politique numérique du `ReferenceSpec`. `point_id`, ordre d'entrée et timestamp de génération sont exclus.

Chaque identifiant d'objectif, contrainte ou métrique est unique dans le `HypothesisBundle`; un doublon d'identifiant est rejeté avant exécution.

Deux entrées identiques sur `(reference_hash, scenario_id, canonical_parameters)` mais dont les projections sémantiques complètes de `RiskPoint` diffèrent ne sont jamais dédupliquées : elles produisent `REPRODUCIBILITY_CONFLICT` et rendent la carte non validable. La projection complète inclut objectifs, contraintes, métriques descriptives, statut, anomalies et hashes de preuve; elle exclut uniquement `point_id`, ordre d'entrée, chemin machine et timestamp de génération. Seuls deux `RiskPoint` aux projections sémantiques bit-identiques peuvent être dédupliqués. Les vecteurs d'objectifs/contraintes servent à la dominance, non à décider seuls de la reproductibilité. La liste est triée lexicographiquement sur sa sérialisation canonique, puis hashée en SHA-256.

## Oracle O8 — Zéro et drawdown nul

Avec les mêmes objectifs que O1 : Z=`(G=0,D=0)` et P=`(G=2,D=0)`. Attendu : P domine Z sur le seul axe G; P est non dominé. Le drawdown nul ne provoque ni division par zéro ni score infini, car aucune dominance par ratio n'est calculée.

## Oracle O9 — Métrique absente ou non finie

M=`(G=null,D=2)` reçoit `NON_TESTABLE` avec raison `MISSING_OBJECTIVE`. I=`(G=+inf,D=2)` reçoit `ERROR` avec raison `NON_FINITE_OBJECTIVE`. Aucun des deux ne participe au Pareto. NaN, `+inf` et `-inf` sont interdits dans la sérialisation canonique.

Le validateur détecte les valeurs non finies à l'entrée, avant construction du `RiskPoint` sérialisable. Il écrit dans `ResultBundle.anomalies` un enregistrement fini `{run_id, field, reason="NON_FINITE_OBJECTIVE", observed_token="+inf"}`; la valeur flottante non finie n'est jamais copiée dans le JSON. Le run terminal est représenté avec `status="ERROR"`, objectifs absents et référence vers l'anomalie.

## Oracle O10 — Domination sur un seul axe

X=`(G=6,D=3)` et Y=`(G=6,D=4)`. Attendu : X domine Y parce que G est égal et D strictement inférieur. Remplacer `<` par `<=` dans l'exigence d'au moins un axe strict doit faire échouer le test d'égalité exacte O1.

## Oracle O11 — Objectifs contradictoires

Q=`(G=4,D=1)` et R=`(G=8,D=5)`. Attendu avec objectifs préenregistrés `max(G), min(D)` : Q et R sont tous deux non dominés. Inverser après calcul l'objectif drawdown en `max(D)` est une nouvelle hypothèse et doit changer le `reference_hash`; aucune sélection automatique entre Q et R n'est autorisée.

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

Les oracles O2, O4 et O7 sont définitionnels : ils ne deviennent acceptés qu'après revue Contradictoire d'une révision figée. Leur présence dans ce fichier ne constitue pas leur validation.

## Statut des oracles définitionnels

| Oracle | Révision revue | Rapport | Statut |
|---|---|---|---|
| O2 | `09653e2` | `CONTRADICTOIRE_DELTA_09653E2.md` | `REVIEWED_ACCEPT_WITH_LIMITS` |
| O4 | `09653e2` | même rapport | `SUPERSEDED_PENDING_REVIEW` après correction F1/F5 |
| O7 | `09653e2` | même rapport | `SUPERSEDED_PENDING_REVIEW` après intégration R1/R2 |

Une modification de l'attendu, de la clé ou du domaine remet uniquement l'oracle concerné à `PENDING_REVIEW`; elle ne révoque pas silencieusement l'historique du rapport.
