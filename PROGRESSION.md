# Progression de la fusion contrôlée

## Situation au 2026-08-06

Les dépôts `paper-trading-codex-restored` et `bitget-paper-trading` ont été comparés. La fusion directe a été rejetée au profit d'une plateforme de paper trading indépendante des fournisseurs, fondée sur des contrats canoniques, un replay déterministe, des oracles indépendants et une cartographie du risque sans promesse de performance.

La documentation définit le modèle comptable, les événements, le temps injecté, les manifestes reproductibles, les métriques, la `RiskMap`, la frontière de Pareto, la provenance des composants et les conditions de NO-GO. Le Protocole Contradictoire impose une branche par hypothèse, des preuves figées, deux lectures critiques et une admission humaine.

## Cycles de consolidation

```text
L1–L12 → R1–R8 → F1–F5 → G1–G4 → H1–H5 → J1–J5 → K1–K5 → L1–L4
```

Chaque cycle sépare l'admission du rapport, la réponse Producteur et la nouvelle demande de réfutation. Les rapports admis et leurs SHA-256 sont indexés dans `docs/fusion/REVIEW_ADMISSION_REGISTRY.md`.

## État de la roadmap

| Gate | Objet | État |
|---|---|---|
| P0 | baselines immuables | préparation |
| P1 | domaine canonique et ledgers | non commencé |
| P2 | replay unique déterministe | non commencé |
| P3 | portage contrôlé des stratégies | non commencé |
| P4 | adaptateurs fournisseurs | non commencé |
| P5 | persistance et éventuel live | non commencé |
| P6 | RiskMap | spécification avancée, code absent |
| P7 | publication | bloqué |

Aucun gate et aucune hypothèse métier ne sont validés. Le code de fusion n'est pas commencé. La baseline du dépôt restauré a été reproduite, mais celle du dépôt Bitget reste une preuve séparée ouverte.

## Jalon courant

La reprise Contradictoire `REV09bis` visant `6867a2d` a été admise au commit `4f281b7`, puis indexée au commit `bff1dcd`; `REV09` reste `SUPERSEDED_PROCEDURAL`. Le travail Producteur courant porte sur P1–P4 : grammaire des admissions d'oracles, vecteurs Unicode négatifs, adjacence du registre et schéma machine de supersession. La preuve externe de protection de l'historique reste ouverte avant P6.

Après revue de ce delta, la prochaine étape est de terminer P0 puis d'ouvrir la première branche d'hypothèse exécutable. Une revue documentaire ne peut jamais attribuer `PASS` à P1 ou P6.
