# H0003 — Evidence Producteur

## Antériorité

```text
ed2731d  préenregistrement BLOCKED_SPEC_AMBIGUITY, aucun code
0fe5610  décision humaine B1–B8, aucun code
0e105c2  vecteurs oracle gelés, aucun code
d817a16  addendum humain B5a, aucun code
be6678a  préenregistrement aligné READY_FOR_IMPLEMENTATION, aucun code
5676de8  première implémentation et M1–M11
9a8f318  gardes Unicode normatives finales
```

Les deux incohérences pré-code ont été fermées avant `5676de8` : clé locale générique par
`object_id` et compatibilité de `Fill.fee_currency`. Aucun ledger, replay, provider ou
enforcement AST n'a été introduit.

## Contrats matérialisés

- `InstrumentSpec` et `ReferenceSpec`, avec compatibilité identité + hash;
- `InstantNs`, `DurationNs` et port pur `Clock`;
- `MarketEvent`, `Fill` et `AccountEvent`;
- rationnels canoniques, JSON NFC bit-exact et SHA-256;
- ordre local et déduplication dans une collection explicite;
- compatibilités devise/instrument/référentiel et `REJECT_OFF_GRID`.

## Exécution ciblée

Commande finale :

```text
nix develop --command pytest tests/hypotheses/H0003 -q
→ 29 passed in 0.08s
```

Les tests couvrent les vecteurs préenregistrés, le round-trip des cinq contrats et M1–M11.
Les rejets utilisent des codes stables, notamment :

| Mutation | Rejet observé |
|---|---|
| M1 multiplicateur non positif | `CONTRACT_MULTIPLIER_NOT_POSITIVE` |
| M2 tick/lot non positif | `TICK_SIZE_NOT_POSITIVE` / `LOT_SIZE_NOT_POSITIVE` |
| M3 devise absente/incompatible | `CURRENCY_REQUIRED`, `REFERENCE_FEE_CURRENCY_INCOMPATIBLE`, `FILL_FEE_CURRENCY_INCOMPATIBLE` |
| M4 rationnel non canonique | `RATIONAL_TEXT_NON_CANONICAL` |
| M5 référentiel incompatible | `REFERENCE_INSTRUMENT_ID_MISMATCH` / `REFERENCE_INSTRUMENT_HASH_MISMATCH` |
| M6 séquence absente | `CONTRACT_FIELDS_INVALID` |
| M7 doublon divergent | `DUPLICATE_DIVERGENT` |
| M8 frais négatif/sans devise | `FEE_NEGATIVE` / `CURRENCY_REQUIRED` |
| M9 signe/kind incohérent | `ACCOUNT_EVENT_SIGN_MISMATCH` |
| M10 ordre de construction | bytes et hash inchangés |
| M11 round-trip | bytes et hash inchangés pour les cinq contrats |

Les contrôles additionnels rejettent grille prix/quantité incompatible, compte/devise
incompatible, ordre inter-types, surrogate Unicode et collision de clés après NFC.

## Échec intermédiaire conservé

Le premier test du garde surrogate a échoué : `_normalize_json` normalisait les valeurs
string directement et laissait `UnicodeEncodeError` sortir au lieu du code stable attendu.
La correction `9a8f318` route toutes les chaînes par le même validateur. Le test final
rejette le surrogate avec `UNICODE_SURROGATE_INVALID` et les collisions NFC avec
`CANONICAL_JSON_DUPLICATE_KEY`.

Cette correction implémente une règle canonique déjà normative; elle n'ajoute aucune
convention H0003.

## Résultat matérialisé

```text
nix develop --command python -m tests.hypotheses.H0003.run_experiment \
  --output docs/fusion/hypotheses/H0003/RESULT.json
sha256sum docs/fusion/hypotheses/H0003/RESULT.json
→ f13814dee86a98d75c28b6dc697f29d8b1185208501bd46996f47376abe7c87d
```

`RESULT.json` référence le code exécuté
`9a8f318c60e82d97eff74a3fb36f532780a718bf`. Les cinq JSON/hashes et les cinq
round-trips concordent exactement.

## Non-régression globale

```text
nix develop --command just check
→ Ruff OK
→ 125 passed
→ couverture globale 90,92 %
→ contracts.py 95 %
→ ledger.py 100 %

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current
```

## Note de scope sur l'allowlist temporelle

`contracts.py` utilise `unicodedata` pour appliquer NFC. L'allowlist P1 v1 documentée ne
contient pas encore ce module. H0003 exclut explicitement l'enforcement AST et démontre la
sérialisation canonique; cette dépendance ne contamine donc pas son résultat.

Classification :

```text
status = OPEN_TOOLING_NOTE
impact_on_H0003 = NON_BLOCKING
scope = P1_CLOCK_ENFORCEMENT
impact_before_P1_PASS = BLOCKING_UNTIL_ALLOWLIST_DECISION
```

Cette note doit rester publiée. Elle n'autorise ni ajout silencieux à l'allowlist ni
réouverture du résultat comptable H0001/H0002.

## Verdict Producteur

```text
H0003 = PASS_PENDING_INDEPENDENT_REVIEW
P1 = NOT_PASSED
spot_ledger = NOT_PROVEN
short_ledger_P1_conformance = NOT_PROVEN
clock_enforcement = NOT_PROVEN
replay = NOT_PROVEN
exchange_fidelity = NOT_PROVEN
```
