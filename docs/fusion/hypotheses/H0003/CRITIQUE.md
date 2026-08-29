# H0003 — Revue Critique indépendante

## Identité, indépendance et mandat

| Champ | Valeur |
|---|---|
| Rôle | `IA_CRITIQUE_INDEPENDANTE` |
| Agent | `OpenAI Codex` |
| Version du modèle | `UNKNOWN` |
| Date | `2026-08-29` (`America/Toronto`) |
| Branche | `hypothesis/H0003-canonical-contract-foundation` |
| Paquet gelé | `44893b0061f13e8a03c4a27f4d299b8b65b5943c` |
| Code Producteur exécuté | `9a8f318c60e82d97eff74a3fb36f532780a718bf` |
| Verdict Critique | **`REJECT`** |

Indépendance : **`PROCEDURAL / ROLE-SEPARATED`**. Le rapport Contradictoire n'a été ni lu
ni modifié. Cette séparation de rôle ne revendique ni IV&V organisationnelle, ni
indépendance statistique, ni réplication externe.

Mandat : examiner la fermeture B1–B8/B5a, l'antériorité des vecteurs, les contrats et
exports, M1–M11, les bytes/hashes/round-trips, l'ordre et la déduplication, les unités et
devises, l'absence de logique ledger/replay, la reproductibilité et la note `unicodedata`.
Seul ce fichier de revue a été remplacé.

## Provenance et fichiers examinés

Chaîne examinée :

```text
ed2731da82326cf938b3634670e7cd1f6e50445f
→ 0fe56109974790792eeaf39e341386164af36822
→ 0e105c25ba287fbf4dbdc25c4baff8bbeca41ad3
→ d817a1642f7123ac367f7b0b7c03186b2d161925
→ be6678a562f77587af6f52ee7607d1a89fa674c1
→ 5676de86b0b84284fdf81bf1edb0e43f36c61558
→ 9a8f318c60e82d97eff74a3fb36f532780a718bf
→ 5bd95dd22dd11274da3d49f259314d614d01fc1f
→ 44893b0061f13e8a03c4a27f4d299b8b65b5943c
```

Fichiers lus :

- `docs/fusion/P1_MINIMAL_EXECUTABLE_PROFILE.md`;
- `docs/fusion/P1_CANONICAL_CONTRACT_DECISIONS.md`;
- `docs/fusion/hypotheses/H0003/HYPOTHESIS.md`;
- `ORACLE_VECTORS.json`, `RESULT.json`, `EVIDENCE.md`, `MANIFEST.json`;
- `H0003_PROTOCOL_OBSERVATIONS.md`;
- `paper_trading_codex/domain/contracts.py` et `domain/__init__.py`;
- `tests/hypotheses/H0003/test_canonical_contract_foundation.py`;
- `tests/hypotheses/H0003/run_experiment.py`;
- `STATUS.md`, `flake.lock`, `pyproject.toml` et historique Git associé.

`CONTRADICTOIRE.md` n'a pas été ouvert.

## Vérifications positives

### Antériorité B1–B8/B5a

La filiation est valide. Le premier préenregistrement `ed2731d` conserve le blocage des
huit ambiguïtés. La décision humaine B1–B8 (`0fe5610`), les vecteurs (`0e105c2`) et
l'addendum humain B5a (`d817a16`) précèdent tous le préenregistrement prêt
`be6678a` et le premier code `5676de8`. Aucun des fichiers normatifs, de l'hypothèse prête
ou des vecteurs ne change ensuite jusqu'au paquet gelé.

Les décisions sont effectivement matérialisées pour les cinq contrats sérialisables :
vocabulaires fermés, `EVENT_PRICE`, forme à onze champs d'`AccountEvent`, compatibilité
instrument/référentiel et devise des frais, ordre local typé, doublon dans une collection
explicite et rationnels JSON irréductibles.

### Bytes, hashes et round-trips

Tous les SHA-256 du manifeste ont été recalculés et correspondent aux fichiers : décisions,
hypothèse, vecteurs, contrats, exports, tests, runner, résultat, preuves, observations,
statut, `flake.lock` et `pyproject.toml`. `RESULT.json` vaut :

```text
f13814dee86a98d75c28b6dc697f29d8b1185208501bd46996f47376abe7c87d
```

Le runner a été reproduit dans un clone détaché à `9a8f318`; sa sortie est identique octet
pour octet. Les cinq vecteurs `InstrumentSpec`, `ReferenceSpec`, `MarketEvent`, `Fill` et
`AccountEvent` produisent les bytes, hashes et round-trips attendus. Les hashes principaux
recalculés sont bien `e0400eeb…a886b4` et `f56b0b9f…febde`.

### M1–M11, ordre, doublons, devises

Les 29 tests ciblés passent. M1–M9 rejettent les mutations avec les codes stables annoncés;
M10 et M11 démontrent l'invariance des bytes/hash et du round-trip. Les contrôles
additionnels rejettent hors-grille, devise de compte incompatible, mélange inter-types,
surrogate Unicode et collision de clés après NFC. La déduplication est idempotente pour
les mêmes bytes, rejette le contenu divergent, puis trie par la clé locale B6.

Les validations d'agrégation disponibles ferment correctement :

- identité + hash instrument/référentiel;
- devise de frais référentiel ∈ devises instrument;
- devise du fill = devise de frais du référentiel;
- grille prix/quantité du fill;
- devise de l'`AccountEvent` selon `BASE/QUOTE/COLLATERAL`.

### Isolation du module

`contracts.py` ne contient aucune logique de ledger, replay, stratégie ou provider et
n'importe aucune source temporelle, réseau ou filesystem. `Clock` reste un port sans
implémentation système. Cette partie du critère d'isolation est satisfaite.

### Exécutions reproduites

```text
nix develop --command pytest tests/hypotheses/H0003 -q
→ 29 passed in 0.07s; code 0

# clone détaché à 9a8f318
nix develop --command python -m tests.hypotheses.H0003.run_experiment \
  --output /tmp/h0003-critique-result.json
→ résultat identique octet pour octet; code 0

# clone détaché à 44893b0
nix develop --command just check
→ Ruff OK; 125 passed; couverture globale 90.92 %;
  contracts.py 95 %; ledger.py 100 %; code 0

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current; code 0
```

## Réfutation décisive : les types temporels n'exécutent pas leur contrat

L'énoncé H0003 inclut explicitement `InstantNs` et `DurationNs`; sa portée exige des
« valeurs immuables et validations de construction » et des types temporels « comme
entiers signés ». Le profil normatif exige en outre le rejet des flottants/datetime
implicites. Or l'implémentation est :

```python
InstantNs = NewType("InstantNs", int)
DurationNs = NewType("DurationNs", int)
```

`NewType` n'effectue aucune validation à l'exécution. Le contrôle Critique démontre :

```text
InstantNs("not-an-int") → str  "not-an-int"   # accepté
DurationNs(True)        → bool True           # accepté
```

De même, un flottant ou un objet arbitraire traverse directement ces constructeurs. La
fonction privée `_integer` protège `event_time` lorsqu'il est incorporé dans les trois
événements, mais elle ne matérialise pas le contrat public autonome `InstantNs` et ne
protège jamais `DurationNs`. Aucun test H0003 ne construit ces deux types invalidement, ne
teste `DurationNs`, ni ne teste le retour d'un `Clock`.

Ce constat réfute l'énoncé plutôt que sa seule généralisation : deux des huit éléments
explicitement annoncés ne fournissent pas la validation de construction requise et une
entrée temporelle incompatible est acceptée. Il satisfait le critère de réfutation 6 et
contredit la ligne `InstantNs / DurationNs / Clock` du profil source. Les succès des cinq
contrats JSON et M1–M11 ne couvrent pas ce défaut.

## Constats `status × impact × scope`

| ID | Statut | Impact | Scope | Constat et effet exact |
|---|---|---|---|---|
| C1 | `CONFIRMED` | `SUPPORTING` | `H0003_SERIALIZABLE_CONTRACTS` | Les cinq vecteurs sérialisables, hashes et round-trips sont exacts et reproductibles. |
| C2 | `CONFIRMED` | `SUPPORTING` | `H0003_B1_B8_B5a` | Les décisions humaines et vecteurs précèdent le code; aucune convention post-observation n'a été trouvée sur ces règles. |
| C3 | `CONFIRMED` | `SUPPORTING` | `H0003_M1_M11` | Les onze familles prescrites et les contrôles additionnels observés passent selon les invariants annoncés. |
| C4 | `REFUTED` | `BLOCKING` | `H0003_CORE_CLAIM` | `InstantNs` et `DurationNs` acceptent des valeurs non entières; les validations de construction temporelles requises ne sont pas exécutables. Effet : H0003 ne peut pas être acceptée sur ce paquet. |
| C5 | `COVERAGE_GAP` | `SUPPORTS_C4` | `H0003_TESTS_AND_RESULT` | Les tests et le runner ne couvrent que cinq contrats sérialisables pour les vecteurs/round-trips et omettent les rejets des scalaires temporels ainsi que le port `Clock`. |
| C6 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `H0003_AGGREGATION` | `MarketEvent.instrument_id` est seulement non vide; contrairement à Fill/AccountEvent, aucune API d'agrégation à une spec n'est fournie. Le profil H0003 ne ferme pas explicitement une règle hash/grille pour MarketEvent, donc ce point borne l'usage mais n'est pas retenu comme réfutation autonome. |
| C7 | `OPEN_TOOLING_NOTE` | `NON_BLOCKING_FOR_H0003` | `P1_CLOCK_ENFORCEMENT` | `unicodedata` est nécessaire à NFC mais absent de l'allowlist P1 v1. H0003 exclut l'enforcement AST : aucun effet sur ses bytes actuels. Avant `P1 PASS`, la décision d'allowlist reste bloquante. |
| C8 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `P1` | H0003 ne prouve ni ledgers spot/short conformes, ni enforcement temporel, replay ou fidélité exchange. |

## Examen explicite de la note `unicodedata`

La classification Producteur est exacte :

```text
status = OPEN_TOOLING_NOTE
impact = NON_BLOCKING_FOR_H0003
scope = P1_CLOCK_ENFORCEMENT
impact_before_P1_PASS = BLOCKING_UNTIL_ALLOWLIST_DECISION
```

La dépendance est visible, déterministe et nécessaire à la règle NFC préenregistrée. Comme
l'enforcement AST est explicitement hors périmètre H0003, elle ne provoque pas le rejet
présent et ne doit pas être transformée silencieusement en extension d'allowlist. Le rejet
H0003 provient exclusivement de C4, indépendamment de cette note.

## Verdict

**`REJECT`**

Le paquet démontre solidement cinq contrats canoniques sérialisables, B1–B8/B5a et
M1–M11, mais ne matérialise pas l'énoncé complet qu'il a préenregistré : les deux types
temporels publics acceptent des valeurs incompatibles sans rejet mécanique. Cette lacune
touche le cœur de H0003 et ne peut pas être publiée comme simple limite non contaminante.

Ce verdict Critique ne déclare ni `P1 PASS`, ni H0003 admise/validée, et ne constitue pas
une décision humaine d'admission.
