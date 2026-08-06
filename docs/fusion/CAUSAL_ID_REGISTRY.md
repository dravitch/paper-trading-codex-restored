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

Le JSON est canonique récursivement : dictionnaires triés par clé Unicode à tous les niveaux; tableaux dans leur ordre normatif; chaînes JSON UTF-8 avec échappement JSON minimal, sans ASCII-forcing; entiers décimaux sans zéro initial; booléens et `null` JSON; flottants interdits; séparateurs `,` et `:` sans espaces. Le hash porte sur les octets UTF-8, sans BOM ni fin de ligne.

Vecteur normatif :

```text
{"cause_family_key":"CFK-A","cause_key":"CK-A","cycle_id":"CYC-000001","failure_signature":{"component_id":"CMP-001-spot-ledger","failure_mode_id":"FM-001-fee-not-applied","symbol_id":"SYM-001-apply-fee"},"root_cause_group_id":null}
SHA-256 = 51857ebbbcc0155f75bf33ae635a6f865a17e74cd324a7cd063c1ef3b47375e6
```

## Codes de raison fermés

| Code | Condition mécanique |
|---|---|
| `INVALID_CAUSAL_ID_STATE` | ID causal non actif utilisé par une nouvelle occurrence |
| `INVALID_OCCURRENCE_HISTORY` | identité, hash causal ou ascendance d'occurrence invalide |
| `INCOMPLETE_GROUP_HISTORY` | cycles ou prédécesseurs connus absents d'un groupe |
| `REGISTRY_HISTORY_VIOLATION` | suppression, mutation ou chaîne de hash invalide du registre machine |

Tout autre code est `UNKNOWN_REASON_CODE` et rend le résultat `NON_TESTABLE`; l'ajout d'un code exige une révision normative préalable.
