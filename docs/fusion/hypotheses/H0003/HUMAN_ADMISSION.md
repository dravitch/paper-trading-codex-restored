# H0003 — Admission humaine du paquet corrigé

## Décision

L'opérateur admet le 2026-08-30 les deux nouvelles revues du paquet H0003 corrigé avec
leur verdict `ACCEPT_WITH_LIMITS`.

```text
first packet 44893b0 = REJECTED
corrected packet d3134e6 = VALIDATED_WITH_PUBLISHED_LIMITS
H0003 = VALIDATED_WITH_PUBLISHED_LIMITS
P1 = NOT_PASSED
```

| Champ | Valeur |
|---|---|
| premier paquet rejeté | `44893b0061f13e8a03c4a27f4d299b8b65b5943c` |
| admission humaine du rejet | `426781e` |
| paquet corrigé examiné | `d3134e63362693b4ca47d61229d1307edf7daca5` |
| commit portant les nouvelles revues | `ec7ae4bb923d3be277237d6f26e4289be1ac9460` |
| Critique corrigée | `ACCEPT_WITH_LIMITS` |
| SHA-256 Critique corrigée | `3948a178381bf0bac9a1d9e579c9b04b5501cb2f6c37616afd0ae70fc7b6cc9f` |
| Contradictoire corrigée | `ACCEPT_WITH_LIMITS` |
| SHA-256 Contradictoire corrigée | `f14a4b64e73459ccbf390075d93d9d00a86ffdfd9f48805ffa0b0c6a9926dfe5` |
| séparation des revues | `PROCEDURAL / ROLE-SEPARATED` |
| indépendance statistique / IV&V | non revendiquée |
| décision H0003 | `VALIDATED_WITH_PUBLISHED_LIMITS` |
| effet sur P1 | `NOT_PASSED` |

## Motif d'admission

Les deux rapports portent sur le même paquet gelé `d3134e6`. Ils reproduisent les
contre-exemples C4/F1/F2 ayant rejeté le premier paquet et confirment leur fermeture avec
les entrées et codes de rejet attendus. Ils vérifient également R1–R3, M1–M11, les
vecteurs, round-trips, hashes, résultats et tests globaux sans trouver de nouveau `FAIL`,
`BLOCKED` ou `NON_TESTABLE` contaminant H0003.

Le Contradictoire a figé son premier verdict sans lire ni recevoir le nouveau verdict
Critique. Cette séparation est fonctionnelle et procédurale, sans revendication
d'indépendance statistique, organisationnelle ou de famille de modèles.

## Limites admises et publiées

- H0003 valide le socle canonique préenregistré, pas les ledgers spot/short conformes ni
  une preuve intégrée de P1.
- Les validateurs relationnels de compatibilité sont des opérations explicites que leurs
  consommateurs devront appeler; H0003 ne prouve pas encore leur intégration aux ledgers.
- Le port `Clock` est structurel; son injection et l'enforcement AST restent à démontrer.
- `unicodedata` reste `NON_BLOCKING_FOR_H0003`, mais son absence de l'allowlist est
  `BLOCKING_UNTIL_ALLOWLIST_DECISION` avant l'enforcement temporel / `P1 PASS`.
- Les revues sont `PROCEDURAL / ROLE-SEPARATED`, pas une réplication externe ou IV&V.

## Histoire expérimentale conservée

```text
preregistration
→ BLOCKED_SPEC_AMBIGUITY
→ human normative decisions
→ implementation
→ REJECT
→ human rejection admission
→ bounded correction
→ regression of exact counterexamples
→ second independent review
→ corrected admission
```

L'admission du paquet corrigé ne réécrit, ne neutralise ni ne réhabilite le paquet
`44893b0`. Son résultat rejeté et les deux premiers rapports restent des preuves
historiques permanentes.

## Portée de la fermeture

H0003 est fermée et ne reçoit aucun nouveau correctif dans cette opération. Cette décision
ne crée aucune H0004, ne fusionne pas la branche et ne déclare pas `P1 PASS`. La prochaine
activité autorisée est une recalibration documentaire P1 sur une branche distincte créée
depuis le présent commit d'admission.
