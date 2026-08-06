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
9. Une occurrence possède un `occurrence_id` unique, un `first_recorded_commit` et un `cycle_id`. Elle est **historique** uniquement si le même `occurrence_id` existe déjà dans un commit ancêtre antérieur au commit qui a rendu l'ID causal non actif. Toute création d'`occurrence_id`, ou toute réutilisation du contenu sous un nouvel `occurrence_id`, est une **nouvelle occurrence**. Le temps mural et l'appréciation de l'opérateur ne participent pas à cette décision.
10. Le contrôleur résout le statut de l'ID au `first_recorded_commit`. Un historique peut être relu après dépréciation sans nouvelle sanction; modifier ses champs causaux crée obligatoirement un nouvel `occurrence_id`. Un ancêtre absent, un ID dupliqué ou une chronologie indécidable produit `NON_TESTABLE` avec raison `INVALID_OCCURRENCE_HISTORY` et compte comme cycle bloqué.
