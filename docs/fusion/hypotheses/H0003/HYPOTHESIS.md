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
| Statut de préimplémentation | `BLOCKED_SPEC_AMBIGUITY` |
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
- ordre local `(event_time, sequence, source_id, event_id)` lorsque ces quatre champs sont
  définis par le contrat;
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

## Audit de suffisance avant implémentation

L'audit du profil et des RFC existantes révèle les décisions nécessaires suivantes qui ne
sont pas encore fermées.

| ID | Statut | Ambiguïté exécutable | Pourquoi le code ne peut pas choisir |
|---|---|---|---|
| B1 | `BLOCKING` | vocabulaires autorisés absents pour `instrument_type` et `rounding_policy` | le profil exige de rejeter un type/politique inconnu sans définir l'ensemble connu |
| B2 | `BLOCKING` | `ReferenceSpec.valuation_price` n'a pas un vocabulaire unique | le modèle cite last/mid/mark/index, son exemple utilise `close`; choisir ou accepter tous serait une nouvelle décision |
| B3 | `BLOCKING` | vocabulaires absents pour `MarketEvent.event_type`, `Fill.side`, `Fill.liquidity_role` et `AccountEvent.kind` | validations, A8 et mutants dépendent de ces ensembles fermés |
| B4 | `BLOCKING` | forme des montants d'`AccountEvent` non définie | « montants signés et devises » ne fixe ni comptes/champs ni association delta↔devise; M9 est indécidable |
| B5 | `BLOCKING` | compatibilité `InstrumentSpec`/`ReferenceSpec` sans liaison sérialisée | `ReferenceSpec` minimal ne porte ni `instrument_id` ni hash d'instrument; M5 ne possède pas de règle de comparaison |
| B6 | `BLOCKING` | clé d'ordre définie avec `source_id,event_id`, absents de `Fill` et `AccountEvent` | appliquer la clé seulement à `MarketEvent` ou ajouter des champs serait une décision nouvelle |
| B7 | `BLOCKING` | identité de doublon divergente non définie par type | `event_id`, `fill_id` et `account_event_id` existent, mais aucune API/portée de registre ni clé de contenu n'est normée |
| B8 | `BLOCKING` | forme JSON d'un rationnel négatif/non entier non vectorisée | le profil dit `numerator/denominator`, mais aucun vecteur P1 n'établit si les entiers sont `"2"` ou `"2/1"` ni les règles `-1/2`, zéro et dénominateur |

Ces points ne sont pas des améliorations facultatives. Ils déterminent les bytes, hashes,
validations ou résultats des mutants annoncés. Les résoudre dans le code violerait le
critère principal de H0003.

## Décision préimplémentation

```text
H0003 = BLOCKED
reason = BLOCKED_SPEC_AMBIGUITY
blocking_findings = [B1, B2, B3, B4, B5, B6, B7, B8]
implementation_started = false
oracle_vectors_frozen = false
P1 = NOT_PASSED
```

Ce statut ne réfute pas l'utilité du profil P1. Il réfute seulement, dans son état actuel,
l'affirmation plus forte selon laquelle le socle peut être codé **sans** décision
supplémentaire.

## Forme attendue de l'oracle après levée explicite des blocages

Une révision humaine du profil devra fournir, avant code :

1. un vocabulaire fermé pour chaque discriminant validé;
2. un schéma exact d'`AccountEvent` et la matrice `kind × signe × devise`;
3. une règle explicite de compatibilité instrument/référentiel;
4. une clé d'ordre complète pour chacun des trois types d'événement;
5. une règle de doublon par identité et projection sémantique;
6. des vecteurs JSON exacts incluant entier, fraction réductible, fraction négative, zéro,
   Unicode NFC et caractères échappés;
7. les bytes UTF-8 et SHA-256 attendus d'au moins un `InstrumentSpec` et un
   `ReferenceSpec`.

H0003 pourra alors être révisée sur la même branche avant implémentation, avec une nouvelle
ancre de préenregistrement clairement postérieure à cette version bloquée. Cette version ne
doit pas être supprimée ni présentée comme un run.

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
provenance ne peut pas être établie. Elle restera `BLOCKED` tant que B1–B8 ne sont pas tous
fermés explicitement. Un éventuel `PASS` ne signifiera ni ledger spot/short valide, ni
enforcement temporel, replay, fidélité exchange ou `P1 PASS`.

## Condition d'arrêt actuelle

Atteinte : H0003 est préenregistrée, aucun code n'a été écrit et l'insuffisance du profil
est rendue falsifiable. La mission s'arrête avant toute implémentation et attend une décision
humaine sur B1–B8.
