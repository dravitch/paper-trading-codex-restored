# Rapport Contradictoire — Proposition de fusion contrôlée

## Objet examiné

Proposition §14 de `CONTROLLED_MERGER_FEASIBILITY.md` :
**« GO conditionnel pour une fusion contrôlée dans `paper-trading-codex-restored` »**, et le dossier de cadrage qui la soutient (`docs/fusion/`).

## Mandat

Agent **Contradictoire** : chercher activement à réfuter la proposition par contre-exemples, mutations, changements de référentiel, cas limites et hypothèses alternatives, avant toute lecture d'un éventuel verdict Critique.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision Git | `d82fb3a9db2c9e2a50dbb82d104ff4faf3d65913` |
| branche | `fusion/controlled-merger` |
| indépendance | aucun fichier `CRITIQUE*.md` présent dans le dépôt au moment du gel du verdict; premier verdict figé sans lecture d'une conclusion Critique |

## Fichiers examinés

- `CONTROLLED_MERGER_FEASIBILITY.md`
- `docs/fusion/README.md`, `00_CORPUS_TRACEABILITY.md`, `01_CONCEPT_DECISION_REGISTER.md`, `02_REFERENCE_MODEL.md`, `03_RISK_TAXONOMY.md`, `04_ENGINE_COMPATIBILITY.md`, `05_RISKMAP_ORACLES.md`, `06_FUSION_GATES.md`, `CANONICAL_CONTRACT_RFCS.md`, `PROTOCOL_CONTRADICTOIRE.md`, `HYPOTHESIS_BRANCH_REGISTER.md`
- `HYPOTHESIS.md`, `REV04.md`, `README.md`, `STATUS.md`, `REPRODUCIBILITY_MANIFEST.json`
- Code : `paper_trading_codex/strategies/grid_bot.py`, `core/portfolio_manager.py`, `core/exchange_simulator.py`, `core/data_fetcher.py`, `tests/conftest.py`
- `ARCHIVES/02_BIGET_PAPERTRADING/bitget-paper-trading/adapters/mock.py`, `core/signal_generator.py`, `tests/test_portfolio.py`, `shell.nix`

## Commandes exécutées

```text
git status / git log --oneline -15 / git rev-parse HEAD
python3 (calculs oracles indépendants, cf. infra)
grep -rn datetime.now|utcnow|random.|hash(  paper_trading_codex/
grep -n hash(symbol)|Timestamp  bitget-paper-trading/adapters/mock.py
grep -c def test_  bitget-paper-trading/tests/test_portfolio.py   -> 9
find bitget-paper-trading -name LICENSE*                            -> aucun
grep -ni "NO.GO|abandon|abort|critère d'arrêt|kill"  CONTROLLED_MERGER_FEASIBILITY.md -> aucune occurrence
python -m venv /tmp/opencode/ptvenv; pip install -e '.[test]'
python -m pytest tests -q   -> échec environnement (libstdc++.so.6 absent; wheel numpy C-extensions)
```

## Vérifications mécaniques indépendantes (recalcul)

| Assertion du dossier | Recalcul | Verdict |
|---|---|---|
| O1 Pareto `{A,B,D,E}` après déduplication sémantique | dominances recalculées; C dominé par B; F doublon de B | **confirmé** |
| spot 100 USD, frais 0,1 %/côté : perte 0,1999 | qty 4,995; cash rendu 99,8001 | **confirmé** |
| short : marge 300, notionnel 600, quantité 6, PnL brut 60 | `300 = 1000×0,3; 600 = 300×2; 6 = 600/100; 60 = 6×10` | **confirmé** |
| H3 seuil `E(1+1/L)/(1+m)` | 138,888… pour E=100, L=2, m=0,08 | **confirmé** sous les hypothèses déclarées (marge isolée, pas de funding, pas de frais de clôture, MMR constant) |
| O6 domaine `2×2×2 = 8` | 8 combinaisons | **confirmé** |
| mock Bitget non reproductible (`hash(symbol)` + `Timestamp.now()`) | `mock.py:41` `rng = default_rng(seed + hash(symbol) % 1000)`; `mock.py:45` `end=pd.Timestamp.now()` | **confirmé** (`hash` est salé par processus, `now()` est une horloge murale) |
| 9 tests Bitget centrés portefeuille | `test_portfolio.py`, 9 `def test_` | **confirmé** |
| shell Nix Bitget installe par réseau dans une venv | `shell.nix` : `virtualenv` + `pip install` dans `shellHook` | **confirmé** |
| projet restauré : timestamps injectés « quelques fallbacks » | `datetime.now()` présent à 4 sites (`grid_bot.py:408`, `portfolio_manager.py:66,157`, `exchange_simulator.py:90`) | **confirmé** — le dossier est honnête sur ce point |
| réseau bloqué dans les tests | `tests/conftest.py` fixture `socket` globale | **confirmé** statiquement |
| « 68 tests, 87,07 % » | **non reproductible dans cette session** : venv Python 3.12 échoue à l'import (`libstdc++.so.6` absent, wheel numpy C-extensions) | non falsifié, non prouvé ici |

Les oracles arithmétiques **résistent** à la réfutation. Les failles sont ailleurs : dans l'univocité des attendus et la complétude des mutations.

## Tentatives de réfutation maintenues (objections ouvertes)

Les limites suivantes conditionnent l'acceptation. Chacune doit être intégrée aux documents et aux gates, sans quoi le verdict reste bloquant pour les gates concernés.

### L1 — O2 n'est pas un attendu univoque (bloquant P6)
`05_RISKMAP_ORACLES.md` O2 admet deux attendus exclusifs (« contrainte dure préenregistrée » OU « objectif à minimiser, axe = 1 ») sans figer la politique. Un test qui tolère deux attendus peut être justifié a posteriori → violation de la règle « aucun évaluateur ne modifie silencieusement l'attendu après observation » (`PROTOCOL_CONTRADICTOIRE.md` §5). **Action : figer une seule politique et un seul attendu avant exécution.**

### L2 — O7 n'a pas de clé canonique définie (NON_TESTABLE)
O7 exige un « hash sémantique qui trie selon la clé canonique préalablement définie ». Cette clé n'est définie nulle part dans le dossier. Sans elle, l'attendu d'O7 est indécidable → **NON_TESTABLE en l'état**, ne peut soutenir un PASS P6.

### L3 — Les cas obligatoires de §9.4 ne sont pas tous oraculés
§9.4 impose : risque/rendement nuls, drawdown nul à rendement positif, métrique manquante ou infinie, domination sur un seul axe, objectifs contradictoires. O1–O7 et les paysages §9.10 ne couvrent pas explicitement ces cas. Risque d'attendu a posteriori pour le premier run qui les rencontre. **Action : ajouter les oracles manquants ou déclarer ces cas NON_TESTABLE.**

### L4 — O4 embarque une règle de voisinage implicite
O4 qualifie le point 3 de « FRAGILE » parce que « son voisinage droit échoue », sans déclarer le rayon du voisinage ni les contraintes de la région admissible que définit §9.7. La règle n'étant pas opérationnalisée, un implémenteur peut la calibrer pour faire passer O4. **Action : déclarer la règle de voisinage préalablement au run.**

### L5 — Tension entre l'invariant hash §8 et la tolérance §8.4 (bloquant P2)
§8 pose `hash(ResultBundle(backtest)) == hash(ResultBundle(replay))` comme « invariant initial » (égalité exacte), alors que §8.4 admet une « tolérance annoncée avant le run ». Une égalité bit-exacte et une tolérance ne coexistent pas sans convention de sérialisation canonique (ou hash sur valeurs tolérées). RFC-008 introduit bien le « hash sémantique », mais l'invariant ne le mentionne pas. **Action : trancher avant P2** — sinon P2 est indécidable.

### L6 — Mutations de gates incomplètes (P1, P3)
La matrice `06_FUSION_GATES.md` ne teste jamais la réintroduction des deux péchés cardinaux que le dossier prétend bannir :
- P1 (domaine) : aucune mutation « réintroduire `now()` / retirer l'horloge injectée », alors que CD-019 est central;
- P3 (stratégies) : aucune mutation « la stratégie accède à un provider / à l'horloge », alors que CD-004 est central.

Sans ces mutations, les gates peuvent passer avec les violations exactes que la discipline interdit. **Action : ajouter ces mutations aux critères PASS des gates.**

### L7 — Convention de règlement des frais non déclarée dans l'oracle spot
L'oracle 0,1999 USD suppose implicitement des frais prélevés en numéraire sur chaque jambe. Un règlement en nature (SOL) sur la jambe de vente modifie la quantité livrée et le résultat. Le `ReferenceSpec` (§2) et `ExecutionSpec` (§6.4) doivent fixer la devise de règlement des frais, faute de quoi l'oracle lui-même devient une convention non déclarée (l'exact défaut que le dossier reproche aux archives).

### L8 — Aucun critère NO-GO de la fusion
Ni §14 ni §10 ne définissent les conditions d'abandon de la fusion. Un « GO conditionnel » sans condition de non-continuation est une porte à sens unique : risque d'engagement croissant si P1–P4 révèlent une contradiction irréductible. **Action : déclarer explicitement les conditions de NO-GO (ex. deux gates consécutifs bloqués pour la même cause, ou invariant de ledger démontré inatteignable).**

### L9 — Licence des composants portés non traitée
Le dépôt Bitget ne contient aucun fichier `LICENSE`/`COPYING`. §11 et Phases 3–5 portent des composants de ce dépôt sans traiter l'attribution et la compatibilité de licence. P7 mentionne « licence » sans exigence de traçabilité. **Action : documenter l'origine et la licence de chaque composant porté avant P3.**

### L10 — Dérive terminologique des contrats de compte
`IsolatedMarginModel` (feasibility §3.1), `IsolatedShortModel` (`04_ENGINE_COMPATIBILITY.md`), `ISOLATED_LINEAR_SHORT_EDU` (RFC-005) désignent le même concept sous trois noms. Une discipline de « contrats canoniques » exige un nommage unique avant P1.

### L11 — P0 dépend de preuves non reproduites
« 68 tests, 87,07 % » n'a pas pu être reproduit dans cette session (échec d'environnement : `libstdc++.so.6` absent, wheel numpy incompatible). Ce n'est pas une réfutation, mais cela rappelle la règle du dossier : un nombre n'est pas une preuve sans environnement déclaré et réexécution. **Action : figer et publier les hashes + commandes P0 des deux dépôts (ce que §15.3 exige déjà) ; le présent échec de reproduction est un motif de vérifier le protocole de verrouillage, pas un échec du projet.**

### L12 — Indépendance limitée des oracles
Les oracles dépendants de définitions (O2, O4, O7) sont produits par le même processus d'auteur que l'implémentation future. Les oracles arithmétiques ont été recalculés ici et sont corrects, mais l'indépendance réelle des oracles définitionnels n'est pas établie tant que leurs règles (L1, L2, L4) ne sont pas figées par une instance tierce.

## Tentatives de réfutation rejetées

- La « neutralité fournisseur » n'est pas démontrée avant P4 : **reconnu** par le dossier (« provider-neutral by design, unknown in practice ») — pas une contradiction, un statut déclaré.
- La fusion exige un « schéma canonique » qui pourrait fuiter la sémantique des providers : risque géré par les profils F0–F4 et le risque « schéma appauvri » (§12); non réfutant dans le domaine déclaré.
- Les projets n'ont pas de concepts interchangeables (SELL, numéraire, horloges) : le dossier l'énonce lui-même (§3.2) et en tire la stratégie « contrat par contrat » — cohérent, non réfutant.
- L'horloge murale subsiste dans le code restauré : annoncé honnêtement (« quelques fallbacks ») et traité par P1; devient bloquant uniquement via L6 (mutation manquante).

## Verdict

**ACCEPT_WITH_LIMITS**

Le GO conditionnel **n'est pas réfuté** dans son domaine déclaré (laboratoire de replay et de risque, premier incrément sans Bitget). Les oracles arithmétiques résistent au recalcul. Toutefois :

- les limites **L1, L2, L3, L5** rendent O2, O7, les cas obligatoires §9.4 et l'invariant P2 **NON_TESTABLE en l'état** — elles bloquent les gates P2 et P6 tant qu'elles ne sont pas figées en attendus univoques;
- les limites **L6, L8, L9, L10** doivent être intégrées aux documents et aux gates avant P1;
- les limites **L7, L11, L12** sont des exigences de déclaration à intégrer dès P0/P1.

Conformément au protocole, cette acceptation conditionnelle ne vaut pas validation et ne suffit pas à franchir un gate. Aucune hypothèse `hypothesis/HNNN-*` n'est concernée : le registre des branches reste vide.
