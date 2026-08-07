# Demande de vérification Contradictoire — réponse Q1–Q4

## Cible

- commit Producteur : `3876fce12eb23daa78293a803a7a658afb5b10bc`;
- source admise : `CONTRADICTOIRE_DELTA_REV10.md`, commit `ae5eb92`;
- correction : `REV11.md`.

## Réfutations demandées

1. Faire lire une admission depuis le Markdown/fence ou accepter doublon, mauvais ordre, oracle/champ inconnu dans `ORACLE_ADMISSIONS.json`.
2. Faire compter une fixture `NON_CANONICAL_CAUSAL_JSON` comme cycle, ou faire ignorer la corruption canonique d'une occurrence déjà enregistrée.
3. Faire accepter résultat first-parent vide hors genesis, merge divergent, merge modifiant le registre ou saut d'une révision.
4. Injecter SUP-000000, trou, doublon, ID appelant, raison inconnue ou `decision_commit` absent/non-ancêtre/simultané sans rejet.
5. Valider les deux JSON, les onze hashes d'admission et la cohérence de REV11 avec les gates/registres.

Revue documentaire indépendante uniquement. Aucun auto-déclenchement Producteur. Aucun gate ne peut être franchi.
