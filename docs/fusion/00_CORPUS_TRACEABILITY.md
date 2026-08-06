# Corpus Codex — inventaire et traçabilité

## Statut

Document d'archéologie. Une présence dans le corpus prouve une intention ou un essai, jamais une validité scientifique.

## Méthode

- **OBSERVE** : recherche statique dans les archives, hors `.git`, venv, caches et résultats générés.
- **OBSERVE** : lecture ciblée des README v1.0/v1.1/v1.1.2, bundles A'–D, anciens moteurs, scripts de replay/risk mapping et mandats Producteur/Critique.
- **INFER** : regroupement par intention stable malgré les duplications.
- **Limite** : aucune ancienne revendication numérique n'est acceptée sans données, manifeste et réexécution.

## Familles documentaires

| Famille | Apport | Défauts constatés | Usage futur |
|---|---|---|---|
| Paper Trading Codex v1.0–1.1.2 | honnêteté, cinq tests critiques, frais, liquidation, benchmarks | tests parfois circulaires, modèles et labels incorrects | historique des invariants à reformuler |
| Bundles A–D | mémoire des bugs, séparation données/exécution, état, monitoring | mélange de faits, inférences et langage promotionnel | catalogue de scénarios et régressions |
| Bundle A' méthodologique | critères avant code, cycles courts, journal de décisions | « optimal » non défini, automatisation parfois confondue avec preuve | discipline de livraison |
| Grid-Bot-Tree | replay/backtest, configuration déclarative, paysage de risque | code et prose mélangés, résultats non manifestés | intentions replay et RiskMap |
| sol-grid-bot backups | implémentations de replay et tables de levier | copies nombreuses, statut canonique incertain | tests de caractérisation seulement |
| sol_grid_bot_pro | exploration multi-paramètres et visualisations | faux Pareto par ratio, biais de survivant | patron d'exploration et visualisation |
| sol-grid-lab | hypothèses normatives, calibration, publication des FAIL | certaines dettes de reproductibilité déclarées | modèle documentaire principal |
| mandats La Barre | contrats, référentiel, ordre des événements, critique indépendante | projet de spécification, pas moteur livré | exigences de schéma et gouvernance |

## Intentions récurrentes

| ID | Intention | Occurrences indépendantes | Statut |
|---|---|---|---|
| CI-01 | replay doit reproduire le backtest | notes, progression, tests d'intégration | RETAIN |
| CI-02 | données et exécution doivent être séparées | bundles, providers historiques/live | RETAIN |
| CI-03 | les tests servent de documentation | bundles et Codex | RETAIN avec oracles indépendants |
| CI-04 | état de position explicite | bundles B–D | RETAIN, sans couplage interne |
| CI-05 | cartographier le risque, pas seulement optimiser | Grid-Bot-Tree, sol_grid_bot_pro | RETAIN/REWRITE |
| CI-06 | paramètres déclaratifs | YAML historiques | RETAIN avec schéma et unités |
| CI-07 | environnement Nix reproductible | A', projets restaurés | RETAIN, sans `pip install` au shellHook |
| CI-08 | monitoring et détection de dérive | bundle D | DEFER jusqu'au flux canonique |
| CI-09 | validation multi-actif/provider | MIF/bundles | RETAIN comme hypothèse, rejeter le label de certification |
| CI-10 | Producteur distinct du Critique | PaperCodex/La Barre | RETAIN comme gouvernance |

## Contradictions historiques à ne pas effacer

1. Sell & Hold a été qualifié de plafond, puis dépassé par le code : l'assertion de plafond était invalide.
2. Des liquidations ont coexisté avec des win rates proches de 100 % : la population de clôtures était incomplète.
3. Des frais ont été dits « réalistes » sans provenance, et parfois comptés deux fois.
4. Des zones « green/safe » ont liquidé sur un scénario synthétique déterministe.
5. Des « frontières efficientes » étaient des classements par ratio rendement/drawdown.
6. Des validations dites MIF ne correspondaient pas à une certification réglementaire démontrée.
7. Le même terme `SELL` a signifié fermeture long et exposition short selon les projets.
8. Des mocks annoncés déterministes utilisaient `hash()` et l'horloge murale.

Ces contradictions deviennent des fixtures de régression documentaire et technique.
