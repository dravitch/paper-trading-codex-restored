# H0004 — Evidence Producteur

## Antériorité

```text
044406f  préenregistrement BLOCKED S1–S7, aucun code
8aa05bc  décision humaine S1–S7, aucun code
56c5e54  second préenregistrement BLOCKED S8, aucun code
cef58c5  décision humaine S8, aucun code
3ed68c5  troisième préenregistrement READY_FOR_IMPLEMENTATION, aucun code
f3c6811  alignement des marqueurs courants, aucun code
a137491  ledger nominal + oracle + deux tests nominaux
ffed088  premier run figé avant mutants
54f252a  instrumentation de conservation + M1–M19
4bd8e1f  runner déterministe final
```

## Premier run discriminant

Le ledger nominal a passé sa première exécution sans correction :

```text
nix develop --command pytest tests/hypotheses/H0004/test_minimal_spot_ledger_nominal.py -q
→ 2 passed in 0.05s
```

`FIRST_RUN.json` lie ce run à `a1374912c4eb233f64566fcc2bc8a443167179ee` et au
SHA-256 initial du ledger `127dc566…8e929`. Les mutants n'existaient pas encore. Le blob
final du ledger diffère seulement par l'ajout du validateur explicite de conservation
utilisé par M6/M11; aucune formule nominale observée n'a été corrigée.

## Résultat comptable

L'oracle séparé dérive les balances uniquement à partir de `SCENARIO.json`. Le runner
compare ensuite séparément ses résultats, le ledger et `ORACLE_EXPECTATIONS.json`.

```text
after BUY:
  base  = 999/200 SOL
  quote = 0/1 USD
  fees  = 1/10 USD
  equity @20 = 999/10 USD

after SELL:
  base  = 0/1 SOL
  quote = 998001/10000 USD
  fees  = 1999/10000 USD
  equity @20 = 998001/10000 USD
```

Les six `AccountEvent` correspondent exactement aux IDs, champs, signes et ordre local B6
préenregistrés. Pour chaque fill, les variations BASE/QUOTE du nouvel état égalent l'ancien
état plus la somme des deltas. `fees_by_currency` est un cumul positif séparé et n'est
jamais déduit deux fois. La valorisation ne mute pas l'état.

## Falsifications

Les 24 tests H0004 exécutent M1–M19, y compris M18a–M18e : insuffisance quote/base,
frais/devise, grille, compatibilités, conservation, signes, pureté, doublons, discriminant
spot, IDs/provenance, double initialisation, cumul des frais, clé du dernier input,
réapplication, fill ancien économiquement applicable, absence de tri/mémoire cachée et
frais BASE hors profil.

Les codes S8 sont observés avant les validations économiques :

```text
equal key   → SPOT_FILL_REAPPLICATION
smaller key → SPOT_FILL_OUT_OF_ORDER
```

## Exécutions finales

```text
nix develop --command pytest tests/hypotheses/H0004 -q
→ 24 passed in 0.14s

nix develop --command just check
→ Ruff OK
→ 159 passed
→ couverture globale 91,77 %
→ spot_ledger.py 100 %

nix develop --command python -m tests.hypotheses.H0004.run_experiment \
  --output docs/fusion/hypotheses/H0004/RESULT.json
sha256sum docs/fusion/hypotheses/H0004/RESULT.json
→ cb6582a112e577b0508c39f15c2c2dc5107af7a11bd9124d6a76db3051402594
```

`RESULT.json` enregistre lui-même le HEAD exécuté `4bd8e1f5da366baaf2d8de6702bcf51b663b24db`.

## Verdict Producteur

```text
H0004 = PASS_PENDING_INDEPENDENT_REVIEW
P1 = NOT_PASSED
canonical_short_model = NOT_PROVEN_BY_H0004
temporal_enforcement = NOT_PROVEN
integrated_P1_proof = NOT_PROVEN
```

Ce verdict ne ferme pas H0004 et ne fusionne aucune branche.
