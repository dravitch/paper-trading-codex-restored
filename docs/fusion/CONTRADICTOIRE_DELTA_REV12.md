# Rapport Contradictoire — delta REV12 (réponse Producteur S1–S4)

## Objet examiné

Commit Producteur `777fc23c4d0683853fe7ae7bf160059f9a2fea5a` « docs: resolve contradictory findings S1-S4 », branche `correction/reconcile-l1-l12`, cible `fusion/controlled-merger`. Portée : réponse aux constats S1–S4 de `CONTRADICTOIRE_DELTA_REV11BIS.md` (admis `102ce6a`, indexé `d8bc959`), documentée dans `REV12.md`, conformément à `docs/fusion/REVIEW_REQUEST_S1_S4.md`. Delta : `REV12.md` créé; `OPERATOR_SUPERSESSION_DECISIONS.json` créé (vide); `06_FUSION_GATES.md`, `CAUSAL_ID_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `PROGRESSION.md` modifiés. Aucun contrôleur n'est implémenté.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-07 |
| révision examinée | `777fc23c4d0683853fe7ae7bf160059f9a2fea5a` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict (aucun fichier `CRITIQUE_*`, `docs/deepsearch/*`, `REVUE_CRITIQUE_*` consulté) |

## Vérifications préalables d'intégrité et sortie attendue

- Ancêtres : `102ce6a` et `d8bc959` sont ancêtres de `777fc23` (`git merge-base --is-ancestor`, code 0).
- Réfutation 5 exécutée mécaniquement : `python3 -m json.tool` code 0 sur les trois JSON (`ORACLE_ADMISSIONS.json`, `OPERATOR_SUPERSESSION_DECISIONS.json`, `NO_GO_CYCLE_REGISTRY.json`); `git diff --check 510d3f5..777fc23` code 0; hashes déclarés recalculés (ci-dessous); cohérence inter-documents vérifiée.
- Chaîne S3 : `git rev-list --first-parent --max-count=1 3876fce -- docs/fusion/NO_GO_CYCLE_REGISTRY.json` = `7039476`; `git rev-list --first-parent --max-count=1 "7039476^1" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json` = `6867a2d`; SHA-256 du blob à `6867a2d` = `a7ad22af7cc6b21bc7c6f5b3d8ec08a929efbb4e044451087c5963f3013322c1` = `previous_blob_sha256` déclaré dans le registre. **Concordance exacte** (code 0).
- Genesis oracle : `git log --diff-filter=A -- docs/fusion/ORACLE_ADMISSIONS.json` = `3876fce`; SHA-256 du blob à `3876fce` = `246f867f77cfbe61fd392297925d4f498946eff28bcf3d66f62a6e22ed3c8209` = hash déclaré. Le registre des décisions vide est octet-pour-octet identique (`diff` code 0) et partage donc le même hash — cohérent, non contradictoire.
- Table **Admissions d'oracles** vide → aucune preuve P6 admissible; `Oracle scope` = `—`.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Construire une transition de `ORACLE_ADMISSIONS.json` qui retire, modifie, remplace ou réintroduit une admission antérieure tout en passant les règles S1; tester aussi ajout O2 après O4, commit non-révision, saut de prédécesseur et merge divergent | **Échoue.** La chaîne est fondée sur Git (rev-list) et non sur un champ interne : `C` = dernier ancêtre de première parenté modifiant le fichier depuis `E`; `P` = dernier ancêtre de `C^1` modifiant le fichier. Entre `P` et `C`, l'ensemble antérieur des `oracle_id` est un sous-ensemble obligatoire et chaque objet antérieur demeure sémantiquement identique dans sa sérialisation canonique; retrait, modification, remplacement, seconde entrée d'un même oracle ou réintroduction → `ORACLE_ADMISSION_HISTORY_VIOLATION`. L'ajout O2 après O4 est explicitement valide : l'ordre fermé `O2,O4,O7` permet de déplacer un objet existant sans le modifier. Un commit non-révision valide le blob porté via son dernier `C` (aucun faux parent). Saut de `P` et merge divergent sont des mutants obligatoires qui échouent. Réserve **T2** |
| 2 | Chercher une circularité dans `run_id`, manifeste, chemin et hash du rapport d'entrée; faire accepter un rapport absent, non déterministe, mal ordonné, dupliqué ou contenant les octets rejetés; contredire la priorité fermée | **Échoue, avec réserve.** Le schéma du rapport est fermé (`{schema_version,run_id,rejections}`, rejets `{input_sha256,code}` triés sans doublon, octets rejetés absents), `run_id` est `^RUN-[0-9a-f]{16}$`, la reproduction est déterministe, et tout écart (chemin absent, hash divergent, champ inconnu, doublon, mauvais ordre, contenu brut) → `NON_TESTABLE`/`INPUT_VALIDATION_REPORT_INVALID` sans compteur métier. La priorité est fermée : registre/occurrence supprimé·e, muté·e ou rendu·e non canonique → `REGISTRY_HISTORY_VIOLATION` (jamais deux codes); sinon identité/hash/ascendance divergente d'une occurrence soumise → `INVALID_OCCURRENCE_HISTORY`; sinon nouvel input brut non canonique → `NON_CANONICAL_CAUSAL_JSON` en pré-validation seulement. Mutants de priorité inversée, comptage d'un input rejeté, omission du rapport vide, recopie des octets et hash divergent fermés. Réserve **T1** (manifeste non ancré) |
| 3 | Recalculer indépendamment `E=3876fce` → `C=7039476` → `P=6867a2d` et le hash `a7ad22af…322c1`; chercher un cas first-parent où la nouvelle définition de `C` accepte un saut, une révision hors branche ou un merge illégitime | **Échoue, avec réserve.** Le recalcul indépendant est exact (voir vérifications) et le faux positif de `REV11bis` est éliminé : `E=3876fce` ne modifiant pas le registre, `C` résout `7039476`, `P` résout `6867a2d`, le blob porté sans modification par `3876fce` ne produit plus de violation. Saut et révision hors première parenté fermés par rev-list épinglé. Réserve **T2** : merge transparent divergent invisible (démontré mécaniquement) |
| 4 | Faire accepter une supersession avec décision seulement narrative, simultanée, absente, mutée, réutilisée, portant une autre occurrence ou une autre raison; chercher une ambiguïté si plusieurs records ou commits correspondent | **Échoue, avec réserve.** La décision doit vivre dans `OPERATOR_SUPERSESSION_DECISIONS.json` (`{decision_id,action,superseded_occurrence_id,reason_code}`, `^DEC-[0-9]{6}$` contigu, `action=APPROVE_SUPERSESSION`, append-only). Au `decision_commit`, le diff avec le premier parent doit ajouter exactement le record invoqué sans modifier ni retirer un record antérieur; le record doit nommer la même occurrence et la même raison. Message Git seul, Markdown, action différente, raison/occurrence divergente, commit sans ajout, décision simultanée (ancêtre strict requis) ou mutation ultérieure → `REGISTRY_HISTORY_VIOLATION`. Le lien via `decision_commit` lève l'ambiguïté multi-commits. Réserve **T3** (réutilisation d'un record entre supersessions) |
| 5 | Valider les JSON, les hashes déclarés, les références Git et la cohérence entre `REV12.md`, `06_FUSION_GATES.md`, `CAUSAL_ID_REGISTRY.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md` et `PROGRESSION.md` | **Satisfaite — vérifié.** Trois JSON valides; hashs déclarés concordants (genesis oracle `246f867f`, blob `6867a2d` = `a7ad22af…322c1`, registre de décisions vide `246f867f`); `git diff --check` propre; ancêtres vérifiés. `REV12.md` ↔ registres : les définitions de `C`/`P` (NO-GO et oracle), la priorité des erreurs, le schéma du rapport d'entrée, le registre des décisions et les mutants listés sont mutuellement cohérents. `PROGRESSION.md` reflète la réponse S1–S4 en cours |

## Constats

### T1 — Manifeste du run : schéma, emplacement et ancrage non définis; circularité temporelle

`CAUSAL_ID_REGISTRY.md:81` : `run_id` est « préenregistré dans le manifeste avant exécution »; `CAUSAL_ID_REGISTRY.md:83` : « Le manifeste du run contient le chemin et le SHA-256 de ce rapport ». Le rapport étant produit **pendant** l'exécution, le manifeste qui contient son SHA-256 ne peut pas être écrit **avant** l'exécution sans être une contrainte (commitment) ou une annexe post-hoc. Or aucun schéma, emplacement, ancrage Git, ni lien au « manifeste P6 » (`06_FUSION_GATES.md:31`) n'est défini pour ce manifeste de run. **Effet : la « pré-inscription » du `run_id` et l'auditabilité du rapport dépendent d'un artefact non normé; un run pourrait écrire un manifeste auto-cohérent après coup sans que le contrôleur puisse le distinguer.** Action : normer le manifeste de run (chemin, schéma, horodatage, commit d'ancrage, lien au manifeste P6) et préciser si le SHA-256 y est un engagement vérifié ou une annexe.

### T2 — Merge transparent divergent : la règle merge ne s'applique qu'à `C`

La règle (`NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`) compare les blobs de tous les parents **si `C` est un merge**. Or `rev-list --first-parent --max-count=1 E -- fichier` ne renvoie le merge que si le fichier diffère de son premier parent. Démonstration mécanique dans un dépôt d'essai (code de sortie 0, commandes reproductibles dans la version finale) : après un merge `-s ours` dont le second parent porte un blob divergent `Y`, `git rev-list --first-parent --max-count=1 HEAD -- reg.txt` renvoie la révision pré-merge `C` (blob `X`), jamais le merge; les modifications du registre apportées par la branche sont **silencieusement abandonnées sans `MERGE_REGISTRY_CONFLICT` ni `ORACLE_ADMISSION_MERGE_CONFLICT`**. **Effet : un merge « transparent » à second parent divergent est accepté alors qu'il « efface silencieusement une branche », ce que la première-parenté prétend interdire.** Action : vérifier les parents de **tous** les merges entre `C` et `E` (pas seulement de `C`), ou comparer les blobs des parents de chaque merge rencontré par le walk.

### T3 — Consommation unique d'une décision : invariant énoncé sans mécanisme

« Il ne peut être consommé que par une supersession » (`CAUSAL_ID_REGISTRY.md`) pose une unicité de consommation, et « réutilisation … produit `REGISTRY_HISTORY_VIOLATION` ». Mais aucun mécanisme ne lie un record `DEC-*` à une seule supersession : deux supersessions pourraient référencer le **même** `decision_commit` (le diff ajoute le record une seule fois), et l'invariant ne serait pas vérifié sans une recherche croisée des supersessions par `decision_commit`. Le record ne porte aucun champ de consommation (`consumed_by`/`supersession_id`). **Effet : la détection de la réutilisation est laissée à l'implémentation, sans invariant spécifié.** Action : exiger l'unicité de `decision_commit` sur l'ensemble des supersessions (index unique) ou ajouter un champ de consommation vérifié.

## Verdict

**ACCEPT_WITH_LIMITS**

Les cinq réfutations échouent dans leur périmètre : la chaîne append-only d'`ORACLE_ADMISSIONS.json` est fondée sur Git avec sous-ensembles obligatoires, identité sémantique et mutants fermés (S1); le rapport d'entrée est à schéma fermé avec reproduction déterministe et priorité des erreurs fermée (S2); `C` est désormais la dernière révision effective et le faux positif `REV11bis` est éliminé, recalcul indépendant exact (S3); la décision de supersession est versionnée dans un registre machine à schéma fermé, ancrée par `decision_commit` (S4); les JSON, hashes, références Git et la cohérence inter-documents sont vérifiés (S5).

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs :

- **T1** — normer le manifeste de run (schéma, emplacement, ancrage, lien au manifeste P6) et lever la circularité « préenregistré avant exécution » vs « contient le SHA-256 du rapport »;
- **T2** — étendre la vérification de merge divergent à tous les merges entre `C` et `E` (merge transparent `-s ours` démontré);
- **T3** — mécaniser l'unicité de consommation d'une décision de supersession.

Effet sur les gates : **aucun**. Le registre machine est vide (aucun cycle exécuté), la table d'admissions d'oracles est vide (aucun oracle admissible), la preuve d'immuabilité externe reste absente → P6 reste `BLOCKED_IMMUTABILITY`; P0 garde ses blocages connus. Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
