# Demande de vérification Contradictoire — réponse N1–N4

## Cible

- commit Producteur : `930b0f9292c18d74b99a3daabc53f1af2b7fba68`;
- source admise : `CONTRADICTOIRE_DELTA_F14546F.md`, commit `cf6aa7a`;
- correction : `REV08.md`.

## Réfutations demandées

1. Faire accepter CRLF, plusieurs marqueurs ou un verdict absent de la table d'admissions d'oracles.
2. Produire deux hashes pour le vecteur causal normatif en respectant toutes les règles, ou modifier une valeur imbriquée sans changer le hash attendu.
3. Retirer ou modifier une entrée historique du registre JSON sans `REGISTRY_HISTORY_VIOLATION`; chercher une ambiguïté au passage genesis→première écriture.
4. Injecter `OCC-000000`, un trou, doublon, ID hors domaine ou ID fourni par l'appelant sans rejet.
5. Recalculer le vecteur SHA-256, valider le JSON et les huit hashes d'admission.

La revue est documentaire. P6 reste bloqué et aucune hypothèse métier n'est validée.
