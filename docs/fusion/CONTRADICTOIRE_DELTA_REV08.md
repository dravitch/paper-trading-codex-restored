# Rapport Contradictoire — delta REV08 (réponse Producteur N1–N4)

## Objet examiné

Commit Producteur `930b0f9292c18d74b99a3daabc53f1af2b7fba68` « docs: resolve contradictory findings N1-N4 », branche `correction/reconcile-l1-l12`, cible `fusion/controlled-merger`. Portée : réponse aux constats N1–N4 de `CONTRADICTOIRE_DELTA_F14546F.md` (admis au commit `cf6aa7a`), documentée dans `REV08.md`, conformément à `docs/fusion/REVIEW_REQUEST_N1_N4.md`. Delta documentaire : `REV08.md` créé; `NO_GO_CYCLE_REGISTRY.json` modifié (ajout `previous_blob_sha256: null`); `CAUSAL_ID_REGISTRY.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md`, `PROGRESSION.md` modifiés. Aucun contrôleur n'est implémenté.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `930b0f9292c18d74b99a3daabc53f1af2b7fba68` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict (aucun fichier `CRITIQUE_*` pour `REV08` dans le dépôt) |

## Vérifications préalables d'intégrité et sortie attendue

- Admission `f14546f` réelle : commit `cf6aa7a` « docs: admit contradictory review of delta f14546f », ancêtre de `930b0f9` (vérifié par `git merge-base --is-ancestor`), contenu limité au rapport + heartbit.
- `930b0f9` est ancêtre de la révision courante `21aefbb` (demande de revue).
- Réfutation 5 exécutée mécaniquement. Commandes : `git show <admission_commit>:<report_path> | sha256sum` pour les huit lignes du registre; `python3 -m json.tool docs/fusion/NO_GO_CYCLE_REGISTRY.json`; calcul SHA-256 du vecteur normatif en Python; `git log --follow` et `git show` sur `NO_GO_CYCLE_REGISTRY.json`; regex `fullmatch` sur les marqueurs et les formes `OCC-NNNNNN`.
- Résultat : **les huit SHA-256 concordent exactement** (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb, 02775ce, 5a8ebe2, cf6aa7a), le JSON est valide (`{"schema_version":1,"previous_blob_sha256":null,"cycles":[],"occurrences":[],"groups":[]}`), le vecteur produit `51857ebbbcc0155f75bf33ae635a6f865a17e74cd324a7cd063c1ef3b47375e6`. Code de sortie 0 sur toutes les vérifications.
- Aucun blob admis ne contient de ligne complète `Oracle-Review: oracle_id=(O2|O4|O7); verdict=(…)$` (les quatre occurrences textuelles dans `F14546F` sont des citations/tables, aucune ne matche l'expression ancrée) → `Oracle scope = —` pour tous les blobs admis, table d'admissions d'oracles vide.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Faire accepter CRLF, plusieurs marqueurs ou un verdict absent de la table d'admissions d'oracles | **Échoue.** Mécaniquement : `fullmatch('^Oracle-Review: oracle_id=(O2|O4|O7); verdict=(ACCEPT|ACCEPT_WITH_LIMITS|REJECT|NON_TESTABLE)$')` est `False` sur une ligne terminée par `\r`; deux lignes matchent → décompte > 1 → non admissible; la table **Admissions d'oracles** est vide (`aucune admission à ce jour`), or la preuve n'est admissible que si son `oracle_id` appartient à cette table, et le verdict extrait doit égaler la colonne `Verdict indexé`, jamais `recorded_status` courant. Réserve **O1** |
| 2 | Produire deux hashes pour le vecteur causal normatif en respectant toutes les règles, ou modifier une valeur imbriquée sans changer le hash | **Échoue.** Vecteur recalculé = `51857e…75e6` (attendu). Sérialisation canonique récursive : clés triées à tous les niveaux, séparateurs fixés, un seul encodage octet → un seul hash par payload logique; modifier une valeur imbriquée change les octets; permuter l'ordre des clés imbriquées produit les mêmes octets canoniques (le tri récursif absorbe la permutation — test falsifiable de REV08 vérifié). Réserve **O2** |
| 3 | Retirer ou modifier une entrée historique du registre JSON sans `REGISTRY_HISTORY_VIOLATION`; chercher une ambiguïté au passage genesis→première écriture | **Échoue comme exploit, ambiguïté réelle trouvée.** Aucune entrée n'existe (listes vides) → aucun retrait/modification démontrable; le retrait d'une entrée d'un parent non vide est fermé par les règles de sous-ensemble obligatoire, d'identité octet-pour-octet et de `previous_blob_sha256` = sha du blob parent. En revanche le passage genesis→première écriture est **non décidable** (voir O3) et l'état courant s'y trouve. Réserve **O3** |
| 4 | Injecter `OCC-000000`, un trou, doublon, ID hors domaine ou ID fourni par l'appelant sans rejet | **Échoue.** `OCC-000000` matche la regex mais est hors domaine `OCC-000001`–`OCC-999999` et hors séquence `000001..len`; trou/doublon/réutilisation → séquence exacte exigée; `OCC-1000000` (7 chiffres) rejeté par `[0-9]{6}`; registre épuisé → `NON_TESTABLE`; « le contrôleur rejette tout ID proposé ». Réserve **O4** |
| 5 | Recalculer le vecteur SHA-256, valider le JSON et les huit hashes d'admission | **Satisfaite — vérifié.** Vecteur concordant, JSON valide, huit hashes concordants, admission `cf6aa7a` ancêtre et sans la modification Producteur évaluée. Aucune contradiction bloquante trouvée |

## Constats

### O1 — Marqueur : « ligne candidate » et référentiel temporel du « Verdict indexé » sous-normés

La politique CRLF est désormais explicite (« découpé uniquement sur l'octet LF (0A). Tout CR (0D) sur la ligne candidate rend le marqueur invalide ») et mécaniquement vérifiée. Il reste deux points non normés : (a) « seconde ligne candidate » sans définition de ce qu'est une « candidate » — une ligne quasi-marquante non ancrée (ex. `# Oracle-Review: …`, citation) est ignorée plutôt que rejetée; aucune règle ne dit si elle compte dans le décompte d'admissibilité. (b) La ligne `Verdict indexé` est ajoutée « dans un commit d'indexation postérieur au commit d'admission » alors que le contrôleur lit le blob au commit d'admission : le référentiel temporel de la colonne (commit consulté, interdiction d'un accord rétroactif, indépendance de l'indexation) n'est pas ancré, et aucune mutation prescrite ne teste « changer le verdict indexé pour diverger du rapport ». **Effet : comportement de rejet correct aujourd'hui, mais porteur d'une lecture non unique à l'implémentation.** Action : définir mécaniquement « ligne candidate » et ancrer le commit de référence de la colonne `Verdict indexé`.

### O2 — Sérialisation : échappement minimal et normalisation Unicode non épinglés

Le tri récursif, les types, l'encodage UTF-8 et les séparateurs sont définis; le vecteur est vérifié. Mais « échappement JSON minimal » n'épingle pas le jeu exact de caractères échappés (`\"`, `\\`, `<0x20` en `\uXXXX`; `\/` autorisé ou non), et aucune normalisation Unicode (NFC/NFD) n'est fixée : deux implémentations normalisant différemment une même chaîne logique non-ASCII produisent deux encodages octet → deux hashes. Le vecteur ne couvre que ASCII/string/null; pas d'entier, de tableau, de chaîne échappée ou non-ASCII. **Effet : pour le vecteur donné le contrat est déterministe, mais pas encore reproductible pour le cas général.** Action : épingler le jeu d'échappements et la normalisation Unicode, étendre le vecteur de test.

### O3 — Registre : passage genesis→première écriture non décidable; la migration du schéma du registre est dans la zone grise

Le registre a été créé à `f14546f` (schéma sans `previous_blob_sha256`, listes vides). Le commit examiné `930b0f9` l'a réécrit (ajout de `previous_blob_sha256: null`); le blob du registre au commit parent `4e96e92` est `de815fd7…`, différent du `null` revendiqué. « Le blob genesis seul porte `previous_blob_sha256: null` » : le blob courant n'est pas le premier blob du fichier (le premier est celui de `f14546f`). Deux lectures possibles non départagées : stricte — `930b0f9` viole sa propre règle (`previous_blob_sha256` ≠ sha du blob du parent) et l'état courant serait `NON_TESTABLE` `REGISTRY_HISTORY_VIOLATION`; par contenu — toute migration de schéma peut réinitialiser une « genesis » tant que les listes sont vides, ouvrant un ré-amorçage de la chaîne. Le « commit parent déclaré » n'a aucun porteur dans le schéma JSON (pas de `parent_commit`/`genesis_commit`), la migration `schema_version` est non régulée et l'algorithme de localisation du blob parent (recherche d'ancêtre par hash) est non spécifié. **Effet : l'append-only dépend d'une définition de genesis ambigüe.** Action : définir genesis par commit de création ou champ `genesis_commit`, déclarer le mécanisme du commit parent, réguler la migration `schema_version` (dont l'écart `f14546f`→`930b0f9` lui-même).

### O4 — Occurrences : interaction supersession ↔ allocation et statut des supersédées non définis

La regex, le domaine, la séquence contiguë et l'allocation exclusive sont désormais normés; les injections sont toutes rejetées. Restent deux zones non définies : (a) « le contrôleur rejette tout ID proposé » vs « une correction ajoute une entrée de supersession pointant vers l'identité antérieure » — la supersession exige que l'opérateur nomme un ID existant; la distinction entre proposition d'un ID neuf (rejetée) et référence d'un ID existant dans une supersession (autorisée) n'est pas énoncée. (b) Le validateur exige « la séquence exacte `000001..len(occurrences)` » sans préciser si une occurrence supersédée reste comptée dans `len` (la réutilisation est interdite, mais la place dans la séquence d'une entrée supersédée n'est pas spécifiée). **Effet : fermeture correcte des injections, supersession sous-définie.** Action : préciser la supersession (référence d'ID existant, allocation d'un éventuel nouvel ID par le contrôleur) et le statut des supersédées dans la séquence.

## Verdict

**ACCEPT_WITH_LIMITS**

Les cinq réfutations échouent dans leur périmètre : CRLF, plusieurs marqueurs et verdict absent de la table d'oracles sont rejetés, le vecteur causal normatif est unique et vérifié (`51857e…75e6`), le retrait d'une entrée enregistrée est fermé par l'append-only (parent hash + sous-ensembles + octet-pour-octet), les injections `OCC-000000`/trou/doublon/hors domaine/appelant sont rejetées, et le vecteur, le JSON et les huit hashes d'admission sont vérifiés concordants.

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs :

- **O1** — définir mécaniquement « ligne candidate » et ancrer le référentiel temporel/indépendant de la colonne `Verdict indexé`;
- **O2** — épingler le jeu d'échappements minimal et la normalisation Unicode, étendre le vecteur de test;
- **O3** — définir genesis par commit de création (ou `genesis_commit`), déclarer le « commit parent déclaré », réguler la migration `schema_version` et résoudre l'écart `f14546f`→`930b0f9`;
- **O4** — distinguer proposition d'ID (rejetée) de référence d'ID existant dans une supersession (autorisée) et préciser le statut des supersédées dans la séquence.

Effet sur les gates : **aucun**. Le registre machine est vide (aucun cycle exécuté), la table d'admissions d'oracles est vide (aucun oracle admissible), la preuve d'immuabilité externe reste absente → P6 reste `BLOCKED_IMMUTABILITY`; P0 garde ses blocages connus. Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
