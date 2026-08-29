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

`PENDING_MUTANTS_AND_FINAL_RUN`
