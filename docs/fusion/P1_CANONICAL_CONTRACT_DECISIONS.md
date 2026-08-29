# Décision humaine — contrats canoniques P1, B1–B8

## Autorité et portée

| Champ | Valeur |
|---|---|
| `decision_authority` | `HUMAN` |
| `decision_date` | `2026-08-29` (`America/Toronto`) |
| `scope` | fermeture normative B1–B8 avant code H0003 |
| `supersedes_ambiguities_detected_at` | `ed2731da82326cf938b3634670e7cd1f6e50445f` |
| `implementation_started` | `false` |
| `effect_on_H0003` | autorise un nouveau préenregistrement, pas l'implémentation directe |
| `effect_on_P1` | `NOT_PASSED` |

Cette décision ferme les représentations minimales nécessaires à H0003. Elle n'ajoute ni
ledger, ni replay, ni stratégie, ni provider, ni enforcement temporel AST. Elle ne modifie
pas rétroactivement le préenregistrement bloqué `ed2731d`.

## B1 — Instrument et arrondi

```text
instrument_type = {SPOT, LINEAR_PERPETUAL}
rounding_policy = {REJECT_OFF_GRID}
```

`REJECT_OFF_GRID` n'arrondit jamais. Toute quantité hors `lot_size` ou tout prix hors
`tick_size` est rejeté. Le multiplicateur, le tick et le lot sont strictement positifs.

**Statut : `RESOLVED`.**

## B2 — Prix de valorisation

```text
valuation_price = {EVENT_PRICE}
```

La valorisation P1 reçoit un prix explicitement porté par l'événement. `LAST`, `CLOSE`,
`MARK`, `MID`, `INDEX` et toute autre source implicite sont hors du profil minimal.

**Statut : `RESOLVED`.**

## B3 — Vocabulaires d'événements

```text
MarketEvent.event_type = {PRICE}
Fill.side = {BUY, SELL}
Fill.liquidity_role = {MAKER, TAKER}
AccountEvent.kind = {INITIALIZE, TRADE, FEE, REALIZED_PNL}
account_model = {SPOT_CASH_V1, ISOLATED_LINEAR_SHORT_EDU_V1}
```

Le niveau de fidélité reste le vocabulaire déjà documenté `{F0,F1,F2,F3,F4}`. Tout token
hors de ces ensembles est rejeté; aucun alias n'est accepté.

**Statut : `RESOLVED`.**

## B4 — Forme fermée d'`AccountEvent`

`AccountEvent` porte exactement :

```text
account_event_id
source_id
source_event_id
account_model
instrument_id
kind
account
delta
currency
event_time
sequence
```

avec :

```text
account = {BASE, QUOTE, COLLATERAL}
delta = rationnel signé canonique
```

La devise autorisée dépend exactement de l'`InstrumentSpec` :

```text
BASE       → InstrumentSpec.base
QUOTE      → InstrumentSpec.quote
COLLATERAL → InstrumentSpec.settlement
```

`kind` décrit la cause et `account` la balance affectée. La validation de contrat applique
seulement les signes indépendants d'un futur ledger :

```text
INITIALIZE   → delta >= 0
FEE          → delta <= 0
TRADE        → delta signé; cohérence économique vérifiée plus tard avec le Fill source
REALIZED_PNL → delta signé
```

Un événement `FEE` positif ou `INITIALIZE` négatif est `ACCOUNT_EVENT_SIGN_MISMATCH`.
Aucun enum combinatoire par produit/opération n'est créé.

**Statut : `RESOLVED`.**

## B5 — Compatibilité instrument/référentiel

`ReferenceSpec` ajoute exactement :

```text
instrument_id
instrument_spec_sha256
```

La compatibilité exige simultanément :

```text
ReferenceSpec.instrument_id == InstrumentSpec.instrument_id
ReferenceSpec.instrument_spec_sha256 == sha256(canonical_bytes(InstrumentSpec))
```

Le symbole seul, un alias ou un seul des deux champs ne suffit pas.

Le token sérialisé de la politique numérique déjà fermée par le profil est
`EXACT_RATIONAL`; le token de l'arrondi est `REJECT_OFF_GRID`.

**Statut : `RESOLVED`.**

## B6 — Ordre local par type

La clé locale est :

```text
(event_time, sequence, source_id, object_id)
```

avec :

```text
MarketEvent → object_id = event_id
Fill        → object_id = fill_id
AccountEvent→ object_id = account_event_id
```

`source_id` est obligatoire sur les trois types. `sequence` est obligatoire et entière.
P1 ne définit aucun ordre total inter-types; le scheduler et l'entrelacement relèvent de
P2.

**Statut : `RESOLVED`.**

## B5a — Compatibilité de la devise des frais

Addendum humain du 2026-08-29, postérieur aux vecteurs H0003-v2 et antérieur à toute
implémentation :

```text
Fill.fee_currency == ReferenceSpec.fee_settlement_currency

ReferenceSpec.fee_settlement_currency ∈ {
  InstrumentSpec.base,
  InstrumentSpec.quote,
  InstrumentSpec.settlement
}
```

Les comparaisons sont des égalités exactes de tokens de devise. Aucune conversion, alias ou
devise implicite n'est autorisé. Une absence produit `CURRENCY_REQUIRED`; une devise du
référentiel hors de l'instrument produit `REFERENCE_FEE_CURRENCY_INCOMPATIBLE`; une devise
du fill différente du référentiel produit `FILL_FEE_CURRENCY_INCOMPATIBLE`.

**Statut : `RESOLVED`.**

## B7 — Doublons divergents

L'identité d'un objet est :

```text
(type, source_id, object_id)
```

Dans une collection passée explicitement au validateur :

- même identité + mêmes bytes canoniques → doublon idempotent accepté puis dédupliqué;
- même identité + bytes canoniques différents → `DUPLICATE_DIVERGENT`;
- aucune mémoire, registre global, singleton ou état caché n'est autorisé.

Le résultat dédupliqué est ordonné par la clé locale B6 à l'intérieur d'un type. Il n'est
jamais trié conjointement avec un autre type.

**Statut : `RESOLVED`.**

## B8 — Rationnel JSON canonique

Tout rationnel est une chaîne ASCII :

```text
"numerator/denominator"
```

Règles fermées :

- fraction irréductible;
- dénominateur strictement positif;
- numérateur signé en base 10, sans `+` ni zéro initial;
- zéro unique `"0/1"`;
- entier `n` rendu `"n/1"`;
- `-0/1`, entier nu, décimal, exposant et dénominateur négatif rejetés;
- une valeur construite comme `2/4` est normalisée avant sérialisation en `"1/2"`.

Vecteurs minimaux requis avant code :

```text
2      → "2/1"
1/2    → "1/2"
2/4    → "1/2"
-1/2   → "-1/2"
0      → "0/1"
```

La sérialisation objet suit le JSON canonique existant : NFC, tri récursif des clés,
séparateurs sans espaces, échappements uniques, UTF-8 sans BOM ni fin de ligne.

**Statut : `RESOLVED`.**

## Décision synthétique

```text
B1 = RESOLVED
B2 = RESOLVED
B3 = RESOLVED
B4 = RESOLVED
B5 = RESOLVED
B6 = RESOLVED
B7 = RESOLVED
B8 = RESOLVED
B5a = RESOLVED
implementation_started = false
H0003 = AUTHORIZED_FOR_REPREREGISTRATION_ONLY
P1 = NOT_PASSED
```

La prochaine étape est un nouveau préenregistrement H0003 citant le commit de cette
décision et gelant les vecteurs bytes/SHA-256. Aucune revue Critique/Contradictoire n'est
requise entre cette décision humaine et ce nouveau préenregistrement.
