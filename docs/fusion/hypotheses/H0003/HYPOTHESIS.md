# H0003 — Fermeture exécutable du socle canonique P1

## Identité et antériorité

| Champ | Valeur |
|---|---|
| ID | `H0003` |
| Type | `DEDUCE`, sous le profil P1 fermé |
| Gate concerné | P1 |
| Branche | `hypothesis/H0003-canonical-contract-foundation` |
| Commit de départ | `56e770af872b5132c1cf76b848a403320cf21876` |
| Source normative immédiate | `docs/fusion/P1_MINIMAL_EXECUTABLE_PROFILE.md` |
| Préenregistrement précédent | `ed2731da82326cf938b3634670e7cd1f6e50445f` |
| Statut précédent | `BLOCKED_SPEC_AMBIGUITY` |
| Décision normative B1–B8 | `0fe56109974790792eeaf39e341386164af36822` |
| Addendum normatif B5a | `d817a1642f7123ac367f7b0b7c03186b2d161925` |
| Statut de préimplémentation | `READY_FOR_IMPLEMENTATION` |
| Code H0003 lors de cet énoncé | aucun |

La branche descend du diagnostic P1 sans fusionner H0001/H0002 ni
`work/p1-capability-gap`. Ce document est créé avant tout code H0003. Aucun attendu,
vocabulaire ou invariant ne peut être ajouté après observation pour faire passer
l'expérience.

## Énoncé exact

Le profil minimal P1 fermé au commit `56e770a` peut-il être matérialisé, sans convention
P1 supplémentaire, en contrats canoniques exécutables pour :

1. `InstrumentSpec`;
2. `ReferenceSpec`;
3. `InstantNs`;
4. `DurationNs`;
5. `MarketEvent`;
6. `Fill`;
7. `AccountEvent`;
8. et, seulement comme port sans source temporelle, `Clock`?

Ces contrats doivent fournir validation, sérialisation rationnelle canonique, hashes
stables, ordre local déterministe et rejets mécaniques des entrées incompatibles. Ils ne
doivent contenir aucune logique de ledger ni dépendance à replay, stratégie, provider,
filesystem, réseau ou temps mural.

H0003 teste aussi la suffisance exécutable du profil. Si une décision métier, numérique ou
de représentation nécessaire manque, H0003 devient `BLOCKED`; elle n'invente pas cette
décision.

## Portée

- valeurs immuables et validations de construction;
- rationnels exacts réduits;
- JSON canonique récursif, UTF-8 NFC, clés triées et sans whitespace;
- SHA-256 des sérialisations canoniques d'`InstrumentSpec` et `ReferenceSpec`;
- unités, devises et discriminants obligatoires;
- `InstantNs`/`DurationNs` comme entiers signés;
- ordre local `(event_time, sequence, source_id, object_id)`, avec `object_id` défini par
  B6 selon le type;
- rejet d'une séquence absente;
- détection d'identités dupliquées au contenu divergent;
- A8 : quantités/prix/notionnels/marges/frais non négatifs, mouvements/PnL/deltas signés;
- round-trip `serialize → deserialize → serialize` bit-identique.

## Hors périmètre

- `SpotAccountModel` et `IsolatedLinearShortAccountModel`;
- application de fills, écritures de balance, frais ou calcul de PnL;
- génération d'ordres/fills et `ExecutionSpec` moteur;
- scheduler, journal ou replay P2;
- enforcement AST des sources temporelles;
- `FixedClock`, `ReplayClock` ou `SystemClock`;
- stratégie/`OrderIntent`, provider, réseau, filesystem et fidélité exchange;
- P6, P7, RiskMap et chaîne d'admission;
- déclaration `P1 PASS`.

## Règles déjà fermées et réutilisables

H0003 peut appliquer sans nouvelle décision :

- les rationnels sous forme réduite `numerator/denominator`, sans tolérance interne;
- `instrument_id` sémantique non vide et hash canonique de la spec pour la compatibilité;
- montants tous associés à une devise;
- événements sans séquence rejetés;
- A8 sous sa forme fermée : magnitudes économiques non négatives, deltas comptables signés;
- `Clock.now_ns() -> InstantNs`, sans import temporel ni valeur par défaut;
- sérialisation JSON canonique déjà définie dans `CAUSAL_ID_REGISTRY.md` : normalisation
  NFC, tri récursif des clés, séparateurs `,`/`:` sans espaces, échappements uniques,
  UTF-8 sans BOM ni fin de ligne.

## Audit de suffisance précédent et résolution

Le préenregistrement `ed2731d` a détecté les huit ambiguïtés ci-dessous avant tout code.
La décision humaine séparée `0fe5610` les ferme sans effacer cet état historique.

| ID | Statut | Ambiguïté exécutable | Pourquoi le code ne peut pas choisir |
|---|---|---|---|
| B1 | `RESOLVED` | vocabulaires instrument/arrondi | `{SPOT,LINEAR_PERPETUAL}`; `REJECT_OFF_GRID` |
| B2 | `RESOLVED` | prix de valorisation | `EVENT_PRICE` uniquement |
| B3 | `RESOLVED` | vocabulaires événements/fills/comptes | ensembles fermés dans la décision humaine |
| B4 | `RESOLVED` | forme d'`AccountEvent` | onze champs exacts, compte, devise et signes fermés |
| B5 | `RESOLVED` | compatibilité instrument/référentiel | identité et SHA-256 de spec tous deux obligatoires |
| B6 | `RESOLVED` | ordre local | clé par type; aucun ordre inter-types P1 |
| B7 | `RESOLVED` | doublons | identité typée, collection explicite, idempotence/divergence fermées |
| B8 | `RESOLVED` | rationnels JSON | chaîne irréductible `numerator/denominator`, dénominateur positif |
| B5a | `RESOLVED` | compatibilité de devise des frais | fill = référentiel; référentiel ∈ devises de l'instrument |

Les règles complètes font autorité dans `P1_CANONICAL_CONTRACT_DECISIONS.md`. Aucun code
n'a été écrit entre la détection et leur décision.

## Nouvel ancrage préimplémentation

```text
previous_preregistration = ed2731da82326cf938b3634670e7cd1f6e50445f
previous_status = BLOCKED_SPEC_AMBIGUITY
normative_decision_commit = 0fe56109974790792eeaf39e341386164af36822
normative_addendum_commit = d817a1642f7123ac367f7b0b7c03186b2d161925
B1-B8+B5a = RESOLVED
implementation_started = false
oracle_vectors_frozen = true
oracle_vectors = ORACLE_VECTORS.json
status = READY_FOR_IMPLEMENTATION
P1 = NOT_PASSED
```

Toute convention supplémentaire découverte pendant l'implémentation replace H0003 en
`BLOCKED`; elle ne peut être ajoutée silencieusement.

## Oracle préenregistré

`ORACLE_VECTORS.json` fige avant code :

- entiers, fractions réductibles, fraction négative et zéro;
- textes rationnels non canoniques devant être rejetés;
- un objet valide pour les cinq contrats sérialisables;
- JSON canonique et SHA-256 de chaque objet;
- bytes UTF-8 exacts d'`InstrumentSpec`, `ReferenceSpec` et du vecteur Unicode/échappements;
- clés d'ordre locales et résultats de doublons idempotent/divergent.

Le hash attendu d'`InstrumentSpec` est
`e0400eeb2ebd95e4ee69884796d18113f05557ed326b1b7bbb49164362a886b4`; celui de
`ReferenceSpec` est
`f56b0b9f915427b0260dc450798d396519ebddeb8ca6567b94bc7a738e0febde`.

## Falsifications préenregistrées

Lorsque B1–B8 auront une réponse normative antérieure au code :

| ID | Mutation devant échouer |
|---|---|
| M1 | `contract_multiplier <= 0` |
| M2 | `tick_size <= 0` ou `lot_size <= 0` |
| M3 | devise absente ou incompatible |
| M4 | rationnel non réduit ou bytes différents pour `1/2` et `2/4` |
| M5 | `ReferenceSpec` incompatible agrégé à l'instrument |
| M6 | événement sans `sequence` |
| M7 | même identité d'événement, contenu divergent |
| M8 | frais négatif ou sans devise |
| M9 | `AccountEvent` avec signe incompatible avec son `kind` |
| M10 | permutation de l'ordre de construction modifiant bytes/hash canoniques |
| M11 | round-trip sérialisé produisant des bytes ou un SHA-256 différents |

Un crash générique ne suffit pas : chaque rejet doit porter un code stable lié à la règle.

## Critères de réfutation

Après levée des blocages, H0003 sera `FAIL` si :

1. deux valeurs sémantiquement identiques produisent des bytes ou hashes différents;
2. deux valeurs sémantiquement différentes partagent une identité/hash accepté;
3. un mutant M1–M11 n'est pas rejeté par sa règle attendue;
4. un round-trip modifie les bytes;
5. l'ordre local dépend de l'ordre de construction;
6. un contrat accepte unité, devise, discriminant ou séquence absent/incompatible;
7. le code importe une logique de ledger, replay, stratégie, provider, réseau ou temps;
8. l'implémentation ajoute une convention non présente dans l'ancre normative révisée.

Elle sera `NON_TESTABLE` si les vecteurs/hashes préenregistrés sont invalides ou si leur
provenance ne peut pas être établie. Elle redevient `BLOCKED` si une décision supplémentaire
est nécessaire. Un éventuel `PASS` ne signifiera ni ledger spot/short valide, ni
enforcement temporel, replay, fidélité exchange ou `P1 PASS`.

## Condition d'arrêt actuelle

Atteinte : H0003-v2 cite la décision humaine distincte, conserve l'ancien blocage, fige ses
vecteurs et reste sans code. La mission s'arrête avant implémentation pour vérification du
nouveau paquet préenregistré.
