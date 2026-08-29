# H0002 — Conservation comptable du short canonique sur une famille de scénarios

## Identité et antériorité

| Champ | Valeur |
|---|---|
| ID | `H0002` |
| Type | `DEDUCE`, sous les conventions H0001 réutilisées ci-dessous |
| Gate concerné | P1 |
| Branche | `hypothesis/H0002-short-ledger-generalization` |
| Commit de départ | `de946c1aa1a9190aebbd1bcba3116cf9be6d521e` — admission H0001 |
| Dépendance | ledger H0001 validé avec limites, non fusionné |
| Statut initial | `DRAFT` |
| Implémentation H0002 lors de cet énoncé | aucune |

La branche est empilée sur H0001 parce que H0002 cherche à réfuter la généralité du
ledger produit par H0001. Cette filiation n'est ni une fusion de H0001 vers
`fusion/controlled-merger`, ni une déclaration `P1 PASS`. Le paquet présent doit être
commité avant toute modification de code ou tout test exécutable H0002.

## Énoncé exact

Pour la famille préenregistrée dans `SCENARIO_FAMILY.json`, le ledger canonique H0001 doit
appliquer sans branchement par identité de scénario les mêmes invariants comptables à tout
short linéaire isolé et produire exactement les états dérivés indépendamment dans
`ORACLE_EXPECTATIONS.json`.

La famille couvre : gain, perte, prix de sortie égal au prix d'entrée, deux échelles de
capital et de marge, trois couples de frais maker/taker, plusieurs prix de clôture et des
conversions USD→SOL rationnelles non terminales.

## Question falsifiable

Le mécanisme comptable né de H0001 conserve-t-il, sur tous les cas :

1. `quantity = margin × leverage / entry_price`;
2. `entry_fee = entry_notional × maker_rate`;
3. `gross_pnl = quantity × (entry_price − exit_price)` pour un short;
4. `exit_fee = quantity × exit_price × taker_rate`;
5. `net_pnl = gross_pnl − exit_fee`;
6. chaque mouvement USD→SOL divisé par le prix de son événement;
7. absence de mouvement réalisé lors d'une observation;
8. fermeture complète de la position et conservation exacte du collatéral final?

## Portée

- cinq positions short linéaires isolées, chacune ouverte puis entièrement clôturée;
- arithmétique rationnelle exacte, sans tolérance interne;
- mêmes types d'événements et mêmes invariants que H0001;
- variations de capital, marge, levier, frais, quantité, observations et prix de sortie;
- fonctions pures, ordre total fourni explicitement, aucun réseau ni temps mural;
- comparaison séparée entre le ledger et une dérivation n'important aucun code de
  production.

## Hors périmètre

- spot, long, positions simultanées, clôture partielle, liquidation et funding;
- réservation ou restitution générale de marge;
- replay P2, `Clock`, provider, persistance, réseau, P6 et T1–T3;
- décision de stratégie ou fidélité exchange;
- résolution de la note A8, sauf si son ambiguïté empêche réellement l'exécution;
- validation complète de P1.

## Conventions autorisées

H0002 réutilise sans extension les conventions H0001 A1–A7, A9 et A10 : conversion
initiale du capital en SOL, equity de taille au prix d'entrée, marge déclarée non débitée,
quantité dimensionnée une seule fois par le levier, frais sur les notionnels de leurs
événements, règlement USD→SOL au prix de l'événement, observations sans réalisation,
absence de liquidation et ordre total préenregistré.

Les maxima observés restent sous le seuil simplifié H0001 de chaque cas : `103 < 138,89`
pour les cas à entrée `100`/levier `2`, `80 < 115,74` pour `SMALL_FRACTIONAL` et
`125 < 155,56` pour `LARGE_WIN`. H0002 n'évalue donc pas la liquidation.

A8 n'est pas testée : les événements existants gardent leurs PnL et deltas signés. Aucun
choix général de représentation n'est ajouté.

Une convention A11/A12 ou un traitement dépendant de `scenario_id` nécessaire pour un cas
ordinaire de cette famille réfute H0002. Une validation structurelle des données d'entrée
n'est pas une convention comptable supplémentaire.

## Famille préenregistrée

| ID | Discrimination principale | Capital / entrée | Marge / levier | Frais maker / taker | Sortie |
|---|---|---|---|---|---|
| `WIN_STANDARD` | short gagnant | `1000 USD / 100` | `3/10 / 2` | `1/2000 / 1/1000` | `90` |
| `LOSS_STANDARD` | short perdant, témoin H0001 | `1000 USD / 100` | `3/10 / 2` | `1/2000 / 1/1000` | `105` |
| `FLAT_HIGH_FEES` | PnL prix nul, perte uniquement par frais | `1000 USD / 100` | `3/10 / 2` | `1/1000 / 1/500` | `100` |
| `SMALL_FRACTIONAL` | petite taille, rationnels non terminaux | `750 USD / 75` | `1/5 / 3/2` | `1/3000 / 1/700` | `80` |
| `LARGE_WIN` | grande taille et autre couple de frais | `2400 USD / 120` | `2/5 / 5/2` | `1/4000 / 3/2000` | `110` |

`SCENARIO_FAMILY.json` contient seulement les inputs et plans ordonnés. Le futur oracle
exécutable recevra uniquement ce fichier. `ORACLE_EXPECTATIONS.json` contient les réponses
préenregistrées mais ne sera accessible ni par l'API ni par les imports de l'oracle; les
tests contrôleront cette séparation statiquement.

## Dérivation indépendante commune

Pour chaque scénario, avec capital `C`, prix initial/entrée `Pe`, fraction de marge `a`,
levier `L`, taux maker `fm`, sortie `Px` et taux taker `ft` :

```text
collateral_initial_sol = C / Pe
margin_usd             = C × a
notional_entry_usd     = margin_usd × L
quantity_sol           = notional_entry_usd / Pe
entry_fee_usd          = notional_entry_usd × fm
collateral_open_sol    = collateral_initial_sol - entry_fee_usd / Pe
gross_pnl_usd          = quantity_sol × (Pe - Px)
exit_fee_usd           = quantity_sol × Px × ft
net_pnl_usd            = gross_pnl_usd - exit_fee_usd
collateral_delta_sol   = net_pnl_usd / Px
collateral_final_sol   = collateral_open_sol + collateral_delta_sol
```

Les observations intermédiaires recopient l'état ouvert. Les résultats irréductibles sont :

| ID | Quantité | Frais entrée | PnL brut | Frais sortie | PnL net | Collatéral final |
|---|---:|---:|---:|---:|---:|---:|
| `WIN_STANDARD` | `6` | `3/10` | `60` | `27/50` | `2973/50` | `31973/3000` |
| `LOSS_STANDARD` | `6` | `3/10` | `-30` | `63/100` | `-3063/100` | `67937/7000` |
| `FLAT_HIGH_FEES` | `6` | `3/5` | `0` | `6/5` | `-6/5` | `4991/500` |
| `SMALL_FRACTIONAL` | `3` | `3/40` | `-15` | `12/35` | `-537/35` | `137301/14000` |
| `LARGE_WIN` | `20` | `3/5` | `200` | `33/10` | `1967/10` | `47923/2200` |

Les valeurs machine complètes, y compris marge, collatéral ouvert et delta final, sont
figées dans `ORACLE_EXPECTATIONS.json`.

## Critères de réfutation

H0002 est `FAIL` si au moins un scénario :

1. diverge d'un attendu rationnel exact;
2. viole un des huit invariants de l'énoncé;
3. exige une convention comptable absente des conventions réutilisées;
4. exige un branchement, une constante ou un ajustement dépendant de `scenario_id`;
5. fait dépendre l'oracle du ledger, de l'ancien `grid_bot` ou des attendus figés;
6. réalise un mouvement de collatéral pendant une observation;
7. applique le levier une seconde fois au PnL;
8. passe alors qu'un input ou un plan ordonné a dérivé;
9. dépend du réseau, d'un provider, du temps mural ou d'une RNG.

H0002 est `NON_TESTABLE` si provenance, unités ou sérialisation rationnelle sont ambiguës.
Elle est `BLOCKED` si une convention nouvelle doit être arbitrée avant un run non ambigu.
`PASS` exige que tous les cas et mutants prévus passent; il ne signifie pas `P1 PASS`.

## Falsifications minimales à implémenter après ce préenregistrement

- exécuter chaque cas après suppression de son `scenario_id`, afin de prouver que l'identité
  n'influence aucun calcul;
- permuter au moins deux scénarios dans la famille : les résultats indexés par contenu
  doivent rester identiques;
- injecter sur des cas différents : signe du PnL inversé, frais d'entrée doublés, frais de
  sortie omis, levier réappliqué et conversion USD traitée comme SOL;
- altérer un `kind`, un prix et un ordre dans les plans : chaque dérive doit être rejetée;
- ajouter un garde statique interdisant à l'oracle les imports de production et la lecture
  de `ORACLE_EXPECTATIONS.json`.

Ces falsifications réutilisent les familles de fautes H0001; elles ne prescrivent aucun
nouveau moteur ni protocole général.

## Condition d'arrêt de la prochaine phase

Après accord sur ce préenregistrement seulement : implémentation minimale, tests et run,
puis `EVIDENCE.md`, manifeste final et observations protocolaires. Aucune revue
Critique/Contradictoire intermédiaire, aucune H0003 et aucun travail P2/P6.

## Statuts possibles

`PASS`, `FAIL`, `BLOCKED`, `NON_TESTABLE`.
