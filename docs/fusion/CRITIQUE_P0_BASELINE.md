# Rapport Critique — Preuve P0 des deux baselines

## 1. Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Critique indépendante du gate P0 |
| modèle | Claude (interface de chat Anthropic), identité de version non auto-déclarable de façon fiable |
| date | 2026-08-08 |
| révision Git examinée | `d1ed53b1b63d3b6d06ad8edcf64dc4655a3574da` (`P0_EVIDENCE_COMMIT`, branche `correction/reconcile-l1-l12`), **et non** le HEAD ultérieur `5ed9f07` |
| indépendance | aucune conclusion Contradictoire de ce dossier P0 lue avant le gel de ce verdict |

**Écart méthodologique déclaré par rapport au mandat** : le mandat suppose que je n'ai « pas accès à un environnement d'exécution fiable ». C'est faux dans cette session : je dispose d'un bash réel avec accès réseau vers `github.com` et `pypi.org`. J'ai donc, au-delà de l'analyse documentaire demandée, **réellement cloné et réexécuté** une partie des preuves Bitget dans un environnement tiers (ni Nix, ni la VM Proxmox du Producteur). Cela ne remplace pas une réexécution dans l'environnement exact déclaré (NixOS 26.05, `systemd-run -p PrivateNetwork=yes`), mais constitue une reproduction indépendante plus forte qu'une simple lecture.

## 2. Périmètre d'accès et fichiers lus

Dépôt cloné : `https://github.com/dravitch/paper-trading-codex-restored` (branche `correction/reconcile-l1-l12`).

Au commit gelé `d1ed53b` :
- `docs/fusion/P0_BASELINE_EVIDENCE.md`
- `PROGRESSION.md`
- `docs/fusion/06_FUSION_GATES.md`
- `docs/fusion/COMPONENT_PROVENANCE.md`
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md` (registre L1–L12 et addendum P0)
- `docs/fusion/PROTOCOL_CONTRADICTOIRE.md`
- `docs/fusion/REVIEW_ADMISSION_REGISTRY.md`

Dépôt tiers cloné et inspecté au commit cité : `https://github.com/dravitch/bitget-paper-trading` à `f2e41890dd5950eb36456503b357bfb76be9ed47` (fichiers : `LICENSE`, `requirements.txt`, `paper_trading/__init__.py`, `paper_trading/portfolio.py`, `tests/test_portfolio.py`, arborescence complète `git ls-files`).

Je n'ai ni accès à la VM Proxmox VMID 110, ni aux artefacts hors dépôt (manifestes `pip freeze`, rapport Coverage XML bruts, dépôt KB local sans remote) : ces éléments restent `UNKNOWN` pour moi, au sens strict — je ne peux confirmer que leur hash déclaré est interne à un document que je ne peux pas recalculer indépendamment.

Je n'ai exercé aucune autorité Git : aucun `add`/`commit`/`push`/`merge` sur le dépôt examiné.

## 3. Commandes réellement exécutées

```text
git clone --branch correction/reconcile-l1-l12 https://github.com/dravitch/paper-trading-codex-restored.git
git show d1ed53b:docs/fusion/P0_BASELINE_EVIDENCE.md   (+ 6 autres fichiers listés en §2)
git ls-remote https://github.com/dravitch/bitget-paper-trading.git
git ls-remote https://github.com/dravitch/paper-trading-codex-restored.git
git clone https://github.com/dravitch/bitget-paper-trading.git ; git checkout f2e41890...
sha256sum LICENSE
git ls-files | wc -l ; git ls-files | sort | sha256sum
grep -c "^    def test_\|^def test_" tests/test_portfolio.py
python3 -m venv (x2 : bare, puis avec deps) ; pip install pytest [+ deps progressives]
python -m pytest --collect-only -q   (répété à chaque palier de dépendances)
python -m pytest -v --no-header
pip install pytest-cov coverage
python -m pytest --cov=. --cov-report=term-missing -q
python -m pytest --cov=paper_trading --cov-report=term-missing -q
python -m pytest --cov=core --cov=paper_trading --cov=adapters --cov-report=term-missing -q
git ls-tree -r --name-only 5bac10b -- tests/  (+ comptage def test_ par fichier, dépôt restauré)
grep -c parametrize sur les 7 fichiers de tests du dépôt restauré
```

Codes de sortie : tous `0` sauf les collectes intermédiaires volontairement incomplètes (`ModuleNotFoundError`, code 2 implicite via interruption pytest), documentées comme telles.

## 4. Matrice des huit assertions Producteur

| # | Assertion | Verdict | Justification / source |
|---|---|---|---|
| 1 | Baseline restaurée : 68 tests, 87,07 %, Ruff 0, exit 0 sous Nix | `PARTIALLY_SUPPORTED` | Non réexécutée dans l'environnement Nix exact (hors périmètre déclaré comme distinct dans ce même document, et déjà couverte par les cycles Contradictoire antérieurs — `CONTRADICTOIRE_DELTA_09653E2.md`, `ACCEPT_WITH_LIMITS`). Comptage indépendant des `def test_` sur les 7 fichiers = 55, pas 68 ; l'écart (13) est plausiblement expliqué par 6 décorateurs `@pytest.mark.parametrize` détectés, mais je n'ai pas exécuté une collecte réelle pour confirmer le compte exact de 68. Voir objection O1. |
| 2 | Baseline Bitget dans VM NixOS 26.05, namespace sans réseau : 9 collectés, 9 réussis, exit 0 | `SUPPORTED` pour le résultat fonctionnel ; `UNKNOWN` pour l'infrastructure exacte | J'ai reproduit indépendamment, dans un environnement Linux générique (ni Nix, ni VM, ni isolation réseau — réseau non nécessaire car les tests ne l'utilisent pas) : `9 tests collected`, `9 passed`, exit 0. Le résultat fonctionnel est donc confirmé par une voie totalement indépendante. Je ne peux ni confirmer ni infirmer les détails d'infrastructure (Proxmox, NixOS 26.05, `systemd-run -p PrivateNetwork=yes`) : `UNKNOWN`, non contradictoire. |
| 3 | Couverture Bitget instrumentée : 38 % global, 80 % pour `paper_trading/portfolio.py` | `SUPPORTED` avec réserve de périmètre | Reproduit **exactement** (`TOTAL 38%`, `portfolio.py 80%`) avec `--cov=paper_trading`. Sous `--cov=.` (tout le dépôt instrumenté, `adapters/`, `core/`, `main.py` inclus), j'obtiens `36 %`. Le mot « globalement » est ambigu sans préciser le périmètre `--cov`. Voir objection O2. |
| 4 | Les deux échecs préalables (`colorama`, puis `libstdc++.so.6`) sont reproductibles et correctement interprétés | `PARTIALLY_SUPPORTED` | Le mécanisme causal sous-jacent (couplage précoce de `paper_trading.portfolio` à des dépendances d'adaptateurs sans rapport avec la comptabilité) est confirmé et même renforcé : dans un venv strictement vide, mon premier blocage est `loguru` (importé directement en ligne 9 de `portfolio.py`), pas `colorama`. Le second palier (`pandas`) puis un troisième non rapporté par le Producteur (`ccxt`, importé transitivement via `adapters/__init__.py → adapters/bitget.py`) sont bien rencontrés en cascade. L'échec `libstdc++.so.6` est lié à l'environnement Nix/liaison C et n'est pas reproductible ni réfutable hors de cet environnement : `UNKNOWN`, non contradictoire. Voir objection O1. |
| 5 | Licence MIT présente au commit Bitget examiné, SHA-256 rapporté, sans rétroagir sur l'ancien commit | `SUPPORTED` | `sha256sum LICENSE` au commit `f2e41890...` = `dd10b10e2f68cef2e58683088bd1f3ff2194ba1151f15191cc60aed742365c83`, identique au SHA-256 déclaré. `git ls-files \| wc -l` = 22, identique au « manifeste des 22 fichiers Git suivis ». Aucune trace de licence rétroactive sur l'ancien commit `adc1d275...` (non ré-examiné ici, cohérent avec `COMPONENT_PROVENANCE.md`). |
| 6 | Concordance ponctuelle des branches distantes via `git ls-remote`, sans preuve de protection contre le force-push | `SUPPORTED` | `git ls-remote` (exécuté par moi, à une date postérieure) confirme toujours `f2e41890...` sur `refs/heads/claude/explore-code-cloud-Hm5n9` et `5ed9f07...` en tête de `correction/reconcile-l1-l12` (avec `5bac10b` comme ancêtre attesté). Aucune règle de protection de branche exportée n'est trouvée nulle part dans le dossier examiné : la réserve du Producteur est honnête et reste d'actualité. |
| 7 | La suite Bitget verte prouve l'exécutabilité historique, pas la validité scientifique ni la fidélité au marché | `SUPPORTED` | Le document ne formule à aucun moment une revendication de performance ou de fidélité ; les neuf tests examinés (`test_portfolio.py`) exercent un `PortfolioManager` réel avec des assertions non tautologiques (aucune assertion `True`/self-mockée détectée), mais restent des tests unitaires de comptabilité simple, sans lien avec une exécution de marché réelle — cohérent avec la portée déclarée. |
| 8 | P0 doit rester `PARTIAL` tant que preuve d'immuabilité et deux revues ne sont pas admises | `SUPPORTED` | `docs/fusion/REVIEW_ADMISSION_REGISTRY.md` (même commit) exige explicitement une preuve de protection distante exportée/hashée ou une archive Git signée « avant toute exécution ou revendication de P6 » ; aucun artefact de ce type n'existe dans le dossier. La présente revue Critique est elle-même l'une des deux revues requises — elle ne suffit pas seule à clore P0. |

## 5. Recherche de circularité, surinterprétation, confusion tests-verts/validité

- Aucune circularité au sens strict (un oracle qui réutiliserait le code testé) n'est détectée dans `test_portfolio.py` : les neuf tests appellent l'implémentation réelle et vérifient des valeurs numériques calculables indépendamment (ex. `quantity == pytest.approx(1000.0/50_000.0)`), pas des invariants triviaux.
- Point de vigilance mineur, non bloquant : le tableau « Périmètre » de `P0_BASELINE_EVIDENCE.md` cite la propre branche du dépôt examiné (`paper-trading-codex-restored`, `correction/reconcile-l1-l12`) comme faisant l'objet d'une vérification de provenance distante — un dépôt qui atteste de son propre commit via `ls-remote` sur lui-même est structurellement auto-référentiel. Ce n'est pas la circularité dangereuse visée par le protocole (un test qui prouverait le code par le code), simplement une note de forme.
- Aucune confusion entre « tests verts » et « validité scientifique/fidélité au marché » n'est commise nulle part dans le dossier P0 : la formulation est systématiquement prudente (« ne vaut ni admission humaine, ni revue Critique/Contradictoire, ni PASS »).

## 6. Objections

### O1 — Sévérité MODÉRÉE : narration causale imprécise des échecs Bitget et compte de tests non recollecté

**Preuve** : reproduction indépendante en §4 (assertions 1 et 4). Le document attribue le premier blocage à `colorama` et décrit la chaîne comme « `paper_trading.portfolio` exécute `paper_trading/__init__.py`, qui importe avidement `engine`, puis les dépendances des adaptateurs » — cela omet que `paper_trading/__init__.py` importe d'abord `.portfolio` elle-même (ligne 1), laquelle importe directement `loguru` (ligne 9 de `portfolio.py`), **avant** même d'atteindre `.engine` (ligne 2). Le nom du module bloquant en premier dépend donc entièrement de l'ordre d'installation local du Producteur, pas d'une propriété stable du code. De même, le compte de 68 tests pour le dépôt restauré n'a pas été recollecté ici (55 `def test_` détectés + 6 `parametrize`, plausible mais non confirmé par une collecte réelle).

**Effet** : le mécanisme sous-jacent dénoncé (couplage précoce non nécessaire) reste vrai et même renforcé (j'ai trouvé un troisième palier, `ccxt`, non mentionné). Il ne s'agit donc pas d'une contradiction de fond, mais d'une imprécision de traçabilité — exactement le type de défaut que ce projet se donne pour discipline de traquer (« aucune affirmation sans source », `06_FUSION_GATES.md` P0).

**Correction attendue** : reformuler la description du chaînage d'imports comme dépendante de l'état d'installation local plutôt que comme une séquence figée ; recollecter les 68 tests du dépôt restauré dans l'environnement Nix déclaré et joindre la sortie brute (actuellement seul le chiffre agrégé est cité, sans log de collecte).

### O2 — Sévérité FAIBLE : ambiguïté de périmètre pour « couverture 38 % globalement »

**Preuve** : reproduction exacte en §4 (assertion 3). `38 %` n'est vrai que sous `--cov=paper_trading` (465 lignes instrumentées) ; sous `--cov=.` (898 lignes, tout le dépôt), le total est `36 %`.

**Effet** : un lecteur non averti peut croire que 38 % couvre l'intégralité du code Bitget observable, alors que `adapters/`, `core/signal_generator.py` et `main.py` sont exclus du calcul cité. Le nombre lui-même n'est pas faux, mais son qualificatif « globalement » est trompeur sans la commande exacte.

**Correction attendue** : citer explicitement la commande `--cov=paper_trading` utilisée, ou recalculer et publier également le chiffre `--cov=.` (36 %) à titre de comparaison, conformément à la propre règle de couverture de `06_FUSION_GATES.md` (« commande exacte et exit code »).

### O3 — Sévérité FAIBLE, non bloquante : artefacts hors dépôt non vérifiables par un tiers

**Preuve** : les hashes de manifeste `pip freeze` (avant/après instrumentation), le rapport Coverage XML et les commits KB (`ac3a3ee`, `27fa89b`) ne sont accessibles que sur la VM Proxmox et un dépôt KB local sans remote.

**Effet** : ces preuves restent, pour tout relecteur externe (Critique ou Contradictoire), des affirmations non vérifiables — le document le reconnaît lui-même implicitement (statut `PRODUCER_EVIDENCE_PENDING_INDEPENDENT_REVIEW`), donc ce n'est pas une contradiction, mais cela borne strictement ce que « revue indépendante » peut réellement couvrir tant que ces artefacts ne sont pas versés dans le dépôt Git principal ou un stockage accessible.

**Correction attendue** : avant la fermeture définitive de P0, committer (ou lier via une preuve hashée accessible) au moins le `pip freeze` final et le `coverage.xml`, pour permettre une vérification tierce complète.

## 7. Conditions exactes de fermeture P0

Aucune trouvée ni ajoutée en contradiction avec `PROGRESSION_TEMP.md` §« Conditions Producteur de fermeture P0 » et `REVIEW_ADMISSION_REGISTRY.md`. Pour rappel, la fermeture exige cumulativement :

1. intégration explicite des objections O1–O3 ci-dessus (ou justification documentée de leur non-intégration) ;
2. admission humaine explicite de ce rapport et du rapport Contradictoire correspondant, dans un commit distinct indexé au registre ;
3. preuve de protection distante (anti force-push/suppression) exportée et hashée, **ou** archive Git signée couvrant les commits P0 — actuellement absente, ce qui à lui seul interdit la fermeture ;
4. contrôle final des ancêtres et SHA-256 après admission ;
5. passage explicite de P0 à `PASS` dans `PROGRESSION.md`, `06_FUSION_GATES.md` et `LIMIT_RESOLUTION_REGISTER.md` — non fait ici, et ne doit pas l'être par cette revue.

## 8. Verdict

**`ACCEPT_WITH_LIMITS`**

Les huit assertions Producteur résistent globalement à une vérification indépendante réelle (et non seulement documentaire) : licence, nombre de fichiers, nombre de tests Bitget, exécution verte et couverture ont tous été reproduits par une voie totalement indépendante de l'infrastructure du Producteur, avec des résultats identiques ou plus favorables (mécanisme de couplage confirmé et étendu). Aucune contradiction de fond n'est trouvée.

Les limites **O1** (précision de la narration causale + recollecte des 68 tests) et **O2** (périmètre explicite de la couverture) doivent être intégrées avant que ce dossier serve de preuve définitive de P0. **O3** est une limite structurelle à lever avant fermeture, pas une faute du Producteur.

P0 reste, conformément au verdict Producteur lui-même, `PARTIAL` : cette revue Critique ne franchit aucun gate, ne valide aucune hypothèse `hypothesis/HNNN-*`, et la preuve d'immuabilité distante exigée par `REVIEW_ADMISSION_REGISTRY.md` demeure absente.
