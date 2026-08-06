# Demande de revue Contradictoire — REV05

## Révision figée

- branche : `correction/reconcile-l1-l12`;
- commit Producteur : `09653e2`;
- base : `e413867` sur `fusion/controlled-merger`;
- objet : consolidation L1–L12 et objections Critique C1–C3.

## Mandat

Former un premier verdict sans recevoir une conclusion Critique sur ce delta. Chercher à réfuter notamment :

1. l'univocité de O2 et l'exclusion des liquidations;
2. la complétude et la stabilité de la clé canonique O7;
3. les attendus O8–O11, y compris égalités, non-finis et objectifs contradictoires;
4. l'opérationnalisation du voisinage O4;
5. la séparation hash exact/tolérance et sa portabilité;
6. la capacité réelle des mutations P1/P3/P7 à échouer;
7. la convention de frais et sa conservation comptable;
8. la falsifiabilité des conditions NO-GO;
9. le statut `BLOCKED_LICENSE` et l'absence de copie Bitget;
10. l'unicité du nom de modèle de compte;
11. la preuve Nix annoncée et ses limites;
12. la non-circularité des oracles définitionnels.

## Preuves Producteur déclarées

```text
nix develop --no-write-lock-file -c bash -lc \
  'pytest -q --cov=paper_trading_codex --cov-report=term-missing && ruff check .'
exit 0; Python 3.12.12; 68 passed; couverture 87.07%; Ruff 0.
```

La revue doit réexécuter ou classer cette preuve `NON_REPRODUCED`; elle ne doit pas simplement recopier le résultat Producteur.

## Mutations documentaires minimales

- rendre O2 optionnel à nouveau;
- inclure `point_id` dans O7 ou retirer le tri;
- accepter NaN dans le Pareto;
- changer le rayon O4 après observation;
- considérer deux hashes différents comme égaux sous tolérance;
- réintroduire `now()` dans P1;
- autoriser un appel provider depuis une stratégie;
- retirer une condition NO-GO;
- copier un fichier Bitget sans licence;
- réintroduire un alias de compte non déclaré;
- présenter la baseline Bitget comme reproduite;
- accepter O2/O4/O7 sans revue tierce.

## Verdicts admis

`ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT`, `NON_TESTABLE`. Toute limite doit identifier le fichier, l'énoncé réfuté, un contre-exemple et l'effet sur les gates.
