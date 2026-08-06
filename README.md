# Paper Trading Codex

Framework Python de paper trading local pour tester une stratégie grid short avec des hypothèses financières explicites et falsifiables.

Dépôt officiel : [dravitch/paper-trading-codex-restored](https://github.com/dravitch/paper-trading-codex-restored)

Vision d'évolution : [fusion contrôlée vers une plateforme universelle de replay et de risque](CONTROLLED_MERGER_FEASIBILITY.md).

Documents de cadrage actifs : [index de la fusion contrôlée](docs/fusion/README.md). Ils documentent les preuves disponibles et ne constituent pas encore une validation du futur moteur.

Le projet simule les ordres localement. Il n'envoie aucun ordre privé à Bitget et ne doit pas être utilisé avec des fonds réels.

## Valeur pour l'utilisateur

- comparer une stratégie à Buy & Hold et Sell & Hold ;
- vérifier les frais d'entrée et de sortie ;
- vérifier une liquidation déterministe et l'arrêt du bot ;
- mesurer rendement, drawdown, Sharpe, Sortino, Calmar, win rate et profit factor ;
- charger ses propres données OHLCV ou utiliser des données synthétiques ;
- reproduire les résultats avec des configurations YAML versionnées.

## Hypothèses testées

Les tests encodent des prédictions dont le résultat est calculable avant l'exécution :

| Hypothèse | Prédiction falsifiable |
|---|---|
| Liquidation | Le scénario applique la fraction déclarée puis le bot s'arrête. |
| Frais | Une entrée et une sortie paient chacune leur commission. |
| Slippage | Un achat est exécuté au-dessus du marché et une vente en dessous. |
| Grid short | Tous les niveaux initiaux sont au-dessus du prix courant. |
| Benchmarks | Buy & Hold et Sell & Hold suivent leurs identités comptables exactes. |
| Drawdown | Une courbe connue produit un drawdown calculable. |
| Timeframe | L'adaptation historique en racine du temps est une heuristique déclarée. |
| Paper trading | Un aller-retour sans slippage suit l'identité comptable attendue. |

Ces invariants sont entièrement hors ligne et déterministes. Les tests du connecteur utilisent un faux client, jamais Internet.

## Installation

### Avec pip

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install '.[test,examples]'
pytest tests -q
```

### Avec Nix

```bash
nix develop
just check
```

Le shell Nix n'installe rien avec pip, ne crée aucun environnement virtuel et ne modifie aucun fichier du projet.

## Utilisation hors ligne

```bash
python examples/quickstart_grid_bot.py --config configs/grid_bot_green.yaml
```

Sans fichier CSV, le quickstart utilise une série synthétique déterministe. Pour tester vos données :

```bash
python examples/quickstart_grid_bot.py \
  --config configs/grid_bot_green.yaml \
  --data /chemin/vers/prices.csv
```

Le CSV doit contenir au minimum une colonne `close`. Les colonnes `open`, `high`, `low` et `volume` sont prises en charge. Les relations OHLC invalides et valeurs manquantes sont filtrées et documentées par le loader.

## API minimale

```python
from datetime import datetime

from paper_trading_codex.strategies import GridBot

config = {
    "initial_capital": 1_000,
    "leverage": 2,
    "grid_size": 3,
    "grid_ratio": 0.02,
}

bot = GridBot(config)
for price in [100, 102, 104, 101, 98]:
    state = bot.step(price, datetime(2024, 1, 1))

print(bot.get_summary(price))
```

## Commandes qualité

```bash
just lint       # Ruff, sans modification
just test       # Tests hors ligne
just coverage   # Couverture lignes + branches, seuil 70 %
just build      # sdist et wheel
just check      # lint + couverture
```

## Configurations

| Fichier | Levier | Usage |
|---|---:|---|
| `grid_bot_green.yaml` | 3x | profil prudent |
| `grid_bot_yellow.yaml` | 5x | profil intermédiaire |
| `grid_bot_red.yaml` | 8x | stress test à haut risque |
| `grid_bot_optimal.yaml` | 2x | paramètres historiques à revalider hors échantillon |

Les performances historiques ou synthétiques ne prédisent pas les performances futures. Le nom « optimal » décrit une ancienne optimisation et ne constitue pas une recommandation.

## Limites Bitget

`BitgetDataFetcher` permet uniquement la lecture de données publiques lorsque ccxt est disponible. Les méthodes privées `create_order`, `get_balance` et `fetch_positions` lèvent volontairement `NotImplementedError`. Le portefeuille et les ordres restent locaux.

Le connecteur public est optionnel : `python -m pip install '.[market-data]'`.

Ne commitez jamais de `.env`, clé API, passphrase, log privé ou résultat contenant des identifiants.

## Structure

```text
paper_trading_codex/   bibliothèque installable
tests/                 invariants et contrats hors ligne
configs/               profils YAML reproductibles
examples/              quickstarts et audit de résultats
HYPOTHESIS.md           énoncés normatifs et critères d'échec
METHODS.md              définitions et dérivations
LIMITATIONS.md          assomptions et inconnues
STATUS.md               compteurs canoniques régénérés
```

## Statut

Version `1.1.2`. Projet éducatif et expérimental sous licence MIT. Les formules,
hypothèses et dettes scientifiques sont normées par `HYPOTHESIS.md`, `METHODS.md`
et `LIMITATIONS.md`. Aucun résultat ne constitue une promesse de performance.
