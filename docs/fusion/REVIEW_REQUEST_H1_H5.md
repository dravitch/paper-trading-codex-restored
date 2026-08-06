# Demande de vérification Contradictoire — réponse H1–H5

## Révision figée

- branche : `correction/reconcile-l1-l12`;
- commit Producteur : `ca8de4f`;
- objet : fermeture documentaire de H1–H5.

## Réfutations requises

1. Trouver une capacité temporelle accessible depuis l'allowlist P1 v1 ou son graphe transitif.
2. Construire un chemin permettant P6 `PASS` avec O2, O4 ou O7 pending, rejeté ou non testable.
3. Trouver un verdict ou une modification d'oracle sans transition définie.
4. Maintenir trois cycles familiaux `UNATTRIBUTED` sans déclencher attribution, scission ou `STOP`.
5. Montrer qu'une même cause multi-surface peut éviter le seuil malgré `root_cause_group_id`, ou que deux causes distinctes sont forcées dans le même groupe.
6. Vérifier que les identifiants du registre sont stables, non dérivés de messages/lignes et liés à une autorité de création.

## Portée

La revue porte sur les contrats documentaires du commit exact. L'allowlist, l'analyse AST et les gardes P6 ne deviennent pas exécutables par cette revue; P1 et P6 restent interdits au statut `PASS`.
