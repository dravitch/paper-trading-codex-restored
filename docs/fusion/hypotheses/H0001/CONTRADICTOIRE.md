# H0001 — Revue Contradictoire indépendante

## Verdict figé

`ACCEPT_WITH_LIMITS`

Ce verdict porte exclusivement sur H0001 dans son scénario unique et sous A1–A10. Il ne
déclare ni H0001 admise/validée, ni `P1 PASS`. Les limites L1–L3 ci-dessous sont publiables
sans rouvrir le paquet Producteur; aucune ne contamine le résultat comptable H0001.

## Identité et paquet examiné

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire indépendante |
| date | `2026-08-28` (`America/Toronto`) |
| branche | `hypothesis/H0001-canonical-ledger-equivalence` |
| base | `7c322a812cc7308d1045c53bd34fa854d0e5bbb4` |
| code Producteur | `2ae00f9d4405cfcbdfee5bf9c2187bf572b7dca4` |
| preuves Producteur | `f49d0c15cb9b36523cda6e6d6e2885f88c6917f7` |
| enveloppe de revue | `df02849b004c4074bb44c59d59a02b76be29a915` |
| SHA-256 attendu de `RESULT.json` | `41f50abf3a962f6644d2f74db552ce368f43899e2bee2c53a5c802ca7ed6fd31` |

Le premier verdict a été arrêté sans lecture de `docs/fusion/hypotheses/H0001/CRITIQUE.md`,
sans réception ni consultation d'un verdict Critique. Ce fichier n'a pas été lu.

## Fichiers lus

- `HYPOTHESIS.md`, `SCENARIO.json`, `P0_OBSERVED_PROJECTION.json`, `EVIDENCE.md`,
  `MANIFEST.json`, `RESULT.json`, `H0001_PROTOCOL_OBSERVATIONS.md` et le placeholder
  antérieur de `CONTRADICTOIRE.md`;
- `paper_trading_codex/domain/ledger.py`;
- `tests/hypotheses/H0001/oracle.py`, `run_experiment.py` et
  `test_canonical_ledger_equivalence.py`;
- `REPRODUCIBILITY_MANIFEST.json`, `flake.lock` et `pyproject.toml` pour contrôler la
  provenance et l'environnement annoncés;
- historique et différences Git limités aux ancres et chemins ci-dessus, en excluant
  explicitement `CRITIQUE.md`.

## Commandes et résultats indépendants

| Contrôle | Résultat | Code |
|---|---|---:|
| `git rev-parse HEAD` | enveloppe exacte `df02849b...` | 0 |
| `git merge-base --is-ancestor` sur base → code → preuves → enveloppe | chaîne d'ascendance exacte | 0 pour chaque arc |
| `sha256sum` sur inputs, projection P0, code, tests, runner, environnement et résultat | toutes les empreintes égales au manifeste | 0 |
| hash des blobs lus par `git show` aux commits code/preuves | ledger, runner et résultat égaux aux empreintes annoncées | 0 |
| `nix develop --command pytest tests/hypotheses/H0001 -vv` | `12 passed in 0.17s` | 0 |
| `nix develop --command just check` | Ruff OK, `80 passed`, couverture exacte `89.53 %`, ledger lignes/branches `100 %` | 0 |

L'arbre était propre avant les exécutions. Les tests ont créé seulement leurs caches
usuels; aucun artefact Producteur n'a été modifié.

## Tentatives de réfutation

### Circularité de l'oracle

L'oracle ne fait aucun import de production et son source ne lit que le chemin de scénario
reçu. Il ne lit ni la projection P0 ni le manifeste final. Ses formules rationnelles
réimplémentent la dérivation préenregistrée et non une projection extraite du ledger. La
ressemblance des formules est imposée par les conventions comptables, tandis que
l'indépendance de code et l'antériorité Git ferment la circularité matérielle recherchée.

**Résultat : réfutation échouée.**

### Dérive de `ordered_events`

Le builder reconstruit les événements à partir des inputs puis exige l'égalité du tuple
complet `(sequence, kind, price)` avec `ordered_events`. Une altération isolée du kind, du
prix, du rang, de la longueur ou de la multiplicité du plan ne peut atteindre le replay.
M7 vérifie le kind; l'égalité structurelle couvre aussi les autres composantes.

**Résultat : réfutation échouée.** Le plan préenregistré est une contrainte effective, même
s'il n'est pas utilisé comme fabrique directe des événements.

### Signe, levier, frais, unités et collatéral

Le levier dimensionne la quantité une fois. Le PnL short est ensuite
`quantity × (entry − exit)`. Les frais USD sont calculés sur les notionnels correspondants
et les deltas SOL sont divisés par le prix de leur événement. Les invariants du ledger et
la comparaison exacte des six snapshots empêchent respectivement les incohérences locales
et une erreur coordonnée qui modifierait les états. La marge `300 USD` est portée dans la
position et projetée aux états ouverts. Le calcul indépendant retrouve exactement
`67937/7000 SOL`.

**Résultat : réfutation échouée.** M1–M6 ciblent bien les défauts préenregistrés avec des
codes stables; M7 ferme la dérive de scénario.

### Dépendances cachées et contamination de scope

Le ledger utilise seulement dataclasses, typing et `Fraction`; il ne consulte ni stratégie,
provider, réseau, RNG, horloge ou projection historique. Les modifications depuis la base
n'importent pas REV13/P6 dans le mécanisme H0001. Les documents bornent expressément les
revendications au scénario unique.

**Résultat : réfutation échouée.**

### Hashes, manifeste et ancrage Git

Les hashes présents dans `MANIFEST.json` ont tous été recalculés avec succès. Le résultat
est identique au blob du commit de preuves, et son commit Producteur correspond au commit
de code dont les blobs ledger/runner possèdent les hashes manifestés. La branche relie les
quatre ancres dans l'ordre annoncé. Le manifeste P0 contient réellement les inputs et la
projection dont les copies H0001 sont issues.

**Résultat : réfutation échouée pour ce paquet gelé.** La réserve générique sur un worktree
sale est conservée en L2.

## Limites classées

| ID | Statut | Impact | Scope | Constat et effet exact |
|---|---|---|---|---|
| L1 / A8 | `OPEN_SPEC_NOTE` | non bloquant | généralisation P1 | A8 annonce magnitudes positives + direction, tandis que PnL et delta de collatéral sont signés sans champ direction séparé. Les valeurs H0001 restent non ambiguës et exactement testées; le choix de représentation général reste ouvert. |
| L2 / HEAD | `PROVENANCE_LIMIT` | non bloquant ici | runner/protocole futur | `_git_head()` atteste le HEAD mais pas la propreté du worktree. Un run sur fichiers suivis modifiés pourrait donc afficher le même commit. Pour ce paquet, arbre propre, hashes manifestés, blobs aux commits et résultat gelé concordent; aucune contamination observée. |
| L3 / mutants | `COVERAGE_LIMIT` | non bloquant | portée des mutations | Les sept mutants sont des corruptions choisies d'événements/plan, pas une campagne exhaustive de mutation du code. Ils établissent les sept sensibilités revendiquées, pas l'absence de toute faute comptable hors scénario. |

## Effet du verdict

H0001 résiste aux contre-exemples demandés dans son domaine préenregistré : oracle séparé,
ordre autoritaire, arithmétique exacte, états et marge observables, mutants ciblés,
projection P0 séparée et provenance finale cohérente. L1–L3 interdisent d'extrapoler cette
preuve vers un ledger général ou une chaîne probatoire universelle, mais ne réfutent aucun
attendu du scénario H0001.

Le verdict contradictoire demeure donc `ACCEPT_WITH_LIMITS`. Il constitue un rapport à
soumettre à l'admission humaine avec la revue Critique séparée. Il n'a, à lui seul, aucun
effet de gate : `P1` reste `NOT_PASSED`, et H0001 n'est déclarée ni validée ni admise ici.

## Provenance d'exécution ajoutée après gel du verdict

Cet ajout documentaire ne modifie ni le verdict ni les constats ci-dessus.

| Champ | Valeur |
|---|---|
| `review_execution` | sous-agent Codex `h0001_contradictoire` (`Gibbs`), contexte distinct |
| `orchestrator` | session Codex parente |
| `model/version` | `UNKNOWN` — identité technique non exposée à la session |
| `review_mandate` | examiner comme Contradictoire le paquet H0001 gelé à `df02849b`, chercher activement réfutations, contre-exemples, mutations, dérives de référentiel et défauts de provenance; figer un verdict unique sans lire le verdict Critique, sans modifier les artefacts Producteur ni déclarer `P1 PASS` |
| `cross_review_visibility_before_first_verdict` | `NONE` — `CRITIQUE.md` non lu et verdict Critique non reçu avant le premier verdict |
| `same_model_family` | `UNKNOWN` — aucune diversité statistique revendiquée |
| `review_independence` | `PROCEDURAL / ROLE-SEPARATED` |
