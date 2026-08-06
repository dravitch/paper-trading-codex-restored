# Rapport Contradictoire — Delta f14546f (réponse Producteur M1–M4)

## Objet examiné

Commit Producteur `f14546ffd40cb1f1e65cd3f9ec52f208752b1d2f` « docs: resolve contradictory findings M1-M4 », branche `correction/reconcile-l1-l12`. Portée : réponse aux constats M1–M4 de `CONTRADICTOIRE_DELTA_DD4CDDE.md` (admis au commit `5a8ebe2`), documentée dans `REV07.md`, conformément à `docs/fusion/REVIEW_REQUEST_M1_M4.md`. Delta documentaire : `REV07.md` et `NO_GO_CYCLE_REGISTRY.json` créés; `06_FUSION_GATES.md`, `CAUSAL_ID_REGISTRY.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md`, `PROGRESSION.md` modifiés.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `f14546ffd40cb1f1e65cd3f9ec52f208752b1d2f` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité et sortie attendue

- Admission `dd4cdde` réelle : commit `5a8ebe2` « docs: admit contradictory review of delta dd4cdde », ancêtre de `f14546f`, contenu limité au rapport + heartbit.
- Réfutation 5 exécutée mécaniquement. Commandes : `git show <admission_commit>:<report_path> | sha256sum` pour les sept lignes du registre; `python3 -m json.tool docs/fusion/NO_GO_CYCLE_REGISTRY.json`. Résultat : **les sept SHA-256 concordent exactement** (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb, 02775ce, 5a8ebe2) et le JSON est valide (`{"schema_version":1,"cycles":[],"occurrences":[],"groups":[]}`). Code de sortie 0 sur toutes les vérifications.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Accepter phrase/sous-chaîne/ligne dupliquée/espace ajouté/verdict divergent comme marqueur `Oracle-Review` | **Échoue.** Marqueur = une ligne unique ancrée, expression complète `^Oracle-Review: oracle_id=(O2|O4|O7); verdict=(ACCEPT|ACCEPT_WITH_LIMITS|REJECT|NON_TESTABLE)$`, ASCII, sans espaces supplémentaires; phrase/citation/sous-chaîne ne correspond pas; deux lignes échouent; le verdict extrait doit égaler le verdict indexé. Réserve **N1** |
| 2 | Modifier un champ causal sous `occurrence_id` historique sans divergence de hash ni sanction | **Échoue.** `causal_payload_sha256` sur le JSON canonique `{cause_family_key,failure_signature,cause_key,root_cause_group_id,cycle_id}`; historique exigé = même ID **et** même hash présents dans un ancêtre antérieur à la désactivation; le contrôleur recalcule et compare au registre au `first_recorded_commit`; hash divergent → `INVALID_OCCURRENCE_HISTORY`, le contenu modifié ne peut jamais hériter du statut historique. Réserve **N2** |
| 3 | Obtenir un compteur de groupe inférieur à l'union des cycles du JSON | **Échoue dans le périmètre.** Source machine `NO_GO_CYCLE_REGISTRY.json` autoritaire; les unions sont recomposées uniquement depuis ce JSON; omission d'un cycle présent → `INCOMPLETE_GROUP_HISTORY` + cycle bloqué. `\|{A,B}∪{B,C}\|=3` satisfait. Réserve **N3** (éditabilité du JSON) |
| 4 | Introduire un `occurrence_id` ou un code de raison hors vocabulaire sans `NON_TESTABLE` | **Échoue pour les codes.** Codes de raison fermés (`INVALID_CAUSAL_ID_STATE`, `INVALID_OCCURRENCE_HISTORY`, `INCOMPLETE_GROUP_HISTORY`); tout autre code → `UNKNOWN_REASON_CODE` → `NON_TESTABLE`; ajout d'un code exige une révision normative. Réserve **N4** pour la forme `OCC-NNNNNN` (pas de regex ni de contrôle de provenance spécifiés) |
| 5 | Vérifier le JSON, les sept hashes et les contradictions entre `REV07.md`, registres et P6 | **Satisfaite — vérifié.** Sept hashes concordants, JSON valide, cohérence `REV07.md`↔registres↔P6 (marqueur unique par rapport, verdict ancré = statut enregistré, registre machine unique). Aucune contradiction bloquante trouvée; réserves N1–N4 |

## Constats

### N1 — M1 : la définition de « ligne » et le verdict indexé restent sous-normés

L'expression régulière est ancrée `^…$`, mais ni le traitement des fins de ligne (`\r` CRLF — l'expression échoue alors par excès de sécurité, sans politique déclarée), ni le référentiel du « verdict indexé » ne sont définis : le tableau d'admission n'a pas de colonne verdict, donc « celui indexé pour cet oracle » renvoie implicitement au `recorded_status` de la preuve courante sans être explicite. Contre-exemple minimal : un rapport conforme ne nommant pas lui-même son oracle ailleurs que dans la ligne `Oracle-Review` — l'appartenance oracle→rapport reste portée par la seule ligne. **Effet : comportement correct mais dépendant d'une lecture unique non normée.** Action : déclarer la politique CRLF et le référentiel exact du verdict indexé (colonne du registre ou champ de preuve).

### N2 — M2 : sérialisation canonique sous-définie pour `failure_signature` imbriqué

Le hash porte sur un objet dont `failure_signature` est imbriqué (`{component_id,symbol_id,failure_mode_id}`), mais la spécification « clés triées, UTF-8, séparateurs `,`/`:` sans espaces » ne dit pas si le tri est récursif ni comment l'objet imbriqué est sérialisé. Contre-exemple minimal : deux implémentations du contrôleur triant seulement les clés de premier niveau produisent des hash différents pour le même payload → soit faux `INVALID_OCCURRENCE_HISTORY`, soit divergence de hash non détectée si l'ordre interne diffère. **Effet : le contrat de hash n'est pas reproductible entre implémentations.** Action : normer la sérialisation canonique récursive (tri récursif des clés, encodage des chaînes et des entiers) et fournir un vecteur de test.

### N3 — M3 : le registre machine est éditable — un cycle retiré du JSON n'est plus « présent »

L'union est recomposée depuis les cycles « présents dans la source machine ». Aucune règle n'interdit la suppression d'un cycle déjà enregistré du JSON (la contrainte « ne peut ajouter ni retirer un cycle » vise le tableau Markdown, pas le JSON). Contre-exemple minimal : retirer un `cycle_id` du JSON puis créer le groupe → le cycle n'étant plus « présent », l'union est plus petite et `INCOMPLETE_GROUP_HISTORY` n'est pas déclenché; la modification est visible dans l'historique mais rien ne la sanctionne mécaniquement. **Effet : l'autorité du registre dépend de son intégrité d'édition.** Action : interdire la suppression des cycles/occurrences/groups enregistrés (supersession seulement) ou ancrer le hash des blobs JSON antérieurs dans les entrées de groupe.

### N4 — M4 : la forme `OCC-NNNNNN` manque de regex et de contrôle de provenance

Contrairement à M1 (expression complète donnée), la forme d'occurrence est énoncée sans regex et l'« allocation monotone » est un devoir, pas un contrôle de rejet. Contre-exemple minimal : un `occurrence_id` `OCC-000000` ou `OCC-999999` injecté manuellement respecte la forme affichée et n'est pas rejeté par une règle mécanique. **Effet : fermeture du vocabulaire incomplète pour les occurrences.** Action : normer l'expression exacte et le contrôle d'allocation (contiguïté, provenance par le contrôleur NO-GO).

## Verdict

**ACCEPT_WITH_LIMITS**

Les cinq réfutations échouent dans leur périmètre : le marqueur `Oracle-Review` est une ligne unique ancrée et à verdict fermé, la modification causale fait diverger un hash recalculé contre le registre au `first_recorded_commit`, le compteur de groupe est recomposé depuis le JSON autoritaire, les codes de raison sont fermés, et le JSON ainsi que les sept hashes d'admission sont vérifiés concordants.

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs :

- **N1** — normer la politique CRLF et le référentiel exact du verdict indexé pour le marqueur;
- **N2** — normer la sérialisation canonique récursive de `failure_signature` avec vecteur de test;
- **N3** — interdire la suppression des entrées enregistrées du registre machine (supersession) ou ancrer les hashes des blobs antérieurs;
- **N4** — donner l'expression exacte et le contrôle d'allocation pour `OCC-NNNNNN`.

Effet sur les gates : **aucun**. Le registre machine est vide (aucun cycle exécuté), aucun blob admis ne porte de ligne `Oracle-Review` (tous `Oracle scope = —`), la preuve d'immuabilité reste absente → P6 reste `BLOCKED_IMMUTABILITY`; P0 garde ses blocages connus. Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
