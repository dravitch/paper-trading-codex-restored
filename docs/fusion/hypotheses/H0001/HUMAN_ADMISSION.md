# H0001 — Admission humaine des revues

## Décision

L'opérateur admet les deux rapports H0001 avec leur verdict
`ACCEPT_WITH_LIMITS`. Cette décision a été communiquée explicitement le
2026-08-28 après lecture des rapports et contrôle de leur séparation fonctionnelle.

| Champ | Valeur |
|---|---|
| paquet Producteur examiné | `df02849b004c4074bb44c59d59a02b76be29a915` |
| commit portant les deux rapports | `e4ff866d2a9689d9d50ca3c884a291236f9c2038` |
| Critique | `ACCEPT_WITH_LIMITS` |
| SHA-256 Critique admis | `eeacede7c285f851665071814e01b7b4f7763d44b3c8b817fab2d19d9390d97e` |
| Contradictoire | `ACCEPT_WITH_LIMITS` |
| SHA-256 Contradictoire admis | `74a8d61e14a5b5c231fc6175ab68d7e8bc99ea6bcf402ffe2d86bf185cbd717f` |
| séparation des revues | `PROCEDURAL / ROLE-SEPARATED` |
| indépendance statistique / IV&V | non revendiquée |
| décision H0001 | `VALIDATED_WITH_PUBLISHED_LIMITS` |
| effet sur P1 | `NOT_PASSED` |

## Motif de recevabilité

Les revues proviennent de deux sous-agents Codex distincts, chacun reparti du même paquet
gelé. Le premier verdict Contradictoire a été figé sans lecture ni réception du verdict
Critique. Chaque rapport contient des contrôles mécaniques propres. L'identité technique
du modèle n'étant pas exposée, elle reste `UNKNOWN`; aucune indépendance statistique ni
diversité de famille de modèles n'est inférée.

Cette provenance satisfait l'indépendance minimale du protocole comme séparation de rôle,
de contexte et de visibilité. Elle ne constitue pas une réplication externe.

## Limites admises et publiées

- A8 reste `OPEN_SPEC_NOTE × NON_BLOCKING × P1_GENERALIZATION` : la représentation
  générale des signes reste à trancher hors H0001.
- L'oracle et les revues établissent une indépendance logicielle et procédurale, pas une
  réplication externe ou statistiquement indépendante.
- Le scénario unique ne généralise pas le ledger à P1.
- Le HEAD enregistré par le runner ne prouve pas seul la propreté d'un worktree; les
  hashes, blobs et reproductions ferment ce risque pour le paquet admis uniquement.
- Les sept mutants prouvent les sensibilités ciblées, pas une mutation exhaustive du code.

Ces limites ne contaminent pas l'égalité comptable revendiquée par H0001. Elles restent
des sorties publiées; elles n'ouvrent pas une correction Producteur rétroactive.

## Portée de l'admission

H0001 est validée uniquement dans son domaine préenregistré et peut sortir de `IN_REVIEW`.
Cette admission ne déclare ni `P1 PASS`, ni fidélité générale à un exchange, ni aptitude
du ledger à couvrir d'autres scénarios. Elle n'autorise pas non plus H0002, P2 ou P6 dans
le cadre de cette décision.
