# P1 — Capability map et gap-to-gate après H0003

## Objet

Ce diagnostic confronte le profil fermé
[`P1_MINIMAL_EXECUTABLE_PROFILE.md`](P1_MINIMAL_EXECUTABLE_PROFILE.md) aux preuves admises
H0001, H0002 et H0003 corrigée. Il ne crée aucune hypothèse, ne modifie aucun code et ne
franchit pas P1.

```text
P1 = NOT_PASSED
next_hypothesis = NOT_YET_ASSIGNED
```

## Ancres admises

| Preuve | Admission | Portée retenue |
|---|---|---|
| H0001 | `de946c1` | exactitude rationnelle d'un short P0 isolé, ouverture puis clôture totale |
| H0002 | `68ca8f8` | invariants du même ledger inchangé sur cinq shorts isolés préenregistrés |
| H0003 corrigée | `6313afc` | contrats canoniques exécutables du paquet `d3134e6`, avec limites publiées |

Le paquet H0003 initial `44893b0` reste `REJECTED`. Son cycle correctif et son admission
n'effacent ni ses rapports ni son résultat rejeté.

## Capability map `REQUIRED_IN_P1`

Les états employés sont :

- `DEMONSTRATED` : preuve exécutable admise pour la portée de la ligne;
- `PARTIAL` : une partie nécessaire est démontrée, mais la ligne du profil ne l'est pas
  entièrement;
- `ABSENT` : aucune preuve exécutable admise de la capacité requise.

| Capability requise | État post-H0003 | Preuve admise | Écart restant avant P1 |
|---|---|---|---|
| `InstrumentSpec` | `DEMONSTRATED` | H0003 : construction, validations, sérialisation/hash, multiplicateur/tick/lot/politique et compatibilité | intégration aux deux ledgers et à la preuve P1 cumulative seulement |
| `ReferenceSpec` | `DEMONSTRATED` | H0003 : identité + hash instrument, numéraire, prix événement, politique numérique et devise de frais | consommation effective par les ledgers et preuve cumulative |
| `InstantNs` | `DEMONSTRATED` | H0003 corrigée : entier signé validé à l'exécution; `bool`, float, chaîne et datetime rejetés | aucun pour le type lui-même |
| `DurationNs` | `DEMONSTRATED` | H0003 corrigée : même frontière d'entier signé et rejets stables | aucun pour le type lui-même |
| port `Clock` | `PARTIAL` | H0003 définit le port pur `now_ns() -> InstantNs` sans source système | injection explicite dans tout composant créant un instant et preuve d'absence de défaut/service locator |
| `MarketEvent` | `DEMONSTRATED` | H0003 : schéma, identité, temps/séquence, ordre local, déduplication divergente, prix et grille instrument | consommation par un modèle de compte ou preuve intégrée hors scope H0003 |
| `Fill` | `DEMONSTRATED` | H0003 : schéma, side, quantité/prix/frais/devise, ordre et compatibilités instrument/référence | application aux transitions spot/short |
| `AccountEvent` | `PARTIAL` | H0003 : schéma, discriminants, delta signé, devise/compte, ordre et doublon | production par les ledgers et preuve `new_balance = old_balance + somme(delta)` |
| sérialisation rationnelle canonique | `DEMONSTRATED` | H0003 corrigée : fractions réduites, bytes/hash stables, round-trip et rejet bool/binary64 | réutilisation dans les futurs états/ledgers, puis preuve cumulative |
| `SpotAccountModel / SPOT_CASH_V1` | `ABSENT` | aucune | état, BUY/SELL, frais, balances, valorisation, conservation, rejets et oracle exact |
| `IsolatedLinearShortAccountModel / ISOLATED_LINEAR_SHORT_EDU_V1` | `PARTIAL` | H0001/H0002 : noyau algébrique exact short full-close sur six configurations; H0003 : contrats réutilisables | relier le ledger aux specs, événements et discriminants; produire les `AccountEvent`; sérialiser/rejeter les capacités unsupported; conserver les oracles admis |
| contrôle AST temporel / allowlist | `ABSENT` | aucune preuve d'enforcement | analyse récursive, alias/dynamiques/filesystem/SystemClock, mutations et décision `unicodedata` |
| manifeste et résultat intégrés P1 | `ABSENT` | dossiers séparés H0001–H0003 seulement | run cumulatif de toutes les capacités requises, hashes, environnement et résultat reproductible |
| Critique + Contradictoire + admission du paquet P1 | `ABSENT` | revues par hypothèse, aucune revue du gate intégré | deux rapports sur le même paquet P1 complet puis admission humaine |

## Ce que H0003 change réellement

Le langage de données nécessaire aux expériences comptables suivantes n'est plus
seulement documentaire : instruments, référentiels, événements, rationnels et scalaires
temporels possèdent maintenant des représentations exécutables, des bytes canoniques et
des rejets admis.

H0003 ne transforme toutefois pas ces contrats en transitions comptables. En particulier :

- l'existence de `Fill` ne prouve aucune application de fill;
- l'existence de `AccountEvent` ne prouve ni sa production par un ledger ni la conservation
  d'une balance;
- le port `Clock` ne prouve pas son injection ni le contrôle AST;
- H0001/H0002 restent un modèle short spécialisé, pas encore le modèle short canonique du
  profil P1.

## Limites et dettes conservées

| Limite/dette | Scope | Effet |
|---|---|---|
| premier paquet H0003 rejeté | historique H0003 | permanent; n'affecte pas l'admission distincte du paquet corrigé |
| validateurs relationnels appelés explicitement | futurs consommateurs P1 | chaque ledger devra démontrer leur appel; non bloquant pour H0003 fermée |
| `unicodedata` absent de l'allowlist | `P1_CLOCK_ENFORCEMENT / ALLOWLIST_V1` | non bloquant H0003; bloquant avant enforcement temporel et `P1 PASS` |
| revues `PROCEDURAL / ROLE-SEPARATED` | preuve | aucune revendication IV&V ou d'indépendance statistique |
| famille short finie/full-close | modèle short P1 | limite publiée de H0001/H0002; complétion canonique encore requise |

## Gap-to-gate restant

| Priorité logique | Bloc | Dépendances désormais disponibles | Motif du blocage |
|---:|---|---|---|
| 1 | ledger spot minimal | contrats H0003 admis | capacité explicitement requise et entièrement absente |
| 2 | complétion canonique du short | contrats H0003 + noyau H0001/H0002 | transitions non reliées aux specs/événements/écritures; exclusions non sérialisées/testées |
| 3 | `Clock` injecté et enforcement AST | scalaires et port H0003 | injection et rejets temporels mécaniques absents; dette allowlist ouverte |
| 4 | preuve intégrée P1 | blocs 1–3 | aucun paquet ne démontre cumulativement toutes les lignes requises |

## Vérification de la prochaine dépendance

H0003 n'a révélé aucune dépendance autonome à fermer avant le ledger spot :

- les types `InstrumentSpec`, `ReferenceSpec`, `Fill`, `AccountEvent` et les rationnels
  requis par son état et ses transitions sont exécutables et admis;
- les validateurs relationnels peuvent être exercés dans l'expérience spot elle-même;
- un ledger appliquant des événements explicitement horodatés n'a pas besoin d'un
  scheduler ni d'une source temporelle, donc l'enforcement AST peut rester un bloc P1
  ultérieur sans contaminer cette expérience;
- replay, stratégie, provider et RiskMap restent hors P1 ou différés.

Le premier bloqueur autonome suivant est donc bien le ledger spot minimal. Cette conclusion
n'attribue aucun identifiant d'hypothèse et n'autorise encore aucune implémentation.

## Conclusion

```text
P1 = NOT_PASSED
canonical_contract_foundation = DEMONSTRATED_WITH_PUBLISHED_LIMITS
minimal_spot_ledger = ABSENT
canonical_short_model = PARTIAL
clock_port = PARTIAL
temporal_enforcement = ABSENT
integrated_p1_proof = ABSENT

next_experiment_candidate = MINIMAL_SPOT_LEDGER
next_hypothesis = NOT_YET_ASSIGNED
```
