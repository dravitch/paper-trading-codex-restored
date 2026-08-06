# REV03 — Corrections de cohérence scientifique

## Statut

Révision en validation. Les preuves finales sont enregistrées après exécution Nix, tests, couverture, lint, wheel et double run.

## R03-01 — Sortino

- **AVANT** : écart-type échantillon des seules pertes; une perte unique produisait `NaN`.
- **APRÈS** : downside deviation `sqrt(mean(min(R-MAR,0)^2))` sur toutes les périodes.
- **Justification** : contradiction mathématique avec une métrique définie pour une série comportant une perte.
- **Test** : `test_sortino_one_loss_uses_documented_downside_deviation`.
- **Preuve** : `[0,10; -0,20; 0,20]`, `P=4` donne `0,577350269…`.

## R03-02 — Calmar

- **AVANT** : moyenne arithmétique périodique × fréquence.
- **APRÈS** : rendement annuel composé `(V_N/V_0)^(P/N)-1`, divisé par MDD.
- **Justification** : le libellé Calmar implique un rendement annualisé, pas une moyenne arithmétique.
- **Test** : `test_calmar_uses_compounded_annual_return`.
- **Preuve** : `[100;110;88;105,6]`, `P=4`, MDD 20 %, donne environ `0,3765`, et non `0,6667`.

## R03-03 — Frais du portefeuille

- **AVANT** : quantité réduite du frais et cash débité de `amount + fee`; frais d'entrée imputés deux fois.
- **APRÈS** : `amount` est un débit brut frais inclus; cash débité de `amount`.
- **Justification** : conservation comptable.
- **Test** : `test_round_trip_fee_conservation_at_constant_price`.
- **Preuve** : achat/revente 100 USD, prix 20, frais 0,1 % → coût `0,1999 USD`, égal aux frais déclarés.

## R03-04 — Quantité et levier

- **AVANT** : `size_sol` excluait le levier puis le PnL le multipliait; la sémantique de quantité était ambiguë et les frais portaient sur le notionnel sans levier.
- **APRÈS** : `size` est la quantité contractuelle `marge×L/prix`; PnL `q(E-X)`; frais sur le notionnel.
- **Justification** : cohérence d'unités et formule du PnL linéaire.
- **Test** : `test_grid_short_pnl_uses_contract_quantity_once`.
- **Preuve** : marge 300, levier 2, entrée 100 → `q=6`; sortie 90 → brut 60, frais sortie 0,54, net 59,46 USD.

## R03-05 — Liquidation

- **AVANT** : formule heuristique présentée comme « standard Bybit/Binance » et `MMR/safety_buffer` sans dérivation.
- **APRÈS** : seuil simplifié dérivé `E(1+1/L)/(1+MMR)`; perte de liquidation explicitement paramétrée et déclarée ASSUME.
- **Justification** : contradiction entre la revendication exchange et le modèle réel.
- **Test** : `test_liquidation_price_formula`, test public de perte déclarée.
- **Preuve** : dérivation complète dans `METHODS.md §4`.

## R03-06 — Événements et auditeur

- **AVANT** : fermetures SL/MTM ignorées, aucun identifiant, succès possible avec zéro paire, frais de clôture contenant entrée+sortie.
- **APRÈS** : `position_id` déterministe, TP/SL/MTM reconnus, zéro paire est un échec, commission par événement et total séparés.
- **Justification** : audit non vacu et absence de double comptage.
- **Tests** : `tests/test_trade_auditor.py`.
- **Preuve** : une fermeture orpheline produit `AUCUNE PAIRE VÉRIFIÉE`; une paire publique produit `OK`.

## R03-07 — Reproductibilité et publication

- **AVANT** : seed global, aucun manifeste canonique, aucune licence.
- **APRÈS** : RNG local seedable, manifeste SHA-256, statut régénéré, licence MIT et métadonnée SPDX.
- **Justification** : résultats attribuables et publication juridiquement explicite.
- **Tests/preuves** : `scripts/validate_reproducibility.py`, `scripts/update_status.py --check`, validation wheel hors dépôt.

## R03-08 — Population des métriques de trades

- **AVANT** : MTM et liquidation étaient absents du win rate/profit factor; le quickstart pouvait afficher 100 % malgré une liquidation.
- **APRÈS** : TP, SL, MTM et liquidation entrent dans les métriques de fermetures; la liquidation est un PnL négatif.
- **Justification** : contradiction entre la trajectoire d'equity et la population statistique annoncée.
- **Test** : `test_calculate_all_filters_closing_trades` avec les quatre événements.
- **Preuve** : un gain, un SL, un MTM nul et une liquidation donnent win rate 25 % et profit factor 0,4.

## R03-09 — Promesses implicites des configurations

- **AVANT** : profils « débutant », « monitoring hebdomadaire », distances et configuration « optimale » sans provenance reproductible.
- **APRÈS** : labels historiques marqués `UNVALIDATED_LABEL`; résultats anciens déclarés non reproductibles.
- **Justification** : aucune preuve ne soutenait ces recommandations.
- **Test** : parsing de toutes les configurations; contrôle documentaire manuel.
- **Preuve** : le quickstart synthétique avec le profil historique vert liquide, ce qui réfute toute lecture de sûreté implicite.
