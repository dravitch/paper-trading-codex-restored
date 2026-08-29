# H0002 — Evidence

## Premier run, avant mutants

Le paquet a été préenregistré au commit `1d63024`. L'oracle et les tests paramétrés ont été
ajoutés au commit `eade1e7`, sans modification du ledger hérité de H0001.

```text
ledger H0001 admis SHA-256 = b917433de9661896a1ac0ec74e9c7b2fb2d8a64864736e48d1ae4161286cf6bc
ledger au premier run SHA-256 = b917433de9661896a1ac0ec74e9c7b2fb2d8a64864736e48d1ae4161286cf6bc
```

Commande exécutée le 2026-08-29 (`America/Toronto`) :

```text
nix develop --command pytest tests/hypotheses/H0002 -vv
```

Résultat observé avant toute correction ou ajout de mutant :

```text
7 collected
7 passed in 0.05s
```

Les cinq cas `WIN_STANDARD`, `LOSS_STANDARD`, `FLAT_HIGH_FEES`,
`SMALL_FRACTIONAL` et `LARGE_WIN` ont produit les états rationnels exacts dérivés par
l'oracle. L'oracle a également reproduit les attendus préenregistrés et le contrôle statique
a confirmé l'absence d'import de production et de lecture d'`ORACLE_EXPECTATIONS.json`.

Classification du premier run :

```text
status = PASS
impact = SUPPORTING
scope = H0002_FIRST_RUN
ledger correction before result = NONE
```

Ce résultat soutient la généralisation limitée testée; il ne constitue encore ni le paquet
Producteur final, ni H0002 validée, ni `P1 PASS`.

## Phase finale

Le code d'instrumentation final est figé au commit
`da720db01f0a10554efc3dc75185d9d804899c68`. Le ledger garde le même blob et le même
SHA-256 que lors de l'admission H0001; aucun correctif de production H0002 n'existe.

### Run ciblé et falsifications

```text
nix develop --command pytest tests/hypotheses/H0002 -vv
→ 16 passed in 0.07s
```

Les contrôles couvrent :

- oracle sans import de production ni lecture des réponses préenregistrées;
- concordance oracle exécutable ↔ attendus préenregistrés;
- concordance exacte ledger ↔ oracle sur les cinq scénarios;
- suppression de `scenario_id` et permutation de la famille sans effet comptable;
- cinq corruptions comptables rejetées avec leur invariant ciblé;
- dérives de `kind`, prix et ordre rejetées par `SCENARIO_EVENT_PLAN_MISMATCH`.

| Mutation | Cas | Code observé |
|---|---|---|
| signe du PnL inversé | `WIN_STANDARD` | `CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH` |
| frais d'entrée doublés | `LOSS_STANDARD` | `OPEN_FEE_MISMATCH` |
| frais de sortie omis | `FLAT_HIGH_FEES` | `CLOSE_FEE_MISMATCH` |
| levier réappliqué au PnL | `SMALL_FRACTIONAL` | `CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH` |
| montant USD traité comme SOL | `LARGE_WIN` | `OPEN_FEE_CURRENCY_MISMATCH` |
| plan : kind/prix/ordre altéré | `WIN_STANDARD` | `SCENARIO_EVENT_PLAN_MISMATCH` |

### Résultat matérialisé

```text
nix develop --command python -m tests.hypotheses.H0002.run_experiment \
  --output docs/fusion/hypotheses/H0002/RESULT.json
sha256sum docs/fusion/hypotheses/H0002/RESULT.json
→ b38e2bcee1992dc8314300f6687b664534290368eee2660621eff2d488050c4b
```

Le runner dérive d'abord les cinq oracles depuis `SCENARIO_FAMILY.json`, compare ensuite
le ledger, puis seulement lit `ORACLE_EXPECTATIONS.json` pour vérifier l'antériorité des
réponses. Le hash canonique des cinq projections est
`3db37271090c2eb96ee33875dac59cdfe4c64cc1dff369ee676c1e93249ef36b`.

### Non-régression globale

```text
nix develop --command just check
→ Ruff OK
→ 96 passed
→ couverture 89,53 %
→ ledger lignes/branches 100 %

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current
```

## Classification Producteur

```text
H0002 = PASS_PENDING_INDEPENDENT_REVIEW
P1 = NOT_PASSED
ledger changes for H0002 = NONE
new accounting conventions = NONE
scenario-specific production logic = NONE
```

H0002 soutient que les invariants du short canonique H0001 se conservent sur la famille
préenregistrée. Elle ne démontre ni long/spot, ni clôture partielle, ni liquidation,
funding, multi-position, fidélité exchange ou P1 complet.
