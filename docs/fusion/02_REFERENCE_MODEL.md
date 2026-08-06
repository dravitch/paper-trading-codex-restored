# Modèle de référence normatif

## Objet

Deux résultats ne sont comparables que s'ils partagent un `ReferenceSpec`. Ce document définit son noyau minimal.

## Définitions

| Terme | Définition normative |
|---|---|
| prix d'observation | valeur portée par un `MarketEvent`, sans implication de fill |
| prix de fill | valeur produite par `ExecutionModel` selon `ExecutionSpec` |
| prix de valorisation | last, mid, mark ou index déclaré dans `ReferenceSpec` |
| quantité | unités de base ou contrats, indiquées par `InstrumentSpec` |
| notionnel | quantité × prix × multiplicateur contractuel |
| numéraire | unité unique des PnL et métriques principales |
| PnL réalisé | variation comptabilisée lors d'un événement de fermeture/funding/frais |
| PnL latent | valorisation réversible d'une position ouverte |
| equity | cash + collatéral valorisé + PnL latent − passifs |
| trade | cycle économique apparié, distinct des ordres et fills |

## Invariants

1. Toute valeur monétaire porte une devise.
2. Toute quantité porte une unité et un multiplicateur.
3. `OrderIntent`, `Order`, `Fill`, `Position` et `Trade` sont distincts.
4. Les frais sont des écritures du ledger, jamais une correction cachée de quantité et cash simultanément.
5. Le levier modifie le rapport notionnel/marge, pas deux fois le PnL.
6. Une métrique ne mélange pas PnL SOL et equity USD.
7. Un benchmark utilise le même horizon et annonce ses frictions.
8. Une liquidation est un événement du modèle de compte, pas un signal de stratégie.
9. Tout arrondi est appliqué par une politique nommée.
10. Toute annualisation déclare la fréquence et la régularité supposée.

## `ReferenceSpec` minimal

```yaml
schema_version: 1
numeraire: USD
valuation_price: close
calendar: crypto_24_7
periods_per_year: 365
risk_free_rate_annual: 0.0
return_definition: simple
drawdown_definition: peak_to_trough_equity
win_policy: pnl_strictly_positive
zero_pnl_policy: non_winner
benchmark_specs: []
numeric_policy:
  decimal_mode: binary64
  comparison_abs_tol: 1.0e-12
  rounding: instrument_spec
```

## Mutations devant être rejetées

- numéraire absent;
- prix de valorisation absent;
- fréquence nulle;
- métrique référencée sans version;
- benchmark sans capital initial ou friction;
- tolérance négative;
- agrégation de deux résultats avec `ReferenceSpec` différents;
- annualisation de timestamps irréguliers sans politique explicite.

## Calculs manuels de référence

### Spot à prix constant

Débit brut 100 USD, frais 0,1 %, prix 20 : quantité `99,9/20 = 4,995`. Revente à 20 : valeur 99,9; frais 0,0999; cash rendu 99,8001. Perte = frais totaux = `0,1999 USD`.

### Short linéaire

Equity 1 000, allocation 30 %, levier 2, entrée 100 : marge 300, notionnel 600, quantité 6. Sortie 90 : PnL brut `6×(100−90)=60 USD`.

### Référentiels incompatibles

Une equity de 10 SOL à 100 USD vaut 1 000 USD. Si SOL tombe à 50 sans trade, le rendement SOL est 0 %, le rendement USD −50 %. Aucun verdict « performance » n'est valide sans choix préalable du numéraire.
