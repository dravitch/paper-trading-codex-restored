# Statut canonique

Ce fichier est la source unique des compteurs de tests. Régénération : `python scripts/update_status.py`; contrôle : `python scripts/update_status.py --check`.

## Tests

<!-- TEST_STATUS_START -->
- Tests collectés : **125** dans **10** fichiers.
- Commande canonique : `python -m pytest tests -q`.
- Fichiers : `tests/hypotheses/H0001/test_canonical_ledger_equivalence.py`, `tests/hypotheses/H0002/test_short_ledger_generalization.py`, `tests/hypotheses/H0003/test_canonical_contract_foundation.py`, `tests/test_contracts.py`, `tests/test_critical_5_5.py`, `tests/test_data_fetcher.py`, `tests/test_data_loader.py`, `tests/test_grid_bot.py`, `tests/test_performance_metrics.py`, `tests/test_trade_auditor.py`.
<!-- TEST_STATUS_END -->

## Critères de publication

| Critère | Statut courant |
|---|---|
| tests hors réseau | PASS — 68/68, fixture socket globale |
| couverture ≥ 70 % | PASS — 87,07 % lignes + branches |
| Ruff zéro erreur | PASS — `All checks passed!` |
| wheel hors dépôt | PASS — 68/68 en 0,41 s depuis `/tmp` |
| reproductibilité du résultat canonique | PASS local — deux fois `fc3531…5491` |
| CI Python 3.10–3.12 | workflow présent, exécution distante unknown |
| MIT | texte et métadonnée présents |

Les valeurs finales sont mises à jour uniquement à partir des commandes enregistrées dans `REV03.md`.

## Artefacts vérifiés

| Artefact | SHA-256 |
|---|---|
| résultat scientifique canonique | `fc3531b6e5f02ec9461126ed1e29451192d0478b29b976b58a6633c00c585491` |
| manifeste complet | `145b228f378ddfc0440c186025f8db81ef8f96f743121b5749a893b57c7bcd2c` |
| wheel | `d686bc2d5dd9b5ba03957c5ac1cd983b3bdb9daaa60b7668bf65a19f9424fa00` |
| sdist | `94216193116f87ecbdfece4eb70edca59065b8246b36bf9d73008840a243316d` |
| graphique USD, deux runs | `e64e94a35ede6ccf81663d60132f13bdde47eb3d01e0593242f77626733e579a` |
| graphique SOL, deux runs | `85ef188317b1514ca1e9e03950700e8616cc6bc55638ab0b733ab3497edeefa7` |
