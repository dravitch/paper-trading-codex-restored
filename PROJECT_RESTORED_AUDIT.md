# Audit technique du projet restauré Paper Trading Codex 1.1.2

> Rapport historique de la phase de restauration. Il est supersédé pour la publication par `PROJECT_PUBLICATION_AUDIT.md`.

## 1. Résumé global

| Élément | Résultat vérifié |
|---|---|
| Source restaurée | `paper-trading-codex-v1.1.2` |
| Copie propre | `paper-trading-codex-restored` |
| Original modifié | Non |
| Environnement | Flake Nix verrouillé, Python 3.12.12 |
| Collecte Pytest | 21 tests collectés |
| Tests | 21 réussis, 0 échec, 0 erreur, 0 ignoré |
| Durée finale | 1,32 s |
| Couverture lignes + branches | 49,01 % |
| Imports des modules | Réussis |
| Configurations YAML | 4/4 parsées |
| Construction du paquet | `sdist` et wheel construits avec succès |
| Appels réseau applicatifs | Aucun pendant les tests |
| Secrets inclus | Aucun `.env` copié ; aucun secret ajouté |

Le noyau testé est fonctionnel : tous les tests métier présents passent. Le projet n'est pas encore prêt pour une publication sans réserve en raison d'une couverture faible sur le chargement de données et le connecteur Bitget, de 48 erreurs Ruff, d'une structure de paquet nommée `src`, de configurations non uniformes et de scripts Nix qui déclenchent encore des installations `pip` automatiques lorsqu'ils sont utilisés directement.

Le statut recommandé est **release candidate technique**, pas « production ready ».

## 2. Structure du projet restauré

```text
paper-trading-codex-restored/
├── README.md
├── PROJECT_RESTORED_AUDIT.md
├── pyproject.toml
├── setup.py
├── requirements.txt
├── flake.nix
├── flake.lock
├── shell.nix
├── devenv.nix
├── justfile
├── configs/
│   ├── grid_bot_green.yaml
│   ├── grid_bot_yellow.yaml
│   ├── grid_bot_red.yaml
│   └── grid_bot_optimal.yaml
├── src/
│   ├── analysis/
│   │   ├── benchmarks.py
│   │   └── performance.py
│   ├── core/
│   │   ├── data_fetcher.py
│   │   ├── data_loader.py
│   │   ├── exchange_simulator.py
│   │   └── portfolio_manager.py
│   └── strategies/
│       └── grid_bot.py
├── tests/
│   ├── test_critical_5_5.py
│   └── test_grid_bot.py
├── examples/
├── scripts/
└── audit_reports/
    ├── pytest-collection.txt
    ├── pytest-output.txt
    ├── pytest-junit.xml
    ├── coverage.json
    ├── coverage.xml
    ├── htmlcov/
    ├── ruff-output.txt
    ├── import-check.txt
    ├── config-check.txt
    ├── package-metadata.txt
    ├── package-build.txt
    └── dist/
```

### Éléments exclus

- environnements : `.venv`, `.direnv`, `.pip_packages` ;
- caches : `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache` ;
- secrets : `.env` et variantes ;
- résultats, logs et archives hérités ;
- données historiques ;
- fichiers de copie suffixés `_`, `__`, `copy` ou `backup` ;
- anciens rapports et images générés.

Les fichiers `__init__.py` ont été conservés : leur double underscore fait partie du nom spécial Python et ne désigne pas une sauvegarde.

## 3. Résultats des tests Pytest

### Commande finale

```bash
PYTHONPATH=. /tmp/paper-trading-audit-nix-python-v2/bin/python -m pytest tests -q \
  --junitxml=audit_reports/pytest-junit.xml \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=xml:audit_reports/coverage.xml \
  --cov-report=json:audit_reports/coverage.json \
  --cov-report=html:audit_reports/htmlcov
```

### Résultat

```text
21 passed in 1.32s
Required test coverage of 49.0% reached.
Total coverage: 49.01%
```

### Domaines testés

- liquidation à -80 % ;
- arrêt des opérations après liquidation ;
- frais d'entrée et de sortie ;
- état externe de position ;
- plafond mathématique par rapport à Sell & Hold ;
- slippage défavorable ;
- commission et validation du côté d'ordre ;
- benchmarks Buy & Hold et Sell & Hold ;
- construction et espacement des grilles ;
- prix de liquidation ;
- limite du nombre de positions ;
- conversion initiale USD/SOL ;
- backtest synthétique de marché baissier ;
- Sharpe et drawdown.

### Limites des tests

- aucun test de `DataLoader` ;
- aucun test réseau ou mock complet de `BitgetDataFetcher` ;
- couverture partielle des métriques avancées ;
- chemins d'erreur et cas limites du portefeuille incomplets ;
- aucun test des quatre fichiers YAML en tant qu'entrée du bot ;
- aucun test des exemples/CLI ni du paper trading continu ;
- aucun test d'installation de la wheel dans un environnement vierge.

Rapports : `audit_reports/pytest-output.txt`, `audit_reports/pytest-junit.xml` et `audit_reports/pytest-collection.txt`.

## 4. Résultats de la couverture

La couverture a été mesurée avec les branches activées dans `pyproject.toml`.

| Module | Instructions | Manquantes | Branches | Partielles | Couverture |
|---|---:|---:|---:|---:|---:|
| `src/__init__.py` | 1 | 0 | 0 | 0 | 100 % |
| `src/analysis/__init__.py` | 2 | 0 | 0 | 0 | 100 % |
| `src/analysis/benchmarks.py` | 29 | 8 | 0 | 0 | 72 % |
| `src/analysis/performance.py` | 63 | 36 | 18 | 2 | 36 % |
| `src/core/__init__.py` | 3 | 0 | 0 | 0 | 100 % |
| `src/core/data_fetcher.py` | 56 | 41 | 8 | 0 | 23 % |
| `src/core/data_loader.py` | 105 | 105 | 44 | 0 | 0 % |
| `src/core/exchange_simulator.py` | 32 | 2 | 10 | 2 | 90 % |
| `src/core/portfolio_manager.py` | 58 | 19 | 12 | 4 | 64 % |
| `src/strategies/__init__.py` | 1 | 0 | 0 | 0 | 100 % |
| `src/strategies/grid_bot.py` | 159 | 25 | 54 | 8 | 78 % |
| **Total** | **509** | **236** | **146** | **16** | **49,01 %** |

Le seuil actuel est fixé à 49 %, valeur de base réelle. Il ne doit pas être abaissé. L'objectif de prochaine release devrait être 70 %, puis 80 % pour le noyau financier.

Rapports : `audit_reports/coverage.json`, `audit_reports/coverage.xml` et `audit_reports/htmlcov/index.html`.

## 5. Liste des erreurs détectées

### E1 — Flake Nix initialement impossible à construire

- Erreur réelle : `attribute 'ccxt' missing` sur `ps.ccxt`.
- Cause : `ccxt` n'existe pas dans le jeu de paquets Python du `nixpkgs` verrouillé.
- Impact : aucune entrée du flake ne pouvait être évaluée.
- État : corrigé dans la copie restaurée en retirant `ps.ccxt`. L'import de ccxt est paresseux et les tests hors ligne n'en ont pas besoin.

### E2 — Outils de packaging absents de l'environnement Nix

- Erreurs réelles successives : `No module named build`, puis `Missing dependencies: wheel`.
- Impact : impossible de produire une distribution GitHub/PyPI.
- État : corrigé par ajout de `setuptools`, `build` et `wheel` au Python Nix.

### E3 — Version de paquet incorrecte et métadonnées concurrentes

- Le `setup.py` original déclarait `1.0.0` dans un dossier `v1.1.2`.
- L'ajout initial du `pyproject.toml` provoquait des avertissements de métadonnées dupliquées avec `setup.py`.
- État : corrigé. `pyproject.toml` est la source canonique en version `1.1.2`; `setup.py` est un shim de compatibilité.

### E4 — Couverture insuffisante

- Couverture vérifiée : 49,01 % avec branches.
- `data_loader.py` : 0 %.
- `data_fetcher.py` : 23 %.
- `performance.py` : 36 %.
- Impact : changements sur les données, l'API ou les métriques susceptibles de régresser sans détection.
- État : non corrigé ; nouveaux tests requis.

### E5 — 48 erreurs Ruff

| Code | Nombre | Nature |
|---|---:|---|
| `F541` | 33 | f-strings sans substitution |
| `F401` | 12 | imports inutilisés ou réexports non explicites |
| `F841` | 2 | variables locales inutilisées |
| `E741` | 1 | nom de variable ambigu `l` dans un test |

Ces erreurs ne cassent pas les 21 tests, mais font échouer un contrôle qualité CI. Détail complet : `audit_reports/ruff-output.txt`.

### E6 — Structure de paquet fragile

- Le paquet installé s'appelle techniquement `src`.
- Les imports sont du type `from src.core...`.
- Les exemples modifient parfois `sys.path` manuellement.
- La wheel est valide et construite, mais le nom `src` peut entrer en conflit avec d'autres projets.
- État : non corrigé, car le renommage demande une migration coordonnée des imports et tests.

### E7 — Environnements Nix non uniformes

- `flake.nix` peut construire le Python corrigé.
- Son `shellHook` lance encore automatiquement `setup-venv`, lequel utilise `pip` et le réseau si `.venv_papertrading` est absent.
- `shell.nix` effectue de nombreuses installations `pip` automatiques et inclut des dépendances non utilisées par ce projet.
- `devenv.nix` est encore le modèle générique « hello » et ne décrit pas l'application.
- `smart-test` formate et répare le code avant les tests, ce qui rend un test CI mutateur.
- État : non corrigé ; utiliser pour l'instant `nix build 'path:.#python'` plutôt que le shell interactif automatique.

### E8 — Configurations partiellement divergentes

- Les quatre YAML sont syntaxiquement valides.
- `grid_bot_optimal.yaml` possède `timeframe`, `max_position_size` et `adaptive_spacing`, absents des trois profils de couleur.
- Les valeurs communes ont une structure compatible, mais aucun schéma ne valide types, bornes et clés obligatoires.
- État : non corrigé.

### E9 — Documentation incohérente avec la copie publique

- Le README demande de copier `.env.example`, volontairement absent de la copie restaurée.
- Les exemples référencent `data/SOL_2021_2022.csv`, exclu de la copie propre.
- Certains messages mentionnent encore `paper-trading-codex-v1.1`.
- État : non corrigé ; le README doit expliquer le mode synthétique et le téléchargement manuel de données.

### E10 — Fonctionnalités Bitget volontairement incomplètes

- Les données publiques peuvent être récupérées par `BitgetDataFetcher` si ccxt est installé.
- `get_balance`, `create_order` et `fetch_positions` lèvent volontairement `NotImplementedError`.
- Ce comportement est compatible avec un simulateur de paper trading, mais incompatible avec une revendication de trading live.
- État : documenté, pas considéré comme défaut du noyau local.

## 6. Corrections proposées

### Corrections déjà appliquées à la copie restaurée

1. Nettoyage sélectif sans modification de l'original.
2. Retrait de `ps.ccxt` invalide dans `flake.nix`.
3. Ajout de `setuptools`, `build` et `wheel` dans l'environnement Nix.
4. Ajout d'un `pyproject.toml` complet avec version 1.1.2, dépendances, options Pytest, couverture et Ruff.
5. Conversion de `setup.py` en shim utilisant les métadonnées du `pyproject.toml`.
6. Seuil de couverture fixé à la base vérifiée de 49 %.

### Corrections prêtes à appliquer ensuite

| Priorité | Cible | Correction concrète | Validation attendue |
|---:|---|---|---|
| P0 | Paquet | Renommer `src/` en `paper_trading_codex/`, remplacer tous les imports `src.*`, retirer les `sys.path.insert` | Wheel installable puis 21 tests verts depuis un dossier externe |
| P0 | Nix | Supprimer les `pip install` des `shellHook`; faire du flake l'unique source de l'environnement de test | `nix develop` sans réseau ni modification du worktree |
| P0 | Tests | Ajouter `tests/test_data_loader.py` pour CSV valide/invalide, timestamps, NaN, doublons, timeframe et adaptation | `data_loader.py` au-dessus de 80 % |
| P0 | API | Mock ccxt dans `tests/test_data_fetcher.py`; tester symboles, rate limit, OHLCV, ticker, client absent et méthodes bloquées | Aucun accès réseau et `data_fetcher.py` au-dessus de 70 % |
| P1 | Métriques | Tester Sortino, Calmar, profit factor, win rate vide, séries constantes et valeurs invalides | `performance.py` au-dessus de 80 % |
| P1 | Config | Ajouter un modèle typé ou un schéma JSON avec valeurs par défaut communes et bornes (`leverage`, ratios, capital) | Validation des 4 YAML en CI |
| P1 | Ruff | Exécuter `ruff check --fix`, puis corriger manuellement les réexports et `E741` | Zéro erreur Ruff, tests inchangés |
| P1 | README | Remplacer l'étape `.env.example`, documenter mode offline/synthétique et acquisition de données | Quickstart reproductible sans secret |
| P2 | CI | Ajouter GitHub Actions : Nix build, Pytest, couverture, Ruff, build wheel | Workflow vert sur push et pull request |
| P2 | Sécurité | Ajouter `.gitignore`, scan de secrets et politique de rotation des clés | Aucun `.env`, secret ou log dans Git |

### Configuration stable proposée

Définir les clés suivantes dans tous les profils :

```yaml
strategy: grid_bot
timeframe: "1h"
initial_capital: 1000
leverage: 3.0
grid_size: 7
grid_ratio: 0.02
max_positions: 5
max_position_size: 0.30
maintenance_margin: 0.08
safety_buffer: 1.30
adaptive_spacing: false
simulation:
  slippage:
    mean: 0.000342
    std: 0.000187
  commission_rate: 0.001
```

Chaque profil peut ensuite surcharger uniquement le risque. Cette proposition n'a pas remplacé les configurations existantes, car ses effets métier doivent être testés.

### Section README à ajouter

```markdown
## Exécution hors ligne

Les tests et le backtest synthétique ne nécessitent aucune clé API ni connexion réseau.
Ne créez un fichier `.env` local que pour lire les données publiques Bitget et ne le
commitez jamais. Les opérations privées ne sont pas prises en charge : tous les ordres
sont simulés localement. Les données historiques ne sont pas incluses dans le dépôt ;
utilisez `--data CHEMIN.csv` ou le fallback synthétique documenté par l'exemple.
```

## 7. Recommandations pour publication GitHub

1. Créer un nouveau dépôt depuis `paper-trading-codex-restored`, pas depuis l'archive complète.
2. Ne pas inclure `audit_reports/htmlcov`, `audit_reports/dist` ou les rapports de travail dans la branche principale ; les publier comme artefacts CI/release si nécessaire.
3. Conserver `PROJECT_RESTORED_AUDIT.md` comme preuve de restauration, avec la date et le commit correspondant.
4. Effectuer le renommage du paquet avant la première release publique afin d'éviter de figer l'API `src.*`.
5. Ajouter une licence explicite ; le README original ne suffit pas à accorder des droits d'utilisation.
6. Ajouter un `.gitignore` couvrant secrets, environnements, caches, builds, rapports et données.
7. Utiliser des données synthétiques minimales pour les tests ; ne pas versionner le CSV historique sans vérifier licence et provenance.
8. Ne pas annoncer le trading live : les endpoints privés sont volontairement bloqués.
9. Publier une prérelease `v1.1.2-rc1` seulement après CI verte, lint corrigé et installation de la wheel testée.
10. Atteindre au moins 70 % de couverture avant `v1.1.2`, avec priorité aux données et invariants financiers.

## 8. Checklist de release GitHub

### CI

- [ ] Workflow GitHub Actions ajouté.
- [ ] Reconstruction Nix non mutatrice.
- [ ] 21 tests actuels verts en CI.
- [ ] Nouveaux tests DataLoader et Bitget mockés ajoutés.
- [ ] Couverture minimale portée à 70 %.
- [ ] Ruff à zéro erreur.
- [ ] Build sdist/wheel vérifié en CI.
- [ ] Installation et import de la wheel testés dans un environnement vierge.

### Packaging

- [x] `pyproject.toml` présent.
- [x] Version cohérente `1.1.2`.
- [x] `setup.py` réduit à un shim.
- [x] sdist et wheel construits avec succès.
- [ ] Paquet `src` renommé.
- [ ] Dépendances optionnelles réseau séparées du noyau.
- [ ] Métadonnées de licence et URLs du projet ajoutées.

### Versioning

- [ ] Dépôt Git propre initialisé.
- [ ] Historique de restauration documenté.
- [ ] Tag `v1.1.2-rc1` créé après CI verte.
- [ ] `CHANGELOG.md` ajouté.
- [ ] Politique SemVer documentée.

### Licence et sécurité

- [ ] Fichier `LICENSE` ajouté.
- [ ] `.gitignore` ajouté.
- [x] Aucun `.env` dans la copie restaurée.
- [ ] Scan de secrets exécuté avant le premier push.
- [ ] Provenance/licence des données documentée.
- [ ] Avertissement financier et périmètre offline confirmés.

### README

- [x] Présentation et avertissement présents.
- [x] Tests critiques documentés.
- [ ] Installation Nix corrigée et documentée.
- [ ] Quickstart sans `.env.example` manquant.
- [ ] Acquisition des données documentée.
- [ ] Limites de Bitget et absence de trading live explicites.
- [ ] Badges CI, couverture et version ajoutés seulement après publication réelle.

## Verdict de validation

- **Code métier testé : validé sur les 21 tests présents.**
- **Environnement Nix de build : validé après corrections.**
- **Paquet source et wheel : construits avec succès.**
- **Publication GitHub immédiate : non recommandée.**
- **Blocages restants : lint, couverture, nom du paquet, shell Nix mutateur, licence, CI et documentation.**
