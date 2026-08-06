# Méthodes et dérivations

## 1. Unités

Cash, equity, PnL et frais sont en USD. Prix est en USD/SOL. Quantité est en SOL. Le collatéral historique du `GridBot` est stocké en SOL et valorisé au prix courant; cette convention et son risque de numéraire sont déclarés dans `LIMITATIONS.md`.

## 2. Achat spot et frais

Pour un débit brut `A`, un taux `f` et un prix exécuté `P` :

```text
commission = A f
quantité = (A - commission) / P
cash_après = cash_avant - A
```

À revente au même prix, `valeur_sortie=A(1-f)` et `commission_sortie=A(1-f)f`. La perte totale est `Af + A(1-f)f`. Débiter `A+Af` tout en réduisant la quantité compterait les frais d'entrée deux fois.

## 3. Taille et PnL short

Pour equity `V`, allocation `a`, levier `L` et prix `E` :

```text
marge M = Va
notionnel Q = ML
quantité q = Q/E
PnL brut à X = q(E-X)
frais entrée = qE f_m
frais sortie = qX f_t
PnL net de fermeture = q(E-X) - qX f_t
```

Le frais d'entrée est débité lors de l'ouverture; il ne doit pas être soustrait une seconde fois du PnL de fermeture.

## 4. Seuil de liquidation simplifié

Pour une position short isolée sans funding, frais de clôture, marge ajoutée ni paliers :

```text
marge initiale + PnL latent = marge de maintenance
Eq/L + (E-X)q = Xqm
E(1+1/L) = X(1+m)
X = E(1+1/L)/(1+m)
```

`liquidation_loss_fraction` décrit ensuite la perte de collatéral du scénario. Ce second paramètre n'est pas dérivé de l'équation et reste une assomption.

## 5. Rendements et risque

Pour `R_t=V_t/V_(t-1)-1`, fréquence annuelle `P`, taux annuel `r_f` et `MAR=r_f/P` :

```text
Sharpe = mean(R-MAR) / std_sample(R-MAR) × sqrt(P)
Sortino = mean(R-MAR) / sqrt(mean(min(R-MAR,0)^2)) × sqrt(P)
MDD = max_t(1 - V_t / max_{u≤t} V_u)
CAGR = (V_N/V_0)^(P/N) - 1
Calmar = CAGR / MDD
Profit factor = somme gains / abs(somme pertes)
Win rate = nombre(PnL>0) / nombre fermetures
```

Les PnL nuls comptent comme non-gagnants. Les ratios infinis ne sont produits que lorsque leur dénominateur est nul et leur numérateur positif.

## 6. Reproductibilité

La représentation canonique est un JSON trié, compact, encodé UTF-8. SHA-256 porte sur ces octets. Les timestamps sont exclus du hash scientifique lorsque le calendrier fixe n'affecte pas le calcul. Versions, seed, config et inputs restent enregistrés séparément dans le manifeste.
