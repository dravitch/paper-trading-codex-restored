# Registre des branches d'hypothèse

## Statuts

`DRAFT`, `TESTING`, `IN_REVIEW`, `REFUTED`, `NON_TESTABLE`, `VALIDATED`, `MERGED`.

## Registre

| ID | Branche | Énoncé court | Gate | Critique | Contradictoire | Statut | Commit de fusion |
|---|---|---|---|---|---|---|---|
| H0001 | `hypothesis/H0001-canonical-ledger-equivalence` | équivalence comptable canonique du scénario P0 | P1 | `ACCEPT_WITH_LIMITS` | `ACCEPT_WITH_LIMITS` | `VALIDATED` | — |
| H0002 | `hypothesis/H0002-short-ledger-generalization` | conservation comptable du short sur une famille préenregistrée | P1 | `ACCEPT_WITH_LIMITS` | `ACCEPT_WITH_LIMITS` | `VALIDATED` | — |
| H0003 | `hypothesis/H0003-canonical-contract-foundation` | suffisance exécutable du socle canonique P1 | P1 | — | — | `DRAFT` | — |

## Règle

Une ligne est créée en même temps que la branche. `VALIDATED` exige les deux rapports indépendants définis par le [Protocole Contradictoire](PROTOCOL_CONTRADICTOIRE.md). `MERGED` exige en plus l'identifiant du commit de fusion.

Pour H0001, `VALIDATED` signifie `VALIDATED_WITH_PUBLISHED_LIMITS` dans le seul domaine
préenregistré. Les rapports sont ancrés au commit `e4ff866`; leur admission et leurs hashes
sont consignés dans [`HUMAN_ADMISSION.md`](hypotheses/H0001/HUMAN_ADMISSION.md). Elle ne
vaut pas `P1 PASS`.

Pour H0002, `VALIDATED` signifie également `VALIDATED_WITH_PUBLISHED_LIMITS` dans la
famille préenregistrée seulement. Les rapports sont ancrés au commit `5658a8b`; leur
admission et leurs hashes sont consignés dans
[`HUMAN_ADMISSION.md`](hypotheses/H0002/HUMAN_ADMISSION.md). Elle ne vaut pas `P1 PASS`.

H0003 reste `DRAFT` dans le vocabulaire du registre. Son premier préenregistrement
`ed2731d` a conclu `BLOCKED_SPEC_AMBIGUITY`; la décision humaine `0fe5610` ferme B1–B8 et
H0003-v2 est `READY_FOR_IMPLEMENTATION`, toujours avant code et avant run.
