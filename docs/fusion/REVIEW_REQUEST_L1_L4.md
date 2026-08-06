# Demande de vérification Contradictoire — réponse L1–L4

## Cible figée

- commit Producteur : `dd4cdde133af1bdc266c21ca943a6401b13dec30`
- source : `CONTRADICTOIRE_DELTA_DECBB42.md`, admise au commit `02775ce`;
- objet : réponse Producteur L1–L4 documentée dans `REV06.md`.

## Réfutations demandées

1. Substituer à O2 un rapport admis visant O4 avec le même verdict : chercher une voie permettant à P6 de passer malgré le `Oracle scope` et le marqueur du blob.
2. Faire accepter comme historique une occurrence créée après la dépréciation, dupliquée sous un nouvel ID, modifiée causalement ou sans ascendance vérifiable.
3. Recréer, fusionner ou scinder un groupe couvrant des causes existantes et obtenir un compteur inférieur à l'union dédupliquée de leurs `cycle_id`.
4. Faire revendiquer P6 sans preuve de protection distante exportée/hashée ni archive Git signée vérifiable.
5. Vérifier que les six SHA-256 du registre concordent avec les blobs des commits d'admission et que les anciennes revues marquées `Oracle scope = —` ne peuvent servir à accepter O2, O4 ou O7.
6. Chercher une contradiction entre `REV06.md`, les quatre registres modifiés et les critères P6.

## Oracles indépendants minimaux

- appartenance croisée : `O2 ∉ {O4}`;
- occurrence B au contenu de A mais nouvel `occurrence_id` après dépréciation : nouvelle occurrence;
- groupes `{A,B}` et `{B,C}` : union `{A,B,C}`, cardinalité `3`;
- preuve d'immuabilité absente : statut exact `BLOCKED_IMMUTABILITY`.

## Limite de portée

La revue porte sur une spécification. Aucun contrôleur P6 n'est encore implémenté, la protection distante n'est pas prouvée et L4 reste `OPEN_PROOF_EXTERNAL`. Un verdict favorable ne peut franchir aucun gate ni accepter une hypothèse métier.

## Sortie attendue

Verdict `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`, commit exact, commandes et codes de sortie, contre-exemples minimaux, effet sur P0/P6 et heartbeat distinct.
