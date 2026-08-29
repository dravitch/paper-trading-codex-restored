# H0002 — Revue Contradictoire indépendante

## Verdict figé

`ACCEPT_WITH_LIMITS`

Le résultat H0002 résiste aux réfutations dans la famille préenregistrée. Ce verdict ne
vaut que pour cinq shorts isolés, ouverts puis fermés entièrement avec la convention de
marge H0001. Il ne déclare ni H0002 admise/validée, ni `P1 PASS`.

## Identité, mandat et indépendance

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| identité/version du moteur | `UNKNOWN` |
| date | `2026-08-29` (`America/Toronto`) |
| révision examinée | `74ce950105c682792c001decf338d1bd7cbfc674` |
| branche | `hypothesis/H0002-short-ledger-generalization` |
| base H0002 | `de946c1aa1a9190aebbd1bcba3116cf9be6d521e` |
| mandat | chercher activement des contre-exemples à H0002 seulement |
| indépendance | `PROCEDURAL / ROLE-SEPARATED` |

La revue a été conduite sans ouvrir, lire ou modifier
`docs/fusion/hypotheses/H0002/CRITIQUE.md`, et sans recevoir son verdict avant le gel du
présent verdict. Cette séparation de rôle ne revendique ni IV&V organisationnelle, ni
indépendance statistique, ni indépendance des modèles/auteurs.

## Fichiers examinés

- `HYPOTHESIS.md`, `SCENARIO_FAMILY.json`, `ORACLE_EXPECTATIONS.json`, `FIRST_RUN.json`,
  `EVIDENCE.md`, `MANIFEST.json`, `RESULT.json`, `H0002_PROTOCOL_OBSERVATIONS.md` et le
  placeholder antérieur de `CONTRADICTOIRE.md`;
- `paper_trading_codex/domain/ledger.py`;
- `tests/hypotheses/H0002/oracle.py`, `test_short_ledger_generalization.py` et
  `run_experiment.py`;
- `flake.lock`, `pyproject.toml`, `STATUS.md` et les objets/historiques Git nécessaires à
  la filiation et aux blobs déclarés.

`CRITIQUE.md` est explicitement exclu de cette liste et de toutes les commandes Git.

## Contrôles exécutés

| Contrôle | Observation | Code |
|---|---|---:|
| `git rev-parse HEAD` | paquet gelé exact `74ce950...` | 0 |
| `git merge-base --is-ancestor` sur base → préenregistrement → instrumentation → premier run → code final → preuves → gel | chaque arc est ancestral | 0 |
| `sha256sum` des artefacts, du ledger, de l'oracle, des tests, du runner et de l'environnement | toutes les valeurs concordent avec `MANIFEST.json` | 0 |
| hash du ledger par `git show` à la base, à l'instrumentation, au premier run, au code final et au gel | toujours `b917433d...6cf6bc` | 0 |
| diff instrumentation `eade1e7` → premier-run `9eec77f` sur ledger/tests | aucune modification | 0 |
| recalcul canonique de `scenario_projections` | `3db37271...49ef36b`, identique à `RESULT.json` | 0 |
| `nix develop --command pytest tests/hypotheses/H0002 -vv` | `16 passed in 0.06s` | 0 |
| `nix develop --command just check` | Ruff OK, `96 passed`, couverture `89.53 %`; ledger lignes/branches `100 %` | 0 |

Les fractions de chaque cas ont été recalculées à partir des seuls inputs. Elles retrouvent
les attentes figées, notamment les collatéraux finaux `31973/3000`, `67937/7000`,
`4991/500`, `137301/14000` et `47923/2200`. Le SHA-256 réel de `RESULT.json` est
`b38e2bcee1992dc8314300f6687b664534290368eee2660621eff2d488050c4b`.

## Réfutations tentées

### R1 — Famille non discriminante

Les cinq cas ne sont pas de simples duplicatas numériques : ils séparent PnL positif,
négatif et nul; perte par frais seuls; trois couples maker/taker; leviers `3/2`, `2` et
`5/2`; capitaux/prix/marges distincts; longueurs de plans différentes; conversions
rationnelles terminales et non terminales. Les résultats changent de signe et d'échelle
sans branchement de production.

La famille reste petite et certaines dimensions sont corrélées; cela borne la conclusion
mais ne rend pas les cinq observations non discriminantes. **Réfutation échouée**, limite
L1 conservée.

### R2 — Oracle circulaire ou contaminé par les réponses

L'oracle lit exclusivement `SCENARIO_FAMILY.json`, n'importe aucun module de production
et ne contient aucune référence à `ORACLE_EXPECTATIONS.json` ou `grid_bot`. Les attentes
étaient commitées avant l'instrumentation. Le runner dérive et compare d'abord les états,
puis ouvre les réponses préenregistrées.

L'oracle et le ledger appliquent nécessairement la même algèbre publiée; leur séparation
est logicielle et procédurale, pas une preuve d'auteur indépendant. Aucun canal concret de
lecture des réponses par l'oracle n'a été trouvé. **Réfutation échouée**, limite L2
conservée.

### R3 — Adaptation du ledger entre H0001 et le premier run

Le blob Git du ledger et son SHA-256 sont identiques à l'admission H0001, au commit
d'instrumentation, au commit du premier run, au code final et au paquet gelé. Entre
`eade1e7` et `9eec77f`, seuls `FIRST_RUN.json` et `EVIDENCE.md` apparaissent; ni ledger ni
tests ne changent. Les sept tests initiaux précèdent donc matériellement leur résultat
enregistré et aucun correctif de ledger H0002 n'est intercalé.

**Réfutation échouée.** Git établit l'absence d'adaptation du code; le journal du premier
run reste une attestation Producteur, pas une observation IV&V en temps réel.

### R4 — Surajustement à `scenario_id` ou à l'ordre de la famille

Le type de production ne reçoit aucun `scenario_id`; le source du ledger ne contient pas
ce terme. La suppression des identités et l'exécution en ordre inverse conservent les
résultats indexés par contenu. Les plans `(sequence, kind, price)` sont comparés en entier,
et les dérives de kind, prix et ordre sont rejetées.

**Réfutation échouée.** Les calculs dépendent des inputs, pas de l'étiquette ou de la place
du cas.

### R5 — Erreurs de signe, frais, levier, unité ou observation

Les snapshots exacts contrôlent collatéral, frais, PnL réalisé, position, quantité et marge
à chaque événement. Les observations recopient l'état ouvert. Cinq corruptions distribuées
sur les cinq cas sont rejetées par leur invariant, et les états finaux concordent avec le
recalcul rationnel. Aucun temps mural, réseau, provider ou RNG n'est consulté.

**Réfutation échouée.** La campagne démontre les fautes ciblées, sans être une mutation
exhaustive du ledger.

## Limites classées

| ID | Statut | Impact | Scope | Effet exact |
|---|---|---|---|---|
| L1 | `PUBLISHED_LIMIT` | non bloquant | généralisation H0002 | Les cinq cas couvrent plusieurs régimes mais gardent tous `initial_price = entry_price`, une position short unique, une fermeture totale et aucun mécanisme de marge réservé. Ils soutiennent uniquement cette famille, pas tout short concevable. |
| L2 | `INDEPENDENCE_LIMIT` | non bloquant | statut probatoire | L'indépendance oracle/ledger est `PROCEDURAL / ROLE-SEPARATED`. Elle n'est ni IV&V, ni statistique, ni une garantie d'auteurs ou de modèles indépendants. |
| L3 | `ASSERTION_COMPLETENESS_LIMIT` | non contaminant ici | runner/tests | La comparaison aux attentes itère les entrées présentes sans exiger explicitement l'égalité des ensembles de clés enregistrées et dérivées. Le fichier gelé contient bien exactement les cinq IDs et tous les champs attendus; aucune réponse n'est absente dans ce paquet. |
| L4 | `MUTATION_SCOPE_LIMIT` | non bloquant | falsifications | Les huit dérives sont ciblées et préannoncées; elles ne constituent pas une campagne exhaustive de mutation du code ni une preuve hors des événements H0001. |

## Provenance et portée du verdict

La filiation, l'antériorité des inputs/réponses, l'immuabilité du ledger, les hashes du
manifeste, le résultat et les contrôles reproduits sont cohérents. Aucun indice de
contamination de scope, d'ajustement par scénario ou de convention A11/A12 n'a été trouvé.

Le verdict contradictoire final est donc `ACCEPT_WITH_LIMITS`. Il soutient seulement la
conservation des invariants H0001 sur la famille H0002 préenregistrée. Les limites peuvent
rester publiées sans correction Producteur. Ce rapport n'admet pas humainement H0002, ne
ferme pas P1 et ne produit aucun `P1 PASS`.
