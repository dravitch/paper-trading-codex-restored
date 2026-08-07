# REV12 — Réponse Producteur S1–S4

## Portée

Réponse au rapport Contradictoire `CONTRADICTOIRE_DELTA_REV11BIS.md`, admis au commit `102ce6a` et indexé au commit `d8bc959`. Cette révision modifie uniquement les contrats documentaires et ajoute un registre machine vide; aucun contrôleur, résultat financier, admission d'oracle ou gate n'est créé.

## Corrections

| Constat | Avant | Après | Oracle falsifiable |
|---|---|---|---|
| S1 | `ORACLE_ADMISSIONS.json` était fermé par snapshot, sans règle d'évolution | genesis ancrée; seul l'ajout d'un oracle est permis; objets antérieurs immuables; dernière révision effective et merges définis | retirer/modifier O2 entre deux révisions, sauter le prédécesseur ou accepter deux parents divergents doit bloquer P6 |
| S2 | rapport de rejet sans chemin/schéma; priorité ambiguë entre deux erreurs historiques | `reports/input_validation/<run_id>.json`, schéma fermé, hash des octets seulement; priorité registre muté → occurrence divergente → nouvel input invalide | une occurrence enregistrée à la fois mutée et non canonique doit produire seulement `REGISTRY_HISTORY_VIOLATION`; un nouvel input NFD ne doit modifier aucun compteur |
| S3 | `C` pouvait être interprété comme tout commit évalué | `E` est le commit évalué; `C` est son dernier ancêtre de première parenté ayant modifié le registre | pour `E=3876fce`, le contrôleur doit résoudre `C=7039476` et `P=6867a2d`, sans faux positif |
| S4 | la décision opérateur n'avait ni emplacement ni grammaire machine | `OPERATOR_SUPERSESSION_DECISIONS.json` à schéma fermé; le commit cité ajoute la décision; occurrence et raison doivent concorder | une décision seulement narrative, simultanée, réutilisée ou portant une autre raison doit être rejetée |

## Contre-exemples indépendants attendus

1. Registre oracle parent `{O2: ACCEPT}` puis enfant `{O2: REJECT}` : `ORACLE_ADMISSION_HISTORY_VIOLATION`.
2. Registre oracle parent `{O4}` puis enfant trié `{O2,O4}` avec O4 inchangé : transition valide; l'ajout en tête n'est pas une mutation d'O4.
3. Évaluation NO-GO à `3876fce` : la dernière révision du fichier est `7039476`; son prédécesseur est `6867a2d`; le `previous_blob_sha256` attendu demeure `a7ad22af7cc6b21bc7c6f5b3d8ec08a929efbb4e044451087c5963f3013322c1`.
4. Payload d'une occurrence déjà enregistrée dont le hash diverge et dont le JSON est NFD : `REGISTRY_HISTORY_VIOLATION`, jamais deux codes et jamais `INVALID_OCCURRENCE_HISTORY`.
5. Nouvel input NFD : une ligne de rejet hashée, zéro allocation OCC/CYC/famille/groupe.
6. Supersession `reason_code=REPAIR_METADATA` pointant une décision `CORRECT_CAUSAL_PAYLOAD` : rejet déterministe.

## Vérifications Producteur exécutées

| Vérification | Résultat observé |
|---|---|
| parsing de `ORACLE_ADMISSIONS.json` par `python3 -m json.tool` | code 0 |
| parsing de `OPERATOR_SUPERSESSION_DECISIONS.json` par `python3 -m json.tool` | code 0 |
| dernière révision NO-GO pour `E=3876fce` | `70394762fc1f8fae7246d389ba3d1974ef98060b` |
| révision précédente depuis `7039476^1` | `6867a2db063321cd39636f87a741452396d93ca7` |
| SHA-256 du blob NO-GO à `6867a2d` | `a7ad22af7cc6b21bc7c6f5b3d8ec08a929efbb4e044451087c5963f3013322c1` |
| SHA-256 du registre de décisions vide | `246f867f77cfbe61fd392297925d4f498946eff28bcf3d66f62a6e22ed3c8209` |
| `git diff --check` | code 0 |

Ces vérifications établissent la cohérence syntaxique et le contre-exemple Git S3. Elles ne simulent pas un contrôleur absent et ne valent donc pas validation des mutants S1, S2 ou S4.

## Limites conservées

- Les schémas ne sont pas encore implémentés dans un contrôleur.
- `OPERATOR_SUPERSESSION_DECISIONS.json` et les admissions d'oracles sont vides.
- L'identité humaine derrière une décision reste une preuve procédurale externe.
- La protection distante ou l'archive Git signée manque toujours.
- P6 reste `BLOCKED_IMMUTABILITY`; P0 reste incomplet; aucun résultat scientifique ou financier n'est validé.
