# H0003 — Décision humaine sur le paquet rejeté

## Décision

L'opérateur admet le 2026-08-29 les deux verdicts `REJECT` portant sur le paquet
Producteur gelé `44893b0`. Le paquet est rejeté; l'hypothèse de faisabilité H0003 n'est
pas abandonnée et passe en cycle correctif dans le même scope.

| Champ | Valeur |
|---|---|
| paquet Producteur examiné | `44893b0061f13e8a03c4a27f4d299b8b65b5943c` |
| commit portant les deux rapports | `04a5a1f5ac7b957f174beccf7ab95a1b1631417c` |
| Critique | `REJECT` |
| SHA-256 Critique admis | `ec087231d8514e0cc390ffbc912d3a6dc984c17c96c8812f8c9c43d809cd5487` |
| Contradictoire | `REJECT` |
| SHA-256 Contradictoire admis | `9649d0c9e0d11e97f7f19a10a99553e2fbbb9721185cae9bc19ce19d95112f20` |
| décision sur le paquet | `REJECTED` |
| état opérationnel H0003 | `TESTING / CORRECTION_REQUIRED` |
| effet sur P1 | `NOT_PASSED` |

## Findings bloquants admis

- **R1 — scalaires temporels** : `InstantNs` et `DurationNs` doivent valider à
  l'exécution `type(value) == int`; `bool`, `float`, `str` et `datetime` doivent être
  rejetés avec un code stable.
- **R2 — frontière rationnelle** : le noyau canonique ne doit jamais convertir
  implicitement un `bool` ou un nombre binary64 en `Fraction`. Les valeurs telles que
  `True`, `False`, `0.1` et `100.005` doivent être rejetées.
- **R3 — compatibilité MarketEvent** : une validation explicite avec
  `InstrumentSpec` doit vérifier l'identité d'instrument et rejeter tout prix hors
  `tick_size` sous `REJECT_OFF_GRID`.

Les contre-exemples exacts publiés par les reviewers deviennent des régressions
permanentes. Le Producteur n'est pas autorisé à les remplacer par des variantes plus
faciles.

## Portée du cycle correctif

Le cycle reste sur `hypothesis/H0003-canonical-contract-foundation`. Il ne modifie ni
l'hypothèse ni les décisions B1–B8/B5a, ne crée pas H0004 et n'ajoute aucune capacité de
ledger, replay, provider ou stratégie.

L'ancien `RESULT.json`, de SHA-256
`f13814dee86a98d75c28b6dc697f29d8b1185208501bd46996f47376abe7c87d`, reste associé au
paquet rejeté et ne doit pas être réécrit comme s'il décrivait le paquet corrigé.

La note `unicodedata` reste `NON_BLOCKING_FOR_H0003` et bloquante avant l'enforcement
temporel / `P1 PASS`. Elle est explicitement hors du présent cycle correctif.

Après R1–R3, un nouveau paquet complet et gelé devra être produit. Les nouvelles revues
recevront les anciens `REJECT` comme contexte; le nouveau Contradictoire restera aveugle
au nouveau verdict Critique jusqu'à fixation de son premier verdict.
