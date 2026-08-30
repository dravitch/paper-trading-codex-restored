# H0004 — Admission humaine du paquet corrigé

## Décision

L'opérateur admet le 2026-08-30 les deux nouvelles revues du paquet H0004 corrigé avec
leur verdict `ACCEPT_WITH_LIMITS`.

```text
first packet 5967ee0 = REJECTED
corrected packet 5f0253d = VALIDATED_WITH_PUBLISHED_LIMITS
H0004 = VALIDATED_WITH_PUBLISHED_LIMITS
P1 = NOT_PASSED
```

| Champ | Valeur |
|---|---|
| premier paquet rejeté | `5967ee06f85bb4b52e0e3bb6fafb19b2856d63db` |
| admission humaine du rejet | `830c0c02e60c8171d43e69a6c9d251365b39e49f` |
| décision normative multiplicateur | `f2d45c9a7ba79adcb1b94e51a6d295b48d8fe66e` |
| paquet corrigé examiné | `5f0253d9d9c552f310eabef5ae019219d828742c` |
| commit portant les nouvelles revues | `40ad46bd914556a5f7cf6399c59c0044861106b9` |
| Critique corrigée | `ACCEPT_WITH_LIMITS` |
| SHA-256 Critique corrigée | `38d0ed34557e106af1df65104461efa2a73ba2b0f2bcee78f5ff7c2b091a0fbd` |
| Contradictoire corrigée | `ACCEPT_WITH_LIMITS` |
| SHA-256 Contradictoire corrigée | `9ee13ee17c438263e9d679f11090117b98bb5ea4a8f81631549e7311386b68f0` |
| séparation des revues | `PROCEDURAL / ROLE-SEPARATED` |
| indépendance statistique / IV&V | non revendiquée |
| décision H0004 | `VALIDATED_WITH_PUBLISHED_LIMITS` |
| effet sur P1 | `NOT_PASSED` |

## Motif d'admission

Les deux rapports portent sur le même paquet gelé `5f0253d`. Ils reproduisent les
contre-exemples F1a, F1b et F2 ayant rejeté le premier paquet, puis confirment leur
fermeture avec les codes stables décidés :

```text
F1a → SPOT_STATE_INSTRUMENT_MISMATCH
F1b → SPOT_STATE_REFERENCE_MISMATCH
F2  → SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED
```

Ils vérifient que ces rejets précèdent toute mutation, que l'état reste inchangé, que la
formule normative demeure `quantity × price`, et que S8, M1–M19, l'oracle, les six
`AccountEvent`, les hashes et les suites ne régressent pas. Aucun nouveau `FAIL`,
`BLOCKED` ou `NON_TESTABLE` contaminant H0004 n'est publié.

Le Contradictoire a figé son premier verdict sans lire ni recevoir le nouveau verdict
Critique. Cette séparation est fonctionnelle et procédurale, sans revendication
d'indépendance statistique, organisationnelle ou de modèle.

## Limites admises et publiées

- M18c borne seulement la surface statique et l'API actuelle à fill individuel; il ne
  constitue pas une preuve générale contre tout tri dans un futur caller de collection.
- S8 gouverne les fills, pas un scheduler ni une déduplication stateful générale des
  événements d'initialisation.
- la preuve positive est limitée à `SPOT_CASH_V1`, mono-instrument, multiplicateur `1/1`,
  frais en devise quote et trajectoire BUY/SELL préenregistrée;
- multi-devise, frais en base, multiplicateur arbitraire, replay, provider et fidélité
  marché ne sont pas démontrés;
- modèle short canonique, enforcement temporel et preuve intégrée P1 restent non prouvés;
- les revues sont `PROCEDURAL / ROLE-SEPARATED`, pas une réplication externe ou IV&V.

## Histoire expérimentale conservée

```text
preregistration
→ BLOCKED S1–S7
→ human decisions S1–S7
→ BLOCKED S8
→ human decision S8
→ implementation and first run
→ 24 H0004 / 159 global tests green
→ REJECT / REJECT
→ human rejection admission
→ bounded F1/F2 correction
→ exact reviewer counterexamples as regressions
→ 28 H0004 / 163 global tests / 91.81 % coverage
→ second role-separated review
→ corrected admission
```

Les nombres de tests et la couverture ne constituent pas à eux seuls une preuve. Le
premier `REJECT` malgré 24/159 tests verts reste une preuve permanente de l'incomplétude
possible d'un espace de falsification préenregistré.

L'admission du paquet corrigé ne réécrit, ne neutralise ni ne réhabilite `5967ee0`. Son
résultat, manifeste, preuve et ses deux rapports rejetants restent historiquement intacts.

## Portée de la fermeture

H0004 est fermée et ne reçoit aucun nouveau correctif dans cette opération. Cette décision
ne crée aucune H0005, ne fusionne pas la branche et ne déclare pas `P1 PASS`. La prochaine
activité autorisée est une recalibration documentaire P1 sur une branche distincte créée
depuis le présent commit d'admission.
