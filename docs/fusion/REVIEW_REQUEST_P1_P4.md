# Demande de vérification Contradictoire — réponse P1–P4

## Cible

- commit Producteur : `70394762fc1f8fae7246d389ba3d1974ef98060b`;
- source admise : `CONTRADICTOIRE_DELTA_REV09BIS.md` + addendum, commit `4f281b7`;
- correction : `REV10.md`.

## Réfutations demandées

1. Faire accepter une ligne `Oracle-Admission` avec octet, ordre, clé, verdict, commit, hash ou chemin divergent; recalculer le vecteur `7dcf17…`.
2. Produire un encodage alternatif conforme du vecteur `5ab872…`, ou faire accepter NFD, surrogate ou clé dupliquée sans `NON_CANONICAL_CAUSAL_JSON`.
3. Faire pointer le registre vers un ancêtre autre que sa dernière révision first-parent sans `REGISTRY_HISTORY_VIOLATION`; vérifier le parent `6867a2d`/blob `a7ad22…`.
4. Superséder par suppression, réutilisation, branche, cycle ou référence absente sans rejet; vérifier que `supersessions` a un schéma déterministe.
5. Vérifier JSON, les dix hashes d'admission, quatre vecteurs/hashes historiques et cohérence inter-documents.

La revue est documentaire et doit provenir de l'IA Contradictoire indépendante. Le Producteur ne déclenche aucune auto-revue. P6 reste bloqué.
