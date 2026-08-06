# Taxonomie des risques

## Statuts

- `MEASURABLE` : calculable avec les données du profil déclaré.
- `APPROXIMABLE` : modèle explicite mais non confronté au réel.
- `LATENT` : détectable seulement par proxy.
- `OUT_OF_MODEL` : ne doit pas recevoir de chiffre.
- `UNKNOWN` : données ou définition insuffisantes.

## Carte

| Risque | Variable/événement | Profil minimal | Mesure proposée | Statut MVP |
|---|---|---|---|---|
| marché directionnel | variations de prix | F0 | PnL, beta au benchmark | MEASURABLE |
| volatilité | rendements réguliers | F0 | vol avec fréquence déclarée | MEASURABLE |
| drawdown | equity ordonnée | F0 | amplitude et durée | MEASURABLE |
| gap | OHLC séquentiel | F1 | distribution des sauts | MEASURABLE |
| ordre intra-barre | high/low | F1 | scénarios pessimiste/optimiste | APPROXIMABLE |
| spread | bid/ask | F2 | coût de traversée | OUT_OF_MODEL en F1 |
| liquidité | carnet | F3 | quantité remplissable/impact | OUT_OF_MODEL en F1 |
| latence | event/receive time | F2 | slippage conditionnel | OUT_OF_MODEL en F1 |
| frais | `ExecutionSpec` | F0 | écritures ledger | APPROXIMABLE jusqu'à profil provider |
| funding | événements funding | F2 | somme des flux | OUT_OF_MODEL sans flux |
| levier | `AccountSpec` | F0 | notionnel/marge | MEASURABLE dans le modèle |
| liquidation | mark + marge | F2/F4 | fréquence, distance, perte | APPROXIMABLE en F1 |
| concentration | expositions | F0 | poids max/H_index | MEASURABLE |
| contrepartie/provider | provenance | F4 | incidents/écarts | UNKNOWN au MVP |
| données | schéma/trous | F0 | complétude, ordre, duplicats | MEASURABLE |
| modèle | scénarios alternatifs | F0 | dispersion inter-modèles | LATENT |
| paramètres | voisinage | F0 | stabilité locale | MEASURABLE |
| sélection | nombre d'essais | F0 | holdout/multiplicité | MEASURABLE |
| statistique | échantillon/dépendance | F0 | IC adaptés, puissance | UNKNOWN par défaut |
| opérationnel | checkpoint/log | live | doublons, pertes événements | DEFER |
| reproductibilité | manifeste/hash | F0 | égalité des bundles | MEASURABLE |

## Règles pédagogiques

1. Un risque `OUT_OF_MODEL` est affiché comme absence, jamais comme zéro.
2. `0 liquidation observée` n'est pas `0 risque de liquidation`.
3. Une approximation indique son mécanisme de réfutation.
4. Les risques de données et de modèle sont affichés avec le risque de marché.
5. Une carte sans taille d'échantillon est incomplète.
6. Le langage `safe`, `optimal`, `garanti` et `réaliste` est interdit sans définition et preuve.
