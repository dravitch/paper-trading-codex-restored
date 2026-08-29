# H0001 — Preuves Producteur

## Identité de l'exécution

| Champ | Valeur |
|---|---|
| hypothèse préenregistrée | `8e36998` puis clarification anti-contamination `39932a9` |
| code initial H0001 | `9302635` |
| code final, M7 et runner lié au HEAD | `2ae00f9d4405cfcbdfee5bf9c2187bf572b7dca4` |
| environnement | Nix, Python 3.12.12, pytest 8.4.2, pytest-cov 6.2.1 |
| réseau requis par l'expérience | aucun |
| résultat Producteur | `PASS_PENDING_INDEPENDENT_REVIEW` |
| effet sur P1 | aucun changement de gate; P1 reste non franchi |

Le Producteur rapporte le résultat de ses tests; il ne valide pas sa propre branche. Le
statut `VALIDATED` reste interdit avant les rapports Critique et Contradictoire et leur
admission humaine.

## Séparation des trois comparaisons

```text
SCENARIO.json (inputs seulement)
          ↓
oracle indépendant en Fraction
          ↓
attendus exacts H0001 ─── comparaison exacte ─── ledger canonique
                                                    ↓
                                      projection comptable H0001
                                                    ↓
                              comparaison séparée, tolérance 5e-13
                                                    ↓
                                  P0_OBSERVED_PROJECTION.json
```

L'oracle ne lit pas la projection P0 et n'importe aucun module de production. La première
comparaison établit une égalité comptable avec l'oracle préenregistré. La seconde établit
seulement que cette projection limitée reproduit les champs observés de P0.

## Résultats exacts

| Grandeur | Oracle indépendant | Ledger | Égalité |
|---|---:|---:|---|
| quantité | `6 SOL` | `6 SOL` | exacte |
| marge déclarée ouverte | `300 USD` | `300 USD` | exacte |
| frais entrée | `3/10 USD` | `3/10 USD` | exacte |
| collatéral après ouverture | `9997/1000 SOL` | `9997/1000 SOL` | exacte |
| PnL prix brut | `-30 USD` | `-30 USD` | exacte |
| frais sortie | `63/100 USD` | `63/100 USD` | exacte |
| PnL net de clôture | `-3063/100 USD` | `-3063/100 USD` | exacte |
| collatéral final | `67937/7000 SOL` | `67937/7000 SOL` | exacte |
| frais totaux | `93/100 USD` | `93/100 USD` | exacte |

Projection P0 : `9.705285714286 SOL` après arrondi à douze décimales, concordante avec
`67937/7000`; quantité, notionnel, frais et PnL net concordent également. L'artefact
`RESULT.json` porte le SHA-256
`41f50abf3a962f6644d2f74db552ce368f43899e2bee2c53a5c802ca7ed6fd31`.

## Autorité effective du plan d'événements

`ShortScenarioSpec` contient désormais la projection fermée de `ordered_events`. Après
construction, le builder compare exactement pour chaque événement `{sequence,kind,price}`
au plan préenregistré. Une divergence produit `SCENARIO_EVENT_PLAN_MISMATCH`; modifier les
seules entrées de plan ne peut plus laisser le run reconstruire silencieusement une autre
séquence depuis `prices_usd_per_sol`.

## Exécution H0001 et mutants

Commande :

```bash
nix develop --command pytest tests/hypotheses/H0001 -vv
```

Résultat final : `12 passed in 0.08s`, code 0.

| Mutant | Défaut injecté | Détection observée |
|---|---|---|
| `M1_DOUBLE_ENTRY_FEE` | frais d'entrée doublé | `OPEN_FEE_MISMATCH` |
| `M2_INVERT_PNL_SIGN` | signe short inversé | `CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH` |
| `M3_DOUBLE_LEVERAGE` | levier réappliqué au PnL | `CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH` |
| `M4_OMIT_EXIT_FEE` | frais de sortie omis | `CLOSE_FEE_MISMATCH` |
| `M5_SWAP_CLOSE_AND_OPEN` | clôture avant ouverture | `POSITION_MISSING` |
| `M6_USD_AS_SOL` | USD débité comme SOL sans conversion | `OPEN_FEE_CURRENCY_MISMATCH` |
| `M7_SCENARIO_EVENT_ORDER_DRIFT` | `kind` du deuxième événement changé en clôture | `SCENARIO_EVENT_PLAN_MISMATCH` |

Les sept mutations sont rejetées par un invariant ciblé et un code stable.

## Runner probatoire

Commande :

```bash
nix develop --command python -m tests.hypotheses.H0001.run_experiment \
  --output docs/fusion/hypotheses/H0001/RESULT.json
```

Résultat : code 0. Le runner exécute `git rev-parse HEAD` dans la racine du dépôt et inscrit
directement `2ae00f9d4405cfcbdfee5bf9c2187bf572b7dca4`; aucun argument ne peut substituer cette
identité. Le JSON déclare séparément :

- `canonical_ledger_equals_independent_oracle: true`;
- `h0001_projection_matches_p0_observation: true`;
- `state_projection_sha256: 0eb6f0b5f5785b5807e3a7e2d6b68eeae1c99ac28fb9de596860d618ccf7dbf5`.

## Suite complète

Commande :

```bash
nix develop --command just check
```

Résultat : Ruff sans erreur; `80 passed`; couverture lignes + branches `89,53 %`, seuil
70 % atteint; code 0. Le ledger H0001 possède 100 % de couverture lignes et branches dans
ce run. `python scripts/update_status.py --check` retourne `STATUS.md is current`, code 0.

## Échec intermédiaire conservé

La première implémentation utilisait `Decimal`. Le run ciblé a donné `2 failed, 8 passed` :
la division exacte `-30,63/105` devenait une décimale finie au contexte courant et ne
pouvait être égale au rationnel `67937/7000`. L'oracle n'a pas été affaibli. Le ledger a
été corrigé pour utiliser `Fraction`, puis les dix tests ont passé. Cet échec montre que la
tolérance de projection P0 ne doit pas contaminer l'égalité comptable interne.

## Ce que la preuve établit

- les conventions A1–A10 suffisent pour ce scénario unique;
- un ledger pur et indépendant de `GridBot` reconstruit les six états attendus;
- la quantité, la marge déclarée, les frais, le PnL et le collatéral final sont vérifiés;
- les six erreurs prescrites sont détectées;
- la dérive du plan d'événements préenregistré est détectée;
- la projection limitée concorde avec le résultat historique P0.

## Ce que la preuve n'établit pas

- `P1 PASS` ou validité d'un modèle comptable général;
- équivalence de la logique de stratégie ou du replay historique;
- réservation réelle de marge, equity latente ou liquidation réaliste;
- fidélité exchange, funding, multi-position, multi-instrument ou multi-devise;
- performance financière ou validité hors du scénario figé;
- admission scientifique avant les deux revues indépendantes.

## `SPEC_NOTE_A8` — dette non bloquante H0001

A8 préenregistrait « tous les montants d'événements sont positifs avec un champ direction ».
L'implémentation respecte cette forme pour quantité, notionnel, marge et frais, mais porte
directement un signe sur `gross_pnl_usd`, `net_pnl_usd` et `collateral_delta_sol`; elle ne
possède pas de champ `direction` séparé pour ces trois deltas.

- statut : `OPEN_SPEC_NOTE`;
- scope : généralisation du modèle d'événements P1;
- impact H0001 : `NON_BLOCKING`, car signes et conversions sont explicites, vérifiés par
  l'oracle et réfutés par M2/M3/M6;
- décision différée : choisir pour P1 entre deltas signés et magnitude positive + direction;
- interdiction : ne pas réécrire rétroactivement A8 pour masquer l'écart.

## Verdict Producteur

`PASS_PENDING_INDEPENDENT_REVIEW`

H0001 est étayée dans son domaine déclaré par la preuve Producteur. La branche passe en
`IN_REVIEW`; aucune revendication de gate n'en découle.
