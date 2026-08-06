# Registre des identifiants causaux

## Statut

Registre normatif initial. Une valeur absente est `UNKNOWN`, jamais une chaîne inventée pendant l'analyse.

## Espaces d'identifiants

| Type | Forme | Exemple | Autorité de création |
|---|---|---|---|
| composant | `CMP-NNN-slug` | `CMP-001-spot-ledger` | RFC de composant acceptée |
| symbole | `SYM-NNN-slug` | `SYM-001-apply-fee` | API publique ou fonction normative |
| mode d'échec | `FM-NNN-slug` | `FM-001-fee-not-applied` | oracle ou mutation préenregistrée |
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
