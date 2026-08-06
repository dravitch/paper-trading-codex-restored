# REV07 — Réponse Producteur M1–M4

## Portée

Réponse au rapport Contradictoire `CONTRADICTOIRE_DELTA_DD4CDDE.md`, admis au commit `5a8ebe2`. Aucun contrôleur n'est implémenté et aucun gate n'est franchi.

## Corrections

| Constat | Avant | Après | Oracle de non-régression |
|---|---|---|---|
| M1 | recherche possible par sous-chaîne | ligne ASCII unique, expression complète et verdict fermé | une phrase négative contenant « Oracle scope » ne correspond pas; deux lignes échouent |
| M2 | identité historique sans égalité du contenu | SHA-256 du payload causal canonique comparé au premier commit | même ID + champ causal modifié ⇒ hash divergent ⇒ `INVALID_OCCURRENCE_HISTORY` |
| M3 | union sans source machine | `NO_GO_CYCLE_REGISTRY.json` autoritaire et versionné | `{A,B} ∪ {B,C}` recomposé depuis le JSON donne exactement `3` |
| M4 | occurrence et raisons hors vocabulaire | `OCC-NNNNNN`, autorité monotone et trois codes fermés | ID/code hors forme ⇒ `NON_TESTABLE` |

## Limites

Le registre machine est vide parce qu'aucun cycle réel n'a encore été exécuté. Son schéma documentaire doit devenir un schéma exécutable et recevoir des tests mutants avant usage. La preuve d'immuabilité L4 reste `OPEN_PROOF_EXTERNAL`; P6 reste `BLOCKED_IMMUTABILITY`.
