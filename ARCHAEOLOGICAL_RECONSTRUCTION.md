# Reconstruction archéologique — PROTOCOL_CONTRADICTOIRE

**Date** : 2026-08-19
**Dépôt** : `paper-trading-codex-restored`
**Branche principale** : `correction/reconcile-l1-l12`
**Branches locales** : `main`, `fusion/controlled-merger`, `correction/reconcile-l1-l12`
**Branches distantes** : identiques + `origin/HEAD -> origin/main`
**Reflog** : aucun SHA orphelins (pas de merge supprimé)
**bitget-paper-trading** : aucun de ces fichiers (6 commits, code pur)

## Commandes exécutées

```bash
git log --all --oneline --follow -- docs/fusion/PROTOCOL_CONTRADICTOIRE.md
git log --all --oneline --follow -- docs/fusion/NO_GO_REGISTER.md
git log --all --oneline --follow -- docs/fusion/CAUSAL_ID_REGISTRY.md
git log --all --diff-filter=A --oneline -- 'docs/fusion/*'
git branch -a
git log --all --oneline --grep="Gate" -i
git log --all --oneline --grep="NO_GO" -i
git log --all --oneline --grep="heartbeat" -i
git log --all --oneline --grep="rev-list" -i
git log --all --oneline --grep="SHA-256" -i
git log --all --oneline --grep="append-only" -i
git log --all --oneline -S "parent_registry_commit" -- 'docs/fusion/*'
git log --all --oneline -S "previous_blob_sha256" -- 'docs/fusion/*'
git log --all --oneline -S "rev-list" -- 'docs/fusion/*'
git reflog --all
```

## Tableau chronologique brut

| # | Élément | Commit | Date | Auteur | Message intégral | Fichiers touchés | source_verifiable |
|---|---|---|---|---|---|---|---|
| 1a | **Gates PASS/FAIL/BLOCKED** | `d82fb3a9db2c9e2a50dbb82d104ff4faf3d65913` | 2026-08-06 01:23:21 -0400 | Corail Synergia `<corail.synergia@proton.me>` | `docs: establish controlled merger protocol` | `06_FUSION_GATES.md` (créé), `PROTOCOL_CONTRADICTOIRE.md` (créé), + 12 autres fichiers `docs/fusion/*` | oui (git) |
| 1b | **PASS/FAIL/BLOCKED dans PROTOCOL** | `d82fb3a9db2c9e2a50dbb82d104ff4faf3d65913` | 2026-08-06 01:23:21 -0400 | Corail Synergia | (même commit) | `PROTOCOL_CONTRADICTOIRE.md` §5.4 : « les statuts possibles : PASS, FAIL, BLOCKED, NON_TESTABLE » | oui (git) |
| 2 | **PROTOCOL_CONTRADICTOIRE.md** | `d82fb3a9db2c9e2a50dbb82d104ff4faf3d65913` | 2026-08-06 01:23:21 -0400 | Corail Synergia | `docs: establish controlled merger protocol` | `docs/fusion/PROTOCOL_CONTRADICTOIRE.md` (créé, 102 lignes) | oui (git) |
| 3a | **NO_GO_REGISTER.md** | `8335ab02722a4687aa79b1e3dbebdca6c0c24d73` | 2026-08-06 02:24:55 -0400 | Corail Synergia | `docs: integrate residual contradictory findings` | `docs/fusion/NO_GO_REGISTER.md` (créé, table Markdown simple, PAS append-only) | oui (git) |
| 3b | **NO_GO_CYCLE_REGISTRY.json** | `f14546f` | 2026-08-06 19:00:22 -0400 | Corail Synergia | `docs: resolve contradictory findings M1-M4` | `docs/fusion/NO_GO_CYCLE_REGISTRY.json` (créé) | oui (git) |
| 4a | **`previous_blob_sha256`** (append-only) | `930b0f9` | 2026-08-06 19:34:48 -0400 | Corail Synergia | `docs: resolve contradictory findings N1-N4` | `docs/fusion/NO_GO_REGISTER.md` (ajouté: « Le registre est append-only entre deux révisions Git. `previous_blob_sha256` doit égaler le SHA-256 exact du blob… ») | oui (git) |
| 4b | **`parent_registry_commit`** (append-only) | `6867a2d` | 2026-08-06 23:14:40 -0400 | Corail Synergia | `docs: resolve contradictory findings O1-O4` | `docs/fusion/NO_GO_REGISTER.md` (ajouté: « le commit parent déclaré ») | oui (git) |
| 4c | **`rev-list --first-parent`** (mécanisme de preuve) | `7039476` | 2026-08-06 23:38:05 -0400 | Corail Synergia | `docs: resolve contradictory findings P1-P4` | `docs/fusion/NO_GO_REGISTER.md` (ajouté: « `git rev-list --first-parent --max-count=1 E -- docs/fusion/NO_GO_CYCLE_REGISTRY.json` ») | oui (git) |
| 5 | **CAUSAL_ID_REGISTRY.md** | `ca8de4f` | 2026-08-06 03:03:13 -0400 | Corail Synergia | `docs: resolve contradictory findings H1-H5` | `docs/fusion/CAUSAL_ID_REGISTRY.md` (créé) | oui (git) |
| 6 | **Premier HEARTBEAT** | `a9f13dbe769888023ee835e497c50c2eccd4055d` | 2026-08-06 01:38:32 -0400 | Corail Synergia | `docs: record contradictory feasibility review` | `docs/fusion/HEARTBEAT_CONTRADICTOIRE.md` (créé) + `docs/fusion/CONTRADICTOIRE_FEASIBILITY.md` (créé) | oui (git) |
| 7a | **SHA-256 (concept)** | `09653e2` | 2026-08-06 02:08:29 -0400 | Corail Synergia | `docs: reconcile contradictory limits L1-L12` | `docs/fusion/LIMIT_RESOLUTION_REGISTER.md` (L2: « SHA-256 dans O7 », L5: « hash exact dans environnement verrouillé ») | oui (git) |
| 7b | **SHA-256 (mécanisme concret)** | `8335ab0` | 2026-08-06 02:24:55 -0400 | Corail Synergia | `docs: integrate residual contradictory findings` | `docs/fusion/NO_GO_REGISTER.md` (créé), `docs/fusion/06_FUSION_GATES.md` (modifié), + 8 autres fichiers | oui (git) |

## Chronologie serrée (même journée, 2026-08-06)

```text
01:23  d82fb3a  Gates + PROTOCOL_CONTRADICTOIRE créés (commit fondateur)
01:38  a9f13db  Premier HEARTBEAT
01:51  b53cb99  Critical feasibility review
01:58  98e16fb  Metadata addendum
02:01  e413867  Human adjudication
02:08  09653e2  SHA-256 comme concept (LIMIT_RESOLUTION_REGISTER)
02:09  273046a  Review request REV05
02:24  8335ab0  NO_GO_REGISTER créé + SHA-256 comme mécanisme
03:03  ca8de4f  CAUSAL_ID_REGISTRY créé
19:00  f14546f  NO_GO_CYCLE_REGISTRY.json créé
19:34  930b0f9  previous_blob_sha256 ajouté (append-only)
23:14  6867a2d  parent_registry_commit ajouté
23:38  7039476  rev-list --first-parent comme mécanisme de preuve
```

## Constats

- Tout est dans `paper-trading-codex-restored`. Rien dans `bitget-paper-trading`.
- Un seul auteur : **Corail Synergia** `<corail.synergia@proton.me>` (tous les 44 premiers commits).
- Tout s'est passé en **une seule journée** (2026-08-06), de 01:23 à 23:38.
- Le protocole n'a pas été importé — il a **cristallisé en ~22 heures** à partir d'un commit initial de 14 fichiers.
- Les 3 branches existent encore localement et distantes.
- Aucun squash confirmé (`git log --follow` fonctionne sur tous les fichiers demandés).
