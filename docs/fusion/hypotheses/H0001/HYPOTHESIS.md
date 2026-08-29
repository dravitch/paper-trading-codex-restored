# H0001 — Équivalence comptable canonique

## Identité et antériorité

| Champ | Valeur |
|---|---|
| ID | `H0001` |
| Type | `DEDUCE`, sous conventions `ASSUME` listées ci-dessous |
| Gate concerné | P1 |
| Branche | `hypothesis/H0001-canonical-ledger-equivalence` |
| Commit de départ | `7c322a812cc7308d1045c53bd34fa854d0e5bbb4` |
| Statut initial | `DRAFT` |
| Implémentation H0001 lors de cet énoncé | aucune |

Le commit `7c322a8` est retenu parce qu'il contient P0 `CLOSED_WITH_DEBT`, son manifeste
reproductible et son handoff documentaire, tout en précédant les commits `01b138e`–`88a404b`
consacrés à REV13/T1–T3, dette de scope P6 sans dépendance H0001. H0001 forme donc une
branche sœur de `work/continuation-2026-08-28`, pas sa descendante.

Ce document et ses inputs doivent être commités avant toute création de module canonique
ou de test exécutable H0001. Aucun résultat ultérieur ne peut modifier silencieusement
l'énoncé, les conventions, l'oracle ou les attendus.

## Énoncé exact

Pour la séquence comptable déterministe extraite du scénario P0
`deterministic_public_grid_scenario`, un ledger canonique minimal, indépendant de
`paper_trading_codex.strategies.grid_bot`, doit reconstruire les états observables suivants :

1. ouverture d'un short linéaire isolé de quantité contractuelle `6 SOL`, notionnel
   `600 USD`, marge déclarée `300 USD` et levier `2` à `100 USD/SOL`;
2. débit du frais d'entrée `0,30 USD`, réglé en collatéral à `100 USD/SOL`, soit
   `0,003 SOL`;
3. absence de mouvement comptable réalisé aux observations intermédiaires `102`, `99` et
   `105 USD/SOL` tant que la position reste ouverte;
4. clôture mark-to-market complète à `105 USD/SOL`, avec PnL prix brut `−30 USD`, frais de
   sortie `0,63 USD`, PnL net `−30,63 USD` et delta de collatéral
   `−30,63/105 SOL`;
5. position finale fermée et collatéral final exact `67937/7000 SOL`, soit
   `9,705285714285714... SOL`, sérialisé à douze décimales comme `9,705285714286`.

L'équivalence porte sur les états comptables, pas sur la façon dont la stratégie choisit
ses ordres. Une réussite H0001 ne ferme pas P1 et ne valide ni replay, ni fidélité exchange,
ni performance financière.

## Portée

- reconstruction d'une seule position short linéaire isolée;
- deux événements économiques : ouverture et clôture MTM;
- quatre prix observés P0 : `100`, `102`, `99`, `105 USD/SOL`;
- collatéral et règlement des frais/PnL en SOL après conversion au prix de l'événement;
- PnL et frais également exposés en USD pour l'audit;
- arithmétique indépendante exacte avec nombres rationnels;
- comparaison à la sérialisation P0 arrondie à douze décimales;
- fonctions pures, événements fournis explicitement et ordre total préenregistré.

## Hors périmètre

- décision de stratégie, construction ou recalcul de grille;
- funding, intérêts, mark/index price réaliste, paliers de marge et liquidation exchange;
- replay multi-période P2, scheduler général ou événements concurrents;
- persistance, provider, réseau, live trading, interface utilisateur;
- RiskMap, chaîne probatoire P6 et réserves T1–T3 de REV13;
- modèle spot, multi-position, multi-instrument ou multi-devise général;
- validation globale de P1.

## Scénario P0 et provenance

La source machine est `REPRODUCIBILITY_MANIFEST.json` au commit de départ :

```text
experiment = deterministic_public_grid_scenario
config_sha256 = d65e674279fbcd734c445ad4cbab80638b02b226df4155bc83a537b523871686
input_sha256 = 7e35c799bbd2f4005791f64014adba578eda447612fd1fe2fbc26675f57fc0af
result_sha256 = fc3531b6e5f02ec9461126ed1e29451192d0478b29b976b58a6633c00c585491
```

Le futur fixture `SCENARIO.json` recopiera uniquement les inputs et observations comptables
utiles, avec ces empreintes de provenance. Le code historique sert de source du scénario
observé, jamais d'oracle pour le nouveau ledger.

## Données d'entrée figées

| Donnée | Valeur | Unité |
|---|---:|---|
| capital initial | `1000` | USD |
| prix initial | `100` | USD/SOL |
| collatéral initial dérivé | `10` | SOL |
| allocation de marge | `0,30` | fraction d'equity USD |
| levier | `2` | ratio |
| prix d'entrée | `100` | USD/SOL |
| taux maker | `0,0005` | fraction du notionnel d'entrée |
| prix de clôture | `105` | USD/SOL |
| taux taker | `0,001` | fraction du notionnel de sortie |
| prix observés ordonnés | `[100,102,99,105]` | USD/SOL |
| motif de clôture | `mtm` | — |
| arrondi de publication | `12` | décimales |

Il n'y a aucune RNG utile au ledger. Le `seed=42` est conservé comme provenance P0, sans
effet sur l'oracle H0001.

## Conventions explicites (`ASSUME`)

| ID | Convention nécessaire | Impact |
|---|---|---|
| A1 | le capital initial `1000 USD` est converti sans frais en `10 SOL` au prix initial `100` | fixe l'état initial du collatéral; H0001 ne valide pas une opération spot réelle |
| A2 | l'equity de taille vaut `collateral_sol × entry_price` à l'ouverture | donne `1000 USD` pour le calcul de marge |
| A3 | marge déclarée = equity × `max_position_size`; elle n'est pas débitée du collatéral dans P0 | reproduit l'état observable P0; la réservation de marge générale reste hors scope |
| A4 | quantité contractuelle = marge × levier / prix d'entrée | le levier est incorporé exactement une fois dans la quantité |
| A5 | frais d'entrée = quantité × prix d'entrée × taux maker; frais de sortie = quantité × prix de sortie × taux taker | fixe base, moment et signe des frais |
| A6 | frais et PnL USD modifient le collatéral SOL par division au prix de leur propre événement | reproduit la convention P0 de règlement en SOL |
| A7 | le collatéral n'intègre pas le PnL latent aux observations; seul un événement de clôture le modifie | distingue l'état réalisé P0 d'une equity mark-to-market générale |
| A8 | tous les montants d'événements sont positifs avec un champ direction; les débits portent un signe négatif dans le ledger | interdit les doubles négations ad hoc |
| A9 | aucune liquidation ne survient car `105 < 100×(1+1/2)/(1+0,08)` | conserve la séquence P0 sans tester le modèle de liquidation |
| A10 | l'ordre total des événements est celui de `SCENARIO.json`; aucun temps mural n'est consulté | isole H0001 de P2 et du port `Clock` |

Toute autre convention nécessaire à la concordance rend le run `NON_TESTABLE`. Deux
représentations raisonnables compatibles avec ce texte mais produisant des états différents
réfutent la suffisance de la spécification.

## Dérivation comptable indépendante

L'oracle est une fonction rationnelle séparée qui n'importe aucun module de
`paper_trading_codex`. Avec `C=1000`, `P0=100`, `a=3/10`, `L=2`, `Pe=100`,
`fe=1/2000`, `Px=105`, `fx=1/1000` :

```text
collateral_initial_sol = C/P0 = 10
equity_entry_usd       = collateral_initial_sol × Pe = 1000
margin_usd             = equity_entry_usd × a = 300
notional_entry_usd     = margin_usd × L = 600
quantity_sol           = notional_entry_usd / Pe = 6
entry_fee_usd          = notional_entry_usd × fe = 3/10
entry_fee_sol          = entry_fee_usd / Pe = 3/1000
collateral_open_sol    = 10 - 3/1000 = 9997/1000

gross_pnl_usd          = quantity_sol × (Pe-Px) = -30
exit_notional_usd      = quantity_sol × Px = 630
exit_fee_usd           = exit_notional_usd × fx = 63/100
net_pnl_usd            = gross_pnl_usd - exit_fee_usd = -3063/100
collateral_delta_sol   = net_pnl_usd / Px = -1021/3500
collateral_final_sol   = 9997/1000 - 1021/3500 = 339685/35000
                       = 9.705285714285714...
```

Correction de notation : la forme irréductible de la valeur finale est
`67937/7000 SOL`; `339685/35000` est la somme intermédiaire équivalente.

Le fichier d'oracle exécutable devra utiliser `fractions.Fraction`, lire
`SCENARIO.json`, et retourner les attendus sans importer le ledger ni la stratégie.

## États attendus exacts

| Après événement | Position | Collatéral SOL | Frais cumulés USD | PnL prix réalisé USD |
|---|---|---:|---:|---:|
| initialisation | aucune | `10` | `0` | `0` |
| ouverture | short `6 SOL @ 100` | `9997/1000` | `3/10` | `0` |
| observation 102 | inchangée | `9997/1000` | `3/10` | `0` |
| observation 99 | inchangée | `9997/1000` | `3/10` | `0` |
| observation 105 | inchangée | `9997/1000` | `3/10` | `0` |
| clôture MTM 105 | aucune | `67937/7000` | `93/100` | `-30` |

Projection finale attendue :

```json
{
  "active_positions": 0,
  "entry_fee_usd": "0.3",
  "exit_fee_usd": "0.63",
  "final_collateral_sol_rounded_12": "9.705285714286",
  "gross_pnl_usd": "-30",
  "net_pnl_usd": "-30.63",
  "quantity_sol": "6",
  "total_fees_usd": "0.93"
}
```

## Tolérances

Les calculs internes de l'oracle et du ledger canonique sont exacts (`Fraction`/`Decimal`),
donc aucune tolérance ne décide l'égalité comptable. La seule tolérance autorisée concerne
la comparaison à un champ P0 déjà sérialisé en binary64 et arrondi à douze décimales :
`abs_tol = 5×10^-13`, soit une demi-unité de la dernière décimale publiée. Les hashes se
comparent octet pour octet et n'utilisent jamais cette tolérance.

## Critères de réfutation

H0001 est `FAIL` si :

1. un état ou attendu exact ci-dessus diverge;
2. quantité, frais, PnL ou collatéral exige une convention absente de A1–A10;
3. un ajustement ad hoc dépend d'une valeur finale P0 plutôt que des inputs;
4. le ledger ou l'oracle importe/appelle `grid_bot` ou une autre implémentation historique;
5. le levier affecte le PnL une seconde fois après avoir dimensionné la quantité;
6. un mouvement obligatoire est omis ou compté deux fois;
7. le résultat dépend du temps système, du réseau, d'un provider ou d'une RNG;
8. deux interprétations raisonnables compatibles avec l'énoncé donnent des états différents;
9. un mutant obligatoire n'est pas détecté.

Le statut est `NON_TESTABLE` si la provenance, les unités ou le manifeste sont invalides.
Il est `BLOCKED` si une convention déclarée doit être arbitrée avant une implémentation non
ambiguë. `PASS` exige oracle indépendant, ledger, mutants et preuves; il ne signifie pas
`P1 PASS`.

## Mutations obligatoires

- `M1_DOUBLE_ENTRY_FEE` : doubler le frais d'entrée;
- `M2_INVERT_PNL_SIGN` : calculer le PnL short comme `quantity × (exit-entry)`;
- `M3_DOUBLE_LEVERAGE` : multiplier encore le PnL par le levier;
- `M4_OMIT_EXIT_FEE` : omettre le débit du frais de sortie;
- `M5_SWAP_CLOSE_AND_OPEN` : appliquer la clôture avant l'ouverture;
- `M6_USD_AS_SOL` : débiter `0,30 SOL` au lieu de convertir `0,30 USD / 100`;

Chaque mutant doit échouer sur un invariant ciblé avec un code stable. Un crash sans
identification de l'invariant ne suffit pas.

## Statuts possibles

`PASS`, `FAIL`, `BLOCKED`, `NON_TESTABLE`.
