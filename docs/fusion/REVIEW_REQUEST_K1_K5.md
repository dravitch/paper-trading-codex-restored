# Demande de vérification Contradictoire — réponse K1–K5

## Révision figée

- branche : `correction/reconcile-l1-l12`;
- commit Producteur : `decbb42`;
- objet : fermeture documentaire de K1–K5.

## Réfutations requises

1. Réécrire rapport et preuve courante ensemble pour contourner l'ancre du commit d'admission.
2. Substituer chemin, commit, verdict ou rapport d'un autre oracle et faire passer P6.
3. Construire implicitement un `Clock` système ou déplacer `SystemClock` dans les modules canoniques sans échec P1.
4. Employer un ID `RESERVED`, `DEPRECATED` ou `RETIRED` dans une nouvelle occurrence sans produire `NON_TESTABLE` et cycle bloqué.
5. Accumuler trois cycles d'un groupe candidat ou des résultats `NON_TESTABLE` sans décision obligatoire.
6. Recalculer indépendamment les cinq hashes du registre depuis les blobs d'admission.

## Portée

Revue documentaire et Git du commit exact. Les contrôleurs restent à implémenter; aucun verdict de cette revue ne peut franchir P1 ou P6.
