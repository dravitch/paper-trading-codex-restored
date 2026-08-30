# P1 — Capability map et gap-to-gate après H0004

## Objet

Ce diagnostic confronte le profil fermé
[`P1_MINIMAL_EXECUTABLE_PROFILE.md`](P1_MINIMAL_EXECUTABLE_PROFILE.md) aux preuves admises
H0001, H0002, H0003 corrigée et H0004 corrigée. Il ne crée aucune hypothèse, ne modifie
aucun code et ne franchit pas P1.

```text
P1 = NOT_PASSED
next_hypothesis = NOT_YET_ASSIGNED
```

## Ancres admises

| Preuve | Admission | Portée retenue |
|---|---|---|
| H0001 | `de946c1` | exactitude rationnelle d'un short P0 isolé, ouverture puis clôture totale |
| H0002 | `68ca8f8` | invariants du même ledger inchangé sur cinq shorts isolés préenregistrés |
| H0003 corrigée | `6313afc` | contrats canoniques exécutables du paquet corrigé `d3134e6`, avec limites publiées |
| H0004 corrigée | `3679903` | `SPOT_CASH_V1` du paquet corrigé `5f0253d`, avec limites publiées |

Les premiers paquets H0003 `44893b0` et H0004 `5967ee0` restent `REJECTED`. Leurs
admissions de rejet, résultats et rapports sont des preuves historiques permanentes; les
paquets corrigés sont des objets distincts.

## Capability map `REQUIRED_IN_P1`

Les seuls états employés sont :

- `DEMONSTRATED` : preuve exécutable admise pour la portée fermée de la ligne;
- `PARTIAL` : une partie nécessaire est démontrée, mais la ligne du profil ne l'est pas
  entièrement;
- `ABSENT` : aucune preuve exécutable admise de la capacité requise.

| Capability requise | État post-H0004 | Preuve admise | Écart restant avant P1 |
|---|---|---|---|
| `InstrumentSpec` | `DEMONSTRATED` | H0003 : construction, validations, bytes/hash et compatibilités; H0004 : consommation effective et liaison hash état/spec | preuve cumulative P1 seulement |
| `ReferenceSpec` | `DEMONSTRATED` | H0003 : contrat et compatibilités; H0004 : consommation effective et liaison hash état/spec | preuve cumulative P1 seulement |
| `InstantNs` | `DEMONSTRATED` | H0003 corrigée : entier signé validé, rejets `bool`/float/chaîne/datetime | aucun pour le type lui-même |
| `DurationNs` | `DEMONSTRATED` | H0003 corrigée : même frontière d'entier signé et rejets stables | aucun pour le type lui-même |
| port `Clock` | `PARTIAL` | H0003 définit le port pur `now_ns() -> InstantNs` sans source système | injection explicite et preuve d'absence de défaut, singleton ou service locator |
| `MarketEvent` | `DEMONSTRATED` | H0003 : schéma, identité, temps/séquence, ordre local, doublon divergent, prix et grille | preuve cumulative; aucune consommation par H0004 n'est revendiquée |
| `Fill` | `DEMONSTRATED` | H0003 : schéma/compatibilités; H0004 : application BUY/SELL, grille, devise, S8 et rejets relationnels | application au modèle short canonique et preuve cumulative |
| `AccountEvent` | `DEMONSTRATED` | H0003 : contrat canonique; H0004 : initialisations explicites, production déterministe et conservation `new = old + somme(delta)` | production par le modèle short canonique et preuve cumulative |
| sérialisation rationnelle canonique | `DEMONSTRATED` | H0003 corrigée : fractions réduites, bytes/hash stables, round-trip et rejet des coercitions; H0004 réutilise les rationnels dans états/oracles | preuve cumulative P1 seulement |
| `SpotAccountModel / SPOT_CASH_V1` | `DEMONSTRATED` | H0004 corrigée : initialisation, BUY/SELL, six écritures, conservation, frais, valorisation pure, specs liées, S8 et rejets | preuve cumulative; limites publiées conservées |
| `IsolatedLinearShortAccountModel / ISOLATED_LINEAR_SHORT_EDU_V1` | `PARTIAL` | H0001/H0002 : algèbre exacte short full-close sur six configurations; H0003 : contrats disponibles | relier état et specs, produire les `AccountEvent`, sérialiser les discriminants/exclusions, conserver les oracles admis |
| injection `Clock` | `ABSENT` | aucun composant créant un instant sous le profil P1 n'a démontré l'injection explicite | fixture/consumer minimal, absence de Clock implicite et tests |
| contrôle AST temporel / allowlist | `ABSENT` | aucune preuve d'enforcement | analyse récursive, alias/dynamiques/filesystem/`SystemClock`, mutants et décision `unicodedata` |
| résultat et manifeste intégrés P1 | `ABSENT` | dossiers séparés H0001–H0004 seulement | run cumulatif de toutes les lignes requises, hashes, environnement et résultat reproductible |
| Critique + Contradictoire du paquet P1 intégré | `ABSENT` | revues par hypothèse seulement | deux rapports sur la même révision cumulative complète |
| admission humaine finale P1 | `ABSENT` | aucune | admission explicite après preuves et deux revues du gate intégré |

## Ce que H0004 change réellement

`SPOT_CASH_V1` n'est plus une capacité absente. Dans son scope admis, le paquet corrigé
démontre :

- initialisation explicite à partir d'`AccountEvent` préenregistrés;
- application de fills `BUY` et `SELL` canoniques;
- production déterministe de trois écritures par fill;
- conservation exacte BASE/QUOTE et absence de double comptage des frais;
- valorisation `EVENT_PRICE` pure;
- consommation effective des validateurs H0003;
- liaison de l'état aux hashes `InstrumentSpec` et `ReferenceSpec`;
- progression locale S8 sans tri ni mémoire cachée;
- multiplicateur spot limité à `1/1`, frais en devise quote et rejets mécaniques.

Cette ligne est donc `DEMONSTRATED`, avec les limites publiées dans l'admission H0004.
Elle ne généralise pas la preuve à multi-devise, frais en base, multiplicateur arbitraire,
scheduler/replay, provider ou fidélité marché.

H0004 renforce aussi `AccountEvent` : son existence comme donnée canonique était déjà
démontrée par H0003; sa production et sa conservation sont maintenant exécutées dans le
ledger spot. Cela ne prouve toutefois pas encore leur production dans le modèle short.

## Limites et dettes conservées

| Limite/dette | Scope | Effet |
|---|---|---|
| premier paquet H0004 rejeté | historique H0004 | permanent; 24 tests H0004 et 159 globaux verts n'ont pas empêché le rejet |
| M18c | force de falsification H0004 | limite publiée non bloquante pour l'API actuelle à fill individuel; aucune preuve générale sur un futur caller de collection |
| initialisation spot | H0004 | inputs explicites appliqués avant fills; aucun scheduler ou registre stateful général démontré |
| multiplicateur/frais spot | H0004 | preuve positive limitée à multiplicateur `1/1` et frais quote |
| famille short finie/full-close | modèle short P1 | limite H0001/H0002; canonicalisation encore requise |
| revues `PROCEDURAL / ROLE-SEPARATED` | preuve | aucune revendication IV&V ou indépendance statistique |
| `unicodedata` absent de l'allowlist | `P1_CLOCK_ENFORCEMENT / ALLOWLIST_V1` | `NON_BLOCKING` pour H0003/H0004; `BLOCKING_UNTIL_ALLOWLIST_DECISION` avant enforcement temporel et `P1 PASS` |

La dette `unicodedata` n'est ni résolue ni déplacée par ce diagnostic.

## Gap-to-gate restant

| Priorité logique | Bloc | Dépendances disponibles | Motif du blocage |
|---:|---|---|---|
| 1 | complétion canonique du short | contrats H0003 + algèbre/oracles H0001/H0002 | modèle short spécialisé non relié aux specs, événements, écritures et exclusions sérialisées du profil |
| 2 | injection `Clock` et enforcement AST | scalaires et port H0003 | injection et rejets temporels mécaniques absents; dette allowlist ouverte |
| 3 | preuve intégrée P1 | contrats + spot admis; short/temps encore incomplets | aucun paquet ne démontre cumulativement toutes les lignes requises |

## Vérification de la prochaine dépendance

H0004 n'a révélé aucune dépendance préalable au short canonique :

- les contrats, rationnels, fills et écritures nécessaires sont exécutables;
- la liaison état/specs et la consommation des validateurs possèdent maintenant un exemple
  ledger admis réutilisable comme contrainte, pas comme oracle métier short;
- les oracles H0001/H0002 et leur famille full-close existent déjà;
- le modèle short reçoit des événements explicitement horodatés et peut donc être
  canonicalisé sans créer d'instant ni attendre l'enforcement temporel;
- replay, provider et ordre global restent hors de ce bloc P1.

La complétion canonique du short est ainsi le premier bloqueur autonome restant. Le bloc
temporel vient ensuite, puis la preuve cumulative du gate. Ce diagnostic n'attribue aucun
identifiant d'hypothèse.

## Conclusion

```text
P1 = NOT_PASSED
canonical_contract_foundation = DEMONSTRATED
minimal_spot_ledger = DEMONSTRATED_WITH_PUBLISHED_LIMITS
canonical_short_model = PARTIAL
clock_port = PARTIAL
clock_injection = ABSENT
temporal_enforcement = ABSENT
integrated_p1_result_manifest = ABSENT
integrated_p1_reviews_admission = ABSENT

next_experiment_candidate = CANONICAL_SHORT_MODEL_COMPLETION
next_hypothesis = NOT_YET_ASSIGNED
```
