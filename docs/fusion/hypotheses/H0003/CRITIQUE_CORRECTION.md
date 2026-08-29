# H0003 — Revue Critique indépendante du paquet corrigé

## Verdict figé

**`ACCEPT_WITH_LIMITS`**

Les contre-exemples admis C4, F1 et F2 sont fermés mécaniquement dans le paquet corrigé.
Les corrections R1–R3 restent dans le scope autorisé, les preuves antérieures M1–M11 et
les vecteurs canoniques demeurent valides, et aucune nouvelle réfutation H0003 n'a été
trouvée. Les limites publiées restent la note `unicodedata`, la portée étroite du socle de
contrats et l'absence de toute preuve intégrée P1.

Ce verdict ne déclare ni H0003 admise/validée, ni `P1 PASS`.

## Identité, révision et indépendance

| Champ | Valeur |
|---|---|
| Rôle | `IA_CRITIQUE_INDEPENDANTE` |
| Agent | `OpenAI Codex` |
| Version du modèle | `UNKNOWN` |
| Date | `2026-08-29` (`America/Toronto`) |
| Branche | `hypothesis/H0003-canonical-contract-foundation` |
| Paquet corrigé gelé | `d3134e63362693b4ca47d61229d1307edf7daca5` |
| Manifeste final corrigé | `5d883f107c1e26bfc44575829d4b34fff5c7aff7` |
| Code Producteur corrigé | `729a138a6db010ac320ff9d056e9591f336f8575` |
| Paquet rejeté historique | `44893b0061f13e8a03c4a27f4d299b8b65b5943c` |
| Rapports rejetants historiques | `04a5a1f5ac7b957f174beccf7ab95a1b1631417c` |
| Décision humaine de correction | `426781eecb86219b306d20db68ee81a978183ff6` |
| Indépendance | `PROCEDURAL / ROLE-SEPARATED` |

Cette indépendance qualifie une séparation de rôle et de nouvelle session. Elle ne
revendique ni IV&V organisationnelle, ni indépendance statistique ou d'auteur, ni
réplication externe. Les anciens rapports étaient un contexte historique obligatoire. Le
nouveau `CONTRADICTOIRE_CORRECTION.md` n'a été ni ouvert, ni lu, ni modifié.

## Mandat et fichiers examinés

Le mandat suivi est `CORRECTION_REVIEW_REQUEST.md` : reproduire exactement C4/F1/F2,
vérifier R1–R3, M1–M11, provenance, hashes, résultat et non-régression, puis chercher de
nouvelles réfutations aux frontières de types et validations relationnelles.

Fichiers lus intégralement ou inspectés pour leur contenu pertinent :

- `CORRECTION_REVIEW_REQUEST.md`;
- anciens `CRITIQUE.md` et `CONTRADICTOIRE.md`;
- `HUMAN_REJECTION_DECISION.md`;
- `HYPOTHESIS.md`, `ORACLE_VECTORS.json`, `EVIDENCE.md`, `MANIFEST.json`;
- `RESULT.json` et `RESULT_REJECTED_44893B0.json`;
- `H0003_PROTOCOL_OBSERVATIONS.md`;
- `P1_MINIMAL_EXECUTABLE_PROFILE.md` et `P1_CANONICAL_CONTRACT_DECISIONS.md`;
- `paper_trading_codex/domain/contracts.py`, `domain/__init__.py` et contrôle de
  non-modification du ledger;
- tests H0003 et runner corrigé;
- historique et différences Git de la chaîne complète.

## Provenance et gel

La filiation suivante est linéaire et chaque arc a été vérifié par
`git merge-base --is-ancestor` :

```text
44893b0 → 04a5a1f → 426781e → 34dc2b7
        → 729a138 → f2455f9 → 5d883f1 → d3134e6
```

- `04a5a1f` conserve les deux rapports `REJECT` historiques;
- `426781e` admet humainement C4/F1/F2 et borne R1–R3;
- `34dc2b7` modifie uniquement les frontières de contrats et l'export requis;
- `729a138` ajoute les régressions permanentes et le runner corrigé;
- `f2455f9` enregistre les preuves;
- `5d883f1` finalise le manifeste;
- `d3134e6` gèle l'enveloppe et le mandat de nouvelle revue.

L'hypothèse, B1–B8/B5a et les vecteurs oracle sont inchangés depuis le paquet rejeté. Le
ledger n'est pas modifié. Le résultat historique rejeté est conservé sous un nouveau nom,
avec ses bytes et son SHA-256 originaux.

## R1 — scalaires temporels

`InstantNs` et `DurationNs` sont maintenant des sous-classes immuables de `int` dont
`__new__` impose exactement `type(value) is int`. Les contre-exemples exacts et leurs
extensions produisent :

```text
InstantNs("not-an-int")     → INSTANT_NS_TYPE_INVALID
InstantNs(True)             → INSTANT_NS_TYPE_INVALID
InstantNs(0.1)              → INSTANT_NS_TYPE_INVALID
InstantNs(datetime(...))    → INSTANT_NS_TYPE_INVALID
DurationNs("not-an-int")    → DURATION_NS_TYPE_INVALID
DurationNs(True)            → DURATION_NS_TYPE_INVALID
DurationNs(0.1)             → DURATION_NS_TYPE_INVALID
DurationNs(datetime(...))   → DURATION_NS_TYPE_INVALID
```

Les trois contrats événementiels convertissent un `int` exact en `InstantNs` et rejettent
les autres types à la frontière commune. Aucune source temporelle ou implémentation système
de `Clock` n'est ajoutée. C4 est **fermée**.

## R2 — frontière rationnelle exacte

La fonction commune `_exact_fraction` accepte seulement les types exacts `int` et
`Fraction`. Elle est appelée par `rational_text` et par tous les champs rationnels publics
d'`InstrumentSpec`, `MarketEvent`, `Fill` et `AccountEvent`.

Les contre-exemples exacts produisent tous `RATIONAL_VALUE_TYPE_INVALID` :

```text
contract_multiplier=True
Fill.quantity=0.1
Fill.price=100.005
Fill.fee_amount=False
```

Des sondes supplémentaires confirment le même rejet pour `tick_size=0.01`,
`lot_size=False`, `MarketEvent.price=100.005` et `AccountEvent.delta=0.1`. Le noyau ne
convertit donc plus implicitement `bool` ou binary64. Un appelant peut fournir une
`Fraction` déjà exacte; cette règle correspond précisément à la décision humaine R2 et
n'ajoute pas de convention numérique. F1 est **fermée**.

## R3 — compatibilité de `MarketEvent`

Le nouveau port pur `validate_market_event_compatibility(event, instrument)` est exporté
et applique :

```text
event.instrument_id == instrument.instrument_id
event.price % instrument.tick_size == 0
```

Les résultats sont :

```text
instrument_id divergent → MARKET_EVENT_INSTRUMENT_INCOMPATIBLE
price = 20001/200 avec tick 1/100 → PRICE_OFF_GRID
```

Le cas valide passe. Le validateur n'ajoute ni référentiel implicite, ni conversion,
arrondi, ledger ou provider. Il matérialise seulement B1 et l'identité instrument déjà
normative. F2 est **fermée**.

## R1–R3 : contrôle de scope

La différence de production par rapport à `44893b0` est limitée à :

- remplacer deux `NewType` par deux scalaires entiers validés;
- centraliser la validation des rationnels exacts;
- ajouter et exporter le validateur relationnel du prix marché.

Aucun changement n'est présent dans l'hypothèse, les décisions B1–B8/B5a, les vecteurs,
le ledger, le replay, la stratégie ou un provider. Les corrections ne créent donc aucune
capacité hors scope et n'introduisent aucune nouvelle convention silencieuse.

## M1–M11, bytes, ordre et déduplication

Les 39 tests ciblés passent. Les onze familles historiques restent exercées :

- M1–M3 : multiplicateur/grilles/devises;
- M4 : normalisation et rejet rationnel non canonique;
- M5 : identité et hash de référence incompatibles;
- M6 : séquence absente;
- M7 : doublon idempotent ou divergent;
- M8–M9 : frais, devise et signe/kind;
- M10 : ordre de construction sans effet sur bytes/hash;
- M11 : cinq round-trips bit-identiques.

Les bytes UTF-8 NFC, échappements, clés triées, absence de BOM/newline, hashes et cinq
objets canoniques sont inchangés. Les contrôles additionnels sur grilles, compte/devise,
ordre inter-types, surrogate Unicode et collision de clés NFC restent verts.

## Hashes, résultat et reproductibilité

Les SHA-256 recalculés concordent avec le manifeste, notamment :

```text
contracts.py                    a9a27f6e991d13d69326dd6cb2b50c64dc38d6360952eec21f272ab7fff39491
domain/__init__.py              2f55abd4d9fe534d6f738e462e98ffc6de8127611d51df8e633e48d3f8353d85
tests                           f4a1a349989d6f7b1c68f267f1d7b3b067f18f7cba394fd80f58cf20c3a3351d
runner                          75d3b7eba368dbc4b51f17835800842c37f845aab66200417c3d4f891b7b5657
RESULT.json                     7acb225a68c0d77ba4ed42dd3f435e1bc93ee24d1a32a66b22fc593c01ef5dd2
RESULT_REJECTED_44893B0.json    f13814dee86a98d75c28b6dc697f29d8b1185208501bd46996f47376abe7c87d
```

Le runner exécuté depuis un clone détaché au commit `729a138` reproduit le nouveau résultat
octet pour octet et enregistre les sept régressions à `true`.

Commandes et résultats :

```text
nix develop --command pytest tests/hypotheses/H0003 -q
→ 39 passed in 0.09s; code 0

# clone détaché à 729a138
nix develop --command python -m tests.hypotheses.H0003.run_experiment \
  --output /tmp/h0003-correction-result.json
→ SHA-256 7acb225a…ef5dd2; aucune différence avec RESULT.json; code 0

# clone détaché à d3134e6
nix develop --command just check
→ Ruff OK; 135 passed; couverture globale 90.97 %;
  contracts.py 95 %; ledger.py 100 %; code 0

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current; code 0
```

## Recherche de nouvelles réfutations

| ID | Statut | Impact | Scope | Constat |
|---|---|---|---|---|
| RC1 | `CLOSED` | `SUPPORTING` | `R1 / C4` | Les scalaires temporels rejettent les quatre classes incompatibles exigées avec codes stables. |
| RC2 | `CLOSED` | `SUPPORTING` | `R2 / F1` | Toutes les frontières rationnelles publiques partagent le rejet exact des bool/binary64. |
| RC3 | `CLOSED` | `SUPPORTING` | `R3 / F2` | Identité instrument et prix événement hors tick sont mécaniquement vérifiés. |
| RC4 | `CONFIRMED` | `SUPPORTING` | `H0003` | M1–M11, vecteurs, round-trips, ordre et déduplication restent valides. |
| RC5 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `H0003` | `Clock` reste volontairement un port structurel sans source ni validation runtime de l'implémentation; l'enforcement est hors scope. |
| RC6 | `OPEN_TOOLING_NOTE` | `NON_BLOCKING_FOR_H0003` | `P1_CLOCK_ENFORCEMENT` | `unicodedata` reste absent de l'allowlist P1 v1; décision obligatoire avant l'enforcement/P1 PASS. |
| RC7 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `P1` | Aucun ledger spot/short canonique intégré, enforcement temporel, replay ou fidélité exchange n'est prouvé. |
| RC8 | `MANIFEST_NOTE` | `NON_BLOCKING` | `PROVENANCE` | Quelques commits correctifs sont abrégés dans le manifeste, mais ils sont non ambigus dans le dépôt et le mandat fournit les ancres complètes principales. |

Tentatives additionnelles sans réfutation : invalidités temporelles sur les deux types,
bool/binary64 sur tous les groupes de champs rationnels, instrument marché divergent, prix
hors tick, invariance des hashes existants, mélange inter-types, doublons, ordre local,
surrogates, collisions NFC, devises Fill/Reference/Account et champs JSON exacts.

## Note `unicodedata`

La classification demeure exacte :

```text
status = OPEN_TOOLING_NOTE
impact_on_H0003 = NON_BLOCKING
scope = P1_CLOCK_ENFORCEMENT
impact_before_P1_PASS = BLOCKING_UNTIL_ALLOWLIST_DECISION
```

La correction ne modifie ni cette dépendance ni l'allowlist. Elle ne contamine donc pas le
résultat H0003 corrigé, mais interdit toujours toute extrapolation vers `P1 PASS` avant
décision et preuve d'enforcement.

## Conclusion

**`ACCEPT_WITH_LIMITS`**

Le paquet corrigé ferme les trois findings humains sans altérer les conventions
préenregistrées ni les preuves canoniques existantes. Les limites RC5–RC8 restent publiées
et non contaminantes pour H0003. L'admission éventuelle appartient à l'opérateur humain;
elle ne découle pas de ce rapport.
