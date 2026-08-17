# P0 Reproducibility Report

**Date** : 2026-08-17
**Commit P0 candidate** : `3a3b2678b957e86768ec05584bbba5a8e90f629e`
**Branche** : `correction/reconcile-l1-l12`

## Environnement

| Champ | Valeur |
|---|---|
| OS | NixOS (nix develop) |
| Python | 3.12.12 |
| Pytest | 8.4.2 |
| Ruff | 0.15.0 |
| NumPy | 2.3.5 (via Nix) |
| Pandas | 2.3.3 (via Nix) |
| Réseau | non contrôlé (tests hors réseau par conception) |

## Commandes exécutées

### 1. Tests

```bash
nix develop --command bash -c 'pytest -q'
```

**Résultat** : `68 passed in 2.09s` — exit code `0`

### 2. Couverture

```bash
nix develop --command bash -c 'pytest --cov=paper_trading_codex --cov-report=term -q'
```

**Résultat** :

| Module | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
| `__init__.py` | 1 | 0 | 0 | 0 | 100% |
| `analysis/__init__.py` | 2 | 0 | 0 | 0 | 100% |
| `analysis/benchmarks.py` | 28 | 7 | 0 | 0 | 75% |
| `analysis/performance.py` | 71 | 4 | 24 | 5 | 91% |
| `core/__init__.py` | 3 | 0 | 0 | 0 | 100% |
| `core/data_fetcher.py` | 56 | 3 | 8 | 1 | 94% |
| `core/data_loader.py` | 107 | 5 | 46 | 10 | 90% |
| `core/exchange_simulator.py` | 37 | 2 | 14 | 2 | 92% |
| `core/portfolio_manager.py` | 58 | 8 | 12 | 3 | 84% |
| `strategies/__init__.py` | 1 | 0 | 0 | 0 | 100% |
| `strategies/grid_bot.py` | 181 | 20 | 70 | 11 | 83% |
| **TOTAL** | **545** | **49** | **174** | **32** | **87%** |

Exit code `0`. Seuil 70% atteint.

### 3. Ruff

```bash
nix develop --command bash -c 'ruff check .'
```

**Résultat** : `All checks passed!` — exit code `0`

### 4. Reproductibilité déterministe

```bash
nix develop --command bash -c 'python scripts/validate_reproducibility.py'
```

**Résultat** : `fc3531b6e5f02ec9461126ed1e29451192d0478b29b976b58a6633c00c585491` — exit code `0`

### 5. Vérification du manifeste

```bash
nix develop --command bash -c 'python -c "import json; m=json.load(open(\"REPRODUCIBILITY_MANIFEST.json\")); print(m[\"result_sha256\"])"
```

**Résultat** : `fc3531b6e5f02ec9461126ed1e29451192d0478b29b976b58a6633c00c585491`

Concordance avec STATUS.md : **OUI**

### 6. État Git après exécution

```bash
git status --short
```

**Résultat** : aucun fichier modifié (uniquement les nouveaux fichiers d'audit non suivis)

## Niveaux de preuve

| Niveau | Statut | Détail |
|---|---|---|
| Documentation | PRÉSENT | `HYPOTHESIS.md`, `METHODS.md`, `LIMITATIONS.md`, `STATUS.md` |
| Dérivation indépendante | PRÉSENT | Formules vérifiables dans METHODS.md, oracles manuels dans HYPOTHESIS.md |
| Test exécutable | **VÉRIFIÉ** | 68/68 tests passent, couverture 87.07%, Ruff 0 erreur |
| Replay reproductible | **VÉRIFIÉ** | `result_sha256` identique (`fc3531b6...`) entre deux exécutions |

## Comparaison avec les preuves Producteur antérieures

| Métrique | Producteur (Nix) | Audit actuel (Nix) | Concordance |
|---|---|---|---|
| Tests | 68 passed | 68 passed | OUI |
| Couverture | 87.07% | 87.07% | OUI |
| Ruff | All checks passed | All checks passed | OUI |
| `result_sha256` | `fc3531b6...` | `fc3531b6...` | OUI |
| `config_sha256` | `d65e6742...` | `d65e6742...` | OUI |
| `input_sha256` | `7e35c799...` | `7e35c799...` | OUI |
| Exit code | 0 | 0 | OUI |

## Limites de cette vérification

1. **Environnement** : exécuté sous Nix sur une machine x86_64-linux, pas dans une VM isolée sans réseau. Les tests sont conçus pour être hors réseau mais le `nix develop` a un accès réseau pour la construction.
2. **Non-Nix** : une exécution sans Nix (`pip install -e '.[test]'`) échoue sur `libstdc++.so.6` — le couplage aux bibliothèques système Nix est documenté et attendu.
3. **Couverture Bitget** : non exécutée dans cet audit (VM dédiée requise). Les preuves Bitget (9/9, 38%) reposent sur les exécutions antérieures (VM 140) et les reproductions Critique/Contradictoire, toutes admises dans le commit `804002f`. Non rejoué dans le présent audit.
4. **Timestamps** : les timestamps du manifeste ne sont pas inclus dans le hash scientifique (conforme à `METHODS.md` §6).
