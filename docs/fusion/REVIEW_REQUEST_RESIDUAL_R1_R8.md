# Demande de vérification Contradictoire — réponse R1–R8

## Révision figée

- branche : `correction/reconcile-l1-l12`;
- commit : `8335ab0`;
- parent : `273046a`;
- portée : réponse Producteur aux limites R1–R8 seulement.

## Questions de réfutation

1. O7 conserve-t-il tous les objectifs et contraintes mandatés sans confondre métrique descriptive et axe de dominance?
2. Deux exécutions de même référentiel/scénario/paramètres mais de résultats différents deviennent-elles bien un conflit plutôt qu'un doublon?
3. La dérivation de `reference_hash` est-elle suffisante dans le domaine documentaire actuel?
4. Les cinq statuts O4 découlent-ils tous de la règle fixée sans adaptation a posteriori?
5. O9 peut-il conserver la preuve d'un non-fini sans sérialiser NaN/infini?
6. Le périmètre de mutation temporelle P1 laisse-t-il une voie de contournement dans les nouveaux modules canoniques?
7. La définition d'un cycle et le registre NO-GO empêchent-ils réellement une remise à zéro cosmétique de la cause?

## Mutations minimales

- retirer un objectif mandaté de `objective_vector`;
- dédupliquer deux runs aux résultats divergents;
- changer un champ du `ReferenceSpec` sans modifier `reference_hash`;
- qualifier le point 3 O4 de robuste;
- sérialiser directement `float("inf")`;
- appeler une horloge murale depuis `domain/` par un alias;
- renommer une cause NO-GO entre deux cycles sans changer sa description causale.

## Sortie attendue

Un verdict ciblé `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`, avec révision, commandes, contre-exemples et effet sur P1/P6. Cette vérification ne réévalue pas les performances financières et ne valide aucun gate.
