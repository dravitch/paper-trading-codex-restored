# H0004 — Revue Critique indépendante

## Verdict figé

**`REJECT`**

Le scénario préenregistré, les six écritures, M1–M19, le premier run et le résultat final
sont reproductibles. Deux contre-exemples nouveaux réfutent toutefois le cœur du compte
mono-instrument canonique : les transitions ne lient pas les specs fournies aux hashes de
l'état, et la formule spot implémentée ajoute silencieusement `contract_multiplier` alors
que la transition normative H0004 est `q × p`.

Ce verdict ne déclare ni H0004 admise/validée, ni `P1 PASS`.

## Identité, révision et indépendance

| Champ | Valeur |
|---|---|
| Rôle | `IA_CRITIQUE_INDEPENDANTE` |
| Agent | `OpenAI Codex` |
| Version du modèle | `UNKNOWN` |
| Date | `2026-08-30` (`America/Toronto`) |
| Branche | `hypothesis/H0004-minimal-spot-ledger` |
| Paquet gelé | `5967ee06f85bb4b52e0e3bb6fafb19b2856d63db` |
| Manifeste Producteur | `b0064c0200384239372ada5c01b5efe3b8aeac7d` |
| Code Producteur | `4bd8e1f5da366baaf2d8de6702bcf51b663b24db` |
| Premier code/run | `a1374912c4eb233f64566fcc2bc8a443167179ee` |
| Indépendance | `PROCEDURAL / ROLE-SEPARATED` |

Cette qualification décrit une session et un rôle séparés. Elle ne revendique ni IV&V
organisationnelle, ni indépendance statistique, d'auteur ou de modèle, ni réplication
externe. `CONTRADICTOIRE.md` n'a été ni ouvert, ni lu, ni modifié.

## Mandat et fichiers examinés

Le mandat `REVIEW_REQUEST.md` a été suivi : vérification du premier run, indépendance de
l'oracle, conservation, appels des validateurs H0003, S8 et priorité de rejet, M1–M19,
hashes, résultat, suite globale et recherche active de contre-exemples.

Fichiers examinés :

- `HYPOTHESIS.md`, `SCENARIO.json`, `ORACLE_EXPECTATIONS.json`;
- `FIRST_RUN.json`, `RESULT.json`, `EVIDENCE.md`, `MANIFEST.json`;
- `H0004_PROTOCOL_OBSERVATIONS.md`, `REVIEW_REQUEST.md`;
- `P1_SPOT_LEDGER_DECISIONS.md` et `P1_SPOT_LEDGER_DECISION_S8.md`;
- `P1_MINIMAL_EXECUTABLE_PROFILE.md`;
- contrats H0003, exports du domaine et `spot_ledger.py`;
- oracle, tests nominaux, tests mutants et runner H0004;
- historique et différences Git de toutes les ancres déclarées.

## Provenance et premier run

La filiation est linéaire et chaque arc a été vérifié :

```text
9c3b758 → 044406f → 8aa05bc → 56c5e54 → cef58c5
→ 3ed68c5 → f3c6811 → a137491 → ffed088 → 54f252a
→ 4bd8e1f → c24a9b9 → b0064c0 → 5967ee0
```

Les états historiques sont conservés : blocage S1–S7, décision humaine S1–S7, blocage S8,
décision humaine S8, puis troisième préenregistrement prêt avant code. L'hypothèse, les
décisions, le scénario et l'oracle figé ne changent pas après `f3c6811`.

Le premier run a été reproduit dans un clone détaché à `a137491` :

```text
nix develop --command pytest \
  tests/hypotheses/H0004/test_minimal_spot_ledger_nominal.py -q
→ 2 passed in 0.10s; code 0
```

Les SHA-256 du ledger, de l'oracle et des tests à ce commit sont exactement ceux de
`FIRST_RUN.json` :

```text
spot_ledger.py  127dc566d1957863309a264e5960ef40680cfa3de9f153fe0e02a6b63fd8e929
oracle.py       a86ffe787b03d64d80d48b367cd8824e7baf328ab7e314a62852375f681de0e9
nominal tests   890785999395452176f03407cf5e4bd2ebecb7333ae9866ac7022702da3dd3f5
```

Le commit mutant `54f252a` ajoute au ledger seulement l'appel et la fonction explicite de
validation de conservation; les formules nominales ne sont pas corrigées. Le premier run
précède donc réellement M1–M19 et passe sans correction comptable observée.

## Oracle, fractions et six `AccountEvent`

L'oracle importe seulement `Fraction` et ne dépend ni du ledger, ni des attentes figées.
Il calcule directement depuis `SCENARIO.json` :

```text
BUY notional       = 999/200 × 20 = 999/10
BUY quote total    = -(999/10 + 1/10) = -100
after BUY          = 999/200 SOL, 0 USD, fees 1/10 USD

SELL quote trade   = +999/10
SELL fee           = -999/10000
final quote        = 999/10 - 999/10000 = 998001/10000
fees total         = 1/10 + 999/10000 = 1999/10000
final base         = 0
```

Sur ce scénario, les six `AccountEvent` sont byte-sémantiquement conformes aux attentes :
IDs S1 déterministes, provenance S2 exacte, trois rôles par fill, devises et signes
corrects, ordre B6 par `account_event_id`. Pour chaque transition nominale, la variation
de balance égale la somme des deltas BASE/QUOTE. `fees_by_currency` cumule les magnitudes
positives et n'est pas ajouté à cette somme; il n'est donc pas double compté.

## Appels des validateurs, S8, tri et mémoire

Sur le chemin nominal, les appels suivants sont effectifs :

- création : `validate_instrument_reference`;
- initialisation : `validate_account_event_compatibility`;
- fill : `validate_fill_compatibility` puis validation des trois écritures dérivées;
- fin de transition : `validate_transition_conservation`.

S8 est exécutée au début d'`apply_fill`, avant modèle de compte, compatibilités, devise et
solvabilité. Les résultats observés sont :

```text
clé égale    → SPOT_FILL_REAPPLICATION
clé moindre  → SPOT_FILL_OUT_OF_ORDER
clé supérieure → poursuite de la transition
```

Le ledger ne reçoit aucune collection de fills, ne la trie pas et ne possède ni historique
d'identités, ni cache, registre, singleton ou champ caché. Le seul `sorted` de production
ordonne les trois écritures dérivées selon B6; il ne réordonne pas les inputs Fill. L'état
ne contient que les sept champs préenregistrés et conserve après chaque fill la clé de ce
fill, non celle d'une écriture dérivée.

## M1–M19 et reproductibilité finale

Les 24 tests ciblés passent et exercent les familles annoncées, y compris M18a–M18e. Le
runner final a été reproduit dans un clone détaché à `4bd8e1f`; sa sortie est identique
octet pour octet :

```text
RESULT.json SHA-256 = cb6582a112e577b0508c39f15c2c2dc5107af7a11bd9124d6a76db3051402594
```

Tous les SHA-256 du manifeste concordent : hypothèse, décisions, scénario, attentes,
premier run, ledger, exports, oracle, tests, runner, résultat, preuves, observations,
statut et environnement.

Commandes reproduites :

```text
nix develop --command pytest tests/hypotheses/H0004 -q
→ 24 passed in 0.24s; code 0

nix develop --command python -m tests.hypotheses.H0004.run_experiment \
  --output /tmp/h0004-critique-result.json
→ aucune différence avec RESULT.json; code 0

nix develop --command just check
→ Ruff OK; 159 passed; couverture globale 91.77 %;
  spot_ledger.py lignes/branches 100 %; code 0

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current; code 0
```

## F1 — specs de transition non liées à l'état

```text
status = FAIL
impact = BLOCKING_H0004
scope = MONO_INSTRUMENT_STATE_COMPATIBILITY
```

`SpotAccountState` sérialise les hashes de l'instrument et du référentiel utilisés à sa
création. Pourtant, `apply_initialization` et `apply_fill` ne vérifient jamais que les
specs reçues correspondent à ces hashes. Les validateurs H0003 sont bien appelés, mais ils
ne comparentent que l'événement/fill, l'instrument et le référentiel **du nouvel appel**;
ils n'agrègent pas ce triplet à l'état existant.

Contre-exemple exécuté :

1. créer et initialiser l'état oracle SOL/USD;
2. construire un `InstrumentSpec` BTC/USD valide, son `ReferenceSpec` au hash exact et un
   fill BTC valide de `1 BTC @ 20 USD`, frais nuls;
3. appeler `apply_fill(state_SOL, fill_BTC, instrument_BTC, reference_BTC)`.

Résultat observé, sans exception :

```text
state hashes before = SOL InstrumentSpec / SOL ReferenceSpec
derived events       = BTC-USD-SPOT, BTC-USD-SPOT, BTC-USD-SPOT
new balances         = 1 base, 80 quote
state hashes after   = toujours les hashes SOL
```

La conservation arithmétique passe parce qu'elle somme les événements BTC dans les
balances de l'état SOL. Le résultat est donc algébriquement expliqué mais sémantiquement
incompatible avec les specs sérialisées. Cela viole directement le scope mono-instrument,
la revendication de validations relationnelles et M5 au niveau de l'état. Le test M5 ne
varie que le fill ou le référentiel contre l'instrument fourni; il ne couvre pas ce
changement cohérent du triplet externe contre l'état.

Le même défaut existe à l'initialisation : un événement et un instrument étrangers mais
mutuellement compatibles peuvent modifier un état dont le hash d'instrument reste celui
d'origine.

## F2 — convention silencieuse `contract_multiplier` dans la formule spot

```text
status = FAIL
impact = BLOCKING_H0004
scope = SPOT_TRANSITION_FORMULA
```

Le profil P1 et `HYPOTHESIS.md` ferment explicitement :

```text
BUY  quote_delta = -(q × p + f)
SELL quote_delta = +(q × p - f)
```

Le code calcule au contraire :

```python
trade_quote = fill.quantity * fill.price * instrument.contract_multiplier
```

Le scénario unique masque l'écart parce que son multiplicateur vaut `1/1`. Aucun invariant
H0004 n'exige qu'un instrument `SPOT` ait un multiplicateur égal à un, et H0003 accepte
tout multiplicateur strictement positif.

Contre-exemple exécuté avec un instrument SPOT valide identique à l'oracle sauf
`contract_multiplier=2`, un référentiel au nouveau hash exact et un BUY valide
`q=1`, `p=20`, `f=0` depuis `100 USD` :

```text
attendu préenregistré q × p : base=1, quote=80
observé code q × p × 2      : base=1, quote=60
AccountEvent QUOTE TRADE    : -40 au lieu de -20
```

La conservation interne ne détecte pas ce défaut puisque l'état et l'écriture dérivée
utilisent la même formule ajoutée. L'oracle n'utilise pas le multiplicateur. Appliquer ce
champ au spot est donc une convention comptable non préenregistrée; alternativement,
restreindre SPOT à `contract_multiplier=1` serait également une nouvelle règle absente.
F2 satisfait le critère interdisant une convention P1 nouvelle pendant le code.

## Findings classés

| ID | Statut | Impact | Scope | Effet exact |
|---|---|---|---|---|
| C1 | `CONFIRMED` | `SUPPORTING` | `FIRST_RUN` | Le nominal passe avant mutants et aucune formule observée n'est corrigée ensuite. |
| C2 | `CONFIRMED` | `SUPPORTING` | `FROZEN_SCENARIO` | Oracle, états, six écritures, conservation, frais et valorisations sont exacts sur le scénario. |
| C3 | `CONFIRMED` | `SUPPORTING` | `S8` | Priorité égalité/ordre décroissant, absence de tri des fills et absence de mémoire cachée sont conformes. |
| C4 | `CONFIRMED` | `SUPPORTING` | `M1_M19` | Les mutants préenregistrés passent avec leurs codes ou invariants annoncés. |
| F1 | `FAIL` | `BLOCKING_H0004` | `MONO_INSTRUMENT_STATE_COMPATIBILITY` | Un triplet fill/instrument/reference étranger mais cohérent est accepté sur un état lié à d'autres hashes. |
| F2 | `FAIL` | `BLOCKING_H0004` | `SPOT_TRANSITION_FORMULA` | Le multiplicateur est appliqué sans règle H0004 et diverge de `q × p` dès qu'il diffère de un. |
| L1 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `H0004` | Une seule trajectoire BUY/SELL, prix constant, frais quote et un instrument sont positivement démontrés. |
| L2 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `P1` | Short canonique, enforcement temporel et preuve P1 intégrée restent hors scope/non prouvés. |

## Conclusion

**`REJECT`**

Le paquet est testable, correctement ancré et convaincant sur son vecteur nominal et ses
mutants. F1 et F2 acceptent néanmoins des transitions incompatibles au cœur du modèle spot
annoncé; ils ne sont ni de simples limites de généralisation, ni des problèmes de tooling.

Ce rapport est uniquement le verdict Critique `PROCEDURAL / ROLE-SEPARATED`. Il ne modifie
aucun artefact Producteur, ne statue pas sur une correction et ne constitue ni admission
humaine ni `P1 PASS`.
