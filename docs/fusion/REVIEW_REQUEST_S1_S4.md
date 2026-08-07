# Demande de vérification Contradictoire — réponse S1–S4

## Cible

- commit Producteur : `777fc23c4d0683853fe7ae7bf160059f9a2fea5a`;
- source admise : `CONTRADICTOIRE_DELTA_REV11BIS.md`, commit d'admission `102ce6a`, index `d8bc959`;
- correction : `REV12.md`;
- branche : `correction/reconcile-l1-l12`;
- destination éventuelle : `fusion/controlled-merger`.

## Réfutations demandées

1. Construire une transition de `ORACLE_ADMISSIONS.json` qui retire, modifie, remplace ou réintroduit une admission antérieure tout en passant les règles S1; tester aussi ajout O2 après O4, commit non-révision, saut de prédécesseur et merge divergent.
2. Chercher une circularité dans `run_id`, manifeste, chemin et hash du rapport d'entrée; faire accepter un rapport absent, non déterministe, mal ordonné, dupliqué ou contenant les octets rejetés; contredire la priorité fermée entre `REGISTRY_HISTORY_VIOLATION`, `INVALID_OCCURRENCE_HISTORY` et `NON_CANONICAL_CAUSAL_JSON`.
3. Recalculer indépendamment `E=3876fce` → `C=7039476` → `P=6867a2d` et le hash `a7ad22af…322c1`; chercher un cas first-parent où la nouvelle définition de `C` accepte un saut, une révision hors branche ou un merge illégitime.
4. Faire accepter une supersession avec décision seulement narrative, simultanée, absente, mutée, réutilisée, portant une autre occurrence ou une autre raison; chercher une ambiguïté si plusieurs records ou commits correspondent.
5. Valider les JSON, les hashes déclarés, les références Git et la cohérence entre `REV12.md`, `06_FUSION_GATES.md`, `CAUSAL_ID_REGISTRY.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md` et `PROGRESSION.md`.

## Sortie attendue

Rapport `docs/fusion/CONTRADICTOIRE_DELTA_REV12.md` et heartbeat distinct publié en dernier, avec commit exact, modèle/session, commandes et codes de sortie, contre-exemples minimaux, verdict unique (`ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`) et effet explicite sur P0/P6.

La publication doit être atomique : écrire sous noms temporaires, renommer le rapport final puis le heartbeat final, signaler seulement après gel et fin de l'analyse. La revue est indépendante; le Producteur ne la déclenche pas, ne la simule pas et ne la committe pas avant admission humaine explicite. Aucun verdict documentaire ne franchit un gate; P6 reste `BLOCKED_IMMUTABILITY`.
