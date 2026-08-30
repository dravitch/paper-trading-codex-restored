# P1 — Décision humaine S8 du ledger spot minimal

## Autorité

```text
decision_authority = HUMAN
ambiguity_detected_at = 56c5e54ada0e90d449329bf2b3fa4d927d9e947e
implementation_started = false
effect_on_H0004 = AUTHORIZED_FOR_REPREREGISTRATION_ONLY
effect_on_P1 = NOT_PASSED
```

## Décision

```text
S8 = STRICTLY_INCREASING_FILL_LOCAL_KEY
```

Après application du premier `Fill`, toute application suivante doit satisfaire :

```text
current_fill_local_key > previous_fill_local_key

fill_local_key = (
  event_time,
  sequence,
  source_id,
  fill_id
)
```

La clé est exactement l'ordre local B6 de H0003. Le ledger ne trie pas les fills et ne
choisit pas leur ordre; il valide seulement une précondition de transition.

## État utilisé

Après chaque fill appliqué, S5 conserve déjà :

```text
last_event_key = (
  "FILL",
  event_time,
  sequence,
  source_id,
  fill_id
)
```

Aucun champ `last_fill_key`, historique, `seen_fill_ids`, cache, singleton ou registre
caché n'est ajouté.

## Premier fill

Lorsque `last_event_key` désigne encore un `ACCOUNT_EVENT` d'initialisation, le premier
fill est accepté sans comparaison inter-types. Cela ne définit aucun ordre entre
`ACCOUNT_EVENT` et `FILL`.

Après ce premier fill, S3 interdit toute nouvelle initialisation. Entre deux applications
de fills, `last_event_key` désigne donc nécessairement le dernier `Fill` appliqué.

## Fills suivants et rejets

Lorsque le dernier input est un `FILL`, la comparaison porte seulement sur les quatre
composants de sa clé locale B6 :

```text
current == stored → SPOT_FILL_REAPPLICATION
current <  stored → SPOT_FILL_OUT_OF_ORDER
current >  stored → précondition S8 satisfaite
```

Une clé plus petite est rejetée même si son `fill_id` n'a jamais été observé. Cette
restriction est intentionnelle : `SPOT_CASH_V1` ne réordonne jamais les inputs. Un
composant P2 pourra ultérieurement fournir les fills dans l'ordre approprié.

## Relation avec B7

La déduplication H0003 sur collection explicite reste inchangée :

```text
même identité + mêmes bytes → IDEMPOTENT_DEDUPLICATE
même identité + bytes différents → DUPLICATE_DIVERGENT
```

B7 intervient avant application lorsqu'une collection est validée. S8 traite uniquement
la transition stateful du ledger et ne promet pas de reconstruire l'historique des
identités consommées.

## Limites

S8 :

- ne crée pas de scheduler;
- ne trie aucun fill;
- ne définit aucun ordre inter-types;
- ne lit aucun temps mural;
- ne modifie ni B6 ni S1–S7;
- ne change aucune balance du chemin nominal H0004;
- borne seulement les inputs acceptés par une transition.

**Statut : `RESOLVED`.**
