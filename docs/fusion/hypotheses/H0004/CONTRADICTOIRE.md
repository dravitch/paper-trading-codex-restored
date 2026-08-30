# H0004 — Revue Contradictoire indépendante

## Verdict figé

`REJECT`

Le scénario préenregistré, l'oracle, les six écritures, S8 et M1–M19 passent tels quels.
Deux contre-exemples nouveaux réfutent toutefois le contrat annoncé : un état accepte un
autre couple cohérent `InstrumentSpec`/`ReferenceSpec` sans vérifier ses hashes stockés,
et le ledger applique silencieusement `contract_multiplier` alors que la transition spot
fermée est `q × p`. Ces défauts restent invisibles avec l'unique multiplicateur oracle
`1/1`.

Ce verdict ne constitue pas une admission humaine et ne déclare pas `P1 PASS`.

## Identité, révision et indépendance

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| identité/version du moteur | `UNKNOWN` |
| date | `2026-08-30` (`America/Toronto`) |
| branche | `hypothesis/H0004-minimal-spot-ledger` |
| paquet Producteur gelé | `5967ee06f85bb4b52e0e3bb6fafb19b2856d63db` |
| manifeste Producteur | `b0064c0200384239372ada5c01b5efe3b8aeac7d` |
| code Producteur exécuté | `4bd8e1f5da366baaf2d8de6702bcf51b663b24db` |
| indépendance | `PROCEDURAL / ROLE-SEPARATED` |

`REVIEW_REQUEST.md` et le paquet H0004 ont été lus intégralement. Le fichier
`docs/fusion/hypotheses/H0004/CRITIQUE.md` et son verdict n'ont été ni ouverts, ni lus,
ni demandés, ni reçus avant fixation du présent verdict. Cette séparation ne revendique
ni IV&V organisationnelle, ni indépendance statistique, ni indépendance des modèles ou
auteurs.

## Fichiers examinés

- `HYPOTHESIS.md`, `SCENARIO.json`, `ORACLE_EXPECTATIONS.json`, `FIRST_RUN.json`,
  `RESULT.json`, `EVIDENCE.md`, `MANIFEST.json`, `H0004_PROTOCOL_OBSERVATIONS.md` et
  `REVIEW_REQUEST.md`;
- `P1_SPOT_LEDGER_DECISIONS.md` et `P1_SPOT_LEDGER_DECISION_S8.md`;
- contrats H0003 dans `paper_trading_codex/domain/contracts.py` et exports du domaine;
- `paper_trading_codex/domain/spot_ledger.py`;
- oracle, tests nominaux, tests mutants et runner H0004;
- `STATUS.md`, `flake.lock`, `pyproject.toml` et objets Git nécessaires à la provenance.

`CRITIQUE.md` a été explicitement exclu de toutes les lectures et recherches.

## Provenance et premier run

La chaîne est ancestrale dans l'ordre annoncé :

```text
9c3b758 → 044406f → 8aa05bc → 56c5e54 → cef58c5
→ f3c6811 → a137491 → ffed088 → 54f252a → 4bd8e1f
→ c24a9b9 → b0064c0 → 5967ee0
```

Les trois préenregistrements conservent respectivement les blocages S1–S7, le blocage S8
et l'état prêt après décisions humaines. Aucun code H0004 ne précède ces décisions.

Au commit `a137491`, le ledger, l'oracle et les deux tests nominaux existent. Le diff
`a137491..ffed088` ajoute seulement `FIRST_RUN.json`; aucun code ou test n'est modifié.
Les mutants arrivent ensuite à `54f252a`. Le blob initial du ledger vaut
`127dc566...8e929`; le seul changement de production ultérieur ajoute l'appel et la
fonction de validation de conservation, donnant `f041b4d2...62b5`, sans modifier les
formules nominales. Le premier run est donc correctement antérieur à M1–M19 et ne masque
aucune correction comptable nominale.

## Contrôles exécutés

| Contrôle | Résultat | Code |
|---|---|---:|
| `git rev-parse HEAD` | paquet exact `5967ee06f85bb4b52e0e3bb6fafb19b2856d63db` | 0 |
| `git merge-base --is-ancestor` sur chaque arc | filiation complète | 0 |
| `sha256sum` des artefacts manifestés | toutes les empreintes concordent | 0 |
| blob du résultat au commit de preuves `c24a9b9` | `cb6582a1...1402594` | 0 |
| `nix develop --command pytest tests/hypotheses/H0004 -q` | `24 passed in 0.23s` | 0 |
| `nix develop --command just check` | Ruff OK; `159 passed`; couverture `91.77 %`; spot ledger 100 % | 0 |
| `nix develop --command python scripts/update_status.py --check` | `STATUS.md is current` | 0 |
| attaque specs cohérentes différentes de l'état | acceptée, état/hash discordants | 0 |
| attaque multiplicateur spot `2/1` | acceptée, débit `40` au lieu de `20` | 0 |

Les fractions ont été recalculées indépendamment :

```text
q × p                  = 999/10
BUY quote total        = -100
SELL quote net         = 998001/10000
frais cumulés          = 1999/10000
collatéral/base final  = 0
```

Elles concordent avec l'oracle et le résultat gelés pour le cas `contract_multiplier=1/1`.

## Vérifications positives demandées

### Oracle et conservation

L'oracle importe seulement `Fraction` et lit des dictionnaires fournis; il n'importe ni
ledger ni attentes. Les trois états et six `AccountEvent` correspondent aux fractions,
IDs, provenances, devises, signes et clés préenregistrés. Pour chaque fill, les sommes BASE
et QUOTE des écritures expliquent exactement la variation d'état. `fees_by_currency` est
une magnitude positive séparée et n'entre pas une seconde fois dans la balance. La
valorisation est pure.

### Validateurs H0003

Les chemins nominaux appellent :

- `validate_instrument_reference` à la création;
- `validate_account_event_compatibility` pour chaque initialisation et écriture dérivée;
- `validate_fill_compatibility` avant toute transition économique de fill.

Ces appels valident les objets fournis entre eux. Ils ne suffisent cependant pas à lier
les specs fournies à l'état existant; c'est la réfutation F1.

### S8, priorité, tri et mémoire

`_validate_fill_progression` est le premier appel d'`apply_fill`, avant discriminant,
validations relationnelles, devise et soldes. Une clé égale produit
`SPOT_FILL_REAPPLICATION`; une clé inférieure économiquement applicable produit
`SPOT_FILL_OUT_OF_ORDER`. Le premier fill après initialisation évite toute comparaison
inter-types.

L'API consomme un fill unique et ne trie aucune collection de fills. Le seul `sorted`
ordonne les trois écritures dérivées selon B6, comme préenregistré. Aucun historique,
`seen_fill_ids`, cache, registre, singleton ou état caché n'a été trouvé; le schéma d'état
reste exactement celui autorisé par S5/S8.

### M1–M19

Les 24 tests exercent les familles annoncées, dont M18a–M18e. Les rejets ciblés et
invariants sont observés : insuffisances, devise/frais, grille, références, conservation,
signes, pureté, déduplication de collection, modèle spot, IDs/provenance, initialisation,
cumul de frais, dernier input, priorité S8 et frais BASE hors profil. Leur succès ne couvre
pas les deux attaques inter-specs ci-dessous.

## Findings bloquants

### F1 — Les specs fournies aux transitions ne sont pas liées aux hashes de l'état

```text
status = FAIL
impact = BLOCKING_H0004
scope = MONO_INSTRUMENT_STATE_COMPATIBILITY
```

`SpotAccountState` sérialise `instrument_spec_sha256` et `reference_spec_sha256`, mais
`apply_fill` et `apply_initialization` ne comparent jamais ces hashes aux specs reçues.
`validate_fill_compatibility` vérifie seulement que fill, instrument et référence **du
même appel** sont cohérents entre eux.

Contre-exemple reproduit :

1. créer et initialiser le compte avec la spec oracle (`multiplier=1`, hashes A);
2. construire une autre `InstrumentSpec` de même `instrument_id`, multiplier `2`, et une
   `ReferenceSpec` portant correctement son nouveau hash B;
3. appliquer un premier BUY valide `q=1`, `p=20`, frais `0` avec ce couple B.

Le fill est accepté. Le nouvel état conserve pourtant le hash A tout en débitant `40 USD`
selon la spec B :

```text
state.instrument_spec_sha256 == hash(A)  → true
supplied instrument hash == hash(B)      → true, B != A
base_balance                             → 1
quote_balance                            → 60
```

Une autre `ReferenceSpec` cohérente mais de hash différent est également acceptée tandis
que `state.reference_spec_sha256` reste l'ancien hash. La même faille existe à
l'initialisation pour l'instrument fourni.

**Effet exact :** l'état prétend être lié à des specs différentes de celles qui ont décidé
la transition. Le compte n'est donc pas mono-instrument/référentiel au sens sérialisé
annoncé, malgré l'appel des validateurs H0003. M5 ne teste qu'un triplet incohérent, pas un
triplet alternatif intérieurement cohérent.

### F2 — Convention silencieuse du multiplicateur dans l'algèbre spot

```text
status = FAIL
impact = BLOCKING_H0004
scope = SPOT_TRANSITION_FORMULA
```

Le profil et H0004 ferment les transitions avec `trade_quote = q × p`. Le code calcule :

```python
trade_quote = fill.quantity * fill.price * instrument.contract_multiplier
```

Le scénario unique utilise `contract_multiplier=1/1`; l'oracle indépendant calcule bien
`q × p` et ne discrimine donc pas les deux formules. Avec une spec SPOT valide de
multiplicateur `2`, `q=1`, `p=20`, frais `0`, le ledger débite `40 USD` et laisse
`60 USD`, alors que la transition normative laisse `80 USD`.

H0004 ne préenregistre ni l'usage du multiplicateur dans le modèle spot, ni l'obligation
`SPOT contract_multiplier == 1`. L'accepter et l'appliquer est donc une convention
comptable supplémentaire, ce que la condition de soutien interdit.

**Effet exact :** le succès nominal démontre seulement le cas dégénéré où les deux
algèbres coïncident; il ne démontre pas la transition spot fermée pour tout
`InstrumentSpec` SPOT accepté par le contrat.

## Limites non déterminantes

- L'idempotence/déduplication B7 reste une opération explicite de collection; S8 régit
  correctement l'application stateful sans mémoire cachée.
- Les initialisations peuvent être fournies en plusieurs écritures avant le premier fill;
  H0004 ne revendique pas de registre historique global. Cette frontière n'est pas utilisée
  comme motif de rejet autonome.
- Les états sont des dataclasses immuables mais publiquement constructibles; les findings
  ci-dessus utilisent uniquement les APIs nominales et ne dépendent pas d'un état forgé.
- H0004 reste limitée à `SPOT_CASH_V1`; elle ne prouve ni short canonique, ni enforcement
  temporel, ni preuve P1 intégrée.

## Verdict et effet

Le paquet est testable et reproductible; `NON_TESTABLE` ne convient pas. Le premier run,
les attentes et les mutants sont crédibles, mais F1 viole la liaison mono-instrument
sérialisée et F2 ajoute une algèbre non autorisée. Ces écarts touchent directement
l'énoncé, donc ils ne peuvent rester de simples limites publiées.

Le verdict contradictoire final est `REJECT`. Il doit être transmis avec le rapport
Critique séparé à une décision humaine. Il n'admet pas H0004, ne modifie aucun gate et
maintient `P1 = NOT_PASSED`.
