# Limites, assomptions et inconnues

## Assomptions actives

| ID | Assomption | Statut | Cible de vérification |
|---|---|---|---|
| A1 | MMR constant par scénario | ASSUME | spécification versionnée du contrat/exchange choisi |
| A2 | frais maker/taker constants | ASSUME | grille tarifaire datée et niveau de compte |
| A3 | slippage gaussien absolu et indépendant de la taille | ASSUME | carnet d'ordres ou exécutions horodatées |
| A4 | perte de liquidation par défaut de 80 % | ASSUME | compte démo et modèle contractuel explicite |
| A5 | OHLCV/close suffit à simuler les déclenchements | ASSUME | données intrabar et règle d'ordre des barrières |
| A6 | collatéral SOL comme numéraire interne | ASSUME | moteur entièrement USD et test d'invariance de numéraire |
| A7 | financement, spread, latence, impact et ADL nuls | HORS MODÈLE | extension du moteur avant usage proche production |
| A8 | fréquence annuelle fournie correctement | RESPONSABILITÉ UTILISATEUR | déduction contrôlée depuis le timeframe |

## Inconnues

- validité hors échantillon de toute configuration;
- qualité des anciennes « calibrations » de slippage et d'optimisation, faute de données de provenance;
- reproductibilité binaire des PNG entre architectures différentes;
- correspondance du simulateur avec les règles Bitget actuelles;
- comportement sous gaps, prix négatifs impossibles, données manquantes longues ou liquidité nulle.

## Portée des résultats

Les résultats synthétiques prouvent uniquement que le code respecte le modèle déclaré sur les inputs fournis. Ils ne valident ni le modèle de marché ni une performance future. Buy & Hold et Sell & Hold sont des références sans friction complète; le short statique omet liquidation, funding et marge dynamique.

## Dette scientifique

| ID | Dette | Bloquante pour |
|---|---|---|
| TD-001 | modèle de liquidation non confronté à un contrat versionné | affirmation de fidélité exchange |
| TD-002 | collatéral SOL et métriques USD mélangés dans la stratégie | comparaison économique forte |
| TD-003 | aucune calibration statistique hors échantillon | affirmation de robustesse de stratégie |
| TD-004 | PNG non garanti bit-identique entre plateformes | reproductibilité binaire inter-machine |
| TD-005 | CI distante non encore observée | publication avec badge vert |

Toute modification de ces assomptions exige une révision `REVxx.md`, un oracle indépendant et une mise à jour de ce tableau.
