# Progression de la fusion contrôlée

## Situation au 2026-08-29

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
| P1 | domaine canonique et ledgers | H0001 et H0002 validées avec limites publiées; premier paquet H0003 rejeté et en correction; gate non franchi |
| P2 | replay unique déterministe | non commencé |
| P3 | portage contrôlé des stratégies | non commencé |
| P4 | adaptateurs fournisseurs | non commencé |
| P5 | persistance et éventuel live | non commencé |
| P6 | RiskMap et chaîne probatoire | spécification avancée; contrôleur et preuves externes absents; `BLOCKED_IMMUTABILITY` |
| P7 | publication | bloqué |

Aucun gate métier n'est franchi. H0001 est validée avec limites publiées dans son unique scénario comptable short P0; elle ne constitue pas P1. P0 est `CLOSED_WITH_DEBT` (commit de clôture `0a11672`), les deux baselines ont été exécutées séparément : le dépôt restauré rapporte 68 tests, 87,07 % de couverture et Ruff sans erreur (exécuté et vérifié lors de l'audit P0 sous Nix) ; la baseline Bitget rapporte 9 tests hors réseau et 38 % sur le seul paquet `paper_trading` (exécuté sur VM NixOS, reproduit par les revues Critique et Contradictoire séparées et aveugles au premier verdict, admises au commit `804002f`, non rejoué lors de l'audit P0). L'immuabilité distante a été rescopée vers P6/P7 (`P0_CONTRACT_SCOPE_DECISION.md`) : elle protège la valeur probatoire, pas l'exécutabilité. Les dettes D01 (immuabilité) et D02 (oracles O2/O4/O7) restent ouvertes pour P6/P7. Les cycles achevés ont consolidé la spécification et son protocole probatoire ; ils ne constituent ni une validation scientifique du moteur futur, ni une preuve de fidélité au marché.

## Jalon courant

La réponse Producteur Q1–Q4 est ancrée au commit `3876fce`. La première tentative d'admission de `REV11` (`a837cea`) est invalide : l'opérateur avait admis les hashes intermédiaires R1–R4, alors que le commit contenait les blobs finaux S1–S4. L'invalidation est documentée par `3415cb3`; aucune admission REV11 invalide n'a été ajoutée au registre.

La reprise contrôlée `REV11bis`, scientifiquement identique à la version finale S1–S4, a reçu un addendum Contradictoire indépendant et l'admission explicite de l'opérateur. Elle est ancrée au commit `102ce6a`, puis indexée séparément au commit `d8bc959`. Son verdict est `ACCEPT_WITH_LIMITS`. La réponse Producteur S1–S4 (`REV12.md`) a été commitée au `777fc23` et la revue Contradictoire (`CONTRADICTOIRE_DELTA_REV12.md`) a reçu `ACCEPT_WITH_LIMITS` avec trois réserves T1 (manifeste de run), T2 (merge transparent divergent), T3 (unicité de consommation décision). Le cycle S1–S4 est clos. Leur réponse REV13 et leur future revue restent sur `work/continuation-2026-08-28`, scope P6, sans bloquer H0001/P1.

H0001 part du handoff post-P0 `7c322a8`. L'hypothèse et l'oracle ont précédé le code. Le
Producteur observe une égalité rationnelle exacte sur six états, une concordance séparée
avec la projection P0, sept mutants rejetés, 80 tests globaux et 89,53 % de couverture. Le
dossier Producteur actualisé est figé au commit `f49d0c1`. Les rapports Critique et
Contradictoire, tous deux `ACCEPT_WITH_LIMITS`, sont ancrés au commit `e4ff866` puis admis
humainement avec une indépendance qualifiée `PROCEDURAL / ROLE-SEPARATED`. H0001 est
`VALIDATED_WITH_PUBLISHED_LIMITS`; ce résultat ne vaut pas `P1 PASS`.

H0002 descend de l'admission H0001 sans fusion intermédiaire. Sa famille de cinq scénarios
et ses attendus rationnels ont été préenregistrés au commit `1d63024`. Le ledger H0001,
inchangé (`b917433d…f6bc`), a passé directement le premier run `7/7`; après ajout des
falsifications, le paquet Producteur rapporte `16/16`, cinq corruptions comptables et trois
dérives de plan rejetées, puis `96/96` tests globaux et 89,53 % de couverture. Le résultat
avait le statut Producteur `PASS_PENDING_INDEPENDENT_REVIEW`. Les deux revues séparées ont
conclu `ACCEPT_WITH_LIMITS` et sont ancrées au commit `5658a8b`, puis admises humainement.
H0002 est `VALIDATED_WITH_PUBLISHED_LIMITS`; elle n'est pas une preuve de `P1 PASS`.

## État des branches

La roadmap est volontairement séparée entre la dette P6 et l'hypothèse P1 :

| Branche | Rôle | État au 2026-08-29 |
|---|---|---|
| `main` | baseline publiable | aucune fusion contrôlée reçue |
| `fusion/controlled-merger` | destination d'intégration | attend la fermeture des gates requis |
| `correction/reconcile-l1-l12` | consolidation documentaire achevée | cycle S1–S4 cloturé; dettes T1/T2/T3 ouvertes pour contrôleur futur |
| `work/continuation-2026-08-28` | dette documentaire P6 | REV13/T1–T3 figés; revue différée avant P6 |
| `hypothesis/H0001-canonical-ledger-equivalence` | première hypothèse P1 | H0001 validée avec limites publiées; non fusionnée; P1 non passé |
| `hypothesis/H0002-short-ledger-generalization` | généralisation short P1 | validée avec limites publiées; non fusionnée; P1 non passé |
| `work/p1-capability-gap` | diagnostic documentaire P1 | diagnostic achevé au `56e770a`; H0003 en descend sans fusion |
| `hypothesis/H0003-canonical-contract-foundation` | socle canonique P1 | paquet `44893b0` rejeté par les deux revues; `TESTING / CORRECTION_REQUIRED`; P1 non passé |

`origin` est un pointeur symbolique vers `origin/main`, pas une branche de travail. Le dossier ignoré `docs/deepsearch/` appartient à un autre périmètre et n'a pas été modifié.

## Prochaine étape contrôlée

1. corriger strictement R1–R3 sur la branche H0003 sans changer B1–B8/B5a;
2. transformer les contre-exemples publiés en régressions permanentes et conserver l'ancien résultat rejeté;
3. produire et geler un nouveau paquet complet, puis le transmettre à deux nouvelles revues ayant les anciens `REJECT` comme contexte;
4. conserver la note `unicodedata` pour le futur enforcement P1 sans la faire contaminer H0003;
5. ne créer ni H0004 ni hypothèse ledger spot avant une nouvelle décision humaine sur H0003.

Le diagnostic courant est publié dans [`docs/fusion/P1_CAPABILITY_GAP.md`](docs/fusion/P1_CAPABILITY_GAP.md). Il classe le noyau short full-close `DEMONSTRATED_LIMITED`, mais constate `InstrumentSpec`, événements canoniques, ledger spot, `Clock`, contrôle temporel et preuve intégrée P1 absents. La cause synthétique est `MISSING_EXECUTABLE_CANONICAL_CONTRACTS_AND_SPOT_LEDGER`.

Une revue documentaire ne peut jamais attribuer `PASS` à P1 ou P6. La fusion vers `fusion/controlled-merger`, puis vers `main`, reste interdite tant que les gates correspondants ne sont pas démontrés.
