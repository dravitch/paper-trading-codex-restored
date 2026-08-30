# H0004 — Revue Critique indépendante du paquet corrigé

## Verdict figé

**`ACCEPT_WITH_LIMITS`**

Les contre-exemples admis F1a, F1b et F2 sont fermés avec les codes décidés, avant toute
mutation. La formule spot redevient exactement `quantity × price`; scénario, oracle, six
écritures, S8 et M1–M19 ne régressent pas. Aucune nouvelle réfutation du paquet corrigé
n'a été trouvée. La force limitée du contrôle M18c et le scope strictement H0004 restent
publiés.

Ce verdict n'admet pas H0004 et ne déclare pas `P1 PASS`.

## Identité, révision et indépendance

| Champ | Valeur |
|---|---|
| Rôle | `IA_CRITIQUE_INDEPENDANTE` |
| Agent | `OpenAI Codex` |
| Version du modèle | `UNKNOWN` |
| Date | `2026-08-30` (`America/Toronto`) |
| Branche | `hypothesis/H0004-minimal-spot-ledger` |
| Paquet corrigé gelé | `5f0253d9d9c552f310eabef5ae019219d828742c` |
| Manifeste corrigé | `d60e96ad7192c9b448aedea1ac19e2c6d2d4fe21` |
| Code Producteur exécuté | `e5f87b3b7567be048d7c77479e3c96339dcaa56e` |
| Paquet rejeté historique | `5967ee06f85bb4b52e0e3bb6fafb19b2856d63db` |
| Rapports rejetants | `6f128758a9c07a5f1bc7ef4fac6c264d794ee9b6` |
| Décision humaine de rejet | `830c0c02e60c8171d43e69a6c9d251365b39e49f` |
| Décision multiplicateur | `f2d45c9a7ba79adcb1b94e51a6d295b48d8fe66e` |
| Indépendance | `PROCEDURAL / ROLE-SEPARATED` |

Les anciens rapports `CRITIQUE.md` et `CONTRADICTOIRE.md` ont été lus comme contexte
historique explicitement requis. Le nouveau `CONTRADICTOIRE_CORRECTION.md` n'a été ni
ouvert, ni lu, ni modifié. La séparation de rôle ne revendique ni IV&V organisationnelle,
ni indépendance statistique, d'auteur ou de modèle, ni réplication externe.

## Mandat et sources examinées

`CORRECTION_REVIEW_REQUEST.md` a été lu intégralement. Ont également été examinés :

- la décision humaine de rejet et la décision normative du multiplicateur;
- hypothèse, décisions S1–S8, scénario et attentes oracle;
- ancien et nouveau `RESULT`, `MANIFEST` et `EVIDENCE`;
- `FIRST_RUN.json`, observations protocolaires et statut;
- contrats H0003, exports, `spot_ledger.py`;
- oracle, tests nominaux, mutants/régressions et runner H0004;
- historique et différences Git du paquet rejeté au paquet corrigé.

## Provenance et conservation historique

Chaque arc suivant est ancestral :

```text
5967ee0 → 6f12875 → 830c0c0 → f2d45c9 → 2c929d4
→ 2e34736 → 419fe9d → e5f87b3 → fa32e2f → d60e96a → 5f0253d
```

Le paquet `5967ee0` reste rejeté. Ses artefacts sont préservés séparément avec leurs
empreintes originales :

```text
RESULT_REJECTED   cb6582a112e577b0508c39f15c2c2dc5107af7a11bd9124d6a76db3051402594
MANIFEST_REJECTED 707deeb0f747396118bb48d1320fcce8ad31a368cd049bd54613c056f4eed2e1
EVIDENCE_REJECTED be02c2761a13e836d647fc05ddd8c3d9c1f67a6e15ae923c66e56c66763bf63d
```

L'hypothèse, S1–S8, le scénario et `ORACLE_EXPECTATIONS.json` sont inchangés depuis le
premier paquet. La seule décision normative nouvelle est humaine, antérieure au correctif,
et borne explicitement `SPOT_CASH_V1` à `contract_multiplier=1/1`.

## Fermeture de F1a — liaison InstrumentSpec

Avant toute validation économique ou construction d'écriture, `apply_fill` exige :

```text
state.instrument_spec_sha256 == instrument.canonical_sha256()
```

Un triplet BTC fill/instrument/reference cohérent présenté à l'état SOL produit désormais
`SPOT_STATE_INSTRUMENT_MISMATCH`. `apply_initialization` applique la même liaison
instrument disponible sans changer son API et rejette également l'instrument BTC avec ce
code.

Les appels ont été exécutés en conservant une référence vers l'état avant rejet; l'état
reste identique. Comme `SpotAccountState` est immuable et que les contrôles précèdent tout
calcul de nouvel état, aucune mutation partielle n'est observée. **F1a est fermée.**

## Fermeture de F1b — liaison ReferenceSpec

`apply_fill` exige également :

```text
state.reference_spec_sha256 == reference.canonical_sha256()
```

La référence alternative exacte du contre-exemple (`numeraire="EUR"`) produit
`SPOT_STATE_REFERENCE_MISMATCH`; l'état reste inchangé. `apply_initialization` ne reçoit
pas et n'utilise pas de `ReferenceSpec`, conformément à son API préexistante : elle vérifie
toute la liaison disponible, sans ajout silencieux de paramètre. **F1b est fermée.**

## Fermeture de F2 — multiplicateur spot

La décision humaine `f2d45c9` ferme avant correction :

```text
SPOT_CASH_V1.contract_multiplier = 1/1 ONLY
trade_quote = quantity × price
```

`create_spot_account` rejette le multiplicateur `2` avec
`SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED`. `apply_fill` répète la garde : même en forgeant un
état dont les deux hashes correspondent exactement aux specs multiplicateur `2`, la
transition est rejetée avec le même code et l'état reste inchangé. Le code nominal calcule
désormais seulement `fill.quantity * fill.price`. **F2 est fermée.**

## Priorités et substitutions de contexte

L'ordre d'`apply_fill` reste : S8, modèle spot, liaison instrument, liaison référence,
garde multiplicateur, validations H0003, devise spot, puis solvabilité et construction.
Ainsi :

- égalité de clé reste `SPOT_FILL_REAPPLICATION` avant contexte ou économie;
- clé moindre reste `SPOT_FILL_OUT_OF_ORDER` avant contexte ou économie;
- pour une clé admissible, les specs étrangères sont rejetées avant toute transition;
- une variation neutralisée de référence est détectée par son hash canonique;
- une variation de multiplicateur ne peut contourner la garde en alignant artificiellement
  les hashes d'état.

Ces priorités sont conformes à S8 et à la décision corrective.

## Oracle, écritures et non-régression

L'oracle demeure indépendant du ledger et calcule les mêmes fractions :

```text
BUY q×p = 999/10; quote final BUY = 0; base = 999/200
SELL quote net = 998001/10000; base final = 0
fees total = 1999/10000
```

Les trois états, les six `AccountEvent`, leurs IDs/provenances/devises/signes et leur ordre
B6 sont inchangés et égaux aux attentes. La conservation explique chaque variation de
balance; `fees_by_currency` reste un cumul positif informatif non compté deux fois. La
valorisation demeure pure.

Les 28 tests ciblés conservent M1–M19, M18a–M18e et ajoutent les quatre régressions de
reviewers. Les changements nécessaires dans M5/M19 alignent explicitement le hash de
référence de l'état pour atteindre l'invariant historique visé; ils ne l'affaiblissent pas.

## Hashes, résultat et commandes reproduites

Tous les SHA-256 du manifeste concordent, notamment :

```text
decision_multiplier d870ace0206128236a17438b560c559e066fb287bd2a4e29e80088ab4547fcd4
spot_ledger.py       8cd52e9bc4fadae88db41924f427e5aba7818e37291d108230a8cacb33e710b4
mutants/regressions  7cd04250d6c9ecefca73084d4ad534ea322aaf74f682e140d402255d3c3ab6f4
runner               1e24e718113264d12e15dc556cd74d82eaa374132073d2e7bfb73384f31e63ba
RESULT.json          65adcc700a8021010c6e8a70121b54216c44f1dd11b2b7c63d5786330e780c72
```

Le runner exécuté dans un clone détaché à `e5f87b3` reproduit `RESULT.json` octet pour
octet et inscrit F1a/F1b/F2 à `true`.

```text
nix develop --command pytest tests/hypotheses/H0004 -q
→ 28 passed in 0.13s; code 0

nix develop --command python -m tests.hypotheses.H0004.run_experiment \
  --output /tmp/h0004-correction-result.json
→ SHA-256 65adcc70…80c72; aucune différence; code 0

nix develop --command just check
→ Ruff OK; 163 passed; couverture globale 91.81 %;
  spot_ledger.py lignes/branches 100 %; code 0

nix develop --command python scripts/update_status.py --check
→ STATUS.md is current; code 0
```

## Findings classés et recherche de nouvelles réfutations

| ID | Statut | Impact | Scope | Constat |
|---|---|---|---|---|
| RC1 | `CLOSED` | `SUPPORTING` | `F1a` | Specs étrangères cohérentes et initialisation étrangère rejetées par le hash instrument avant mutation. |
| RC2 | `CLOSED` | `SUPPORTING` | `F1b` | Référence alternative rejetée par le hash référence avant mutation. |
| RC3 | `CLOSED` | `SUPPORTING` | `F2` | Multiplicateur différent de un rejeté à la création et à la transition; formule `q×p` restaurée. |
| RC4 | `CONFIRMED` | `SUPPORTING` | `H0004` | Oracle, six écritures, conservation, S8 et M1–M19 ne régressent pas. |
| L1 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `M18c` | M18c inspecte statiquement la surface actuelle et l'API applique un fill individuel; il ne constitue pas une preuve générale qu'aucun futur caller/adapter ne triera une collection avant appel. S8 garantit seulement que le ledger individuel ne trie pas et rejette une clé non croissante. |
| L2 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `STATE_TRUST_BOUNDARY` | Un état publiquement forgé peut choisir des hashes arbitraires; les transitions garantissent la cohérence avec les hashes déclarés, pas l'authenticité historique de la construction de cet état. Les contre-exemples fermés utilisent les APIs nominales; aucune persistance/signature d'état n'est revendiquée. |
| L3 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `H0004` | Preuve positive limitée à `SPOT_CASH_V1`, multiplicateur un, frais quote et trajectoire BUY/SELL figée. |
| L4 | `PUBLISHED_LIMIT` | `NON_BLOCKING` | `P1` | Modèle short canonique, enforcement temporel et preuve intégrée P1 restent non prouvés. |
| P1 | `STATUS` | `NOT_PASSED` | `GATE` | Aucun résultat ou rapport H0004 ne suffit à franchir P1. |

Attaques additionnelles sans nouvelle réfutation : triplet étranger cohérent, référence
neutralisée, initialisation avec instrument étranger, multiplicateur deux à la création,
état artificiellement aligné au multiplicateur deux, priorités S8 contre contexte invalide,
immutabilité après rejet, champs relationnels H0003, grilles, devises, conservation,
double comptage de frais, ordre des écritures et absence de mémoire cachée.

## Conclusion

**`ACCEPT_WITH_LIMITS`**

Le paquet corrigé ferme F1a/F1b/F2 dans la portée décidée sans réhabiliter le paquet
historique rejeté et sans altérer les preuves nominales. Les limites L1–L4 doivent rester
publiées; elles ne contaminent pas la conclusion H0004 bornée.

Ce rapport est uniquement le verdict Critique. Toute admission demeure une décision
humaine ultérieure; `P1` reste `NOT_PASSED`.
