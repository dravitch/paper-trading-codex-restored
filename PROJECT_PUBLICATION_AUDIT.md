# Audit de publication final

## Résumé

Le paquet est installable, testé, linté, couvert à 87,07 %, licencié MIT et reproductible localement. La publication reste contrôlée : la CI GitHub distante est `unknown`, et le positionnement doit rester celui d'un laboratoire éducatif.

## Critères

| Critère | Résultat | Preuve |
|---|---|---|
| Pytest 100 % | PASS | 68/68 en Nix |
| réseau interdit | PASS | fixture socket `autouse` |
| couverture ≥ 70 % | PASS | 87,07 % branches incluses |
| Ruff | PASS | zéro erreur |
| wheel/sdist | PASS | deux artefacts construits avec licence |
| installation hors dépôt | PASS | 68/68 depuis `/tmp` |
| quickstart répétable | PASS local | texte identique hors chemin, deux paires de PNG identiques |
| manifeste | PASS local | input/config/seed/versions/résultat hashés |
| documentation normative | PASS | sept documents obligatoires + audits |
| licence MIT | PASS | `LICENSE` et `license = "MIT"` |
| CI Python 3.10–3.12 | CONFIGURÉE, NON OBSERVÉE | workflow présent; aucun run GitHub localement |
| secret | PASS local | aucun secret requis; réseau absent des tests |

## Packaging

- wheel : `paper_trading_codex-1.1.2-py3-none-any.whl`, SHA-256 `d686bc…fa00`;
- sdist : `paper_trading_codex-1.1.2.tar.gz`, SHA-256 `942161…316d`;
- paquet importable : `paper_trading_codex`;
- Python déclaré : ≥3.9; matrice CI : 3.10, 3.11, 3.12.

## Documentation

`HYPOTHESIS.md`, `THESIS.md`, `METHODS.md`, `LIMITATIONS.md`, `STATUS.md`, `REV03.md`, le manifeste et les deux audits sont présents. Les affirmations de sûreté des profils ont été retirées.

## Blocages

1. exécuter réellement la CI GitHub sur les trois versions Python;
2. confirmer le titulaire « Symbioticode » et l'année 2026 avant publication juridique définitive;
3. ne pas présenter le projet comme fidèle à Bitget ni validé économiquement;
4. ne pas commiter les caches, builds temporaires ou sorties utilisateur.

## Verdict

**Prêt techniquement pour une revue de publication GitHub MIT, pas encore autorisé à publier.** Le push/release reste bloqué jusqu'à validation humaine de la licence et première CI distante verte.
