# Rapport Contradictoire — Delta 8335ab0 (réponse Producteur R1–R8)

## Objet examiné

Commit Producteur `8335ab0` « docs: integrate residual contradictory findings », branche `correction/reconcile-l1-l12`, parent `273046a`. Portée : réponse aux limites résiduelles R1–R8 de `CONTRADICTOIRE_DELTA_09653E2.md`, conformément à `docs/fusion/REVIEW_REQUEST_RESIDUAL_R1_R8.md`.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `8335ab02722a4687aa79b1e3dbebdca6c0c24d73` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité

Mes artefacts corrigés ont été commités tels quels par le Producteur : `44b83d7c…` (rapport 09653e2), `9778cb77…` (heartbit), `40b2ebea…` (addendum) — hashes identiques à l'addendum, corrections O8 et `data_fetcher.py:27` présentes, arbre de travail propre.

## Fichiers examinés (delta 8335ab0)

- `CONTROLLED_MERGER_FEASIBILITY.md` (§12.1, cycle)
- `docs/fusion/05_RISKMAP_ORACLES.md` (O4 table, O7 clé, O9 ingestion, statuts)
- `docs/fusion/06_FUSION_GATES.md` (P1)
- `docs/fusion/CANONICAL_CONTRACT_RFCS.md` (RFC-008)
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md`, `NO_GO_REGISTER.md`, `README.md`, `REV05.md`

## Réponses aux sept questions de réfutation

| Q | Question | Verdict |
|---|---|---|
| Q1 | O7 conserve-t-il tous objectifs/contraintes sans confondre descriptif et axe de dominance ? | **Satisfaite** — `objective_vector`/`constraint_vector` par expérience, métriques descriptives exclues de la dominance mais conservées dans le `RiskPoint`. Réserve F4 (conflit sur clé incomplète) |
| Q2 | Mêmes référentiel/scénario/paramètres mais résultats différents → conflit, pas doublon ? | **Satisfaite** — règle `REPRODUCIBILITY_CONFLICT`, carte non validable; seuls les doublons de la clé complète sont dédupliqués. Réserve F4 |
| Q3 | Dérivation de `reference_hash` suffisante ? | **Satisfaite** — `SHA-256(canonical_json(ReferenceSpec))`, clés triées, UTF-8 sans whitespace, politique numérique. Exiger l'unicité des identifiants de métriques pour l'ordre canonique |
| Q4 | Les cinq statuts O4 découlent-ils de la règle fixée ? | **Non — F1** : points 1 et 2 satisfont la définition `ROBUST` mais sont étiquetés `STABLE_REGION_MEMBER` (terme non défini). Contradiction interne |
| Q5 | O9 conserve-t-il la preuve d'un non-fini sans sérialiser NaN/infini ? | **Satisfaite** — détection à l'entrée, anomalie finie `{run_id, field, reason, observed_token="+inf"}`, `status="ERROR"`, jamais la valeur flottante dans le JSON |
| Q6 | Le périmètre P1 laisse-t-il une voie de contournement ? | **Oui — F2** : la mutation ne cible que `datetime.now()` littéral dans `domain/`/`replay/`; alias, `time.time()`, `time.monotonic()`, `datetime.now(tz)` contournent |
| Q7 | Cycle + registre NO-GO empêchent-ils une remise à zéro cosmétique ? | **Partiellement** — cause ID stable et contestation Contradictoire; mais l'identité causale est en prose, sans clé mécanique. Réserve F3 |

## Couverture des mutations minimales

| Mutation | Couverte ? |
|---|---|
| retirer un objectif mandaté de `objective_vector` | ✓ (vecteurs = tous les objectifs préenregistrés) |
| dédupliquer deux runs aux résultats divergents | ✓ (conflit sur `(reference_hash, scenario_id, canonical_parameters)`) |
| changer un champ du `ReferenceSpec` sans modifier `reference_hash` | ✓ (hash sur l'objet canonique complet) |
| qualifier le point 3 O4 de robuste | ✓ (attendu figé `FRAGILE`) |
| sérialiser directement `float("inf")` | ✓ (détection pré-sérialisation + anomalie finie) |
| appeler une horloge murale depuis `domain/` par un alias | **✗ — F2** |
| renommer une cause NO-GO sans changer sa description causale | **◐ — F3** (gouvernance, pas mécanique) |

## Constats

### F1 — O4 : la table des cinq statuts contredit la règle (bloquant P6)

Règle figée : « Un point est `ROBUST` seulement si lui-même et tous ses voisins existants sont admissibles. » Recalcul :
- point 1 (`G=2,D=2`) : admissible; voisin unique 2 admissible → **ROBUST** selon la règle; table : `STABLE_REGION_MEMBER`;
- point 2 (`G=3,D=2`) : admissible; voisins 1 et 3 admissibles → **ROBUST** selon la règle; table : `STABLE_REGION_MEMBER`;
- points 3, 4, 5 conformes (`FRAGILE`, `FAIL_CONSTRAINT`).

Contre-exemple de la mutation « qualifier le point 3 de robuste » : la mutation est bien rejetée, mais les statuts 1 et 2 sont dérivés d'un critère implicite non déclaré (vraisemblablement « non dominé »), et `STABLE_REGION_MEMBER` n'est défini nulle part. **Effet : O4 est `NON_TESTABLE`** : deux lectures incompatibles de la même règle interdisent un PASS P6. Action : soit amender la règle (ex. ROBUST = Pareto + voisinage admissible, avec `STABLE_REGION_MEMBER` défini), soit corriger la table (1 et 2 = `ROBUST`), avant toute implémentation.

### F2 — P1 : mutation temporelle contournable par alias (bloquant P1)

`06_FUSION_GATES.md` P1 : « appeler `datetime.now()` dans `paper_trading_codex/domain/` ou `paper_trading_codex/replay/` ». Un module canonique peut lire l'horloge murale sans ce littéral : `from datetime import datetime as dt; dt.now()`, `time.time()`, `time.monotonic()`, `time.gmtime()`, `datetime.now(timezone.utc)`. **Effet : P1 peut passer avec une horloge murale dans le domaine.** Action : élargir la mutation à toute source temporelle (scan statique de `datetime.now/utcnow/timestamp`, `time.time/monotonic/gmtime/localtime`) ou restriction d'imports dans les modules canoniques, le legacy restant hors périmètre comme déclaré.

### F3 — NO-GO : identité de cause en prose (mineur)

`NO_GO_REGISTER` interdit la remise à zéro par changement d'étiquette, mais l'identité causale repose sur la « description causale » et le jugement du Contradictoire. Action recommandée : clé de cause canonique dérivée de preuves mécaniques (gate + mutation/invariant concernés), rendant un re-étiquetage détectable sans appréciation.

### F4 — O7 : conflit de reproductibilité sur clé incomplète (mineur)

Le conflit compare `(reference_hash, scenario_id, canonical_parameters)` + vecteurs de résultat. Une divergence limitée aux métriques descriptives (mêmes vecteurs objectifs/contraintes) serait silencieusement dédupliquée alors que, dans un moteur déterministe, elle est une violation de reproductibilité. Action : déclarer le conflit sur toute différence du `RiskPoint` complet, ou justifier le choix de la clé.

### F5 — Statuts des oracles : O4 modifié mais laissé `REVIEWED` (livre)

Le delta ajoute la table O4 mais ne met à jour que le statut d'O7 (`SUPERSEDED_PENDING_REVIEW`), en contradiction avec sa propre règle : « Une modification de l'attendu, de la clé ou du domaine remet uniquement l'oracle concerné à `PENDING_REVIEW`. » La table modifie les attendus d'O4 → O4 doit être `PENDING_REVIEW` (il l'est en pratique par F1).

## Verdict

**ACCEPT_WITH_LIMITS**

La réponse Producteur traite correctement R2, R5, R7, R8 et la majeure partie de R1/R3/R6. Deux limites sont bloquantes pour les gates concernés, à intégrer avant P1/P6 :

- **F1 + F5** : O4 est `NON_TESTABLE` tant que la règle et la table ne sont pas réconciliées; son statut doit repasser `PENDING_REVIEW`;
- **F2** : la mutation P1 doit couvrir toute source d'horloge murale, pas seulement `datetime.now()`.

F3 et F4 sont des exigences de précision à intégrer avec les mêmes documents. Aucun gate n'est franchi par ce delta; O4 et O7 demeurent non validés pour P6. Ce verdict ne réévalue pas de performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
