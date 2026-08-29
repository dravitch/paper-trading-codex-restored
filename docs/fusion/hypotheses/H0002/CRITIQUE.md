# H0002 — Revue Critique indépendante

## Identité, révision et mandat

| Champ | Valeur |
|---|---|
| Rôle | `IA_CRITIQUE_INDEPENDANTE` |
| Agent | `OpenAI Codex` |
| Version du modèle | `UNKNOWN` |
| Date | `2026-08-29` (`America/Toronto`) |
| Révision examinée | `74ce950105c682792c001decf338d1bd7cbfc674` |
| Branche | `hypothesis/H0002-short-ledger-generalization` |
| Base H0002 | `de946c1aa1a9190aebbd1bcba3116cf9be6d521e` |
| Préenregistrement | `1d63024aee44e56c236d5bc67b3128f03994aa92` |
| Premier instrument | `eade1e71b740a67bba8a803ed9568585735fb696` |
| Premier run ancré | `9eec77fb4cdeb58b16f579959c22003fa734fdf8` |
| Code Producteur final | `da720db01f0a10554efc3dc75185d9d804899c68` |
| Preuves Producteur | `90dd9e1d467317bdfdd127e7321a119e11277b74` |
| Verdict | **`ACCEPT_WITH_LIMITS`** |

Mandat : tenter de réfuter la conservation exacte du ledger short H0001 sur les cinq cas
préenregistrés, le caractère discriminant de cette famille, l'indépendance de l'oracle,
l'absence d'adaptation du ledger avant le premier run et la portée revendiquée. La revue
porte exclusivement sur le paquet gelé. `CONTRADICTOIRE.md` n'a été ni lu ni modifié.

Indépendance de cette revue : **`PROCEDURAL / ROLE-SEPARATED`**. Cela signifie séparation
de rôle et premier verdict établi sans le rapport Contradictoire. Cela ne constitue ni une
IV&V organisationnelle, ni une indépendance statistique, ni une réplication externe.

## Provenance et fichiers examinés

- `HYPOTHESIS.md`, `SCENARIO_FAMILY.json`, `ORACLE_EXPECTATIONS.json`;
- `FIRST_RUN.json`, `EVIDENCE.md`, `MANIFEST.json`, `RESULT.json`;
- `H0002_PROTOCOL_OBSERVATIONS.md`;
- `paper_trading_codex/domain/ledger.py` et son historique Git;
- `tests/hypotheses/H0002/oracle.py`;
- `tests/hypotheses/H0002/test_short_ledger_generalization.py`;
- `tests/hypotheses/H0002/run_experiment.py`;
- `STATUS.md`, `flake.lock`, `pyproject.toml`;
- filiation et contenus Git des commits ancrés.

## Résultats des contrôles

### Antériorité et ledger inchangé

La filiation Git est linéaire et vérifiée :

```text
de946c1 → 1d63024 → eade1e7 → 9eec77f → da720db → 90dd9e1 → 74ce950
```

Les trois artefacts préenregistrés (`HYPOTHESIS`, famille et attentes) sont identiques entre
`1d63024` et le paquet final. Le blob Git de `ledger.py` est le même
`4433f0fac8c7d908b6bcaf7fd6f544273e90d99f` à la base H0001 admise, au premier
instrument, au code final et au paquet gelé. Son SHA-256 reste
`b917433de9661896a1ac0ec74e9c7b2fb2d8a64864736e48d1ae4161286cf6bc`.

Le commit `eade1e7` ajoute uniquement l'oracle et sept tests H0002; `9eec77f` enregistre
ensuite le premier run. Aucun code de production n'a donc été adapté entre H0001 et ce
premier résultat.

### Recalcul comptable

J'ai recalculé les cinq cas à partir des formules préenregistrées. Les résultats
irréductibles concordent avec l'oracle, les attentes et `RESULT.json` :

| Cas | Quantité | PnL brut | Frais sortie | PnL net | Collatéral final |
|---|---:|---:|---:|---:|---:|
| `WIN_STANDARD` | `6` | `60` | `27/50` | `2973/50` | `31973/3000` |
| `LOSS_STANDARD` | `6` | `-30` | `63/100` | `-3063/100` | `67937/7000` |
| `FLAT_HIGH_FEES` | `6` | `0` | `6/5` | `-6/5` | `4991/500` |
| `SMALL_FRACTIONAL` | `3` | `-15` | `12/35` | `-537/35` | `137301/14000` |
| `LARGE_WIN` | `20` | `200` | `33/10` | `1967/10` | `47923/2200` |

Les unités sont cohérentes : grandeurs commerciales en USD, quantité/collatéral en SOL,
prix en USD/SOL, et conversion de chaque mouvement au prix de son événement. Les états
d'observation ne réalisent aucun mouvement.

### Caractère discriminant de la famille

La famille discrimine utilement, mais seulement dans son espace paramétrique annoncé :

- signe du PnL : positif, négatif et nul;
- frais seuls dans `FLAT_HIGH_FEES`;
- quantités `3`, `6`, `20`, capitaux `750`, `1000`, `2400`;
- trois couples maker/taker et leviers `3/2`, `2`, `5/2`;
- conversions rationnelles non terminales;
- deux longueurs de plans et plusieurs observations sans réalisation.

Les cinq mutations comptables ciblent cinq cas différents et sont rejetées par les
invariants attendus. Les dérives de `kind`, prix et ordre sont toutes rejetées. La
suppression de `scenario_id` et la permutation de la famille n'affectent pas le calcul.

Cette discrimination ne change toutefois jamais de chemin économique : tous les cas sont
des shorts isolés, ouverture unique, observations passives, clôture MTM totale. Elle
soutient une généralisation **paramétrique sur ce chemin**, pas une généralisation du
ledger à d'autres capacités comptables.

### Indépendance de l'oracle

L'oracle exécutable reçoit seulement `SCENARIO_FAMILY.json`, n'importe aucun code de
production et ne contient aucune référence à `ORACLE_EXPECTATIONS.json` ou `grid_bot`.
Le runner dérive la famille et compare le ledger avant de lire les attentes
préenregistrées. Les attentes ont été figées avant le code H0002 et n'ont pas changé.

Cette indépendance est **procédurale et physique au sein du paquet Producteur**. Oracle,
attentes et tests restent issus du même processus Producteur et appliquent les mêmes
conventions préenregistrées; je ne revendique donc ni IV&V ni indépendance statistique.

### Hashes, manifeste et reproductibilité

Tous les SHA-256 du manifeste ont été recalculés et concordent : hypothèse, famille,
attentes, premier run, ledger, oracle, tests, runner, résultat, preuves, observations,
statut, lock Nix et `pyproject.toml`. Le SHA-256 de `RESULT.json` vaut
`b38e2bcee1992dc8314300f6687b664534290368eee2660621eff2d488050c4b`; le hash canonique
des projections vaut `3db37271090c2eb96ee33875dac59cdfe4c64cc1dff369ee676c1e93249ef36b`.

Commandes reproduites dans des copies/clones temporaires des commits exacts :

```text
# eade1e7, avant mutants
nix develop --command pytest tests/hypotheses/H0002 -vv
→ 7 passed in 0.09s; code 0

# da720db, instrumentation finale
nix develop --command pytest tests/hypotheses/H0002 -vv
→ 16 passed in 0.07s; code 0

nix develop --command python -m tests.hypotheses.H0002.run_experiment \
  --output /tmp/h0002-critique-result.json
→ résultat identique octet pour octet; code 0

# 74ce950, paquet gelé
nix develop --command just check
→ Ruff OK; 96 passed; couverture 89.53 %; ledger lignes/branches 100 %; code 0

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current; code 0
```

## Tentatives de réfutation et objections

| ID | Statut | Impact | Scope | Constat |
|---|---|---|---|---|
| C1 | `CONFIRMED` | `SUPPORTING` | `H0002` | Les cinq cas concordent exactement avec l'oracle préenregistré et les huit invariants annoncés. |
| C2 | `CONFIRMED` | `SUPPORTING` | `H0002_FIRST_RUN` | Le ledger H0001 inchangé passe les sept tests initiaux avant l'ajout des mutants; aucune adaptation de production n'est observée. |
| C3 | `CONFIRMED` | `SUPPORTING` | `H0002` | Identité de scénario et ordre de la liste sans influence; cinq mutants et trois dérives de plan sont rejetés. |
| C4 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `H0002` | Les cas varient les paramètres mais exercent tous le même chemin short isolé et clôture totale. La portée exacte est une généralisation paramétrique finie, non structurelle. |
| C5 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `EVIDENCE_STRENGTH` | L'indépendance de l'oracle est procédurale/physique, pas une réplication externe ou statistiquement indépendante. |
| C6 | `OPEN_TOOLING_NOTE` | `NON_BLOCKING` | `RUNNER` | La comparaison aux attentes itère les entrées présentes sans exiger explicitement l'égalité des ensembles de clés. Le fichier gelé contient bien les cinq cas et a été vérifié intégralement; une attente supprimée pourrait toutefois échapper à ce garde dans un futur paquet. |
| C7 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `P1` | Aucun long, spot, close partiel, marge réservée, liquidation, funding, simultanéité, multi-position, multi-actif ou fidélité exchange n'est exercé. |

Tentatives sans réfutation : inversion du signe, double frais d'entrée, omission du frais de
sortie, double levier, confusion USD/SOL, dérives du plan, suppression de l'identité,
permutation des cas, recalcul manuel, vérification du blob ledger, reproduction du runner
et suite globale. Aucun critère `FAIL`, `BLOCKED` ou `NON_TESTABLE` n'est rencontré.

C6 ne contamine pas le résultat présent : les cinq identifiants de la famille existent
dans `ORACLE_EXPECTATIONS.json`, leurs dix valeurs sont comparées et les hashes
préenregistrés concordent. Il s'agit d'une limite de robustesse du garde, pas d'une demande
de correction Producteur pendant cette revue.

## Verdict

**`ACCEPT_WITH_LIMITS`**

H0002 fournit une preuve exacte, reproductible et préenregistrée que le ledger H0001
inchangé conserve ses invariants sur les cinq shorts isolés de la famille. Les limites
C4–C7 doivent rester publiées et bornent strictement l'inférence à cette généralisation
paramétrique finie.

Ce verdict est celui de la seule revue Critique `PROCEDURAL / ROLE-SEPARATED`. Il ne
déclare ni `P1 PASS`, ni H0002 validée ou admise, et ne remplace pas l'admission humaine.
