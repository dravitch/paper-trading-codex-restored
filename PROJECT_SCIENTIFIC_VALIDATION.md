# Validation scientifique finale

## 1. Sens du code

| Fonction | Définition | Statut |
|---|---|---|
| achat spot simulé | débit brut frais inclus, quantité nette | conforme à H1 |
| taille short | marge × levier / prix | conforme à H2 |
| PnL short | quantité × (entrée − sortie) | conforme à H2 |
| liquidation | modèle isolé simplifié dérivé | valide dans le modèle H3, non fidèle à un exchange revendiqué |
| Sharpe | excès moyen / écart-type échantillon | défini |
| Sortino | excès moyen / downside deviation | corrigé et défini |
| Calmar | CAGR / MDD | corrigé et défini |
| MDD, win rate, profit factor | définitions de `METHODS.md` | définis |

Chaque transformation publique est reliée à `HYPOTHESIS.md` et dérivée dans `METHODS.md`. Les heuristiques restantes sont étiquetées ASSUME dans `LIMITATIONS.md`.

## 2. Falsifiabilité

H1–H6 possèdent chacune un oracle numérique indépendant et un critère d'échec. Les contre-exemples ayant déclenché REV03 sont conservés : Sortino `NaN` avec une perte, Calmar arithmétique `0,6667` au lieu du composé, coût spot déclaré inférieur au coût économique, auditeur `OK` avec zéro paire.

Après correction :

- Sortino connu : `0,577350269…`;
- Calmar connu : environ `0,3765`;
- round-trip constant : perte et frais `0,1999 USD`;
- short : quantité 6, brut 60, frais sortie 0,54, net 59,46 USD;
- fermeture orpheline : `AUCUNE PAIRE VÉRIFIÉE`.

## 3. Reproductibilité

| Preuve | Résultat |
|---|---|
| tests hors réseau | 68/68 |
| wheel testée hors dépôt | 68/68 en 0,41 s |
| résultat canonique, deux runs | SHA-256 identique `fc3531…5491` |
| manifeste complet, deux runs | SHA-256 identique `145b22…cd2c` |
| PNG USD, deux runs | `e64e94…579a` |
| PNG SOL, deux runs | `85ef18…fa7` |

Le verrou Nix et les versions exactes sont enregistrés. L'identité binaire entre architectures différentes reste `unknown`; elle n'a été observée que deux fois dans le même environnement Nix.

## 4. Valeur utilisateur

L'utilisateur peut fournir une série OHLCV et une configuration, exécuter hors ligne, comparer des scénarios et interpréter des métriques définies. Les événements portent un identifiant public et sont auditables. Le manifeste fixe input, config, seed, versions et résultat.

Le projet ne démontre ni profitabilité ni fidélité exchange. Le scénario synthétique « green » aboutit à une liquidation et −69,6 % USD : ce constat réfute toute promesse implicite de sûreté et est publié sans sélection favorable.

## 5. Cohérence scientifique

- Buy & Hold : exact dans le modèle sans frais.
- Sell & Hold : référence linéaire stylisée; funding, liquidation et frais de sortie absents.
- TP, SL, MTM et liquidation : inclus dans les métriques de fermetures.
- Frais : une commission par événement; total de fermeture séparé.
- Levier : incorporé dans la quantité une seule fois.
- Liquidation : identité simplifiée H3; fraction de perte distincte et explicitement assumée.

## 6. Non-circularité

Les tests ajoutés n'appellent aucune fonction privée et ne construisent aucun attendu avec la fonction testée. Les anciens tests privés de liquidation et le test Buy & Hold circulaire ont été remplacés par l'API publique et des tables numériques. Les tests de structure restants ne sont pas utilisés comme preuves scientifiques.

## 7. Hypothèses explicites

Les six hypothèses normatives H1–H6 couvrent conservation spot, PnL short, seuil de liquidation simplifié, métriques, déterminisme et audit non vacu. Leurs équations et critères d'échec sont dans `HYPOTHESIS.md`.

## 8. Hypothèses implicites détectées

Elles sont désormais explicites sous A1–A8 : MMR, frais, slippage, perte de liquidation, observation OHLCV, numéraire SOL, frictions omises et fréquence d'annualisation.

## 9. Risques épistémologiques

| Risque | Statut |
|---|---|
| confusion simulation/exchange | atténué par renommage et limites, non supprimé |
| extrapolation de performance | avertissement explicite; aucune validation hors échantillon |
| biais de numéraire SOL/USD | ouvert, TD-002 |
| modèle intrabar absent | ouvert, A5 |
| calibrations historiques sans provenance | réfutées comme preuves, conservées comme ASSUME |
| reproductibilité inter-architecture | unknown |

## 10. Verdict scientifique

**Scientifiquement valide dans le périmètre étroit H1–H6 du laboratoire déterministe.**

**Non validé comme modèle de marché, moteur fidèle à Bitget ou stratégie rentable.** Ce second verdict est bloquant pour toute communication de performance ou usage proche production.

## 11. Recommandations GitHub MIT

- publier seulement comme laboratoire éducatif;
- conserver `LICENSE`, les métadonnées MIT et tous les documents normatifs;
- ne pas publier les anciennes valeurs « optimales » comme résultats validés;
- attendre une CI distante verte Python 3.10–3.12;
- traiter TD-001 à TD-004 avant toute revendication économique externe;
- versionner toute nouvelle hypothèse dans un `REVxx.md` avec oracle et preuve.
