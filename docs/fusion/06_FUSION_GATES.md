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
| P6 RiskMap | domaine, Pareto, stabilité | O1–O11 et paysages passent; O2/O4/O7 ont une preuve de revue vérifiée et sont `REVIEWED_ACCEPT` ou `REVIEWED_ACCEPT_WITH_LIMITS` sur leur révision courante | supprimer un FAIL; changer clé/politique après run; modifier un statut sans rapport concordant |
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

Le contrôle analyse l'AST de tous les fichiers Python sous `paper_trading_codex/domain/` et `paper_trading_codex/replay/`. Il est conservateur : une provenance temporelle impossible à résoudre statiquement est rejetée, sauf exemption nominative préenregistrée.

Il construit une table des symboles par module et propage les alias simples jusqu'au point fixe (`x = y`, `x = y.z`, import aliasé). Le matcher porte sur le module source, jamais seulement sur le nom lié. Toute forme `import time`, `import time as t`, `from time import X as Y`, `import datetime` ou `from datetime import X as Y` est donc interdite, y compris `date`, `datetime` et `timezone`.

Sont aussi interdits :

1. imports dynamiques par `__import__`, `importlib.import_module` ou alias résolu; un argument non littéral ou non résolu est rejeté;
2. appels directs ou aliasés provenant de `time`/`datetime` : `now`, `utcnow`, `today`, `time`, `time_ns`, `monotonic`, `monotonic_ns`, `perf_counter`, `perf_counter_ns`, `process_time`, `process_time_ns`, `thread_time`, `thread_time_ns`, `gmtime`, `localtime`, `fromtimestamp`, `utcfromtimestamp`;
3. lectures de temps de fichier issues de `os.stat`, `os.fstat`, `os.lstat`, `Path.stat` ou `Path.lstat`, notamment `st_atime`, `st_atime_ns`, `st_ctime`, `st_ctime_ns`, `st_mtime`, `st_mtime_ns`. La provenance suit les affectations simples; ambiguïté, réflexion ou réaffectation complexe = rejet.

La seule origine temporelle admise est une dépendance explicite satisfaisant le port `Clock`, visible dans la signature. Constructeur implicite, singleton, défaut temporel et service locator sont interdits. Les implémentations système de `Clock` vivent hors `domain/` et `replay/`; les implémentations de replay sont déterministes et testées. Une exemption est une liste fermée `{fichier, symbole qualifié, justification, échéance}` et bloque le gate jusqu'à revue.

Le port importable et ses types sont définis par [`CLOCK_CONTRACT.md`](CLOCK_CONTRACT.md). Son module interne `paper_trading_codex.domain.clock` appartient au graphe transitif autorisé et ne contient lui-même aucune source temporelle.

Le test injecte au minimum : `datetime.now()`, alias `dt.now()`, `time.time()`, `time.monotonic()`, `datetime.now(timezone.utc)`, `date.fromtimestamp(ts)`, `__import__("time").time_ns()`, `importlib.import_module("time").time_ns()`, `os.stat(path).st_mtime`, `clock_fn = time.time; clock_fn()` et `stat = os.stat(path); stat.st_mtime`. Il injecte aussi les mutants du contrat : construction implicite d'un `Clock` système comme valeur par défaut et déplacement de `SystemClock` sous `domain/` puis `replay/`. Chaque mutant doit échouer avec fichier, ligne et règle. Une nouvelle primitive, bibliothèque ou exemption exige une modification préenregistrée et un mutant correspondant.

Limite déclarée : l'AST intraprocédural ne prouve pas les flux à travers conteneurs, closures, réflexion ou appels intermodules. Réflexion et imports non allowlistés sont donc interdits dans ces répertoires jusqu'à disponibilité d'une analyse interprocédurale. Cette règle bannit également les conversions `datetime` déterministes; un futur adaptateur pur exigera sa propre RFC et ses mutants.

### Allowlist d'import P1 — version 1

Imports externes autorisés dans `domain/` et `replay/` : `__future__`, `collections`, `collections.abc`, `dataclasses`, `decimal`, `enum`, `fractions`, `hashlib`, `json`, `math`, `operator`, `statistics`, `typing`. Les imports internes sous `paper_trading_codex.domain` et `paper_trading_codex.replay` sont autorisés seulement si leur graphe transitif passe le même contrôle.

Tout autre import, notamment `os`, `pathlib`, `time`, `datetime`, `importlib`, `numpy`, `pandas`, réseau, filesystem ou provider, est rejeté. L'exclusion de NumPy/Pandas empêche notamment `datetime64("now")` et `Timestamp.now()`. Ajouter un module à l'allowlist exige une RFC préenregistrée, un audit de ses capacités temporelles/transitives et au moins un mutant prouvant que sa voie temporelle éventuelle est rejetée.

## Preuve de revue P6

Pour O2, O4 et O7, la preuve mécanique contient `{oracle_id, reviewed_commit, admission_commit, report_path, admitted_sha256, report_verdict, recorded_status}`. Le contrôleur applique [`REVIEW_ADMISSION_REGISTRY.md`](REVIEW_ADMISSION_REGISTRY.md) : le hash est recalculé depuis le blob au commit d'admission, distinct et ancêtre, jamais depuis une valeur auto-déclarée dans la preuve courante. Il vérifie aussi que le rapport cite `reviewed_commit` et que son verdict correspond exactement à `recorded_status`. Un statut accepté sans admission, avec rapport modifié, mauvais commit ou verdict divergent bloque P6.

Mutations obligatoires : élever pending vers accepté sans rapport; substituer le rapport d'un autre oracle; modifier un octet du rapport; recalculer seulement le hash courant; changer le commit examiné ou d'admission; transformer `REJECT`/`NON_TESTABLE` en accepté. Chacune doit échouer.
