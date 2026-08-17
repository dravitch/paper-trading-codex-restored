# P0 Paper Trading Capability Map

**Date** : 2026-08-17
**Baseline principale** : `paper-trading-codex-restored` (P0_EVIDENCE_COMMIT `3a3b267`)
**Baseline secondaire** : `bitget-paper-trading` (commit `f2e41890`)

## Légende

- **IMPLEMENTED** : code présent et fonctionnel
- **TESTED** : au moins un test exécutable couvre la capacité
- **DOCUMENTED_ONLY** : documenté mais pas de test dédié
- **PARTIAL** : implémentation partielle ou limitée
- **ABSENT** : pas de code pour cette capacité
- **?** : incertain — nécessite investigation

---

## Baseline restaurée (`paper-trading-codex-restored`)

| Capacité | Module/fichier | Test | Niveau | Limites connues |
|---|---|---|---|---|
| Portfolio accounting (spot) | `core/portfolio_manager.py` | `test_contracts.py` | TESTED | Modèle simplifié, pas de multi-actif |
| Portfolio accounting (short) | `strategies/grid_bot.py` | `test_grid_bot.py`, `test_contracts.py` | TESTED | Quantité contractuelle uniquement |
| PnL short linéaire | `strategies/grid_bot.py` | `test_grid_bot.py` (H2) | TESTED | Levier unique par position |
| Frais entry/exit | `core/exchange_simulator.py`, `core/portfolio_manager.py` | `test_contracts.py` (H1) | TESTED | Commission unique, pas maker/taker séparés |
| Slippage | `core/exchange_simulator.py` | `test_grid_bot.py` | TESTED | Gaussien absolu, pas calibré au marché |
| Liquidation (modèle isolé) | `strategies/grid_bot.py` | `test_grid_bot.py` (H3) | TESTED | Simplifié : pas de funding, pas de paliers, pas de frais de clôture |
| Grid short (stratégie) | `strategies/grid_bot.py` | `test_grid_bot.py` | TESTED | Une seule stratégie, paramètres fixes |
| Métriques (Sharpe, Sortino, Calmar, MDD, win rate, profit factor) | `analysis/performance.py` | `test_performance_metrics.py` (H4) | TESTED | Fréquence annuelle = 365, assumptions déclarées |
| Benchmarks (Buy & Hold, Sell & Hold) | `analysis/benchmarks.py` | `test_contracts.py` | TESTED | Références sans friction, pas de fidélité exchange |
| Audit de trades | `examples/trade_auditor_v2.py` | `test_trade_auditor.py` (H6) | TESTED | Appariement ouverture/fermeture |
| Chargement données CSV | `core/data_loader.py` | `test_data_loader.py` | TESTED | Validation OHLC, NaN, format standard |
| Données marché (lecture seule) | `core/data_fetcher.py` | `test_data_fetcher.py` | TESTED | Faux client, jamais Internet ; endpoints privés `NotImplementedError` |
| Validation paramètres | `core/exchange_simulator.py`, `strategies/grid_bot.py` | `test_grid_bot.py` | TESTED | Entrées invalides levées |
| Déterminisme du cœur | `REPRODUCIBILITY_MANIFEST.json` | `scripts/validate_reproducibility.py` (H5) | TESTED | Même config → même `result_sha256` |
| Configurations YAML | `configs/*.yaml` | — | DOCUMENTED_ONLY | 4 profils, pas de validation automatique |
| Adaptation timeframe | `core/data_loader.py` | — | DOCUMENTED_ONLY | `adapt_config_to_timeframe` et `validate_timeframe_consistency` sans test dédié |
| Exécution continue | `examples/continuous_paper_trading.py` | — | DOCUMENTED_ONLY | Exemple, pas de test |
| Replay déterministe | — | — | ABSENT | Objectif P2, pas dans cette baseline |
| Persistance / checkpoint | — | — | ABSENT | Objectif P5 |
| RiskMap | — | — | ABSENT | Objectif P6 |
| Oracles indépendants | — | — | ABSENT | Objectif P6 |
| Modèle comptable canonique (domain/) | — | — | ABSENT | Objectif P1 |
| Horloge injectée (Clock port) | — | — | ABSENT | Objectif P1 |
| Multi-fournisseur / abstraction exchange | `core/data_fetcher.py` | — | PARTIAL | Un seul fournisseur (Bitget), lecture seule |
| Gestion funding | — | — | ABSENT | Hors modèle actuel (A7) |
| Gestion liquidation dynamique | — | — | ABSENT | Modèle statique (A1) |
| Impact de marché / spread | — | — | ABSENT | Hors modèle (A7) |

---

## Baseline Bitget (`bitget-paper-trading`)

| Capacité | Module/fichier | Test | Niveau | Limites connues |
|---|---|---|---|---|
| Portfolio accounting (spot) | `paper_trading/portfolio.py` | `tests/test_portfolio.py` | TESTED | 80% couverture sur ce fichier |
| PnL short | `paper_trading/portfolio.py` | `tests/test_portfolio.py` | TESTED | Couverture partielle |
| Frais entry/exit | `paper_trading/portfolio.py` | `tests/test_portfolio.py` | TESTED | Commission unique |
| Grid short (stratégie) | `paper_trading/engine.py` | — | ABSENT de la couverture | Importé mais non testé |
| RSI / MA (stratégies) | `paper_trading/strategies.py` | — | ABSENT de la couverture | Importé mais non testé |
| Métriques | `paper_trading/metrics.py` | — | ABSENT de la couverture | Importé mais non testé |
| Données marché (Bitget) | `paper_trading/adapters/` | — | ABSENT de la couverture | Dépendances lourdes (ccxt, pandas, numpy) |
| CLI | `paper_trading/cli.py` | — | ABSENT de la couverture | Import avide, couplage précoce |
| Checkpoint | `paper_trading/checkpoint.py` | — | ABSENT de la couverture | Importé mais non testé |
| Couverture globale | — | — | 38% `paper_trading`, 36% `--cov=.` | 9 tests seulement, pas de test métrique/stratégie |
| Licence | `LICENSE` (MIT) | — | TESTED | Présente au commit `f2e41890` |

---

## Croisement des capacités

| Capacité | Restored | Bitget | Couverture croisée |
|---|---|---|---|
| Portfolio accounting | TESTED | TESTED | Complémentaire — même modèle, implémentations distinctes |
| PnL short | TESTED | TESTED | Complémentaire |
| Frais | TESTED | TESTED | Complémentaire |
| Liquidation | TESTED | ABSENT | Restored uniquement |
| Grid short | TESTED | NON TESTÉ | Restored uniquement |
| Métriques | TESTED | NON TESTÉ | Restored uniquement |
| Benchmarks | TESTED | ABSENT | Restored uniquement |
| Audit trades | TESTED | ABSENT | Restored uniquement |
| Données CSV | TESTED | ABSENT | Restored uniquement |
| Données marché | PARTIAL | PARTIAL | Aucune ne couvre de bout en bout |
| Replay | ABSENT | ABSENT | Objectif P2 |
| Persistance | ABSENT | ABSENT | Objectif P5 |
| RiskMap | ABSENT | ABSENT | Objectif P6 |

---

## Constat principal

La baseline restaurée couvre fonctionnellement les capacités de paper trading essentielles : comptabilité, PnL, frais, liquidation, stratégie grid, métriques, benchmarks, audit. La baseline Bitget apporte une validation croisée de la comptabilité et des PnL (9 tests, 80% sur `portfolio.py`) mais ne couvre ni les métriques, ni la stratégie, ni la liquidation.

**Aucune des deux baselines ne démontre** : fidélité au marché, exécution réelle, replay déterministe multi-période, persistance, ou RiskMap. Ces capacités sont toutes dans le périmètre P1+.
