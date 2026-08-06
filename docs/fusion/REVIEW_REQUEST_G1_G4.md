# Demande de vérification Contradictoire — réponse G1–G4

## Révision figée

- branche : `correction/reconcile-l1-l12`;
- commit Producteur : `894b585`;
- objet : fermeture documentaire de G1–G4.

## Réfutations requises

1. Contourner le contrôle temporel par import aliasé, import dynamique, `fromtimestamp`, `time_ns`, métadonnée fichier, alias indirect, réflexion ou dépendance tierce.
2. Montrer deux défauts indépendants qui produisent la même `cause_key` malgré des signatures normalisées différentes.
3. Montrer qu'un changement de ligne, message, traceback ou preuve change indûment la clé d'une même cause.
4. Vérifier les transitions fermées des statuts d'oracle et chercher un chemin permettant P6 `PASS` avec un statut pending.
5. Vérifier dans Git l'admission effective des artefacts `8335ab0` et l'absence de l'ancienne affirmation périmée dans le registre actif.

## Limite de portée

La revue évalue la spécification, pas une implémentation AST encore absente. Un verdict favorable ne franchit ni P1 ni P6. Toute nouvelle limite doit fournir un contre-exemple minimal et indiquer si elle bloque la fusion documentaire ou seulement l'implémentation future.
