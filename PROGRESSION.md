# Progression de la fusion contrôlée

## Situation au 2026-08-19

Les dépôts `paper-trading-codex-restored` et `bitget-paper-trading` ont été comparés. La fusion directe a été rejetée au profit d'une plateforme de paper trading indépendante des fournisseurs, fondée sur des contrats canoniques, un replay déterministe, des oracles indépendants et une cartographie du risque sans promesse de performance.

La documentation définit le modèle comptable, les événements, le temps injecté, les manifestes reproductibles, les métriques, la `RiskMap`, la frontière de Pareto, la provenance des composants et les conditions de NO-GO. Le Protocole Contradictoire impose une branche par hypothèse, des preuves figées, deux lectures critiques et une admission humaine.

## Cycles de consolidation documentaire

```text
L1–L12 → R1–R8 → F1–F5 → G1–G4 → H1–H5 → J1–J5 → K1–K5 → L1–L4 → M1–M4 → N1–N4 → O1–O4 → P1–P4 → Q1–Q4 → S1–S4
```

Chaque cycle sépare l'admission du rapport, la réponse Producteur et la nouvelle demande de réfutation. Les rapports admis et leurs SHA-256 sont indexés dans `docs/fusion/REVIEW_ADMISSION_REGISTRY.md`.

## État de la roadmap

| Gate | Objet | État |
|---|---|---|
| P0 | baselines | `CLOSED_WITH_DEBT` — rescoping immuabilité vers P6/P7; 68/68 restored, 9/9 bitget, revues admises; dette : preuve d'immuabilité distante et oracles O2/O4/O7 (scope P6/P7) |
| P1 | domaine canonique et ledgers | non commencé |
| P2 | replay unique déterministe | non commencé |
| P3 | portage contrôlé des stratégies | non commencé |
| P4 | adaptateurs fournisseurs | non commencé |
| P5 | persistance et éventuel live | non commencé |
| P6 | RiskMap et chaîne probatoire | spécification avancée; contrôleur et preuves externes absents; `BLOCKED_IMMUTABILITY` |
| P7 | publication | bloqué |

Aucun gate et aucune hypothèse métier ne sont validés. Le code de fusion n'est pas commencé. P0 est `CLOSED_WITH_DEBT` (commit de clôture `0a11672`), les deux baselines ont été exécutées séparément : le dépôt restauré rapporte 68 tests, 87,07 % de couverture et Ruff sans erreur (exécuté et vérifié lors de l'audit P0 sous Nix) ; la baseline Bitget rapporte 9 tests hors réseau et 38 % sur le seul paquet `paper_trading` (exécuté sur VM NixOS, reproduit par les revues Critique et Contradictoire séparées et aveugles au premier verdict, admises au commit `804002f`, non rejoué lors de l'audit P0). L'immuabilité distante a été rescopée vers P6/P7 (`P0_CONTRACT_SCOPE_DECISION.md`) : elle protège la valeur probatoire, pas l'exécutabilité. Les dettes D01 (immuabilité) et D02 (oracles O2/O4/O7) restent ouvertes pour P6/P7. Les cycles achevés ont consolidé la spécification et son protocole probatoire ; ils ne constituent ni une validation scientifique du moteur futur, ni une preuve de fidélité au marché.

## Jalon courant

La réponse Producteur Q1–Q4 est ancrée au commit `3876fce`. La première tentative d'admission de `REV11` (`a837cea`) est invalide : l'opérateur avait admis les hashes intermédiaires R1–R4, alors que le commit contenait les blobs finaux S1–S4. L'invalidation est documentée par `3415cb3`; aucune admission REV11 invalide n'a été ajoutée au registre.

La reprise contrôlée `REV11bis`, scientifiquement identique à la version finale S1–S4, a reçu un addendum Contradictoire indépendant et l'admission explicite de l'opérateur. Elle est ancrée au commit `102ce6a`, puis indexée séparément au commit `d8bc959`. Son verdict est `ACCEPT_WITH_LIMITS`. La réponse Producteur S1–S4 (`REV12.md`) a été commitée au `777fc23` et la revue Contradictoire (`CONTRADICTOIRE_DELTA_REV12.md`) a reçu `ACCEPT_WITH_LIMITS` avec trois réserves T1 (manifeste de run), T2 (merge transparent divergent), T3 (unicité de consommation décision). Le cycle S1–S4 est maintenant cloturé. Aucun gate n'est franchi et P6 reste `BLOCKED_IMMUTABILITY`.

## État des branches

Trois branches réelles existent localement et sur le dépôt distant :

| Branche | Rôle | État au 2026-08-07 |
|---|---|---|
| `main` | baseline publiable | aucune fusion contrôlée reçue |
| `fusion/controlled-merger` | destination d'intégration | attend la fermeture des gates requis |
| `correction/reconcile-l1-l12` | consolidation documentaire achevée | cycle S1–S4 cloturé; dettes T1/T2/T3 ouvertes pour contrôleur futur |

`origin` est un pointeur symbolique vers `origin/main`, pas une quatrième branche. Le dossier non suivi `docs/deepsearch/` appartient à un autre périmètre et n'a pas été modifié.

## Prochaine étape contrôlée

1. intégrer explicitement les limites S1–S4 dans la spécification ou les classer comme exigences de l'implémentation future;
2. ouvrir une branche `hypothesis/HNNN-*` pour la première hypothèse exécutable;
3. implémenter tests, oracles et manifestes avant toute revendication de `PASS`;
4. obtenir séparément les verdicts Critique et Contradictoire, puis l'admission humaine.

Une revue documentaire ne peut jamais attribuer `PASS` à P1 ou P6. La fusion vers `fusion/controlled-merger`, puis vers `main`, reste interdite tant que les gates correspondants ne sont pas démontrés.
