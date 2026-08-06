# Thèse et traduction en code

## Énoncé

`paper-trading-codex` est un laboratoire local permettant de réfuter des hypothèses comptables simples sur une grille short. Sa thèse minimale est : **un scénario entièrement spécifié peut produire un journal déterministe dont chaque PnL, coût et métrique est recalculable indépendamment**.

Le projet n'établit aucun alpha de trading et ne prédit aucun prix.

## Chaîne de preuve

| Maillon | Code | Oracle |
|---|---|---|
| exécution spot | `ExchangeSimulator`, `PortfolioManager` | conservation cash + position − frais |
| exposition short | `GridBot._calculate_position_size` | `q = equity × allocation × L / E` |
| PnL | `GridBot._close_position` | `q(E-X) − frais_sortie` |
| liquidation | `GridBot.calculate_liquidation_price` | dérivation de `METHODS.md` |
| risque | `PerformanceTracker` | séries manuelles et définitions de `METHODS.md` |
| traçabilité | événements avec `position_id` | chaque fermeture a une ouverture publique |
| reproductibilité | script de validation | SHA-256 des inputs, config et résultat |

## Robustesse revendiquée

La robustesse visée est logicielle et comptable : types d'événements stables, erreurs explicites, réseau interdit dans les tests, seed locale, wheel testée hors dépôt et environnement Nix verrouillé. La robustesse économique hors échantillon reste **unknown** : aucune étude indépendante de données de marché n'est incluse.

## Critère global d'échec

La thèse est réfutée si un invariant H1–H6 échoue, si un résultat ne peut être reproduit depuis son manifeste, ou si une métrique publique n'a pas une définition unique. Un test vert n'est pas une preuve de profitabilité.
