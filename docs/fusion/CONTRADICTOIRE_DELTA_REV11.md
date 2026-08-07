# Rapport Contradictoire — delta REV11 (réponse Producteur Q1–Q4)

## Objet examiné

Commit Producteur `3876fce12eb23daa78293a803a7a658afb5b10bc` « docs: resolve contradictory findings Q1-Q4 », branche `correction/reconcile-l1-l12`, cible `fusion/controlled-merger`. Portée : réponse aux constats Q1–Q4 de `CONTRADICTOIRE_DELTA_REV10.md` (admis au commit `ae5eb92`), documentée dans `REV11.md`, conformément à `docs/fusion/REVIEW_REQUEST_Q1_Q4.md`. Delta documentaire : `REV11.md` créé; `docs/fusion/ORACLE_ADMISSIONS.json` créé (vide); `CAUSAL_ID_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `06_FUSION_GATES.md`, `PROGRESSION.md` modifiés. Aucun contrôleur n'est implémenté.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06/07 |
| révision examinée | `3876fce12eb23daa78293a803a7a658afb5b10bc` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict (aucun fichier `CRITIQUE_*` ni `docs/deepsearch/*` consulté); aucun auto-déclenchement Producteur pour ce cycle |

## Vérifications préalables d'intégrité et sortie attendue

- Admission `ae5eb92` réelle : contenu limité au rapport + heartbit, ancêtre de `3876fce` (vérifié par `git merge-base --is-ancestor`), `3876fce` ancêtre de la révision courante `510d3f5`, non ancêtre de `ae5eb92`.
- Réfutation 5 exécutée mécaniquement. Commandes : `git show <admission_commit>:<report_path> | sha256sum` pour les onze lignes du registre; `python3 -m json.tool` sur `NO_GO_CYCLE_REGISTRY.json` et `ORACLE_ADMISSIONS.json`; calcul SHA-256 de la ligne `Oracle-Admission` (vecteur `7dcf17…`) et des trois vecteurs causaux; `git rev-list --first-parent --max-count=1 "C^1" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json`; `git show` des blobs aux commits de la chaîne.
- Résultat : **les onze SHA-256 concordent exactement** (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb, 02775ce, 5a8ebe2, cf6aa7a, a7c8a69, `4f281b7` = `981e5b08…`, `ae5eb92` = `0a865294…`), les deux JSON sont valides, `ORACLE_ADMISSIONS.json` = `{schema_version:1, records:[]}`, le vecteur machine produit `7dcf174ee657868f5dc784973bf6cface2d62ef9ee1b51145139562f1be07067` et les trois vecteurs causaux `51857e…75e6`, `eacf3f…7563`, `5ab872…feee` (tous exacts). Code de sortie 0 sur toutes les vérifications.
- Chaîne du registre : `4ff3bef1…` (genesis `930b0f9`) → `a7ad22af…` (`6867a2d`) → `9e626d79…` (`7039476`); `git rev-list --first-parent --max-count=1 "7039476^1" -- fichier` = `6867a2d`, blob `a7ad22af…` = `previous_blob_sha256` déclaré. `3876fce` porte le blob `9e626d79…` sans le modifier.
- Table **Admissions d'oracles** vide → aucune preuve P6 admissible; `Oracle scope` = `—` pour les onze blobs admis.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Faire lire une admission depuis le Markdown/fence ou accepter doublon, mauvais ordre, oracle/champ inconnu dans `ORACLE_ADMISSIONS.json` | **Échoue.** La seule source machine est `ORACLE_ADMISSIONS.json`, « jamais ce fichier Markdown ni un bloc de code ». Schéma fermé `{schema_version:1, records:[…]}`, records triés selon l'ordre fermé `O2`, `O4`, `O7`, au plus une entrée par oracle, aucune autre clé racine ou d'enregistrement. Grammaire de rendu : préfixe ASCII exact `Oracle-Admission: ` + objet canonique à cinq clés dans l'ordre canonique, regex par champ, clés dupliquées rejetées avant construction d'objet. Vecteur recalculé = `7dcf17…067` (attendu). Mutants (octet, permutation/duplication, verdict/commit/hash/chemin, CR, réordonnancement, doublon) bloquent tous P6. Réserve **S1** |
| 2 | Faire compter une fixture `NON_CANONICAL_CAUSAL_JSON` comme cycle, ou faire ignorer la corruption canonique d'une occurrence déjà enregistrée | **Échoue.** L'erreur canonique survient avant allocation d'`occurrence_id`/`cycle_id`/famille/groupe : aucune entrée dans le registre NO-GO, ne compte jamais comme cycle bloqué, inscrite seulement dans le rapport de validation d'entrée. À l'inverse, un payload déjà enregistré devenu non canonique à la relecture → `REGISTRY_HISTORY_VIOLATION`, qui compte comme cycle bloqué. Le code est retiré de la table des raisons NO-GO; `MERGE_REGISTRY_CONFLICT` est ajouté. Réserve **S2** |
| 3 | Faire accepter résultat first-parent vide hors genesis, merge divergent, merge modifiant le registre ou saut d'une révision | **Échoue.** Commande épinglée : `git rev-list --first-parent --max-count=1 "C^1" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json`; sortie vide autorisée uniquement si `C` est exactement la genesis (parent/hash `null`, tableaux vides), interdite autrement. Merge : blobs des parents comparés, toute divergence avec le premier parent → `MERGE_REGISTRY_CONFLICT`; un merge ne peut ni modifier ni réconcilier le registre (réconciliation = commit linéaire ultérieur + décision versionnée + union exhaustive validée). Saut d'une révision et précédence `previous_blob_sha256` fermés par mutants obligatoires. Vérifié sur la chaîne réelle. Réserve **S3** |
| 4 | Injecter SUP-000000, trou, doublon, ID appelant, raison inconnue ou `decision_commit` absent/non-ancêtre/simultané sans rejet | **Échoue.** `supersession_id` : `^SUP-[0-9]{6}$`, domaine `SUP-000001`–`SUP-999999`, tout SUP proposé rejeté, allocation `SUP-{n+1:06d}` en transaction, séquence exacte `000001..len(supersessions)` sans trou/doublon/réutilisation. `reason_code` ∈ `{CORRECT_CAUSAL_PAYLOAD, REATTRIBUTE_CAUSE, REPAIR_METADATA}`. `decision_commit` : `[0-9a-f]{40}`, existe dans le dépôt, ancêtre strict du commit écrivant la supersession, contient une décision opérateur; décision simultanée refusée. Réserve **S4** |
| 5 | Valider les deux JSON, les onze hashes d'admission et la cohérence de REV11 avec les gates/registres | **Satisfaite — vérifié.** Deux JSON valides; onze hashes concordants; vecteurs `51857e`/`eacf3f`/`5ab872`/`7dcf17` concordants; chaîne et parent first-parent vérifiés; admission `ae5eb92` ancêtre, distincte, limitée au rapport + heartbit. Aucune contradiction bloquante inter-documents (REV11 ↔ ORACLE_ADMISSIONS.json ↔ NO_GO_CYCLE_REGISTRY.json ↔ CAUSAL_ID_REGISTRY ↔ NO_GO_REGISTER ↔ REVIEW_ADMISSION_REGISTRY ↔ 06_FUSION_GATES ↔ LIMIT_RESOLUTION_REGISTER ↔ PROGRESSION) |

## Constats

### S1 — `ORACLE_ADMISSIONS.json` : pas de chaîne append-only ni de règle de mutation des records

Le fichier est désormais la seule source machine des admissions d'oracles, avec ordre fermé et unicité par snapshot. Mais aucune règle d'évolution des `records` n'est énoncée : ajout progressif d'un oracle (ex. `O4` ajouté après `O2`), modification d'un record existant, retrait, ni la chaîne d'immuabilité du fichier (parent/hash/sous-ensembles, contrairement à `NO_GO_CYCLE_REGISTRY.json`). Les mutants « modifier un octet / changer verdict » valident un blob donné, pas l'historique du fichier. **Effet : la protection contre une réécriture rétroactive d'une admission repose uniquement sur la preuve externe (absente → P6 bloqué), pas sur une contrainte mécanique propre au fichier.** Action : étendre append-only/parent-blob à `ORACLE_ADMISSIONS.json` ou énoncer sa sémantique de mutation.

### S2 — Rapport de validation d'entrée indéfini et frontière `INVALID_OCCURRENCE_HISTORY`/`REGISTRY_HISTORY_VIOLATION` non tracée

La classification pré-validation (jamais de compteur) est claire. Mais le « rapport de validation d'entrée » qui inscrit `NON_CANONICAL_CAUSAL_JSON` (avec hash des octets rejetés, sans recopier le contenu) n'a ni emplacement, ni schéma, ni chaîne ni rétention. Par ailleurs, pour une entrée déjà enregistrée, la frontière n'est pas tracée entre `INVALID_OCCURRENCE_HISTORY` (règle 10 : hash divergent de l'occurrence) et `REGISTRY_HISTORY_VIOLATION` (payload redevu non canonique) lorsque les deux conditions sont simultanément vraies. **Effet : l'auditabilité des rejets et le code de raison applicable à un historique corrompu restent à l'implémentation.** Action : normer le rapport d'entrée et prioriser les codes sur une entrée corrompue.

### S3 — Le « commit candidat C » n'est pas épinglé comme révision du registre : faux `REGISTRY_HISTORY_VIOLATION` sur un commit non-révision

La commande first-parent est fermée, mais `C` n'est pas défini comme un commit qui **modifie** le registre. Vérification mécanique : le blob `9e626d79…` a été créé au commit `7039476` avec `previous_blob_sha256: a7ad22af…` (blob de `6867a2d`); le commit `3876fce` porte le même blob sans le modifier. En appliquant la règle au candidat `C=3876fce`, `git rev-list --first-parent --max-count=1 "3876fce^1" -- fichier` renvoie `7039476`, dont le blob `9e626d79…` diffère du `previous_blob_sha256` déclaré → `REGISTRY_HISTORY_VIOLATION` **faussement positif** sur la chaîne pourtant valide. **Effet : tout contrôleur qui valide le registre à un commit non-révision (ex. un commit P6 ultérieur) rejette une chaîne légitime.** Action : épingler `C` = révision du registre (dernier ancêtre ayant modifié le fichier) ou redéfinir `previous_blob_sha256` relativement à la révision précédente du fichier.

### S4 — `decision_commit` : localisation et format de la « décision opérateur » non définis

L'existence, l'ancestralité stricte et la non-simultanéité du `decision_commit` sont fermées. Mais « contient une décision opérateur nommant l'occurrence source et la raison » suppose que le contrôleur lise et interprète un document versionné dont ni l'emplacement ni la grammaire ne sont spécifiés, et qu'il croise la raison déclarée (`reason_code`) avec le contenu de cette décision. Aucune règle ne dit où vit la décision (fichier, tableau), quelle en est la forme minimale, ni comment le contrôleur vérifie qu'elle « nomme » bien l'occurrence et la raison. **Effet : la dernière condition de la supersession n'est pas mécaniquement implémentable telle quelle.** Action : normer l'emplacement/format de la décision opérateur et le croisement avec `reason_code`.

## Verdict

**ACCEPT_WITH_LIMITS**

Les cinq réfutations échouent dans leur périmètre : lecture exclusivement depuis `ORACLE_ADMISSIONS.json` (Markdown/fence ignorés, doublon/ordre/oracle/champ invalides), `NON_CANONICAL_CAUSAL_JSON` en pré-validation sans compteur (et `REGISTRY_HISTORY_VIOLATION` pour une entrée déjà enregistrée), commande first-parent épinglée avec genesis/merge/saut fermés et chaîne réelle vérifiée, espace `SUP` complet avec raisons fermées et `decision_commit` ancré, et les deux JSON, les onze hashes d'admission, les vecteurs et la cohérence inter-documents vérifiés concordants.

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs :

- **S1** — étendre append-only/parent-blob à `ORACLE_ADMISSIONS.json` ou énoncer sa sémantique de mutation;
- **S2** — normer le rapport de validation d'entrée et la priorité `INVALID_OCCURRENCE_HISTORY`/`REGISTRY_HISTORY_VIOLATION` sur une entrée corrompue;
- **S3** — épingler `C` = révision du registre (faux positif démontré sur `3876fce`);
- **S4** — normer l'emplacement/format de la décision opérateur et le croisement avec `reason_code`.

(La lettre R est déjà allouée aux limites résiduelles R1–R8; la série continue donc en S.)

Effet sur les gates : **aucun**. Le registre machine est vide (aucun cycle exécuté), la table d'admissions d'oracles est vide (aucun oracle admissible), la preuve d'immuabilité externe reste absente → P6 reste `BLOCKED_IMMUTABILITY`; P0 garde ses blocages connus. Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
