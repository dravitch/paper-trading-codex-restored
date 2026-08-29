# H0002 — Admission humaine des revues

## Décision

L'opérateur admet le 2026-08-29 les deux rapports H0002 avec leur verdict
`ACCEPT_WITH_LIMITS`. Les limites sont publiées comme bornes de l'inférence; elles ne
rouvrent pas le paquet Producteur.

| Champ | Valeur |
|---|---|
| paquet Producteur examiné | `74ce950105c682792c001decf338d1bd7cbfc674` |
| commit portant les deux rapports | `5658a8b24ce2c79df421c1ab91bd01a81b720e7b` |
| Critique | `ACCEPT_WITH_LIMITS` |
| SHA-256 Critique admis | `08abbaf6348778ba26c48987579d32d9eedb0db4ac78c819df214977316e4b09` |
| Contradictoire | `ACCEPT_WITH_LIMITS` |
| SHA-256 Contradictoire admis | `47064523d31df3486f1b6cd9d8ff61372aff76d55ba4f541705e9ff8392acf24` |
| séparation des revues | `PROCEDURAL / ROLE-SEPARATED` |
| indépendance statistique / IV&V | non revendiquée |
| décision H0002 | `VALIDATED_WITH_PUBLISHED_LIMITS` |
| effet sur P1 | `NOT_PASSED` |

## Motif de recevabilité

Les deux agents distincts ont examiné le même paquet gelé. Le Contradictoire a figé son
premier verdict sans lire ni recevoir le verdict Critique; le Critique n'a pas lu le
rapport Contradictoire. Chacun a recalculé la filiation, les hashes, les résultats
rationnels et les exécutions. La séparation est fonctionnelle et procédurale, sans
revendication d'indépendance statistique, organisationnelle ou de famille de modèles.

## Limites admises et publiées

- La généralisation démontrée est paramétrique et finie : cinq shorts isolés sur le même
  chemin d'ouverture et clôture totale, avec `initial_price = entry_price`.
- L'oracle et les revues sont séparés procéduralement; ils ne constituent pas une
  réplication externe ou une IV&V.
- Le runner ne vérifie pas explicitement l'égalité des ensembles de clés des attendus. Le
  paquet admis contient néanmoins exactement les cinq cas et tous leurs champs, vérifiés
  indépendamment; cette note est non contaminante pour H0002.
- Les cinq corruptions comptables et trois dérives de plan sont ciblées, non une campagne
  exhaustive de mutation.
- Long, spot, clôture partielle, marge réservée, liquidation, funding, simultanéité,
  multi-position, multi-actif et fidélité exchange restent hors démonstration.

Ces limites restent visibles sans correction Producteur rétroactive.

## Portée de l'admission

H0002 est validée uniquement sur sa famille préenregistrée et sort de `IN_REVIEW`. Cette
admission ne déclare pas `P1 PASS`, ne fusionne ni H0001 ni H0002 dans
`fusion/controlled-merger` et ne crée aucune H0003.

La prochaine activité autorisée est un diagnostic séparé des capacités et écarts P1 à
partir de H0001 + H0002. La prochaine hypothèse sera décidée seulement après ce diagnostic.
