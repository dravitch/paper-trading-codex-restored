# Gates de fusion falsifiables

## Règle

Un gate est `PASS`, `FAIL`, `BLOCKED` ou `NON_TESTABLE`. `PASS` exige tous les artefacts et commandes. Une revue humaine ne remplace pas un test mécanique, et inversement.

Toute hypothèse suit en plus le [`PROTOCOL_CONTRADICTOIRE.md`](PROTOCOL_CONTRADICTOIRE.md) : branche dédiée, dossier probatoire, Critique indépendante et Contradictoire indépendante. Un double avis IA ne remplace aucune preuve exigée par le gate.

| Gate | Livrable | Critères PASS | Mutation devant échouer |
|---|---|---|---|
| P0 Baselines | hashes, versions, limites et provenance/licence des deux dépôts | aucune affirmation sans source; résultats reproduits ou `NON_REPRODUCED` | retirer une source/hash |
| P1 Domaine | événements, instruments, ledgers spot/short | oracles comptables exacts; horloge injectée | doubler frais/levier; réintroduire `now()` |
| P2 Replay | scheduler et journal canonique | bundle backtest = replay | permuter ordre TP/SL |
| P3 Stratégies | Grid/RSI/MA sans I/O | intentions sur tables connues; aucun accès provider/clock | changer seuil/signe; injecter un appel provider |
| P4 Providers | deux adaptateurs interchangeables | même flux canonique → même bundle | changer unité/timestamp |
| P5 Live | checkpoint + event log | reprise sans doublon; replay live identique | rejouer dernier event |
| P6 RiskMap | domaine, Pareto, stabilité | O1–O11 et paysages passent | supprimer un FAIL; changer clé/politique après run |
| P7 Publication | CI, wheel, docs, licence | Python 3.10–3.12 verts; termes normatifs sourcés | drift STATUS/docs; réintroduire « Sell & Hold = plafond » sans hypothèse |

## Ordre obligatoire

P0 → P1 → P2 → P3 → P4 → P5 → P6 → P7.

Le prototypage d'un gate ultérieur est autorisé, mais aucune intégration dans `main` ni revendication de statut ne l'est avant les gates précédents.

## Preuves par gate

- commande exacte et exit code;
- versions et environnement;
- JUnit/couverture lorsque applicable;
- manifeste et SHA-256;
- liste des skips/censures;
- résultat des mutations;
- décision Producteur;
- rapports Critique et Contradictoire indépendants;
- désaccords et réfutations non résolus.

## Blocages immédiats connus

- P0 : baseline distante Bitget non exécutée dans son environnement déclaré;
- P0 : licence du dépôt Bitget source non établie;
- P1 : contrats encore documentaires, pas de schémas exécutables;
- P2+ : interdits à la publication comme accomplis.
