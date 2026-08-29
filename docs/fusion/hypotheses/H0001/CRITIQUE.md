# H0001 — Revue Critique indépendante

## Identité et paquet examiné

| Champ | Valeur |
|---|---|
| Rôle | `IA_CRITIQUE_INDEPENDANTE` |
| Date | `2026-08-28` (`America/Toronto`) |
| Branche | `hypothesis/H0001-canonical-ledger-equivalence` |
| Base | `7c322a812cc7308d1045c53bd34fa854d0e5bbb4` |
| Code exécuté | `2ae00f9d4405cfcbdfee5bf9c2187bf572b7dca4` |
| Preuves Producteur | `f49d0c15cb9b36523cda6e6d6e2885f88c6917f7` |
| Enveloppe de revue | `df02849b004c4074bb44c59d59a02b76be29a915` |
| SHA-256 attendu de `RESULT.json` | `41f50abf3a962f6644d2f74db552ce368f43899e2bee2c53a5c802ca7ed6fd31` |
| Verdict Critique | **`ACCEPT_WITH_LIMITS`** |

Cette revue porte exclusivement sur le paquet gelé ci-dessus. Aucun verdict
Contradictoire n'a été lu ni utilisé. Aucun fichier Producteur n'a été modifié.

## Fichiers lus

- `docs/fusion/hypotheses/H0001/HYPOTHESIS.md`
- `docs/fusion/hypotheses/H0001/SCENARIO.json`
- `docs/fusion/hypotheses/H0001/P0_OBSERVED_PROJECTION.json`
- `docs/fusion/hypotheses/H0001/EVIDENCE.md`
- `docs/fusion/hypotheses/H0001/MANIFEST.json`
- `docs/fusion/hypotheses/H0001/RESULT.json`
- `docs/fusion/hypotheses/H0001/H0001_PROTOCOL_OBSERVATIONS.md`
- `paper_trading_codex/domain/ledger.py`
- `paper_trading_codex/domain/__init__.py`
- `tests/hypotheses/H0001/oracle.py`
- `tests/hypotheses/H0001/run_experiment.py`
- `tests/hypotheses/H0001/test_canonical_ledger_equivalence.py`
- `REPRODUCIBILITY_MANIFEST.json`, `flake.lock`, `pyproject.toml`
- historique et différences Git entre les quatre ancres de revue.

`CONTRADICTOIRE.md` n'a pas été ouvert pour cette revue.

## Vérifications indépendantes

### Antériorité, gel et filiation

L'historique établit la séquence suivante : hypothèse préenregistrée à `8e36998`,
séparation anti-contamination à `39932a9`, première implémentation à `9302635`, code final
à `2ae00f9`, preuves à `f49d0c1`, enveloppe à `df02849`. `HYPOTHESIS.md`,
`SCENARIO.json` et `P0_OBSERVED_PROJECTION.json` ne diffèrent pas entre `39932a9` et
l'enveloppe finale. Les relations d'ancêtre `BASE → CODE → EVIDENCE → ENVELOPE` sont
toutes vraies. Aucun code H0001 ne diffère entre `2ae00f9` et `df02849`.

### Définitions, unités et calculs

Les unités sont cohérentes dans le domaine déclaré : notionnel, marge, frais et PnL sont
en USD; quantité et collatéral sont en SOL; toute conversion USD→SOL est divisée par le
prix de l'événement. Le levier intervient dans la quantité et n'est pas réappliqué au PnL.

Le recalcul rationnel indépendant donne :

```text
quantity_sol         = (10 × 100 × 3/10 × 2) / 100 = 6
entry_fee_usd        = 6 × 100 × 1/2000 = 3/10
collateral_open_sol  = 10 - (3/10)/100 = 9997/1000
gross_pnl_usd        = 6 × (100 - 105) = -30
exit_fee_usd         = 6 × 105 × 1/1000 = 63/100
net_pnl_usd          = -30 - 63/100 = -3063/100
collateral_delta_sol = (-3063/100)/105 = -1021/3500
collateral_final_sol = 9997/1000 - 1021/3500 = 67937/7000
```

Ces valeurs concordent exactement avec l'oracle, le ledger, les six états et
`RESULT.json`. La publication à douze décimales donne `9.705285714286`, compatible avec
la projection P0 dans la tolérance préenregistrée `5e-13`.

### Indépendance et autorité du scénario

L'oracle n'importe aucun module `paper_trading_codex`, ne nomme ni `grid_bot` ni la
projection historique, et son API ne reçoit que `SCENARIO.json`. La projection P0 est lue
par le runner seulement après dérivation et comparaison exacte.

Le ledger construit ses événements depuis les inputs, puis impose l'égalité exacte du plan
sur `sequence + kind + price`. Le mutant M7 confirme qu'une dérive du plan préenregistré
est rejetée avec `SCENARIO_EVENT_PLAN_MISMATCH`. A10 est donc mécaniquement liée au run.
Le ledger est pur et immuable; aucune lecture réseau, provider, RNG ou temps mural ne se
trouve dans son chemin comptable.

### Mutants et tests

Les mutants M1–M6 prescrits et M7 additionnel sont de vrais défauts injectés dans les
événements ou le plan. Chacun est rejeté par le code stable annoncé. M2 et M3 partagent le
code `CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH`, qui nomme explicitement les deux familles et
reste suffisamment ciblé pour H0001; M5 atteint `POSITION_MISSING`, l'invariant économique
pertinent lorsque la clôture précède l'ouverture.

Exécution détachée au commit `2ae00f9` :

```text
nix develop <worktree-2ae00f9> --command pytest tests/hypotheses/H0001 -vv
→ 12 passed in 0.21s; code 0

nix develop <worktree-2ae00f9> --command \
  python -m tests.hypotheses.H0001.run_experiment
→ code 0
→ SHA-256 41f50abf3a962f6644d2f74db552ce368f43899e2bee2c53a5c802ca7ed6fd31
→ aucune différence avec RESULT.json
```

Exécution détachée de l'enveloppe `df02849` :

```text
nix develop <worktree-df02849> --command just check
→ Ruff: succès; 80 passed; couverture 89.53 %; code 0

nix develop <worktree-df02849> --command python scripts/update_status.py --check
→ STATUS.md is current; code 0
```

La couverture lignes et branches de `ledger.py` est de 100 % dans cette exécution.

### Manifeste, hashes et reproductibilité

Tous les SHA-256 inscrits pour l'hypothèse, le scénario, la projection P0, le ledger,
l'oracle, les tests, le runner, `flake.lock`, `pyproject.toml` et `RESULT.json` concordent
avec les fichiers de l'enveloppe. `RESULT.json` et `MANIFEST.json` désignent le même
`producer_code_commit=2ae00f9d...`. Le runner obtient ce commit par `git rev-parse HEAD`
et le résultat a été reproduit octet pour octet depuis un worktree détaché de ce commit.

## Tentatives de réfutation

| Tentative | Résultat | Effet |
|---|---|---|
| Recalcul manuel exact des frais, PnL, conversion et collatéral | concordance | aucune réfutation |
| Recherche d'une double application du levier | absente et M3 rejeté | aucune réfutation |
| Recherche d'une contamination oracle par P0 ou production | aucune dépendance trouvée | aucune réfutation |
| Dérive de `ordered_events` | M7 rejeté par l'invariant attendu | aucune réfutation |
| Reproduction du résultat depuis `CODE` | résultat identique octet pour octet | aucune réfutation |
| Recalcul des empreintes et filiation Git | concordance complète | aucune réfutation |
| Exécution des suites ciblée et globale | 12/12 et 80/80 | aucune réfutation |

Aucun critère de `FAIL`, `BLOCKED` ou `NON_TESTABLE` défini dans `HYPOTHESIS.md` n'a été
observé.

## Constats classés `status × impact × scope`

| ID | Statut | Impact | Scope | Constat et effet exact |
|---|---|---|---|---|
| C1 | `CONFIRMED` | `SUPPORTING` | `H0001` | Égalité rationnelle exacte des six états et concordance séparée avec P0; soutient H0001 dans son seul scénario. |
| C2 | `CONFIRMED` | `SUPPORTING` | `H0001` | Oracle physiquement indépendant et projection historique inaccessible pendant sa dérivation; aucune contamination détectée. |
| C3 | `CONFIRMED` | `SUPPORTING` | `H0001` | Plan préenregistré autoritaire, sept mutants rejetés, résultat et environnement reproductibles. |
| C4 | `OPEN_SPEC_NOTE` | `NON_BLOCKING` | `P1_GENERALIZATION` | A8 exige littéralement des magnitudes positives plus une direction, tandis que `CloseShort` porte des PnL et deltas signés. Pour H0001, les signes sont non ambigus, exacts et testés; pour P1, le modèle d'événements reste à choisir. |
| C5 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `H0001` | L'indépendance démontrée est logicielle et procédurale, non une réplication par un auteur ou une méthode externe : oracle et ledger suivent les mêmes conventions préenregistrées et sont dans le même paquet Producteur. Cela ne contamine pas cette comparaison, mais borne sa force probatoire. |
| C6 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `P1` | Une seule position short, un seul chemin ouverture/observations/clôture, sans marge réservée, liquidation, funding, concurrence, multi-actif ou multi-devise. Aucune généralisation comptable P1 n'en découle. |

## Traitement de `SPEC_NOTE_A8`

La note est correctement conservée sans réécriture rétroactive de l'hypothèse. L'écart est
réel sur la forme de représentation, mais pas sur le sens comptable : quantité, notionnel,
marge et frais restent non négatifs; `gross_pnl_usd`, `net_pnl_usd` et
`collateral_delta_sol` sont explicitement signés et leurs relations algébriques sont
contrôlées. Je la classe donc `OPEN_SPEC_NOTE × NON_BLOCKING × P1_GENERALIZATION`. Elle
n'entraîne ni correction Producteur de H0001 ni rejet de son résultat limité.

## Verdict

**`ACCEPT_WITH_LIMITS`**

Le paquet gelé fournit une preuve reproductible, exacte et non contaminée de l'énoncé
H0001 dans son scope déclaré. Les limites C4–C6 doivent rester publiées : elles ne changent
pas le résultat de H0001, mais interdisent toute extrapolation vers un modèle comptable
général.

Ce verdict est uniquement celui de la revue Critique. Il ne déclare ni `P1 PASS`, ni H0001
validée ou admise, et ne transforme pas le statut Producteur
`PASS_PENDING_INDEPENDENT_REVIEW` en validation.

## Provenance d'exécution ajoutée après gel du verdict

Cet ajout documentaire ne modifie ni le verdict ni les constats ci-dessus.

| Champ | Valeur |
|---|---|
| `review_execution` | sous-agent Codex `h0001_critique` (`Einstein`), contexte distinct |
| `orchestrator` | session Codex parente |
| `model/version` | `UNKNOWN` — identité technique non exposée à la session |
| `review_mandate` | examiner comme Critique le paquet H0001 gelé à `df02849b`, vérifier définitions, calculs, code, tests, unités, domaine, reproductibilité, ancres et hashes; rendre un verdict unique sans modifier les artefacts Producteur ni déclarer `P1 PASS` |
| `cross_review_visibility_before_first_verdict` | `NONE` — `CONTRADICTOIRE.md` non lu avant le premier verdict |
| `same_model_family` | `UNKNOWN` — aucune diversité statistique revendiquée |
| `review_independence` | `PROCEDURAL / ROLE-SEPARATED` |
