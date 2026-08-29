# Demande de revue indépendante — réponse T1–T3

## Révision à examiner

Le Producteur renseignera ici le commit figé de `REV13.md` avant transmission. La revue
porte exclusivement sur ce commit et son delta par rapport à son premier parent.

```text
PRODUCTEUR_COMMIT=PENDING
branche=work/continuation-2026-08-28
```

## Artefacts obligatoires

- `REV13.md`;
- `docs/fusion/CAUSAL_ID_REGISTRY.md`;
- `docs/fusion/NO_GO_REGISTER.md`;
- `docs/fusion/REVIEW_ADMISSION_REGISTRY.md`;
- `docs/fusion/06_FUSION_GATES.md`;
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md`;
- `PROGRESSION.md`.

## Réfutations obligatoires

1. Construire une chronologie où le même artefact prétend encore être pré-run tout en
   contenant le hash d'un rapport futur; chercher aussi un `run_id` choisissable après
   observation ou une collision traitée opportunistement.
2. Reproduire un merge transparent `-s ours` avec un parent secondaire divergent et
   déterminer si le walk normé le détecte même lorsque l'historique limité au chemin ne
   retourne pas le merge.
3. Construire deux supersessions qui consomment le même `decision_commit`, avec mêmes puis
   différentes occurrence et raison; les deux variantes doivent être rejetées.
4. Vérifier la cohérence des chemins, schémas, domaines de hashes, ancres Git, codes
   d'erreur et mutants entre tous les artefacts obligatoires.
5. Vérifier que la réponse ne revendique ni implémentation, ni résultat de mutant, ni
   `PASS` de P1/P6.

## Sortie attendue

Produire un rapport Critique et un rapport Contradictoire dans deux contextes indépendants,
avec commit exact, modèle/session, commandes et codes de sortie, contre-exemples minimaux,
verdict unique (`ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`) et effet
explicite sur les gates. La Contradictoire fige son premier verdict sans lire celui de la
Critique. L'admission reste une décision humaine explicite.

