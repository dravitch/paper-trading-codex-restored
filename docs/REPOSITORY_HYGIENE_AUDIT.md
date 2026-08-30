# Audit conservateur d'hygiène du dépôt

## 1. État synthétique du dépôt

### Périmètre et méthode

Audit en lecture réalisé le 2026-08-30 sur `work/repo-hygiene-audit`, créé depuis
`044406f38116658864ebe07ce3fa14a3a08d5f20` (préenregistrement H0004). Aucun fichier
existant, code, preuve, branche ou artefact local n'a été modifié ou supprimé.

Les contrôles ont combiné `git status --short --ignored`, `git ls-files`, les fichiers
ignorés/non suivis, `git check-ignore -v`, `git grep`, `git log --all -- <path>`, SHA-256,
filiation, upstream et ahead/behind des branches.

### Résultat général

- Le worktree suivi était propre au départ.
- Les caches Python, caches de tests/lint, `.coverage`, `dist/`, `.egg-info`, sessions et
  rapports générés visibles sont tous **ignorés et non suivis**. Aucun cache/build Python
  n'est présent dans l'index Git.
- `.gitignore` couvre déjà `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `.pytest_cache/`,
  `.ruff_cache/`, `.coverage`, `htmlcov/`, `build/`, `dist/`, `audit_reports/`,
  `publication_reports/`, `docs/deepsearch/` et `session-ses_*.md`.
- Les trois `PROGRESSION_TEMP*`, `REV03`–`REV12` et 126 fichiers sous `docs/fusion/` sont
  suivis. Ils appartiennent à la chaîne P0/P6 ou aux hypothèses admises : leur nom ou leur
  ancienneté n'autorise aucune suppression.
- Les branches d'hypothèses forment une filiation vérifiable et restent disponibles sur
  `origin`. H0001–H0003 sont des archives expérimentales fermées; H0004 est en cours et
  bloquée avant code.
- Aucun gain de taille Git notable ne résulterait d'une suppression locale : les objets
  Git occupent environ 434 KiB packés; le bruit local identifié est ignoré.

### Classification synthétique

| Famille | Git | Références/provenance | Classe |
|---|---|---|---|
| sources, tests, configurations, scripts | suivis | actifs et utilisés par les preuves | `KEEP_ACTIVE` |
| dossiers H0001–H0003 | suivis | manifests, résultats, revues, admissions, hashes | `DO_NOT_TOUCH` |
| dossier H0004 | suivi | préenregistrement actif `BLOCKED_SPEC_AMBIGUITY` | `KEEP_ACTIVE` |
| corpus historique P0/P6 et `docs/fusion/` | suivi | registres, admissions, liens et hashes | `KEEP_HISTORICAL_EVIDENCE` |
| caches Python/test/lint | ignorés | reconstructibles, aucune référence probatoire | `DELETE_SAFE_LOCAL` |
| `dist/` racine et `.egg-info` | ignorés | builds locaux courants, non référencés | `DELETE_SAFE_LOCAL` |
| `audit_reports/` | ignoré | chemins cités par l'audit historique restauré | `CLEANUP_CANDIDATE_REQUIRES_HUMAN` |
| `publication_reports/` | ignoré | binaries dont les hashes sont publiés | `KEEP_HISTORICAL_EVIDENCE` |
| sessions locales | ignorées | aucune référence suivie ni historique Git | `DELETE_SAFE_LOCAL` |
| `docs/deepsearch/` | ignoré | autre périmètre explicitement déclaré | `DO_NOT_TOUCH` |

## 2. Artefacts locaux et générés

### Python, tests et couverture

| Candidat | Constat | Classe | Action proposée |
|---|---|---|---|
| `**/__pycache__/`, `*.pyc` | ignorés, non suivis; plusieurs versions pytest coexistent dans `tests/__pycache__` | `DELETE_SAFE_LOCAL` | suppression locale réversible au Tier 0; aucune modification `.gitignore` requise |
| `.pytest_cache/`, `.ruff_cache/` | ignorés, non suivis, environ 44 KiB et 52 KiB | `DELETE_SAFE_LOCAL` | suppression locale Tier 0 |
| `.coverage` | ignoré, non suivi, environ 108 KiB | `DELETE_SAFE_LOCAL` | suppression locale Tier 0 après toute consultation désirée |
| `paper_trading_codex.egg-info/` | ignoré, non suivi, métadonnées recréées par installation/build | `DELETE_SAFE_LOCAL` | suppression locale Tier 0 |

La prévention est déjà correcte. Ajouter de nouveaux motifs génériques à `.gitignore`
n'apporterait aucun bénéfice démontré.

### Builds et distributions

Trois couples wheel/sdist 1.1.2 existent localement, mais ils ne sont pas byte-identiques :

| Emplacement | wheel SHA-256 | sdist SHA-256 | Interprétation | Classe |
|---|---|---|---|---|
| `dist/` | `23483ec5…102cb4` | `095e37a8…5be76` | build local courant non référencé | `DELETE_SAFE_LOCAL` |
| `audit_reports/dist/` | `06ddaf1c…7b4d5` | `cc576641…ef22` | build de l'audit restauré historique | `CLEANUP_CANDIDATE_REQUIRES_HUMAN` |
| `publication_reports/dist/` | `d686bc2d…24fa00` | `94216193…3316d` | hashes exactement publiés dans `PROJECT_PUBLICATION_AUDIT.md` | `KEEP_HISTORICAL_EVIDENCE` |

Les différences peuvent venir du contenu source et des métadonnées de build. Ces fichiers
ne sont donc ni des doublons ni interchangeables. Aucun ne doit être déplacé ou régénéré
en place pendant un nettoyage.

### Rapports générés

| Zone | Constat | Classe |
|---|---|---|
| `audit_reports/` | environ 832 KiB; pytest, coverage, Ruff, build et HTML cités précisément par `PROJECT_RESTORED_AUDIT.md`; le rapport historique recommande lui-même de ne pas les versionner | `CLEANUP_CANDIDATE_REQUIRES_HUMAN` |
| `publication_reports/` | environ 880 KiB; résultats de publication et distributions dont les hashes sont affirmés dans le document suivi | `KEEP_HISTORICAL_EVIDENCE` |
| HTML coverage statique commun | quelques assets byte-identiques entre les deux dossiers (`favicon`, JS, CSS, `.gitignore`) | `DO_NOT_TOUCH` |

Les assets HTML identiques ne doivent pas être dédupliqués : ils appartiennent à deux
exécutions historiques distinctes. Une suppression d'`audit_reports/` resterait locale et
sans effet Git, mais rendrait plusieurs liens du rapport historique inconsultables dans ce
workspace; elle exige donc une décision humaine.

### Sessions et recherche locale

| Candidat | Constat | Classe |
|---|---|---|
| `session-ses_02a7.md`, `session-ses_ff22.md` | ignorés, non suivis, aucun historique Git ni référence entrante; environ 712 KiB | `DELETE_SAFE_LOCAL` |
| `docs/deepsearch/` | ignoré, non suivi dans cette branche, environ 288 KiB; `PROGRESSION.md` le déclare hors périmètre | `DO_NOT_TOUCH` |

`DELETE_SAFE_LOCAL` signifie seulement qu'une suppression future ne changerait pas Git ou
les preuves suivies; elle ne constitue pas une autorisation donnée par cet audit.

## 3. Documentation et preuves

### Fichiers temporaires en apparence

| Fichier | Constat | Classe |
|---|---|---|
| `PROGRESSION_TEMP.md` | suivi; dossier de passage P0, cité par la revue Critique; historique aux commits `d1ed53b`/`5ed9f07` | `KEEP_HISTORICAL_EVIDENCE` |
| `PROGRESSION_TEMP_CRITIQUE.md` | suivi; handoff P0 préservé à `7c322a8` | `KEEP_HISTORICAL_EVIDENCE` |
| `PROGRESSION_TEMP_CONTRADICTOIRE.md` | suivi; cité explicitement par `CONTRADICTOIRE_P0_BASELINE.md`, préservé à `7c322a8` | `KEEP_HISTORICAL_EVIDENCE` |

Les trois fichiers ont des SHA-256 différents; ils ne sont pas des copies jetables.

### Cycles REV, Contradictoire, heartbeat, demandes et addenda

`REV03.md`–`REV12.md` sont suivis et reliés aux rapports, registres, demandes de revue et
documents de progression. Les variantes `REV09bis`/`REV11bis`, supersessions, invalidation
et addenda encodent des distinctions procédurales explicites. Les heartbeats pointent vers
leurs rapports complets et matérialisent la chronologie des sessions.

Classification de toute cette famille : `KEEP_HISTORICAL_EVIDENCE`.

Un déplacement vers un répertoire plus esthétique changerait des chemins référencés dans
les documents et registres. Sans mécanisme de redirection stable et nouvelle admission,
il est `DO_NOT_TOUCH` en pratique.

### Hypothèses et gates

| Zone | Classe | Motif |
|---|---|---|
| `docs/fusion/hypotheses/H0001/` | `DO_NOT_TOUCH` | paquet admis, hashes et provenance |
| `docs/fusion/hypotheses/H0002/` | `DO_NOT_TOUCH` | paquet admis, premier run, hashes et provenance |
| `docs/fusion/hypotheses/H0003/` | `DO_NOT_TOUCH` | paquet initial rejeté + paquet corrigé admis; réécriture interdite |
| `docs/fusion/hypotheses/H0004/` | `KEEP_ACTIVE` | préenregistrement en cours, sans code |
| registres, gates, RFC et décisions P1/P6 | `KEEP_UNTIL_GATE_CLOSED` | sources normatives et historiques encore nécessaires |

Deux JSON suivis sont byte-identiques : `ORACLE_ADMISSIONS.json` et
`OPERATOR_SUPERSESSION_DECISIONS.json` ont le SHA-256 du tableau vide
`246f867f…c8209`. Ils représentent néanmoins deux registres sémantiquement distincts et
sont référencés séparément. Classification : `DO_NOT_TOUCH`.

### Documents racine

| Document/famille | État sémantique | Classe |
|---|---|---|
| `HYPOTHESIS.md`, `THESIS.md`, `METHODS.md`, `LIMITATIONS.md` | baseline normative/scientifique; largement référencée | `KEEP_HISTORICAL_EVIDENCE` |
| `CONTROLLED_MERGER_FEASIBILITY.md` | rapport directeur cité par le corpus fusion | `KEEP_UNTIL_GATE_CLOSED` |
| `PROJECT_PUBLICATION_AUDIT.md` | audit de publication canonique de la baseline | `KEEP_HISTORICAL_EVIDENCE` |
| `PROJECT_RESTORED_AUDIT.md` | explicitement supersédé pour publication, mais source historique et référencé | `KEEP_HISTORICAL_EVIDENCE` |
| `FINAL_VALIDATION_REPORT.md`, `PROJECT_SCIENTIFIC_VALIDATION.md`, `PROJECT_TECHNICAL_AUDIT.md` | rapports de la release initiale; peu ou pas de références entrantes mais partie du commit initial validé | `KEEP_HISTORICAL_EVIDENCE` |
| `AI_AFFINITY_ANALYSIS.md`, `ARCHAEOLOGICAL_RECONSTRUCTION.md` | analyses rétrospectives sans rôle de gate actuel | `KEEP_HISTORICAL_EVIDENCE` |

Aucun document racine examiné n'est démontré `ORPHANED` au sens supprimable. L'absence de
référence entrante ne suffit pas à neutraliser un livrable du commit initial ou une
reconstruction méthodologique versionnée.

## 4. Branches Git

Toutes les branches listées ont un upstream homonyme sur `origin` et sont à `ahead=0`,
`behind=0` au moment de l'audit. « Non merged » signifie non ancêtre de `main`; ce n'est
pas un jugement d'obsolescence. Les branches de la chaîne P1 sont ancêtres de H0004 et de
la branche d'audit, mais volontairement non fusionnées vers `main`.

| Branche | HEAD | Base/ancêtre pertinent | Merge | Rôle / statut | Suppression locale | Suppression distante |
|---|---|---|---|---|---|---|
| `main` | `bd1a9d5` | racine publiée | branche canonique | baseline / `ACTIVE` | NO | NO |
| `fusion/controlled-merger` | `e413867` | `main` | non fusionnée dans `main` | cible contrôlée / `ACTIVE` | NO | NO |
| `correction/reconcile-l1-l12` | `7c322a8` | descend de `e413867` | non fusionnée dans `main`; ancêtre chaîne P1 | consolidation et handoff P0 / `CLOSED_EVIDENCE` | NO | NO |
| `hypothesis/H0001-canonical-ledger-equivalence` | `de946c1` | base `7c322a8` | non fusionnée; ancêtre H0002+ | hypothèse admise / `CLOSED_EVIDENCE` | NO | NO |
| `hypothesis/H0002-short-ledger-generalization` | `68ca8f8` | base `de946c1` | non fusionnée; ancêtre diagnostic+ | hypothèse admise / `CLOSED_EVIDENCE` | NO | NO |
| `work/p1-capability-gap` | `56e770a` | base `68ca8f8` | non fusionnée; ancêtre H0003+ | profil documentaire / `WORK_ARCHIVE` | YES, seulement après décision humaine | NO |
| `hypothesis/H0003-canonical-contract-foundation` | `6313afc` | base `56e770a` | non fusionnée; ancêtre post-gap+ | hypothèse admise, rejet conservé / `CLOSED_EVIDENCE` | NO | NO |
| `work/p1-capability-gap-after-h0003` | `9c3b758` | base `6313afc` | non fusionnée; ancêtre H0004 | diagnostic documentaire / `WORK_ARCHIVE` | YES, seulement après décision humaine | NO |
| `hypothesis/H0004-minimal-spot-ledger` | `044406f` | base `9c3b758` | non fusionnée | préenregistrement bloqué / `IN_PROGRESS` | NO | NO |
| `work/continuation-2026-08-28` | `88a404b` | diverge de la chaîne P1 à `7c322a8` | non fusionnée | REV13/dette P6 / `IN_PROGRESS` | NO | NO |

La branche courante `work/repo-hygiene-audit` part de `044406f` et est `ACTIVE` jusqu'à
admission éventuelle du présent rapport. Elle ne doit pas être supprimée pendant l'audit.

Les deux branches `work/p1-capability-gap*` pourraient être supprimées **localement** sans
perte d'objet si leurs upstreams restent accessibles et si la filiation ci-dessus est
révérifiée au moment de l'action. Leur suppression distante n'est pas recommandée : elles
documentent les décisions ayant attribué H0003/H0004.

## 5. Plan de nettoyage proposé

### TIER 0 — nettoyage purement local et réversible

Décision humaine minimale, aucune modification Git :

1. supprimer les `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`, `.coverage` et
   `paper_trading_codex.egg-info/` (`DELETE_SAFE_LOCAL`);
2. supprimer le `dist/` racine courant (`DELETE_SAFE_LOCAL`), après confirmation qu'aucun
   opérateur ne souhaite examiner ce build précis;
3. supprimer les deux exports `session-ses_*.md` (`DELETE_SAFE_LOCAL`) après confirmation
   qu'ils ne sont pas une archive personnelle voulue;
4. ne pas toucher `audit_reports/`, `publication_reports/` ou `docs/deepsearch/` dans ce
   tier.

### TIER 1 — `.gitignore` / prévention de nouveau bruit

État actuel : protection déjà adéquate. Proposition : **aucun changement immédiat**.

Une amélioration future pourrait documenter dans `.gitignore` pourquoi
`publication_reports/` reste ignoré alors que certains fichiers locaux sont des preuves
historiques. Cette modification purement explicative est
`CLEANUP_CANDIDATE_REQUIRES_HUMAN`; elle n'est pas nécessaire à l'hygiène fonctionnelle.

### TIER 2 — suppressions Git potentiellement sûres nécessitant admission humaine

Aucune suppression suivie n'est actuellement démontrée sûre.

- `PROGRESSION_TEMP*` : `KEEP_HISTORICAL_EVIDENCE`;
- `REV*`, heartbeats, addenda et demandes : `KEEP_HISTORICAL_EVIDENCE`;
- rapports racine : `KEEP_HISTORICAL_EVIDENCE` ou `KEEP_UNTIL_GATE_CLOSED`;
- registres vides byte-identiques : `DO_NOT_TOUCH`.

Seule la suppression locale d'`audit_reports/` pourrait être étudiée, sans commit Git,
après une décision explicite sur la perte des liens consultables de
`PROJECT_RESTORED_AUDIT.md`. Classe : `CLEANUP_CANDIDATE_REQUIRES_HUMAN`.

### TIER 3 — archivage/réorganisation documentaire

Ne rien déplacer maintenant. Toute réorganisation de `REV*`, `PROGRESSION_TEMP*` ou
`docs/fusion/` casserait des liens et modifierait potentiellement des blobs/hashs admis.

Une future vue d'index peut être **ajoutée** sans déplacer les sources; c'est préférable à
un archivage physique. Un déplacement réel est `DO_NOT_TOUCH` jusqu'à fermeture des gates
concernés et protocole humain de migration des références.

### TIER 4 — refactors structurels hors mission

- packaging : `pyproject.toml` est explicitement la source de vérité;
  `setup.py` est un shim de compatibilité et `requirements.txt` un raccourci d'installation
  éditable. `flake.nix` + `flake.lock` définissent l'environnement Nix reproductible;
  `shell.nix` délègue au flake. `devenv.nix` répète la liste Python pour compatibilité
  devenv. Il existe une duplication de dépendances, mais pas une ambiguïté silencieuse sur
  la source de métadonnées. Classification : `KEEP_ACTIVE`; consolidation hors mission.
- branches : ne rebase, squash, merge ou supprime aucune branche historique dans un
  chantier d'hygiène;
- preuves : ne recalcule jamais en place un manifeste ou résultat admis;
- code et architecture : aucun refactor ne relève du toilettage conservateur.

## Arrêt

Le rapport s'arrête à l'inventaire et aux propositions. Aucun nettoyage n'a été exécuté.
Toute action Tier 0–4 attend une décision humaine distincte.
