# Pourquoi les IA sont à l'aise dans ce projet

**Date** : 2026-08-19
**Statut** : Analyse rétrospective des origines méthodologiques

## Constat

Toutes les IA ayant travaillé sur ce projet (Critique, Contradictoire, Producteur) montrent un niveau de rigueur inhabituel. Trois caractéristiques structurelles expliquent cette affinité.

## 1. Précontraintes fortes — origine : `06_FUSION_GATES.md`

**Document fondateur** : `docs/fusion/06_FUSION_GATES.md`, commit initial `d82fb3a` (2026-08-06).

Le gate system impose un cadre binaire : `PASS`, `FAIL`, `BLOCKED`, `NON_TESTABLE`. Chaque gate exige :
- des artefacts nommés (pas « il faut des tests » mais « `REPRODUCIBILITY_MANIFEST.json` »)
- des commandes exactes avec exit code
- des **mutations obligatoires** qui doivent échouer

Ce n'est pas un document de méthodologie importé. C'est un ensemble de contraintes conçu **dès le départ** pour un workflow IA. La colonne « Mutation devant échouer » de la table des gates est le signal le plus clair : le projet a été pensés pour des agents qui vérifient mécaniquement, pas pour des humains qui lisent du code.

**Évolution** : les 14 cycles de revue Contradictoire ont renforcé ces précontraintes à chaque itération. Chaque constat (L1–L12, R1–R8, … S1–S4) a ajouté des mutants, des schémas JSON fermés et des règles Git-chained. Le gate initial était un squelette ; les revues l'ont ossifié.

## 2. Vérifiabilité mécanique — origine : `PROTOCOL_CONTRADICTOIRE.md` + pratique des revues

**Document fondateur** : `docs/fusion/PROTOCOL_CONTRADICTOIRE.md`, commit `d82fb3a` (2026-08-06).

Le protocole exige dès l'article 5.3 :

> « Les deux évaluations enregistrent au minimum : identité et version du modèle lorsque disponibles, date, révision Git, prompt ou mandat, fichiers examinés, commandes exécutées, verdict et objections ouvertes. Une simple mention 'reviewed by AI' est invalide. »

Cette règle a évolué **par la pratique** plutôt que par écriture anticipée :

- **Cycles L1–L12** : les revues documentaires ont produit des constats textuels vérifiables (hashes, références Git)
- **Cycle P0** (`CONTRADICTOIRE_P0_BASELINE.md`) : première exécution sur VM dédiée avec `systemd-run -p PrivateNetwork=yes`, `pip freeze`, `coverage.xml`, `sha256sum` — la vérifiabilité mécanique est devenue **matérielle** (pas seulement documentaire)
- **Cycles S1–S4** : la chaîne `git rev-list --first-parent --max-count=1` est devenue la vérification standard pour les registres append-only

Ce n'est pas une méthodologie importée. C'est une **pratique émergente** qui s'est formalisée à chaque fois qu'une revue a trouvé un écart entre « ce qui est écrit » et « ce qui est vérifiable ».

## 3. Registres append-only — origine : `NO_GO_REGISTER.md` + `CAUSAL_ID_REGISTRY.md`

**Documents fondateurs** : `docs/fusion/NO_GO_REGISTER.md` et `docs/fusion/CAUSAL_ID_REGISTRY.md`, commit `d82fb3a` (2026-08-06).

Le pattern append-only avec chaînage Git (parent blob hash + sous-ensembles obligatoires) a été conçu dès le départ pour les registres machine :

- `NO_GO_CYCLE_REGISTRY.json` : chaîné via `parent_registry_commit` + `previous_blob_sha256`
- `ORACLE_ADMISSIONS.json` : chaîné via `rev-list --first-parent` (ajouté au cycle S1, constaté comme manquant dans `CONTRADICTOIRE_DELTA_REV11.md` : « pas de chaîne append-only ni de règle de mutation des records »)
- `OPERATOR_SUPERSESSION_DECISIONS.json` : schéma fermé `DEC-*` contigu, ajouté au cycle S1–S4

Le pattern n'est pas unique à ce projet — c'est un pattern de blockchain/append-only log. Mais son **application aux registres de décisions IA** est spécifique. L'idée centrale : si une IA peut réécrire l'historique des ses propres admissions, le protocole perd sa valeur. Le chaînage Git résout ce problème sans infrastructure externe.

**Raffinements par les revues** :
- REV08 (`CONTRADICTOIRE_DELTA_REV08.md`) : « l'append-only dépend d'une définition de genesis ambigüe » → genesis définie par commit de création
- REV09 (`CONTRADICTOIRE_DELTA_REV09.md`) : « parent_registry_commit est déclaré librement » → exigé = révision précédente
- REV12 (`CONTRADICTOIRE_DELTA_REV12.md`) : « merge transparent divergent invisible à rev-list » → réserve T2 ouverte

## Ce qui n'est PAS une skill

Ces trois patterns ne forment **pas une skill réutilisable telle quelle**. Ils sont émergents du projet :

| Pattern | Importé ? | Spécifique au projet ? |
|---|---|---|
| Gates PASS/FAIL avec mutants | non — conçu pour ce projet | oui — les mutants sont domain-specific |
| Vérifiabilité mécanique | partiellement — pratiques standard de testing | non — mais l'application aux revues IA l'est |
| Append-only Git-chained | oui — pattern blockchain classique | non — mais l'application aux registres de décisions IA l'est |

La **vraie skill émergente** est la combinaison des trois : un protocole où les IA ne peuvent pas se tromper sur ce qu'elles savent (gates), ne peuvent pas prétendre avoir vérifié sans preuve (mécanique), et ne peuvent pas réécrire leur historique (append-only). C'est cette combinaison qui crée l'affinité — pas un document de méthodologie unique.

## Référence : `PROTOCOL_OBSERVATIONS_FROM_P0.md`

Les observations 1–8 de P0 confirment cette analyse rétrospective. L'observation 7 est particulièrement pertinente :

> « Toute la chaîne NO-GO, les registres causaux, les schémas JSON et les mutants sont spécifiés mais pas implémentés. La chaîne documentaire est cohérente, mais aucun code ne la valide mécaniquement. »

Le contrôleur (code qui exécute les gates) n'existe pas encore. Les IA travaillent dans un système où les **règles sont mécaniques mais l'exécution est encore humaine/IA**. C'est un état transitoire — et c'est peut-être pour ça que ça fonctionne bien : les IA sont les meilleures pour exécuter des protocoles mécaniques qui ne sont pas encore automatisés.
