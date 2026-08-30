# P1 — Décision humaine sur le multiplicateur spot H0004

## Autorité

```text
decision_authority = HUMAN
finding = F2 SPOT_CONTRACT_MULTIPLIER_SEMANTICS_DIVERGED
rejected_packet = 5967ee06f85bb4b52e0e3bb6fafb19b2856d63db
implementation_started_for_correction = false
effect_on_H0004 = AUTHORIZED_BOUNDED_CORRECTION
effect_on_P1 = NOT_PASSED
```

## Décision

Le sous-profil comptable minimal H0004 est borné à :

```text
SPOT_CASH_V1.contract_multiplier = 1/1 ONLY
```

Un `InstrumentSpec` de type `SPOT` dont `contract_multiplier != 1/1` reste structurellement
constructible selon H0003, mais il est hors du sous-profil H0004 et doit être rejeté avec :

```text
SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED
```

La formule H0004 reste exactement :

```text
trade_quote = quantity × price
```

H0004 n'est pas généralisée à `quantity × price × contract_multiplier`. Cette décision ne
modifie ni H0003 ni la sémantique future d'autres modèles; elle borne seulement
`SPOT_CASH_V1` dans le profil P1 minimal.

## Correction F1 autorisée sans nouvelle convention

L'état sérialise déjà les hashes instrument/référence. Avant toute transition, le
Producteur doit donc vérifier les liaisons disponibles :

```text
state.instrument_spec_sha256 == instrument.canonical_sha256()
otherwise → SPOT_STATE_INSTRUMENT_MISMATCH

state.reference_spec_sha256 == reference.canonical_sha256()
otherwise → SPOT_STATE_REFERENCE_MISMATCH
```

`apply_initialization`, qui ne reçoit pas de `ReferenceSpec` et ne l'utilise pas, vérifie
la liaison instrument disponible sans changer son API. `apply_fill` vérifie les deux
liaisons avant toute validation économique ou mutation.

**Statut : `RESOLVED_FOR_BOUNDED_CORRECTION`.**
