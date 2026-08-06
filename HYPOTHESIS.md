# Hypothèses normatives

Ce document distingue les **définitions** (D), **hypothèses réfutables** (H), **assomptions** (A) et **constats mesurés** (C). Une configuration n'est jamais une preuve de rentabilité.

## Nomenclature

| Symbole | Définition |
|---|---|
| `E`, `X` | prix d'entrée et de sortie en USD/SOL |
| `q` | quantité contractuelle en SOL |
| `L` | levier = notionnel / marge allouée |
| `m` | taux de marge de maintenance du modèle |
| `f_m`, `f_t` | taux de frais maker et taker |
| `MAR` | rendement minimal acceptable périodique |
| `N` | périodes observées |

## Hypothèses falsifiables

### H1 — Conservation comptable du spot simulé

Pour un achat brut `A` à prix `P`, la quantité reçue est `(A-Af)/P` et le cash baisse de `A`. À revente au même prix, la perte est exactement la somme des deux commissions.

- Test : `test_round_trip_fee_conservation_at_constant_price`.
- Échec : écart supérieur à la tolérance numérique de Pytest.

### H2 — PnL du short linéaire

La marge allouée est `M`, le notionnel `ML`, la quantité `q=ML/E`, et le PnL brut `q(E-X)`. Le levier ne doit apparaître qu'une fois.

- Test : `test_grid_short_pnl_uses_contract_quantity_once`.
- Échec : quantité, PnL ou frais différents de l'oracle manuel.

### H3 — Seuil de liquidation du modèle isolé simplifié

Sous les seules hypothèses « marge isolée, pas de funding, pas de frais de clôture, MMR constant », le seuil short est `E(1+1/L)/(1+m)`.

- Test : `test_liquidation_price_formula`.
- Échec : contradiction algébrique ou seuil inférieur/égal à `E` dans le domaine valide.

### H4 — Métriques définies

- Sortino : `mean(R-MAR)/sqrt(mean(min(R-MAR,0)^2))*sqrt(P)`.
- Calmar : `((V_N/V_0)^(P/N)-1)/MDD`.
- MDD : `max(1-V_t/max_{u≤t}V_u)`.

- Tests : `tests/test_performance_metrics.py` sur séries écrites à la main.
- Échec : valeur non finie non prévue ou désaccord avec l'oracle indépendant.

### H5 — Déterminisme du cœur

À prix, configuration, seed et versions identiques, le journal canonique est identique bit à bit.

- Test : `scripts/validate_reproducibility.py` exécuté deux fois.
- Échec : `result_sha256` différent.

### H6 — Audit non vacu

Une fermeture n'est contrôlée que si son `position_id` l'apparie à une ouverture. Zéro paire vérifiée est un échec.

- Tests : `tests/test_trade_auditor.py`.
- Échec : verdict `OK` avec `verified_pairs == 0` ou fermeture non appariée.

## Ce qui n'est pas affirmé

- que la stratégie est rentable, prédictive ou adaptée au trading réel;
- que les paramètres fournis sont optimaux;
- que le seuil H3 reproduit Bitget, Binance ou Bybit;
- que le slippage constant représente un carnet d'ordres réel;
- que 80 % est une perte de liquidation universelle : c'est un paramètre de scénario.
