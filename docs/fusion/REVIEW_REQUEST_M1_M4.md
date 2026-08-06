# Demande de vérification Contradictoire — réponse M1–M4

## Cible

- commit Producteur : `f14546ffd40cb1f1e65cd3f9ec52f208752b1d2f`;
- source admise : `CONTRADICTOIRE_DELTA_DD4CDDE.md`, commit `5a8ebe2`;
- correction : `REV07.md`.

## Réfutations demandées

1. Faire accepter une phrase, sous-chaîne, ligne dupliquée, espace ajouté ou verdict divergent comme marqueur `Oracle-Review` valide.
2. Modifier un champ causal sous un `occurrence_id` historique sans faire diverger le hash recalculé ou sans sanction.
3. Obtenir un compteur de groupe inférieur à l'union des cycles présents dans `NO_GO_CYCLE_REGISTRY.json`.
4. Introduire un `occurrence_id` ou un code de raison hors vocabulaire sans `NON_TESTABLE`.
5. Vérifier le JSON, les sept hashes d'admission et les contradictions entre `REV07.md`, registres et P6.

## Oracles minimaux

- correspondance du marqueur : ligne complète unique seulement;
- payload causal différent ⇒ SHA-256 différent;
- `|{A,B} ∪ {B,C}| = 3`;
- valeur hors ensemble fermé ⇒ rejet.

La revue reste documentaire. Aucun verdict ne franchit P6; la preuve d'immuabilité externe reste absente.
