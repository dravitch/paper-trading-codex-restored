# Heartbeat — IA Critique (P0 baselines)

| Champ | Valeur |
|---|---|
| rôle | IA Critique indépendante |
| date | 2026-08-08 |
| commit examiné | `d1ed53b1b63d3b6d06ad8edcf64dc4655a3574da` (`correction/reconcile-l1-l12`) |
| fichiers lus | `docs/fusion/P0_BASELINE_EVIDENCE.md`, `PROGRESSION.md`, `docs/fusion/06_FUSION_GATES.md`, `docs/fusion/COMPONENT_PROVENANCE.md`, `docs/fusion/LIMIT_RESOLUTION_REGISTER.md`, `docs/fusion/PROTOCOL_CONTRADICTOIRE.md`, `docs/fusion/REVIEW_ADMISSION_REGISTRY.md` + dépôt tiers `bitget-paper-trading` à `f2e41890...` |
| exécution | **réelle**, hors mandat par défaut : clonage + réinstallation de dépendances + `pytest`/`pytest-cov` réexécutés indépendamment (environnement Linux générique, sans Nix ni VM) |
| résultats de reproduction | LICENSE SHA-256 identique ; 22 fichiers suivis identiques ; 9 tests collectés/9 réussis/exit 0 confirmés ; couverture 38 %/80 % reproduite exactement sous `--cov=paper_trading` (36 % sous `--cov=.`, ambiguïté relevée) |
| verdict | `ACCEPT_WITH_LIMITS` |
| objections ouvertes | O1 (modéré) narration causale des échecs d'import imprécise + 68 tests du dépôt restauré non recollectés ; O2 (faible) périmètre de couverture « 38 % globalement » ambigu sans commande explicite ; O3 (faible, structurelle) artefacts VM/KB non vérifiables par un tiers |
| gates | aucun franchi ; P0 reste `PARTIAL` ; preuve d'immuabilité distante toujours absente ; P6 reste `BLOCKED_IMMUTABILITY`, non affecté |
| rapport complet | `docs/fusion/CRITIQUE_P0_BASELINE.md` |

État : **revue Critique du dossier P0 terminée**, formée sans lecture préalable d'une conclusion Contradictoire sur ce même dossier.
