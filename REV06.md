# REV06 — Fermeture Producteur des limites L1–L4 après `decbb42`

## Portée

Réponse au rapport admis `docs/fusion/CONTRADICTOIRE_DELTA_DECBB42.md`. Cette révision modifie des spécifications et des gates; elle n'implémente pas les contrôleurs P6 et ne valide aucun gate.

## L1 — Liaison oracle–rapport

- **Avant** : un rapport admis pouvait être substitué entre O2, O4 et O7 si ses métadonnées générales concordaient.
- **Après** : le registre possède un `Oracle scope`; le blob admis doit contenir `Oracle scope: <oracle_id>` et le contrôleur exige l'appartenance aux deux sources.
- **Justification** : l'identité de l'oracle doit provenir du blob historique, pas de la preuve courante contrôlée.
- **Test requis** : remplacer le rapport O2 par un rapport O4 ayant le même verdict doit bloquer P6.
- **Preuve minimale** : `O2 ∉ {O4}`; la conjonction `index_scope_contains && blob_marker_matches` vaut `false`.

## L2 — Nouvelle occurrence

- **Avant** : « historique » dépendait d'une qualification non décidable de l'opérateur.
- **Après** : une occurrence n'est historique que si son `occurrence_id` existe dans un commit ancêtre antérieur à la désactivation de l'ID. Toute nouvelle identité ou modification causale est nouvelle.
- **Justification** : l'ascendance Git et l'identité enregistrée sont vérifiables sans temps mural.
- **Test requis** : dupliquer une occurrence dépréciée sous un nouvel ID doit produire `NON_TESTABLE INVALID_CAUSAL_ID_STATE`; falsifier son ascendance doit produire `INVALID_OCCURRENCE_HISTORY`.
- **Preuve minimale** : occurrence A existante avant dépréciation = lecture historique; occurrence B au contenu identique mais nouvel ID = nouvelle occurrence sanctionnée.

## L3 — Héritage des groupes

- **Avant** : un nouveau groupe candidat pouvait repartir de zéro en recouvrant des causes déjà comptées.
- **Après** : son historique est l'union dédupliquée des `cycle_id` de ses causes et groupes prédécesseurs; les prédécesseurs et le hash canonique sont obligatoires.
- **Justification** : un changement de partition ne change pas les événements observés.
- **Test requis** : regrouper `{C1:[A,B], C2:[B,C]}` doit donner trois cycles, jamais zéro, deux ou quatre.
- **Preuve numérique** : `|{A,B} ∪ {B,C}| = |{A,B,C}| = 3`.

## L4 — Immuabilité avant P6

- **Avant** : la protection de branche ou l'archive signée n'était exigée qu'à la publication finale.
- **Après** : P6 exige préalablement une règle de protection distante exportée et hashée ou une archive Git signée vérifiable; sinon `BLOCKED_IMMUTABILITY`.
- **Justification** : un hash de blob ne protège pas contre la réécriture de l'histoire qui le porte.
- **Test requis** : supprimer la preuve d'immuabilité du manifeste doit bloquer P6.
- **Preuve actuelle** : `UNKNOWN`; aucune protection distante ni archive signée n'est affirmée par cette révision. L4 est spécifiée mais reste `OPEN_PROOF_EXTERNAL`.

## Résultat

L1–L3 sont `RESOLVED_SPEC_PENDING_REVIEW`. L4 est `RESOLVED_SPEC_OPEN_PROOF_EXTERNAL`. Aucun statut `PASS` n'est attribué à P1 ou P6.
