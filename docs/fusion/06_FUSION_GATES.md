# Gates de fusion falsifiables

## Règle

Un gate est `PASS`, `FAIL`, `BLOCKED` ou `NON_TESTABLE`. `PASS` exige tous les artefacts et commandes. Une revue humaine ne remplace pas un test mécanique, et inversement.

Toute hypothèse suit en plus le [`PROTOCOL_CONTRADICTOIRE.md`](PROTOCOL_CONTRADICTOIRE.md) : branche dédiée, dossier probatoire, Critique indépendante et Contradictoire indépendante. Un double avis IA ne remplace aucune preuve exigée par le gate.

| Gate | Livrable | Critères PASS | Mutation devant échouer |
|---|---|---|---|
| P0 Baselines | hashes, versions, limites et provenance/licence des deux dépôts | aucune affirmation sans source; résultats reproduits ou `NON_REPRODUCED` | retirer une source/hash |
| P1 Domaine | événements, instruments, ledgers spot/short | oracles comptables exacts; seule l'interface `Clock` fournit le temps aux nouveaux modules canoniques | doubler frais/levier; injecter n'importe quelle source temporelle directe ou alias dans `domain/`/`replay/` |
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
- P1 : quatre fallbacks temporels legacy restent à caractériser puis purger ou adapter; ils sont hors périmètre de la mutation jusqu'à leur migration dans les modules canoniques;
- P2+ : interdits à la publication comme accomplis.

## Contrôle temporel P1

Un contrôle AST porte sur tous les fichiers Python de `paper_trading_codex/domain/` et `paper_trading_codex/replay/`. Il rejette les imports directs ou alias de `time` et `datetime`, ainsi que les appels identifiés à `now`, `utcnow`, `today`, `time`, `monotonic`, `perf_counter`, `gmtime` et `localtime`. La seule source temporelle autorisée est un objet satisfaisant le port `Clock`, reçu explicitement en dépendance.

Le test de mutation injecte successivement `datetime.now()`, `from datetime import datetime as dt; dt.now()`, `time.time()`, `time.monotonic()` et `datetime.now(timezone.utc)` dans un module canonique. Chaque mutation doit faire échouer le contrôle. Une nouvelle bibliothèque temporelle exige une modification préenregistrée de cette règle et un cas mutant correspondant.
