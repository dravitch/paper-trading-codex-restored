# H0004 — Conservation comptable d'un compte spot cash canonique

## Préenregistrement

| Champ | Valeur |
|---|---|
| hypothèse | `H0004` |
| gate | P1 |
| branche | `hypothesis/H0004-minimal-spot-ledger` |
| commit de base documentaire | `9c3b758547c332c1721aa13c17f51ba3c772f46f` |
| dépendance admise | H0003 corrigée, admission `6313afc` |
| code H0004 lors de cet énoncé | aucun |
| statut | `BLOCKED_SPEC_AMBIGUITY` |
| P1 | `NOT_PASSED` |

## Énoncé candidat

> À partir d'un `InstrumentSpec`, d'un `ReferenceSpec` et de `Fill` canoniques conformes
> à H0003, un `SpotAccountModel / SPOT_CASH_V1` minimal peut appliquer des achats et
> ventes spot sans dette ni marge, produire des `AccountEvent` qui expliquent exactement
> chaque variation de balance, conserver les balances base/quote et leur valorisation
> rationnelle, et rejeter mécaniquement toute opération incompatible avec le profil P1,
> sans convention comptable supplémentaire.

## Portée

H0004 couvre exclusivement un compte `SPOT_CASH_V1` mono-instrument : balances base et
quote rationnelles, fills explicites `BUY`/`SELL`, frais dans la devise autorisée,
valorisation `EVENT_PRICE`, conservation et validations relationnelles H0003.

Sont hors scope : short, borrow, dette, marge, funding, génération ou reconstruction de
fill, stratégie, replay/scheduler, provider, slippage, carnet, multi-instrument,
multi-devise et enforcement temporel. Les instants sont fournis par les événements; le
ledger n'en crée aucun.

## Ancres normatives suffisantes

Les éléments suivants sont fermés avant code :

- types, bytes et validations de `InstrumentSpec`, `ReferenceSpec`, `Fill` et
  `AccountEvent` par H0003;
- transitions spot du profil P1 :

```text
BUY:
  base_delta  = +q
  quote_delta = -(q × p + f)

SELL:
  base_delta  = -q
  quote_delta = +(q × p - f)
```

- trois écritures distinctes par fill : mouvement BASE, mouvement QUOTE hors frais et
  FEE QUOTE;
- conservation `new_balance = old_balance + Σ AccountEvent.delta`;
- valorisation pure `equity_quote = quote_balance + base_balance × valuation_price`;
- absence de dette : quote insuffisant au BUY et base insuffisante au SELL sont rejetés.

Le scénario et les attendus rationnels déterminés par ces règles sont gelés dans
`SCENARIO.json` et `ORACLE_EXPECTATIONS.json`. L'oracle numérique n'utilise aucun futur
code de ledger.

## Ambiguïtés bloquantes découvertes

Ces décisions changent les bytes, l'ordre, l'idempotence ou l'état observable. Elles ne
peuvent pas être inventées par l'implémentation.

| ID | Ambiguïté exécutable | Pourquoi elle bloque |
|---|---|---|
| S1 | identité déterministe des trois `AccountEvent` dérivés d'un `Fill` | B4 exige `account_event_id`, mais aucune règle ne dérive les IDs BASE/QUOTE/FEE du `fill_id`; plusieurs bytes/hashes valides sont possibles |
| S2 | `source_id`, `source_event_id`, `event_time` et `sequence` des écritures produites | le rattachement au fill est intuitif mais non normatif; trois événements partageant la séquence du fill ou recevant des sous-séquences produisent des ordres locaux différents |
| S3 | représentation de l'initialisation | le profil exige un événement d'initialisation explicite sans dire s'il est appliqué par le ledger, fourni comme `AccountEvent`, ni comment ses deux balances/IDs sont formés |
| S4 | sémantique de `fees_by_currency` | le profil nomme l'état sans fixer si le cumul stocke une magnitude positive payée ou la somme signée des deltas `FEE`; les deux donnent des états différents |
| S5 | valeur initiale et mise à jour de `last_event_key` | aucune sentinelle canonique n'est fixée; P1 ne définit pas d'ordre inter-types et ne dit pas si la clé mémorisée est celle du `Fill` ou d'un `AccountEvent` produit |
| S6 | répétition d'un fill déjà appliqué | B7 définit la déduplication dans une collection explicitement validée, mais pas l'idempotence d'une API de transition stateful; réappliquer, accepter sans effet ou rejeter change la conservation |
| S7 | allocation des frais dans une autre devise autorisée | B5a autorise base, quote ou settlement, tandis que les transitions spot minimales ferment seulement des frais quote; il faut soit borner H0004 aux frais quote, soit définir la transition base/settlement |

Tant que S1–S7 ne sont pas fermées par décision humaine normative, H0004 ne peut pas
produire des `AccountEvent` byte-exacts ni un état complet unique. Aucun code n'est
autorisé.

## Oracle indépendant déjà déterminé

Pour le scénario `SPOT_ROUND_TRIP_CONSTANT_PRICE` :

```text
initial quote = 100/1 USD
initial base  = 0/1 SOL

BUY:
q × p = 999/200 × 20/1 = 999/10 USD
quote delta total = -(999/10 + 1/10) = -100/1 USD
base delta = +999/200 SOL

after BUY:
quote = 0/1 USD
base = 999/200 SOL
equity @20 = 0/1 + 999/200 × 20/1 = 999/10 USD

SELL:
trade quote = +999/10 USD
fee quote = -999/10000 USD
base delta = -999/200 SOL

final:
base = 0/1 SOL
quote = 999/10 - 999/10000 = 998001/10000 USD
```

Ces valeurs sont uniques. Les champs dépendant de S1–S7 sont explicitement marqués
`UNRESOLVED_SPEC` dans les attendus plutôt que complétés arbitrairement.

## Réfutations préenregistrées

Après levée du blocage, H0004 devra rejeter avec invariant/code stable :

| ID | Contre-exemple |
|---|---|
| M1 | BUY avec quote insuffisant |
| M2 | SELL supérieur au base disponible |
| M3 | frais négatif ou devise de frais incompatible |
| M4 | fill hors tick ou lot |
| M5 | instrument ou `ReferenceSpec` incompatible |
| M6 | omission ou double comptage d'un `AccountEvent` |
| M7 | signe incorrect d'une écriture BASE/QUOTE/FEE |
| M8 | valorisation mutant les balances |
| M9 | fill dupliqué identique ou divergent traité contrairement à S6 |
| M10 | mélange avec `ISOLATED_LINEAR_SHORT_EDU_V1` |
| M11 | mouvement de balance non expliqué par la somme des `AccountEvent` |

Un crash générique ne compte pas comme détection.

## Condition de soutien futur

H0004 pourra seulement soutenir `PASS_PENDING_INDEPENDENT_REVIEW` si l'oracle rationnel
indépendant égale le ledger, si chaque variation est expliquée exactement, si la
valorisation est pure, si M1–M11 sont détectés, si aucun solde négatif n'est accepté, si
toutes les validations relationnelles H0003 sont appelées et si aucune convention P1
nouvelle n'apparaît pendant le code.

Même alors, H0004 ne signifiera ni `P1 PASS`, ni modèle short conforme, ni enforcement
temporel démontré.

## Condition d'arrêt atteinte

```text
implementation_started = false
scenario_frozen = true
numeric_oracle_frozen = true
S1-S7 = UNRESOLVED_SPEC
H0004 = BLOCKED_SPEC_AMBIGUITY
P1 = NOT_PASSED
```

La prochaine opération autorisée est une décision normative humaine S1–S7, enregistrée
séparément. Il ne faut lancer ni code ni revues Critique/Contradictoire sur ce paquet
bloqué.
