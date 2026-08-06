# Rapport Contradictoire — Delta 4225bc5 (réponse Producteur F1–F5)

## Objet examiné

Commit Producteur `4225bc5` « docs: resolve residual findings F1-F5 », branche `correction/reconcile-l1-l12`, parent probatoire `a1e9892`. Portée : réponse aux constats F1–F5 de `CONTRADICTOIRE_DELTA_8335AB0.md`, conformément à `docs/fusion/REVIEW_REQUEST_F1_F5.md`.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `4225bc54f5db0e754a40e478d4324cbe48a32920` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict (`REVIEW_INTAKE_CRITIQUE.md` non consulté) |

## Vérifications préalables d'intégrité

- L'admission de mes artefacts `8335ab0` est réelle : commit `a1e9892` « docs: admit contradictory review of delta 8335ab0 », et `git ls-files` confirme `CONTRADICTOIRE_DELTA_8335AB0.md` et `HEARTBEAT_CONTRADICTOIRE_DELTA_8335AB0.md` suivis.
- Le delta ne modifie aucun code ; il est purement documentaire. Réexécution Nix sans objet.

## Fichiers examinés (delta 4225bc5)

- `docs/fusion/05_RISKMAP_ORACLES.md` (table O4, clé de reproductibilité O1, statuts des oracles)
- `docs/fusion/06_FUSION_GATES.md` (ligne P1, contrôle temporel P1)
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md` (constats F1–F5)
- `docs/fusion/NO_GO_REGISTER.md` (clé causale)
- `REV05.md`

## Réponses aux six vérifications du mandat

| # | Vérification | Verdict |
|---|---|---|
| 1 | Recalculer O4 et confirmer `ROBUST`, `ROBUST`, `FRAGILE`, `FAIL_CONSTRAINT`, `FAIL_CONSTRAINT` | **Confirmé.** Admissibilité (rendement `>= 0`, drawdown `<= 10`, non liquidé) : P1 `(2,2)` oui, P2 `(3,2)` oui, P3 `(20,2)` oui, P4 `(−8,20)` non (viole les deux seuils), P5 `(−10,30)` non. Voisins (rayon 1, bornes tronquées) : P1→{2}, P2→{1,3}, P3→{2,4}, P4→{3,5}, P5→{4}. P1 et P2 et tous leurs voisins admissibles → `ROBUST`; P3 a P4 non admissible → `PARETO_DESCRIPTIVE`+`FRAGILE`; P4, P5 non admissibles → `FAIL_CONSTRAINT`. Table conforme à la règle |
| 2 | O4 et O7 tous deux `SUPERSEDED_PENDING_REVIEW` | **Confirmé sur la table** (O4 « après correction F1/F5 », O7 « après intégration R1/R2 »). Réserve **G3** : littéral non défini dans le vocabulaire |
| 3 | Deux `RiskPoint` de même clé mais métriques descriptives différentes → `REPRODUCIBILITY_CONFLICT` | **Satisfaite.** La clé de déduplication est désormais la projection sémantique complète (objectifs, contraintes, métriques descriptives, statut, anomalies, hashes de preuve), excluant seulement `point_id`, ordre d'entrée, chemin machine et timestamp. Deux `RiskPoint` `(R, S, θ)` aux objectifs identiques mais `descriptive_metrics.sharpe = 1.5` vs `1.6` → projections différentes → jamais dédupliqués, `REPRODUCIBILITY_CONFLICT`, carte non validable. Cohérent avec O1 (F = doublon sémantique de B dans l'ensemble Pareto, mécanisme distinct de la dédup de carte) et avec l'invariance de permutation O7 |
| 4 | Les cinq mutations temporelles P1 échouent-elles ; alias non couvert ? | **Partiellement.** Les cinq mutations nommées échouent (imports de `time`/`datetime` rejetés, alias `dt` rejeté à l'import, `now`/`time`/`monotonic` dans la liste d'appels). **Mais un alias non couvert subsiste — G1** |
| 5 | Deux cycles aux preuves/descriptions différentes conservent la même `cause_key` | **Satisfaite.** `cause_key = SHA-256(canonical_json({gate_id, no_go_criterion_id, violated_invariant_id, failing_mutation_id}))`; descriptions, révisions et hashes de preuves enregistrés par cycle mais exclus de la clé → le compteur n'est pas remis à zéro |
| 6 | Deux causes réellement différentes partagent-elles une clé ? | **Oui — G2** |

## Constats

### G1 — Contrôle temporel P1 : voies non couvertes par la règle AST (pré-implantation)

Les cinq mutations nommées (`datetime.now()`, `from datetime import datetime as dt; dt.now()`, `time.time()`, `time.monotonic()`, `datetime.now(timezone.utc)`) échouent bien. Mais la règle de `06_FUSION_GATES.md` ne couvre pas :

```python
from datetime import date
date.fromtimestamp(ts)               # fromtimestamp absent de la liste d'appels;
                                     # l'import du nom date n'est pas un import "de datetime"
__import__("time").time_ns()         # aucun import statique; time_ns absent de la liste
import importlib
importlib.import_module("time").time_ns()
os.stat(path).st_mtime               # temps de fichier via os, ni import interdit ni appel listé
```

L'échappatoire « une nouvelle bibliothèque temporelle exige une modification préenregistrée » ne couvre pas ces cas : ils n'introduisent aucune bibliothèque, ils empruntent `time`/`datetime` par dérivation d'attribut, import dynamique ou métadonnées de fichiers. En outre, la sémantique du matcher d'import est ambiguë : « imports directs ou alias de `time` et `datetime` » se lit par nom lié (comme ci-dessus) ou par module source ; la distinction change l'issue pour `from datetime import date`. **Effet : si le contrôle est implémenté à l'identique de la règle, P1 peut passer avec une source temporelle réelle dans `domain/`/`replay/`.** Action avant implémentation : préciser le matcher (tout import issu des modules `time`/`datetime`, quelle que soit l'étiquette liée), ajouter ces mutants (`fromtimestamp`, `time_ns`, `st_mtime`, import dynamique) à la liste de mutation, ou bannir `__import__`/`importlib` dans les modules canoniques.

### G2 — NO-GO : collision de `cause_key` entre causes réellement distinctes

`cause_key` ne contient aucune signature de défaillance (locus, symbole, hash de traceback normalisé). Contre-exemple : gate P1, critère §12.1, invariant « oracles comptables exacts », mutation « doubler frais/levier ». Deux défauts indépendants — un dans l'application des frais du ledger spot, un dans la gestion de la taille du ledger short — font chacun échouer le même invariant sous la même mutation → clé identique, causes distinctes. La règle de scission par décision opérateur ne couvre que la « véritable redéfinition de l'invariant ou de la mutation », pas deux défauts sous le même invariant. **Effet : le registre confond les causes et le compteur de cycles peut enfler artificiellement sur une cause composite.** Action : ajouter un `failure_signature` optionnel (hash du traceback ou symbole fautif normalisé) à la clé lorsqu'il discrimine, ou documenter explicitement la conflation et la procédure de scission opérateur dans ce cas.

### G3 — Statut d'oracle `SUPERSEDED_PENDING_REVIEW` : littéral non défini (documentaire)

La table de `05_RISKMAP_ORACLES.md` utilise `SUPERSEDED_PENDING_REVIEW` pour O4 et O7, mais la règle du même fichier ne connaît que `PENDING_REVIEW` (« remet uniquement l'oracle concerné à `PENDING_REVIEW` »), et `REV05.md` parle d'« O4 et O7 restent PENDING_REVIEW » en prose. Le vocabulaire des statuts de revue d'oracle (`REVIEWED_*`, `PENDING_REVIEW`, `SUPERSEDED_PENDING_REVIEW`) n'est défini nulle part. **Effet : lecture incohérente possible — la table et la règle peuvent diverger sans violation détectable.** Action : définir le vocabulaire et la transition (notamment la relation `SUPERSEDED_PENDING_REVIEW` vs `PENDING_REVIEW`).

### G4 — Registre : note d'admission périmée (documentaire)

`LIMIT_RESOLUTION_REGISTER.md` : « Les artefacts source `CONTRADICTOIRE_DELTA_8335AB0.md` et son heartbeat restent non suivis jusqu'à validation explicite de leur admission par l'opérateur. » Cette affirmation est fausse à `HEAD` : `a1e9892` « admit contradictory review of delta 8335ab0 » a déjà validé l'admission et les deux fichiers sont suivis (`git ls-files`). **Effet : le registre contredit l'historique git.** Action : corriger ou supprimer la note.

## Verdict

**ACCEPT_WITH_LIMITS**

Les vérifications 1, 2, 3 et 5 sont satisfaites ; O4 est réconcilié avec sa règle (F1 résolu), la clé de reproductibilité couvre le `RiskPoint` complet (F4 résolu), la clé causale est mécanique (F3 résolu), les cinq mutations nommées sont couvertes (partie de F2 résolue). O4 et O7 restent bien `PENDING_REVIEW`/`SUPERSEDED_PENDING_REVIEW` et aucun gate ne peut devenir `PASS`.

Limites à intégrer avant la fermeture de la spécification :

- **G1** (contrôle temporel P1) : matcher d'import à préciser et mutants `fromtimestamp`/`time_ns`/`st_mtime`/import dynamique à préenregistrer ;
- **G2** (registre NO-GO) : signature de défaillance ou procédure de scission pour les causes distinctes sous le même invariant ;
- **G3**, **G4** (documentaires) : définir le vocabulaire des statuts d'oracle ; corriger la note d'admission périmée.

Ce verdict ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*` ; les contrôles exécutables P1/P6 restent à implémenter.
