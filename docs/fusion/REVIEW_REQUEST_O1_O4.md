# Demande de vérification Contradictoire — réponse O1–O4

## Cible

- commit Producteur : `6867a2db063321cd39636f87a741452396d93ca7`;
- source admise : `CONTRADICTOIRE_DELTA_REV08.md`, commit `a7c8a69`;
- correction : `REV09.md`.

## Réfutations demandées

1. Faire accepter une candidate citée/préfixée, deux candidates, ou modifier rétroactivement le verdict indexé sans blocage P6.
2. Produire un encodage canonique alternatif conforme pour NFC, slash, contrôles ou Unicode; recalculer les deux vecteurs.
3. Contester la chaîne genesis `930b0f9` → blob courant, retirer une entrée, ou réinitialiser via migration de schéma.
4. Superséder une occurrence en réutilisant son ID, en supprimant l'ancienne ou en créant un trou sans rejet.
5. Vérifier le JSON, les neuf hashes d'admission, les hashes genesis/vecteurs et les contradictions inter-documents.

La revue est documentaire. P6 reste `BLOCKED_IMMUTABILITY` et aucun oracle n'est admis.
