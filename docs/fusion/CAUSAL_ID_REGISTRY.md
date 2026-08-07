# Registre des identifiants causaux

## Statut

Registre normatif initial. Une valeur absente est `UNKNOWN`, jamais une chaîne inventée pendant l'analyse.

Cycle de vie fermé : `RESERVED → ACTIVE → DEPRECATED → RETIRED`. `RESERVED` prépare une spécification mais ne peut pas apparaître dans une `failure_signature` observée. `ACTIVE` exige l'acceptation de l'autorité indiquée et autorise l'usage. `DEPRECATED` reste lisible pour l'historique mais interdit les nouvelles occurrences. `RETIRED` est terminal et ne supprime jamais l'identifiant.

## Espaces d'identifiants

| Type | Forme | Exemple | Autorité de création et activation |
|---|---|---|---|
| composant | `CMP-NNN-slug` | `CMP-001-spot-ledger` | RFC de composant acceptée |
| symbole | `SYM-NNN-slug` | `SYM-001-apply-fee` | contrat canonique accepté nommant le symbole |
| mode d'échec | `FM-NNN-slug` | `FM-001-fee-not-applied` | oracle ou mutation accepté avant exécution |
| groupe racine | `RCG-NNN-slug` | `RCG-001-fee-policy-drift` | décision opérateur versionnée |
| occurrence | `OCC-NNNNNN` | `OCC-000001` | contrôleur NO-GO uniquement; aucun ID fourni par l'appelant |

## Registre initial

| ID | Définition | Introduit par | Statut |
|---|---|---|---|
| `CMP-001-spot-ledger` | modèle comptable spot canonique | RFC-005 | `RESERVED` |
| `CMP-002-isolated-short-ledger` | modèle short linéaire isolé canonique | RFC-005 | `RESERVED` |
| `CMP-003-replay-scheduler` | ordonnanceur de replay canonique | gate P2 | `RESERVED` |
| `CMP-004-risk-map` | calcul et sérialisation RiskMap | gate P6 | `RESERVED` |
| `SYM-001-apply-fee` | application d'un frais au ledger | modèle de référence | `RESERVED` |
| `SYM-002-position-size` | calcul de taille/notionnel | modèle de référence | `RESERVED` |
| `FM-001-fee-not-applied` | frais déclaré sans écriture correspondante | mutation P1 | `RESERVED` |
| `FM-002-wrong-notional` | notionnel différent de quantité × prix × multiplicateur | invariant P1 | `RESERVED` |
| `FM-003-wall-clock-access` | lecture temporelle hors port `Clock` | mutation P1 | `RESERVED` |
| `FM-004-result-divergence` | mêmes inputs, projections sémantiques différentes | oracle O7 | `RESERVED` |

## Règles

1. Les identifiants sont immuables; une définition changée reçoit un nouvel ID.
2. Un alias ou renommage conserve l'ID et son historique.
3. `root_cause_group_id` ne remplace jamais les signatures observées; il les relie.
4. Une fusion/scission de groupe cite preuves, anciennes et nouvelles clés.
5. Aucun message libre, ligne de code ou traceback ne devient un ID.
6. L'activation cite le commit d'autorité, la décision Critique/Contradictoire applicable et la date.
7. Un ID `RESERVED`, `DEPRECATED` ou `RETIRED` utilisé dans une nouvelle occurrence rend le résultat `NON_TESTABLE` avec raison `INVALID_CAUSAL_ID_STATE`; il compte comme cycle bloqué de la famille. L'ID n'est jamais activé/réactivé rétroactivement pour faire passer le même run.
8. Les lignes initiales restent `RESERVED` jusqu'à acceptation des RFC/gates qui les autorisent.
9. Une occurrence possède un `occurrence_id` unique, un `first_recorded_commit`, un `cycle_id` et `causal_payload_sha256`. Ce hash est calculé sur le JSON canonique `{cause_family_key,failure_signature,cause_key,root_cause_group_id,cycle_id}` : clés triées, UTF-8, séparateurs `,`/`:` sans espaces, valeurs absentes encodées `null`. Elle est **historique** uniquement si le même `occurrence_id` et le même `causal_payload_sha256` existent dans un commit ancêtre antérieur au commit qui a rendu l'ID causal non actif. Toute création d'identité ou divergence de hash est une **nouvelle occurrence**. Le temps mural et l'appréciation de l'opérateur ne participent pas à cette décision.
10. Le contrôleur recalcule le hash courant et le compare au registre au `first_recorded_commit`. Un historique inchangé peut être relu après dépréciation sans sanction. Hash divergent, ancêtre absent, ID dupliqué ou chronologie indécidable produit `NON_TESTABLE` avec raison `INVALID_OCCURRENCE_HISTORY` et compte comme cycle bloqué; le contenu modifié ne peut jamais hériter du statut historique.
11. Une occurrence satisfait `^OCC-[0-9]{6}$`, avec domaine `OCC-000001` à `OCC-999999`. Le contrôleur rejette tout ID proposé, alloue exactement `OCC-{n+1:06d}` où `n` est le plus grand suffixe du registre autoritaire, puis écrit l'occurrence dans la même transaction. Le validateur exige la séquence exacte `000001..len(occurrences)`, sans trou, doublon ni réutilisation. `OCC-000000`, une valeur hors séquence ou un registre épuisé produit `NON_TESTABLE` avec `INVALID_OCCURRENCE_HISTORY`.

### Sérialisation canonique causale

Le JSON est canonique récursivement : dictionnaires triés par valeur scalaire Unicode des clés à tous les niveaux; tableaux dans leur ordre normatif; entiers décimaux sans zéro initial; booléens et `null` JSON; flottants interdits; séparateurs `,` et `:` sans espaces. Toute clé et chaîne doit déjà être en NFC; une entrée non NFC ou contenant un surrogate Unicode est rejetée, jamais normalisée silencieusement.

Échappements uniques : `"`, `\\`, `\b`, `\t`, `\n`, `\f`, `\r`; les autres U+0000–U+001F utilisent `\u00xx` en hexadécimal minuscule. `/` n'est jamais échappé. Tout autre caractère, notamment non ASCII NFC, est encodé directement en UTF-8. Le hash porte sur ces octets, sans BOM ni fin de ligne.

Vecteur normatif :

```text
{"cause_family_key":"CFK-A","cause_key":"CK-A","cycle_id":"CYC-000001","failure_signature":{"component_id":"CMP-001-spot-ledger","failure_mode_id":"FM-001-fee-not-applied","symbol_id":"SYM-001-apply-fee"},"root_cause_group_id":null}
SHA-256 = 51857ebbbcc0155f75bf33ae635a6f865a17e74cd324a7cd063c1ef3b47375e6
```

Vecteur étendu (le texte contient NFC `é`, un slash non échappé et `\n`) :

```text
{"labels":["é","a/b","line\n"],"n":7,"ok":true}
SHA-256 = eacf3f8071439cd6315c7693159449aeb6f9988a727eba234ab063da9f7e7563
```

Vecteur de couverture (clé NFC non ASCII, entier, booléen, U+0000 et U+001F) :

```text
{"a":"\u0000\u001f","é":[1,true]}
SHA-256 = 5ab8722b166d50ee50983b73ca8dc02cadc2114ef529d97f1dc7a5d70e87feee
```

Fixtures de rejet obligatoires, sans hash produit : clé NFD `e\u0301`; valeur NFD `e\u0301`; surrogate isolé U+D800; paire de surrogates encodée au lieu du scalaire Unicode; clé dupliquée après décodage. Chaque fixture lève l'erreur de pré-validation `NON_CANONICAL_CAUSAL_JSON`; normaliser puis accepter est une mutation qui doit échouer.

Cette erreur survient avant allocation de `occurrence_id`, `cycle_id`, famille ou groupe. Elle ne crée aucune entrée dans le registre NO-GO et ne compte jamais comme cycle bloqué. Elle est inscrite seulement dans le rapport de validation d'entrée avec hash des octets rejetés et sans recopier le contenu potentiellement sensible. Si un payload déjà enregistré devient non canonique lors d'une relecture, il s'agit au contraire de `REGISTRY_HISTORY_VIOLATION`, qui compte comme cycle bloqué.

### Supersession des occurrences

Une correction crée une entrée dans `supersessions` de forme exacte `{supersession_id, superseded_occurrence_id, replacement_occurrence_id, reason_code, decision_commit}`. `supersession_id` satisfait `^SUP-[0-9]{6}$`, domaine `SUP-000001` à `SUP-999999`. Le contrôleur rejette tout SUP proposé, alloue `SUP-{n+1:06d}` dans la même transaction et exige la séquence exacte `000001..len(supersessions)`, sans trou, doublon ni réutilisation.

Les deux occurrences existent, sont distinctes et `replacement_occurrence_id` est le prochain OCC alloué dans la même transaction. `reason_code` appartient exactement à `{CORRECT_CAUSAL_PAYLOAD, REATTRIBUTE_CAUSE, REPAIR_METADATA}`. `decision_commit` satisfait `[0-9a-f]{40}`, existe dans le dépôt, est ancêtre strict du commit qui écrit la supersession et contient une décision opérateur nommant l'occurrence source et la raison; une décision créée dans la même transaction est refusée.

L'ancienne occurrence demeure immuable dans `occurrences`, compte toujours dans `len(occurrences)` et son statut dérivé est terminal `SUPERSEDED`. Une occurrence possède au plus une supersession entrante et une sortante; la chaîne est acyclique. Le remplacement a son propre hash et ne masque aucun cycle. Supprimer l'événement, réutiliser un ID, référencer une occurrence absente ou créer une branche/cycle produit `REGISTRY_HISTORY_VIOLATION`.

## Codes de raison fermés

| Code | Condition mécanique |
|---|---|
| `INVALID_CAUSAL_ID_STATE` | ID causal non actif utilisé par une nouvelle occurrence |
| `INVALID_OCCURRENCE_HISTORY` | identité, hash causal ou ascendance d'occurrence invalide |
| `INCOMPLETE_GROUP_HISTORY` | cycles ou prédécesseurs connus absents d'un groupe |
| `REGISTRY_HISTORY_VIOLATION` | suppression, mutation ou chaîne de hash invalide du registre machine |
| `MERGE_REGISTRY_CONFLICT` | parents de merge portant des blobs de registre divergents |

Tout autre code est `UNKNOWN_REASON_CODE` et rend le résultat `NON_TESTABLE`; l'ajout d'un code exige une révision normative préalable.

`NON_CANONICAL_CAUSAL_JSON` est un code de pré-validation, pas un code de raison NO-GO; il est régi par la section de sérialisation ci-dessus.
