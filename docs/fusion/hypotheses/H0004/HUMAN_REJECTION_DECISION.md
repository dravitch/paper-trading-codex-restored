# H0004 — Décision humaine sur le paquet rejeté

## Décision

L'opérateur admet le 2026-08-30 les deux verdicts `REJECT` portant sur le paquet Producteur
gelé `5967ee0`.

```text
packet 5967ee0 = REJECTED
H0004 = CORRECTION_REQUIRED
P1 = NOT_PASSED
```

| Champ | Valeur |
|---|---|
| paquet examiné | `5967ee06f85bb4b52e0e3bb6fafb19b2856d63db` |
| commit portant les rapports | `6f128758a9c07a5f1bc7ef4fac6c264d794ee9b6` |
| Critique | `REJECT` |
| SHA-256 Critique | `795c0adaacdd3a60dbd473945b4c4d9f58d940b76245dd0d87541263e2c06707` |
| Contradictoire | `REJECT` |
| SHA-256 Contradictoire | `6cd51d2dc44063a9f13392d44ab6e04e4b8ddacc860bd30e84fc929172ed0b32` |
| séparation | `PROCEDURAL / ROLE-SEPARATED` |
| décision paquet | `REJECTED` |
| état H0004 | `TESTING / CORRECTION_REQUIRED` |
| effet P1 | `NOT_PASSED` |

## Findings bloquants admis

```text
F1 = STATE_SPEC_BINDING_MISSING
F2 = SPOT_CONTRACT_MULTIPLIER_SEMANTICS_DIVERGED
```

- F1 : des specs cohérentes entre elles mais étrangères à l'état peuvent autoriser une
  transition tout en laissant les hashes d'état inchangés et mensongers.
- F2 : le Producteur applique `q × p × contract_multiplier` alors que la formule H0004
  préenregistrée est `q × p`; le seul scénario à multiplicateur un masque l'écart.

F1 est une violation de la liaison déjà observable dans l'état. F2 exige une décision
normative humaine avant correction.

## Portée du cycle correctif

Le cycle reste H0004 sur la même branche. Il ne crée pas H0005, ne modifie pas les
équations nominales, ne réécrit ni le premier run ni le paquet rejeté et ne revendique pas
`P1 PASS`.

Les contre-exemples exacts F1/F2 deviennent des régressions permanentes. Le résultat,
manifeste, preuves et rapports de `5967ee0` restent des preuves historiques rejetées.
