# Revue Critique — Proposition de fusion contrôlée + rapport Contradictoire

## 0. Socle de connaissance produit — déclaration préalable

Avant toute critique touchant à la mécanique d'un exchange réel :

- Formule exacte de liquidation Bitget (isolée/croisée, MMR par palier de notionnel) : **β=N**, non vérifiée dans ce dossier.
- Mécanisme ADL Bitget et son effet sur le PnL simulé : **β=N**.
- Funding rate Bitget et périodicité : **β=N**.
- Profondeur de carnet typique SOL/USDT perp Bitget : **β=N**.

Ces `β=N` sont d'ailleurs déjà déclarés dans le dossier lui-même (`LIMITATIONS.md` A1/A2/A5, `TD-001`). Je ne fabrique donc aucune critique de fidélité Bitget non vérifiée — j'évalue uniquement la cohérence interne du modèle déclaré (H1–H6) et les affirmations mécaniques faites *sur le code lui-même*.

**Note d'indépendance méthodologique** : le rapport Contradictoire (`CONTRADICTOIRE_FEASIBILITY.md`) était déjà présent dans le contexte transmis avant que je forme mon propre verdict. Le protocole (`PROTOCOL_CONTRADICTOIRE.md §Indépendance minimale`) exige que la Contradictoire fige son verdict sans lire la Critique — l'inverse n'est pas explicitement interdit, mais l'esprit du protocole (deux sessions distinctes, pas de lecture croisée avant premier verdict figé) est affaibli ici puisque je lis son rapport complet avant de conclure le mien. Je le signale comme limite de procédure plutôt que de la dissimuler.

---

## 1. Checklist de patterns de défaillance — sur le code livré

```
[PASS]
Point : Liquidation = arrêt
Évidence : grid_bot.py, step() — dès current_price >= position["liquidation_price"],
le code enregistre le trade LIQUIDATION, vide self.positions, met self.liquidated=True
et exécute un `return` immédiat avant toute autre étape (TP, recalcul grille, ouverture).
Confirmé aussi par test_liquidation_is_terminal_for_identical_future_inputs : un second
step() à prix différent ne modifie ni collateral_sol ni trades.
```

```
[PASS]
Point : Benchmark Buy&Hold suit le prix 1:1
Évidence : buy_and_hold = prices * self.initial_sol. Recalcul manuel sur
[100,120,80,100] avec initial_sol=10 → [1000,1200,800,1000], exactement la valeur
retournée par test_buy_hold_preserves_units_on_hand_computed_path.
```

```
[β=N]
Point : Benchmark plafond (Sell&Hold structurel)
Évidence : aucun test n'affirme ni ne vérifie que le Grid Bot ne peut PAS dépasser
Sell&Hold. Le corpus documente lui-même (00_CORPUS_TRACEABILITY.md, contradiction #1)
qu'une revendication passée de "plafond" était fausse. La revendication a été retirée
du code (compare() ne fait que rapporter beats_sell_hold, sans invariant), donc il n'y a
plus de FAIL actif — mais il n'y a pas non plus de garde-fou qui détecterait un retour
silencieux de cette confusion si un futur document réintroduit le mot "plafond".
Qui devrait vérifier : le Producteur, avant toute réintroduction du terme.
```

```
[PASS]
Point : Frais doubles (round-trip spot)
Évidence : recalcul manuel indépendant — achat 100 USD à 20, commission 0,1
(0,1%×100), qty=(100-0,1)/20=4,995, balance=900. Vente qty×20=99,9, commission
0,0999, balance+=99,9-0,0999=99,8001 → balance finale 999,8001. Total frais
0,1+0,0999=0,1999. Identique à test_round_trip_fee_conservation_at_constant_price.
Côté GridBot (frais séparés de PortfolioManager) : recalcul de
test_grid_short_pnl_uses_contract_quantity_once — entry_fee=6×100×0,0005=0,30 ✓,
exit_fee=6×90×0,001=0,54 ✓, net=60-0,54=59,46 ✓. Aucun double débit détecté dans les
deux implémentations parallèles.
```

```
[PASS — déclaré, pas caché]
Point : Slippage calibré
Évidence : ExchangeSimulator({"mean":0.000342,"std":0.000187}) — provenance non
citée dans le code, mais LIMITATIONS.md A3 le marque explicitement ASSUME
("slippage gaussien absolu... ASSUME"). La discipline de déclaration est respectée.
```

```
[PASS — déclaré, pas caché]
Point : Transposition de domaine (adaptation timeframe)
Évidence : adapt_config_to_timeframe utilise un facteur √t pour grid_ratio.
Le README le qualifie lui-même explicitement d'"heuristique déclarée", pas de
loi validée empiriquement sur le domaine cible.
```

```
[FAIL]
Point : Contrainte d'exchange vérifiée sur LE fournisseur actuel
Évidence : data_fetcher.py bloque get_balance/create_order/fetch_positions en citant
littéralement "Erreur 40099" de l'API Demo Bitget, à la fois dans les messages
d'exception et dans le docstring de ExchangeSimulator ("Contourne l'Erreur 40099 de
Bitget Demo API"). Cette affirmation factuelle sur le comportement d'un fournisseur
précis n'est accompagnée d'aucune date de vérification, aucun test contre un
comportement réel (les tests mockent le client, ils ne vérifient jamais l'existence
de l'erreur 40099 elle-même), et hérite manifestement d'une version antérieure du
projet. Aggravant : le contexte utilisateur indique que Bitget devient indisponible
pour les utilisateurs canadiens après le 15 août et qu'un nouveau fournisseur est en
cours de sélection — ce code fige donc un comportement d'un fournisseur qui va être
remplacé, sans marquage `LEGACY`/`UNVERIFIED` ni date. Un futur Producteur qui
porterait ce module vers le nouveau fournisseur sans relire ce point risque de
transposer une contrainte non re-vérifiée (pattern explicitement visé par la
checklist §2 point "Transposition de domaine").
Comment reproduire : lire paper_trading_codex/core/data_fetcher.py lignes du
docstring de classe et les trois méthodes bloquées ; aucun test n'appelle un vrai
endpoint Bitget pour confirmer 40099 toujours actif.
```

```
[PASS — auto-corrigé]
Point : Résultat "trop propre"
Évidence : configs/grid_bot_optimal.yaml annonçait historiquement +363,19%,
Sharpe 2,55, 0 liquidation — chiffres désormais marqués "UNVALIDATED_LABEL" et
le quickstart avec ce même profil liquide sur données synthétiques (R03-09,
STATUS.md). Le résultat suspect a été activement réfuté, pas seulement toléré.
```

```
[β=N — NON_TESTABLE au stade actuel]
Point : Tests multiples / RiskMap
Évidence : §9.8 de CONTROLLED_MERGER_FEASIBILITY.md exige la publication du nombre
total de combinaisons tentées, mais RiskMap (Phase 6) n'est pas implémentée
(docs/fusion/README.md : "code de fusion : non commencé"). Il n'y a rien à
vérifier actuellement — correctement scopé comme exigence de gate future, pas
comme une lacune dissimulée du présent livrable.
```

```
[PASS]
Point : État/Logique de GridBot.step
Évidence : step() lit self.positions/self.liquidated en interne (pas un paramètre
explicite has_position). Ce n'est pas un bug caché — c'est cohérent avec l'état
actuel du code (bot à état interne, pas encore StrategySpec pure). Mais c'est un
FAIL projeté contre la cible normative RFC-003/CD-004 ("la stratégie produit des
intentions sans effet de bord") — déjà noté REWRITE dans 01_CONCEPT_DECISION_REGISTER
(CD-004). Pas un défaut caché, un écart déjà tracé.
```

---

## 2. Vérification du test lui-même (mutation mentale)

```
[PASS]
Point : test_liquidation_price_formula n'est pas déduit du code
Évidence : le test recalcule expected = 100*(1+1/3)/(1+0.05) indépendamment de
l'implémentation. Mutation mentale : si _calculate_liquidation_price devenait
entry_price*(1-1/L)/(1+m) (signe inversé), le test échouerait car l'oracle est
recalculé séparément, pas lu depuis le code.
```

```
[PASS]
Point : test_auditor_rejects_a_close_without_public_pair_identifier détecte un
auditeur vacuement optimiste
Évidence : mutation mentale — si verify_short_logic_correct() retournait "OK" par
défaut pour verified_pairs==0, ce test échouerait explicitement sur
result["verdict"] == "AUCUNE PAIRE VÉRIFIÉE". Le test couvre bien le cas H6
(circularité de l'audit).
```

---

## 3. Vérification du rapport Contradictoire

Spot-checks indépendants (pas d'acceptation de son verdict sans recalcul) :

```
[PASS]
Point : L5 (tension §8 hash exact vs §8.4 tolérance)
Évidence : lecture directe de CONTROLLED_MERGER_FEASIBILITY.md §8 point 4
("exiger une égalité exacte OU une tolérance annoncée") suivi de l'"Invariant
initial" énoncé comme égalité stricte de hash sans mention de tolérance. La
tension est réelle, confirmée par lecture indépendante du texte cité.
```

```
[PASS]
Point : L1 (O2 ambiguïté contrainte dure vs objectif)
Évidence : 05_RISKMAP_ORACLES.md, Oracle O2, contient textuellement les deux
formulations alternatives sans trancher. Confirmé par relecture directe, pas
seulement par confiance dans la citation Contradictoire.
```

```
[PASS]
Point : L9 (absence de LICENSE dans le dépôt Bitget porté)
Évidence : aucun fichier LICENSE n'apparaît dans la liste des documents fournis
pour le dépôt Bitget ; ce point ne peut être vérifié positivement ici (le contenu
du dépôt Bitget n'est pas dans mon contexte), donc je ne peux confirmer que la
méthode de vérification alléguée (`find bitget-paper-trading -name LICENSE*`),
pas son résultat brut. β=N sur le résultat exact, mais le point soulevé
(absence de traçabilité de licence dans §11/Phase 3-5) est structurellement
valide au vu du texte de CONTROLLED_MERGER_FEASIBILITY.md, qui ne mentionne
effectivement aucune clause de licence avant P7.
```

Aucune des limites L1–L12 examinées ne s'effondre à la relecture. Le rapport Contradictoire respecte la règle "pas de correction silencieuse" (il liste les objections sans les résoudre à sa place).

---

## 4. Synthèse

- **Un FAIL bloquant est présent** : la contrainte d'exchange (erreur 40099) est affirmée comme fait permanent sans re-vérification, dans un contexte où le fournisseur change. Ce n'est pas un défaut du modèle H1–H6 (qui reste valide dans son domaine), mais c'est exactement le pattern "transposition de domaine non re-justifiée" que la checklist interdit de laisser passer silencieusement.
- Les invariants comptables (frais, liquidation=arrêt, benchmark Buy&Hold) résistent tous à la vérification manuelle indépendante — **PASS confirmés, pas supposés**.
- Le rapport Contradictoire est lui-même solide sur relecture ciblée (L1, L5, L9 confirmés par lecture directe des sources citées), mais l'indépendance procédurale Critique/Contradictoire est affaiblie ici par l'ordre de lecture — à noter dans le registre si ce rapport doit compter comme la revue indépendante exigée par le protocole.
- **Verdict global sur le livrable examiné (proposition §14 + code actuel)** : `ACCEPT_WITH_LIMITS`, sous réserve intégrée de :
  1. marquer explicitement `data_fetcher.py`/`exchange_simulator.py` comme `LEGACY_BITGET_DEMO_UNVERIFIED` avant tout portage vers le nouveau fournisseur post-15-août ;
  2. toutes les limites L1, L2, L3, L5 du rapport Contradictoire (bloquantes pour P2/P6) ;
  3. absence de garde-fou testé contre la réapparition du terme "plafond Sell&Hold".

Ce FAIL et ces limites reviennent à un tour de Producteur séparé pour correction — je ne les corrige pas ici.