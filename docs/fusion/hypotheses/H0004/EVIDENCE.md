# H0004 — Preuves Producteur du paquet corrigé

## Historique préservé

Le paquet Producteur `5967ee0` reste rejeté. Ses artefacts sont conservés sans
réécriture sous les noms `*_REJECTED_5967EE0` :

```text
RESULT    cb6582a112e577b0508c39f15c2c2dc5107af7a11bd9124d6a76db3051402594
MANIFEST  707deeb0f747396118bb48d1320fcce8ad31a368cd049bd54613c056f4eed2e1
EVIDENCE  be02c2761a13e836d647fc05ddd8c3d9c1f67a6e15ae923c66e56c66763bf63d
```

Les deux rapports `REJECT` sont figés à `6f12875`. La décision humaine `830c0c0`
admet F1 et F2 comme réfutations du premier candidat. La décision normative
`f2d45c9` borne ensuite `SPOT_CASH_V1` à `contract_multiplier = 1/1`.

## Corrections bornées

Le commit `2e34736` ferme uniquement les findings admis :

```text
F1a  hash InstrumentSpec de l'état != spec fournie
     → SPOT_STATE_INSTRUMENT_MISMATCH

F1b  hash ReferenceSpec de l'état != spec fournie
     → SPOT_STATE_REFERENCE_MISMATCH

F2   InstrumentSpec SPOT avec contract_multiplier != 1/1
     → SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED
```

Les liaisons disponibles sont contrôlées avant toute mutation comptable.
`apply_initialization` contrôle l'instrument sans modifier son API. `apply_fill`
contrôle instrument et référence. La formule reste celle préenregistrée :

```text
trade_quote = quantity × price
```

Les contre-exemples exacts des reviewers sont des régressions permanentes. Les
rejets laissent l'état d'entrée inchangé.

## Non-régression nominale

Le scénario et l'oracle préenregistrés sont inchangés. Le résultat corrigé conserve :

```text
after BUY:
  base  = 999/200 SOL
  quote = 0/1 USD
  fees  = 1/10 USD

after SELL:
  base  = 0/1 SOL
  quote = 998001/10000 USD
  fees  = 1999/10000 USD
```

Les six `AccountEvent`, leurs identités, S8, la conservation et les valorisations
restent exactement égaux aux attendus gelés. Le premier run historique `ffed088`
n'est ni remplacé ni présenté comme un run du candidat corrigé.

## Exécutions corrigées

```text
nix develop --command pytest tests/hypotheses/H0004 -q
→ 28 passed

nix develop --command just check
→ Ruff OK
→ 163 passed
→ couverture globale 91,81 %
→ spot_ledger.py 100 %

nix develop --command python -m tests.hypotheses.H0004.run_experiment \
  --output docs/fusion/hypotheses/H0004/RESULT.json
sha256sum docs/fusion/hypotheses/H0004/RESULT.json
→ 65adcc700a8021010c6e8a70121b54216c44f1dd11b2b7c63d5786330e780c72
```

Le runner `419fe9d` exécute lui-même F1a, F1b et F2, en plus de la comparaison
oracle/ledger. `RESULT.json` enregistre le HEAD exécuté
`e5f87b3b7567be048d7c77479e3c96339dcaa56e`.

## Verdict Producteur corrigé

```text
H0004 = PASS_PENDING_INDEPENDENT_REVIEW
first packet 5967ee0 = REJECTED
P1 = NOT_PASSED
canonical_short_model = NOT_PROVEN_BY_H0004
temporal_enforcement = NOT_PROVEN
integrated_P1_proof = NOT_PROVEN
```

Ce verdict n'admet pas H0004 et ne réhabilite pas le premier paquet.
