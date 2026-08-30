# H0004 — Mandat de revue indépendante

## Paquet

Les deux revues examinent exactement le commit portant ce mandat. Le manifeste Producteur
est ancré à `b0064c0200384239372ada5c01b5efe3b8aeac7d`, SHA-256
`707deeb0f747396118bb48d1320fcce8ad31a368cd049bd54613c056f4eed2e1`.

## Questions de réfutation

1. Le premier run `a137491` précède-t-il réellement l'instrumentation M1–M19 et le ledger
   nominal a-t-il passé sans correction comptable?
2. L'oracle est-il physiquement et logiquement indépendant du ledger et reproduit-il les
   fractions préenregistrées?
3. Les six `AccountEvent` expliquent-ils exactement chaque variation, sans double compter
   `fees_by_currency`?
4. Les validations relationnelles H0003 sont-elles effectivement appelées?
5. S8 rejette-t-elle égalité et ordre décroissant avant les contrôles économiques, sans tri
   ni mémoire cachée?
6. M1–M19, dont M18a–M18e, sont-ils discriminants et produisent-ils leurs invariants/codes?
7. Les conclusions restent-elles bornées à `SPOT_CASH_V1` et maintiennent-elles
   `P1 = NOT_PASSED`?

Chaque reviewer doit recalculer hashes, fractions, filiation Git, résultat, tests ciblés et
suite globale, puis chercher des contre-exemples nouveaux.

## Séparation

Le Critique écrit uniquement `CRITIQUE.md`. Le Contradictoire écrit uniquement
`CONTRADICTOIRE.md` et fige son premier verdict sans lire ni recevoir le verdict Critique.
Les deux partent du même paquet, dans deux contextes distincts. L'indépendance doit être
qualifiée `PROCEDURAL / ROLE-SEPARATED`, sans revendication IV&V ou statistique.

Verdicts autorisés : `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT`, `BLOCKED`, `NON_TESTABLE`.
Aucun reviewer ne peut admettre H0004 ou déclarer `P1 PASS`.
