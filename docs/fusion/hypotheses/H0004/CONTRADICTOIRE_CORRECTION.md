# H0004 — Revue Contradictoire du paquet corrigé

## Verdict figé

`ACCEPT_WITH_LIMITS`

Les contre-exemples admis F1a, F1b et F2 sont fermés avec leurs codes exacts, avant toute
mutation d'état. La décision humaine borne explicitement le multiplicateur spot à `1/1`,
et l'implémentation calcule de nouveau `quantity × price`. Le scénario, l'oracle, les six
écritures, S8 et M1–M19 n'ont pas régressé. Aucune nouvelle réfutation bloquante n'a été
trouvée.

Ce verdict concerne exclusivement le paquet corrigé `5f0253d`. Il ne réhabilite pas le
paquet rejeté `5967ee0`, ne constitue aucune admission humaine et ne déclare pas
`P1 PASS`.

## Identité, mandat et indépendance

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire — cycle correctif H0004 |
| identité/version du moteur | `UNKNOWN` |
| date | `2026-08-30` (`America/Toronto`) |
| branche | `hypothesis/H0004-minimal-spot-ledger` |
| paquet corrigé gelé | `5f0253d9d9c552f310eabef5ae019219d828742c` |
| manifeste corrigé | `d60e96a` |
| code Producteur exécuté | `e5f87b3b7567be048d7c77479e3c96339dcaa56e` |
| indépendance | `PROCEDURAL / ROLE-SEPARATED` |

`CORRECTION_REVIEW_REQUEST.md` a été lu intégralement. Les anciens rapports
`CRITIQUE.md` et `CONTRADICTOIRE.md` ont été lus comme contexte historique explicitement
autorisé. Le nouveau `CRITIQUE_CORRECTION.md` et son verdict n'ont été ni ouverts, ni lus,
ni demandés, ni reçus avant fixation du présent verdict. Cette séparation ne revendique
ni IV&V organisationnelle, ni indépendance statistique, ni indépendance des modèles ou
auteurs.

## Fichiers et provenance examinés

- mandat correctif, anciens rejets et `HUMAN_REJECTION_DECISION.md`;
- décision humaine `P1_SPOT_CONTRACT_MULTIPLIER_DECISION.md`;
- `HYPOTHESIS.md`, décisions S1–S8, scénario, attentes, premier run, preuves, manifeste,
  résultat courant et artefacts `*_REJECTED_5967EE0`;
- contrats H0003, `spot_ledger.py`, exports, oracle, tests nominaux/mutants et runner;
- `STATUS.md`, `flake.lock`, `pyproject.toml` et objets Git nécessaires.

La filiation corrective est ancestrale :

```text
5967ee0 paquet rejeté
→ 6f12875 anciens rapports
→ 830c0c0 décision humaine de rejet
→ f2d45c9 décision normative multiplicateur/F1
→ 2c929d4 préservation des artefacts rejetés
→ 2e34736 correction de production
→ 419fe9d runner des régressions
→ e5f87b3 statut/code exécuté
→ fa32e2f preuves
→ d60e96a manifeste
→ 5f0253d enveloppe gelée
```

L'hypothèse, S1–S8, le scénario, les attentes, le premier run, l'oracle et les tests
nominaux gardent leurs hashes antérieurs. La décision `f2d45c9` précède le correctif de
production. Les anciens résultat, manifeste et preuves sont préservés sous noms distincts.

## Contrôles exécutés

| Contrôle | Résultat | Code |
|---|---|---:|
| `git rev-parse HEAD` | paquet exact `5f0253d9d9c552f310eabef5ae019219d828742c` | 0 |
| `git merge-base --is-ancestor` sur chaque arc correctif | filiation complète | 0 |
| `sha256sum` des artefacts manifestés | concordance complète | 0 |
| ancien résultat depuis `5967ee0` | `cb6582a1...1402594`, inchangé | 0 |
| nouveau résultat depuis `fa32e2f` | `65adcc70...80c72`, exact | 0 |
| blobs ledger/runner au code exécuté | hashes manifestés exacts | 0 |
| `nix develop --command pytest tests/hypotheses/H0004 -q` | `28 passed in 0.12s` | 0 |
| `nix develop --command just check` | Ruff OK; `163 passed`; couverture `91.81 %`; spot ledger 100 % | 0 |
| `nix develop --command python scripts/update_status.py --check` | `STATUS.md is current` | 0 |

## Reproduction des anciens findings

### F1a — triplet étranger cohérent

Un état SOL/USD initialisé a reçu le même triplet BTC cohérent que dans le rejet
historique. Le résultat est désormais :

```text
SPOT_STATE_INSTRUMENT_MISMATCH
state_after == state_before
```

Le rejet intervient après la priorité S8 mais avant validation économique, dérivation
d'écritures ou construction d'un nouvel état. Une substitution moins visible — même
`instrument_id`, autre tick/multiplicateur et référence au nouveau hash — est également
capturée par le hash canonique.

```text
status = CLOSED
impact = SUPPORTING
scope = F1a / STATE_INSTRUMENT_BINDING
```

### F1b — référence alternative

Une `ReferenceSpec` structurellement valide mais au contenu/hash différent produit :

```text
SPOT_STATE_REFERENCE_MISMATCH
state_after == state_before
```

`apply_fill` vérifie désormais les deux hashes de l'état. `apply_initialization`, qui ne
reçoit aucune référence, vérifie toute la liaison disponible : un instrument étranger
produit `SPOT_STATE_INSTRUMENT_MISMATCH` sans changement d'API ni mutation.

```text
status = CLOSED
impact = SUPPORTING
scope = F1b / STATE_REFERENCE_BINDING
```

### F2 — multiplicateur spot

Un instrument SPOT de multiplicateur `2/1`, accompagné d'une référence au hash exact,
est rejeté à la création par :

```text
SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED
```

Une attaque supplémentaire forgeant uniquement un état dont les hashes correspondent au
couple multiplicateur deux est aussi rejetée dans `apply_fill` par le même code. La formule
de transition est désormais littéralement :

```python
trade_quote = fill.quantity * fill.price
```

La décision humaine `f2d45c9` autorise précisément ce bornage `1/1 ONLY`; aucune algèbre
spot généralisée n'a été ajoutée.

```text
status = CLOSED
impact = SUPPORTING
scope = F2 / SPOT_CONTRACT_MULTIPLIER
```

## Non-régression du paquet initial

Les calculs indépendants restent :

```text
BUY notional       = 999/10
BUY quote total    = -100
after BUY          = 999/200 SOL, 0 USD, frais 1/10 USD
SELL quote net     = 998001/10000 USD
frais cumulés      = 1999/10000 USD
base finale        = 0
```

Les trois états et six `AccountEvent` gardent exactement leurs IDs S1, provenance S2,
signes, devises et ordre B6. Les variations de balances égalent la somme des écritures;
`fees_by_currency` reste informatif et n'est pas double compté. La valorisation ne mute
pas l'état. Le runner exécute F1a/F1b/F2 puis compare séparément oracle, états, écritures
et valorisations aux attentes gelées.

S8 reste le premier contrôle d'`apply_fill` : égalité et ordre décroissant sont rejetés
avant contexte et économie. Aucun tri de fills ni mémoire cachée n'a été ajouté. M1–M19,
y compris M18a–M18e, conservent leurs codes ou invariants.

## Recherche de nouvelles réfutations

Les attaques suivantes n'ont pas produit de divergence :

- instrument étranger de même ID avec propriétés neutralisées ou modifiées;
- référence alternative ne changeant pas les compatibilités H0003 mais changeant son hash;
- substitution de contexte après initialisation et après progression de fills;
- multiplicateur non-unitaire à la création et à la transition avec hashes réalignés;
- priorité S8 combinée à des specs incompatibles et à un fill économiquement invalide;
- initialisation avec instrument étranger;
- mutation potentielle après chaque rejet;
- fractions, conservation, cumul des frais, ordre des écritures et round-trip des inputs.

Aucune nouvelle convention comptable ou capacité hors scope n'a été nécessaire.

## Limites publiées

| ID | Statut | Impact | Scope | Effet exact |
|---|---|---|---|---|
| L1 | `TEST_STRENGTH_LIMIT` | non bloquant pour le code actuel | M18c | Le test statique interdit l'attribut `.sort` et certains noms de mémoire, mais ne prouverait pas à lui seul l'absence de `sorted(fills)` aliasé dans une future API de collection. L'API actuelle reçoit un fill individuel et l'inspection du code confirme l'absence de tri de fills. |
| L2 | `PUBLISHED_LIMIT` | non bloquant | initialisation | S8 ne gouverne que les fills. Les `AccountEvent(INITIALIZE)` explicites sont appliqués dans l'ordre fourni avant le premier fill; H0004 ne démontre pas un scheduler ou une déduplication stateful générale des initialisations. |
| L3 | `PUBLISHED_SCOPE_LIMIT` | non bloquant | P1 | Une seule trajectoire SPOT cash, frais quote et multiplicateur un est positivement démontrée. Short canonique, enforcement temporel et preuve P1 intégrée restent non prouvés. |

L1 est la limite de force demandée : elle porte sur le mutant statique M18c, pas sur S8
individuel. Le comportement individuel est directement exécuté et demeure conforme.

## Verdict et effet

Le paquet corrigé est testable, ancré et reproductible. F1a/F1b/F2 sont fermés sans
réécriture des attentes ni régression du nominal. Les limites restantes bornent la force
de certains tests ou le périmètre; elles ne contaminent pas l'énoncé H0004 corrigé.

Le verdict contradictoire est donc `ACCEPT_WITH_LIMITS`. Il doit être confronté au nouveau
rapport Critique puis soumis à une décision humaine distincte. Il n'admet pas H0004, ne
réhabilite pas `5967ee0` et maintient `P1 = NOT_PASSED`.
