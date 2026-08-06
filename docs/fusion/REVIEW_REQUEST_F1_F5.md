# Demande de vérification Contradictoire — réponse F1–F5

## Révision figée

- branche : `correction/reconcile-l1-l12`;
- commit Producteur : `4225bc5`;
- parent probatoire : `a1e9892`;
- objet : fermeture documentaire de F1–F5.

## Vérifications requises

1. Recalculer O4 et confirmer les statuts `ROBUST`, `ROBUST`, `FRAGILE`, `FAIL_CONSTRAINT`, `FAIL_CONSTRAINT`.
2. Vérifier que O4 et O7 sont tous deux `SUPERSEDED_PENDING_REVIEW`.
3. Construire deux `RiskPoint` de même référentiel/scénario/paramètres et objectifs, mais de métriques descriptives différentes : attendu `REPRODUCIBILITY_CONFLICT`.
4. Tenter les cinq mutations temporelles nommées dans P1 et chercher un alias non couvert par la règle AST.
5. Vérifier que deux cycles aux preuves ou descriptions différentes conservent la même `cause_key` si gate, critère, invariant et mutation sont identiques.
6. Chercher un cas où deux causes réellement différentes auraient pourtant la même clé causale.

## Verdict attendu

`ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`, avec révision exacte et contre-exemples. Cette revue ferme seulement la spécification; les contrôles exécutables P1/P6 restent à implémenter et aucun gate ne peut devenir `PASS`.
