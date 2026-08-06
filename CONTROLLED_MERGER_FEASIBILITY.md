# Proposition de fusion contrôlée — plateforme universelle de paper trading

## 1. Objet

Construire à partir de `paper-trading-codex-restored` et `bitget-paper-trading` une plateforme de paper trading qui soit :

- indépendante des fournisseurs de données, exchanges, API et processus d'exécution;
- capable de rejouer un flux historique ou synthétique selon un ordre canonique;
- falsifiable par rapport à un référentiel déclaré avant le run;
- reproductible à partir d'un manifeste complet;
- capable de cartographier le risque au lieu de sélectionner silencieusement une configuration gagnante;
- utilisable avec plusieurs stratégies, instruments, numéraires et modèles d'exécution;
- honnête sur la fidélité réellement atteinte.

Le projet cible n'est ni un client Bitget générique, ni un grid bot SOL élargi. C'est un **laboratoire de replay et de risque dont les fournisseurs et stratégies sont des plugins remplaçables**.

## 2. Continuité avec l'intention historique

Cette proposition ne part pas de zéro. L'audit des archives retrouve les intentions suivantes :

| Intention historique retrouvée | Source d'archive | Traduction proposée |
|---|---|---|
| le replay historique doit reproduire le backtest avant tout mode live | `sol-grid-bot_backup/_work/notes1.md` | invariant de parité replay/backtest |
| remplacer `HistoricalDataProvider` par `LiveDataProvider` sans changer le simulateur | `sol-grid-bot_backup/_work/notes1.md` | ports de données indépendants du moteur |
| cartographier le paysage de risque, pas uniquement chercher un optimum | `Grid-Bot-Tree/prod_one/one.md` | moteur de scénarios et surfaces de risque |
| séparer hypothèse, production et critique | `sol_grid_lab/deepsearch_papertrading/producteur-papercodex.md` | gouvernance Producteur/Critique et preuves externes |
| formaliser `StrategySpec`, `HypothesisBundle` et `RunManifest` | mandats Producteur/Critique de `sol_grid_lab/deepsearch_papertrading` | contrats versionnés de l'expérience |
| déclarer numéraire, benchmark, funding, fill et arrondi | mêmes mandats | `ReferenceSpec` et `ExecutionSpec` obligatoires |
| marquer une donnée fournisseur non vérifiée comme `UNVERIFIED` | mandat critique | profil de fidélité avec machine à états |

Ces traces sont des **preuves d'intention**, pas des preuves de fonctionnement. Les anciennes mentions « identique à 100 % », « universel » ou « optimal » ne seront reprises que si un protocole actuel les confirme.

## 3. Audit de faisabilité de la fusion

### 3.1 Comparaison des deux dépôts

| Domaine | `paper-trading-codex-restored` | `bitget-paper-trading` | Décision de fusion |
|---|---|---|---|
| vocation | laboratoire scientifique grid short | application de paper trading orientée Bitget | conserver la rigueur du premier et l'ergonomie du second |
| stratégie | grid short SOL | RSI et moyenne mobile | convertir les trois en plugins `Strategy` |
| données | CSV/synthétique et connecteur public limité | mock et Bitget ccxt | définir un port `MarketDataSource` neutre |
| exécution | simulateur local testé | orchestration simulate/backtest/paper | conserver un moteur unique piloté par une horloge injectable |
| positions | short à levier explicite | portefeuille spot long | séparer `SpotAccountModel` et `IsolatedLinearShortAccountModel` |
| persistance | manifeste scientifique | état JSON redémarrable | séparer checkpoint opérationnel et manifeste de preuve |
| métriques | définitions normatives et oracles | rendement, drawdown, win rate simples | garder le registre métrique normatif |
| tests | 68 tests, réseau bloqué, 87,07 % | 9 tests centrés portefeuille | porter chaque composant avant intégration |
| packaging | wheel, CI, Ruff, Nix | scripts sans paquet ni CI | le dépôt restauré reste le réceptacle |
| documentation | hypothèses, méthodes, limites, révisions | README et notes opératoires | réunir sans diluer la distinction normative |

### 3.2 Faisabilité technique

**Faisabilité : élevée sous fusion progressive, faible sous fusion directe.**

Les projets possèdent des responsabilités complémentaires, mais leurs concepts ne sont pas interchangeables :

- `SELL` signifie fermeture d'un long dans `bitget-paper-trading`, alors que le projet restauré modélise un short;
- l'un stocke un collatéral SOL, l'autre une equity USDT;
- les événements, frais, quantités et horloges n'ont pas le même contrat;
- le mock du dépôt Bitget utilise `hash(symbol)` et `Timestamp.now()`, donc sa sortie n'est pas reproductible entre processus;
- le shell Nix Bitget crée une venv et installe par réseau, contrairement à l'environnement déclaratif cible;
- le dépôt Bitget annonce des futures, mais son chemin d'exécution courant est essentiellement spot long;
- aucune filiation Git commune ne permet un merge mécanique fiable.

Une copie globale introduirait des ambiguïtés de numéraire, de sens des ordres et de vérité comptable. La fusion doit se faire **contrat par contrat**, après tests de caractérisation puis tests normatifs.

### 3.3 Valeur respective

`paper-trading-codex-restored` apporte :

- les conventions financières explicites;
- les oracles indépendants et la non-circularité;
- le manifeste de reproductibilité;
- le packaging, la CI et les documents normatifs;
- la discipline `OBSERVE / INFER / DEDUCE / ASSUME`.

`bitget-paper-trading` apporte :

- les adaptateurs exchange;
- une CLI multi-mode;
- la boucle temps réel alignée sur les bougies;
- les stratégies RSI et moyenne mobile;
- la persistance et la reprise de session;
- une architecture initiale `adapter → signal → engine → portfolio`.

### 3.4 Verdict de faisabilité

La fusion est pertinente si elle vise une plateforme neutre et conserve les deux niveaux de vérité :

1. **vérité scientifique** : expérience figée, replay déterministe, oracle, preuve et possibilité de réfutation;
2. **continuité opérationnelle** : flux live, checkpoint, reprise et observation continue.

Elle n'est pas pertinente si elle consiste à ajouter ccxt dans le cœur scientifique ou à renommer le moteur Bitget en moteur universel.

## 4. Principes normatifs de la plateforme cible

1. Le domaine ne dépend d'aucun SDK fournisseur.
2. Un adaptateur traduit vers un schéma canonique; il ne définit pas le sens financier.
3. Replay, backtest et paper utilisent le même moteur d'événements.
4. L'horloge est toujours injectée; aucun `now()` dans les calculs reproductibles.
5. Toute source de hasard reçoit un algorithme et une seed explicites.
6. Tout résultat nomme son numéraire, son benchmark et ses conventions comptables.
7. Aucun résultat n'est comparable si son référentiel diffère silencieusement.
8. Une stratégie produit des intentions; elle ne modifie pas directement le portefeuille.
9. Le modèle d'exécution transforme les intentions en fills selon une politique déclarée.
10. Le modèle de compte applique marge, frais, funding, liquidation et arrondi.
11. Une métrique provient d'un registre normatif versionné.
12. Une configuration « optimale », « sûre » ou « robuste » est interdite sans protocole hors échantillon.
13. Un fournisseur peut être remplacé sans modifier stratégie, compte, replay ou métriques.
14. Un statut `PASS` signifie seulement que le critère préenregistré a survécu au run.

## 5. Architecture cible

```text
Sources externes                 Contrats canoniques                 Noyau pur

CSV / Parquet ─┐
Bitget ────────┼─> MarketDataSource ─> MarketEvent ─┐
Binance ───────┤                                    │
Kraken ────────┤                                    v
Synthétique ───┘                              ReplayScheduler
                                                       │
Clock historique/live ───────> Clock ──────────────────┤
                                                       v
Strategy plugins ───────> OrderIntent ───────> ExecutionModel
                                                       │
Venue/fee profiles ─────> ExecutionSpec ───────────────┤
                                                       v
Account models ─────────> AccountSpec ─────────> Ledger + Events
                                                       │
ReferenceSpec ─────────────────────────────────────────┤
HypothesisBundle ──────────────────────────────────────┤
                                                       v
                                     Metrics + RiskMap + ResultBundle
                                                       │
                                                       v
                              RunManifest + hashes + verdicts PASS/FAIL
```

Les imports doivent toujours pointer vers l'intérieur : les adaptateurs connaissent le domaine, le domaine ne connaît jamais ccxt, Bitget, pandas ou un format de fichier particulier.

## 6. Contrats canoniques minimaux

### 6.1 `InstrumentSpec`

- identifiant interne stable;
- type : spot, future daté, perpetual;
- base, quote, settlement et numéraire;
- tick size, lot size et politique d'arrondi;
- multiplicateur contractuel;
- calendrier et timezone;
- règles de marge et de financement référencées par version.

### 6.2 `MarketEvent`

- `event_id`, `source_id`, timestamp d'événement et timestamp de réception;
- type : trade, quote, candle, funding, index, mark, corporate action;
- instrument et unité;
- payload canonique validé;
- provenance, schéma, checksum et rang dans l'ordre canonique.

Une bougie OHLCV ne doit jamais prétendre fournir la même fidélité qu'un carnet L2. Le type de données limite explicitement les modèles de fill autorisés.

### 6.3 `StrategySpec`

- version et hash du code;
- paramètres et domaines admissibles;
- inputs requis;
- état sérialisable;
- hypothèses auxquelles la stratégie se rattache;
- intentions de sortie sans appel exchange.

### 6.4 `ExecutionSpec`

- modèle de fill et priorité intra-événement;
- ordre canonique si TP et SL sont touchés dans la même barre;
- frais, spread, slippage, latence et impact;
- politique maker/taker;
- précision et arrondi;
- comportement sur trous, gaps et liquidité insuffisante.

### 6.5 `AccountSpec`

- spot, marge isolée, marge croisée ou modèle pédagogique;
- numéraire comptable;
- règles de réservation de cash/marge;
- PnL réalisé et latent;
- funding;
- maintenance, liquidation, faillite et ADL;
- invariants du grand livre.

### 6.6 `ReferenceSpec`

Le référentiel est obligatoire et fixé avant le replay :

- numéraire principal;
- benchmark(s) et leur modèle de friction;
- fréquence et calendrier d'annualisation;
- taux sans risque ou MAR;
- conventions des métriques;
- source de prix de valorisation : last, mid, mark ou index;
- tolérances numériques;
- horizons et budgets de risque.

### 6.7 `HypothesisBundle`

Pour chaque hypothèse : énoncé, type d'affirmation, données admissibles, oracle indépendant, résultat attendu avant exécution, critère d'échec, puissance ou tolérance, et limites d'interprétation.

### 6.8 `RunManifest`

- hashes des données, configurations, code, dépendances et contrats;
- versions Python/Nix et plateforme;
- seeds et algorithmes RNG;
- ordre des événements;
- références `StrategySpec`, `ExecutionSpec`, `AccountSpec`, `ReferenceSpec` et `HypothesisBundle`;
- profil de fidélité;
- commandes de reproduction;
- hashes des résultats et graphiques.

### 6.9 `ResultBundle`

- journal append-only;
- ledger réconcilié;
- equity et expositions;
- métriques avec définition/version;
- verdicts par hypothèse;
- anomalies, censures et données rejetées;
- carte de risque et domaines non testables.

## 7. Référentiel de replay crédible

Un replay n'est crédible que relativement à un profil de fidélité explicite.

| Niveau | Données | Ce qui peut être affirmé |
|---|---|---|
| F0 | prix de clôture | logique directionnelle grossière uniquement |
| F1 | OHLCV | barrières avec politique intra-barre déclarée |
| F2 | trades/quotes | séquence, spread et latence simplifiée |
| F3 | carnet L2 | fills dépendants de profondeur et priorité modélisée |
| F4 | flux exchange complet + compte démo | confrontation empirique fournisseur |

États de validation d'un adaptateur :

```text
UNVERIFIED -> SCHEMA_VALIDATED -> REPLAY_VALIDATED -> EMPIRICALLY_PROFILED
```

Toute transition exige une preuve. Renseigner un nom de fournisseur ne change jamais automatiquement le statut.

## 8. Falsifiabilité du replay

Le protocole minimal impose :

1. préenregistrer input, référentiel, hypothèses et attendus;
2. lancer le même événement canonique dans le backtest et le replay;
3. comparer journal, fills, ledger, equity et métriques;
4. exiger un hash sémantique bit-exact dans le même environnement verrouillé; utiliser les tolérances préenregistrées seulement pour les assertions numériques, jamais pour rendre deux hashes égaux;
5. exécuter des tests de mutation qui doivent échouer si l'on modifie frais, ordre TP/SL, quantité, levier, seed ou numéraire;
6. publier les échecs, y compris une stratégie perdante ou une région de liquidation.

Invariant initial :

```text
hash(ResultBundle(backtest, manifest M))
    == hash(ResultBundle(replay, manifest M))
```

Cet invariant compare une sérialisation canonique excluant les métadonnées non sémantiques. Entre environnements différents, un résultat peut être `NUMERICALLY_EQUIVALENT` sous les tolérances du manifeste, mais il n'est `BIT_REPRODUCIBLE` que si les hashes sont identiques.

Si les moteurs live et replay doivent diverger pour des raisons opérationnelles, la divergence est un événement explicite, jamais un chemin de code silencieux.

## 9. Cartographie avancée du risque

La plateforme ne cherche pas un unique maximum de rendement. Elle calcule une surface de risque sur un domaine préenregistré.

### 9.1 Héritage retrouvé et statut scientifique

La recherche dans les archives a retrouvé 66 fichiers mentionnant `risk frontier`, `risk mapping`, « frontière efficiente » ou « cartographie du risque », hors caches et résultats générés. Ils prouvent que l'intention était ancienne et répétée. Ils ne prouvent pas que les calculs étaient valides.

| Artefact historique | Intention utile | Défaut scientifique observé | Décision |
|---|---|---|---|
| `src/analysis/sol_metrics.py::calculate_risk_frontier` | comparer levier, rendement, liquidation, Sharpe et drawdown | simple table triée par levier; aucune dominance ni incertitude | conserver le concept de table de sensibilité, rejeter le nom « frontier » |
| `sol_grid_bot_pro/scripts/optimize.py::_calculate_efficient_frontier` | chercher un compromis rendement/risque | trie par ratio rendement/drawdown et prend le top 10; ce n'est pas une frontière de Pareto | réécrire entièrement l'algorithme |
| `_calculate_risk_boundaries` du même script | distinguer faible, moyen et haut risque | seuils aux 25e/75e percentiles du même échantillon, sans signification externe | conserver comme visualisation descriptive, jamais comme catégorie normative |
| `run_optimization_v1.py::risk_mapping_optimization` | explorer toutes les combinaisons et conserver les raisons d'échec | critères de succès arbitraires, dataset et modèle uniques, pas de holdout | conserver le patron d'exploration exhaustive après préenregistrement |
| `src/optimization/risk_mapper.py` | encapsuler la cartographie dans un composant | méthodes centrales laissées comme stubs | ne pas porter le code |
| `visualization.py::plot_risk_frontier` | représenter plusieurs métriques | suppose que l'input est déjà une frontière valide | porter seulement après définition du nouveau schéma |
| `bundle_a_intelligence_en.md` | exprimer zone de survie et sweet spot de levier | valeurs non manifestées, contradictions et vocabulaire « safe/optimal/suicide » | conserver comme hypothèses historiques réfutables, jamais comme résultat |
| `Grid-Bot-Tree/prod_one/one.md` | cartographier le paysage de risque plutôt qu'un gagnant | intention en prose sans protocole complet | intégrer comme objectif fondateur |

Le code de fusion ne doit donc pas importer un ancien `risk_mapper`. Il doit traduire les intentions dans un nouveau composant construit depuis une spécification préalable.

### 9.2 Intentions historiques à préserver

Les intentions suivantes sont recevables indépendamment des anciennes implémentations :

1. faire varier le levier et rendre visible la transition survie → fragilité → liquidation;
2. étudier conjointement levier, espacement de grille, allocation et nombre de positions;
3. conserver toutes les configurations, y compris échecs et erreurs;
4. produire des heatmaps et surfaces plutôt qu'un seul score;
5. distinguer performance, drawdown, liquidation et activité de trading;
6. rechercher des régions stables, pas uniquement un maximum ponctuel;
7. rendre les paramètres entièrement déclaratifs;
8. comparer la stratégie à un référentiel explicite.

Ces intentions deviennent des exigences fonctionnelles. Les anciennes valeurs 2x/3x/5x/8x, les zones « green/yellow/red » et les plages dites optimales deviennent des **fixtures historiques de réfutation** : le nouveau système devra montrer s'il les reproduit ou les contredit, avec le manifeste correspondant.

### 9.3 Définition normative de `RiskMap`

Une `RiskMap` est l'ensemble complet des résultats d'un plan d'expérience préenregistré :

```text
RiskMap = {
    ExperimentDomain,
    ScenarioSet,
    EvaluationReference,
    RunManifest[] ,
    RiskPoint[] ,
    ParetoSet,
    Uncertainty,
    NonTestableRegions,
    FailureMap
}
```

Un `RiskPoint` représente une combinaison effectivement exécutée, jamais une interpolation silencieuse. Il contient au minimum :

- paramètres et scénario;
- statut `PASS`, `FAIL`, `ERROR`, `CENSORED` ou `NON_TESTABLE`;
- rendement et risque dans le numéraire déclaré;
- drawdown et durée sous l'eau;
- liquidations et temps de survie;
- exposition maximale, turnover, frais, funding et slippage;
- nombre de trades et taille effective de l'échantillon;
- métriques d'incertitude;
- hashes du manifeste et du résultat;
- raisons structurées de l'échec ou de la non-testabilité.

### 9.4 Frontière de Pareto, pas classement par ratio

Pour des objectifs à maximiser `G` et des risques à minimiser `R₁…Rₖ`, un point `a` domine `b` si :

```text
G(a) >= G(b)
R_i(a) <= R_i(b) pour tout i
et au moins une inégalité est stricte.
```

La frontière est l'ensemble des points non dominés. Aucun poids, score composite ou ratio rendement/drawdown ne doit être introduit sans `ReferenceSpec` distinct. Le système peut présenter plusieurs projections de Pareto, mais il ne déclare pas un unique « meilleur » point.

Cas obligatoires :

- risque nul et rendement nul;
- drawdown nul avec rendement positif;
- point liquidé avec rendement temporairement élevé;
- métrique manquante ou infinie;
- égalité exacte;
- point dominé sur un seul axe;
- objectifs contradictoires;
- points issus de scénarios ou référentiels incompatibles.

Les points provenant de référentiels différents ne peuvent pas appartenir à la même frontière.

### 9.5 Axes minimaux

- levier, allocation, nombre de positions et concentration;
- frais, spread, slippage, latence et profondeur;
- volatilité, dérive, gaps, queues et changements de régime;
- paramètres de stratégie;
- timeframe et qualité des données;
- MMR, funding et politique de liquidation;
- numéraire et benchmark;
- ordre intra-barre;
- seed pour les modèles stochastiques.

### 9.6 Sorties

- probabilité/fréquence de liquidation;
- perte maximale et expected shortfall avec convention explicite;
- maximum drawdown et durée sous l'eau;
- distribution du PnL et du temps de survie;
- sensibilité locale et globale aux paramètres;
- frontière rendement/risque;
- zones de survie, fragilité et non-identifiabilité;
- taux d'échec par régime;
- écart au benchmark avec intervalle d'incertitude;
- carte des hypothèses confirmées, réfutées ou non testables.

### 9.7 Incertitude et stabilité

Une frontière calculée sur des estimations ponctuelles est descriptive, pas robuste. La plateforme doit fournir :

- intervalles de confiance ou bandes de bootstrap lorsque leur usage est justifié;
- dispersion entre seeds pour les scénarios stochastiques;
- dispersion entre fenêtres pour les données historiques;
- sensibilité au voisinage des paramètres;
- fréquence de domination sous rééchantillonnage;
- séparation entre risque de marché, risque de modèle, risque de données et risque opérationnel.

Un point n'est qualifié de **région stable** que si un voisinage préenregistré satisfait les contraintes. Pour l'oracle MVP O4, ce voisinage et ces contraintes sont fixés dans `docs/fusion/05_RISKMAP_ORACLES.md`; toute autre étude doit les préenregistrer dans son `HypothesisBundle`. Un optimum isolé entouré d'échecs est classé fragile.

### 9.8 Règle anti-optimisation trompeuse

Les données de sélection et de confirmation sont distinctes. La carte complète, les configurations perdantes et le nombre d'essais sont conservés. Une configuration n'est qualifiée de robuste que si sa région voisine reste admissible et si elle survit hors échantillon.

Les règles supplémentaires sont :

- aucune suppression des runs liquidés, en erreur ou sans trade;
- aucun choix de seuil après observation sans nouvelle révision préenregistrée;
- correction ou déclaration du risque de comparaisons multiples;
- aucun changement de numéraire entre sélection et confirmation;
- aucun benchmark calculé avec une friction plus favorable que la stratégie sans justification;
- publication du nombre total de combinaisons tentées;
- publication séparée des résultats in-sample, validation et holdout;
- conservation des configurations qui réfutent la thèse.

### 9.9 Hypothèses falsifiables du futur moteur

| ID | Énoncé | Oracle indépendant | Critère d'échec |
|---|---|---|---|
| RF-H1 | le domaine généré correspond exactement au produit cartésien déclaré | petit domaine énuméré à la main | combinaison absente, dupliquée ou ajoutée |
| RF-H2 | chaque combinaison produit un statut terminal | nombre attendu de `RiskPoint` | run silencieusement perdu |
| RF-H3 | la dominance de Pareto est correcte | nuage manuel de 6–10 points | point dominé présent ou non dominé absent |
| RF-H4 | changer l'ordre des inputs ne change pas la frontière | permutation fixe des mêmes points | hash sémantique différent |
| RF-H5 | un run liquidé reste dans `FailureMap` | scénario analytique de liquidation | exclusion du run ou classement gagnant |
| RF-H6 | deux référentiels incompatibles ne sont pas agrégés | numéraires USD et SOL explicites | frontière commune acceptée |
| RF-H7 | la carte est reproductible | double exécution depuis le même manifeste | hash différent |
| RF-H8 | une région fragile est distinguée d'une région stable | grille synthétique avec pic isolé | pic qualifié robuste |
| RF-H9 | la mutation d'un frais ou d'un fill modifie les résultats attendus | scénario manuel avec frais non nuls | résultat inchangé ou mutation non détectée |
| RF-H10 | les zones insuffisamment observées sont `NON_TESTABLE` | échantillon sous le minimum préenregistré | verdict PASS/FAIL produit malgré l'absence de puissance |

### 9.10 Calibration avant données réelles

Le moteur doit d'abord être testé sur des paysages synthétiques dont la frontière est connue analytiquement :

1. fonction monotone simple avec tous les points dominés sauf un;
2. compromis convexe produisant plusieurs points non dominés;
3. plateau d'égalité;
4. optimum ponctuel instable;
5. région interdite ou liquidée;
6. bruit seedé avec frontière probabiliste connue;
7. changement de numéraire qui inverse artificiellement un classement.

Les anciens résultats SOL peuvent ensuite servir de jeu de caractérisation. Ils ne deviennent une preuve qu'après passage par le moteur canonique et production d'un nouveau `RunManifest`.

## 10. Plan de fusion contrôlée

### Phase 0 — Baseline immuable

- taguer les deux dépôts;
- capturer leurs tests, sorties et limites actuelles;
- ne déclarer aucun résultat du dépôt Bitget validé avant exécution séparée;
- créer un registre de décisions architecturales.

**Gate P0** : les deux baselines sont reproductibles ou leurs inconnues sont consignées.

### Phase 1 — Domaine canonique

- créer les dataclasses/schémas des contrats §6;
- porter le ledger spot avec invariants cash/position/frais;
- porter le modèle short isolé comme modèle distinct;
- imposer horloge, IDs et arrondis injectables.

**Gate P1** : oracles spot et short passent; aucune dépendance fournisseur dans le domaine.

### Phase 2 — Replay unique

- créer `ReplayScheduler` et ordre canonique;
- faire passer CSV et synthétique par `MarketEvent`;
- démontrer parité backtest/replay;
- ajouter tests de mutation.

**Gate P2** : bundle et hashes identiques pour un même manifeste.

### Phase 3 — Portage des stratégies

- porter Grid, RSI et MA derrière `Strategy`;
- retirer horloge, I/O et portefeuille des stratégies;
- caractériser leurs sorties sur tables manuelles.

**Gate P3** : intentions identiques sur inputs connus; aucune stratégie n'accède à un provider.

### Phase 4 — Adaptateurs

- porter Mock sans `hash()` Python ni `now()`;
- porter CSV/Parquet;
- porter Bitget ccxt comme extra optionnel;
- ajouter au moins un second adaptateur ou un adaptateur fixture pour prouver la neutralité;
- valider schémas et provenance.

**Gate P4** : le même dataset canonique provenant de deux adaptateurs produit le même résultat.

### Phase 5 — Persistance et live

- séparer `Checkpoint` mutable et `RunManifest` immuable;
- injecter `LiveClock` sans modifier le moteur;
- enregistrer tous les événements reçus pour replay ultérieur;
- comparer paper live enregistré et replay de ce même flux.

**Gate P5** : après redémarrage, aucun double traitement; replay du flux live identique selon le profil déclaré.

### Phase 6 — RiskMap

- définir espaces de paramètres avant calcul;
- exécuter scénarios synthétiques et historiques;
- produire surfaces, frontières et zones non testables;
- calibrer les tests statistiques sur des contrôles où le modèle est vrai.

**Gate P6** : chaque carte est régénérable et chaque verdict peut devenir FAIL.

### Phase 7 — Publication

- CI Python 3.10–3.12;
- wheel installée hors dépôt;
- Ruff et couverture ≥ 70 %;
- fixtures sans réseau en CI standard;
- tests réseau séparés, opt-in et sans secrets dans les logs;
- documentation normative et exemples sans promesse de performance.

**Gate P7** : revue indépendante Producteur/Critique et aucun blocage HIGH_IMPACT ouvert.

## 11. Composants à porter ou à rejeter

| Composant | Action |
|---|---|
| manifeste, métriques et tests du projet restauré | conserver comme socle |
| CLI du dépôt Bitget | porter après séparation I/O/domaine |
| adaptateur Bitget | porter dans un extra fournisseur |
| MockAdapter | réécrire avec seed et calendrier fixes |
| persistance JSON | porter vers un schéma `Checkpoint` versionné |
| RSI/MA | porter avec oracles et paramètres documentés |
| portfolio Bitget | caractériser puis porter comme `SpotAccountModel` |
| grid short | conserver comme plugin expérimental |
| shell Nix Bitget avec `pip install` et suppression de venv | rejeter |
| noms « optimal », « green/safe » non validés | rejeter |
| dépendance ccxt dans le cœur | rejeter |
| logique `SELL` ambiguë | remplacer par `OpenLong`, `CloseLong`, `OpenShort`, `CloseShort` |

## 12. Risques de programme

| Risque | Gravité | Réduction |
|---|---|---|
| abstraction trop générique avant preuve | élevée | commencer spot + short isolé, ajouter par contrat |
| faux sentiment de fidélité multi-exchange | critique | profils F0–F4 et états de validation |
| divergence live/replay | critique | un moteur, flux live enregistré, parité hashée |
| ambiguïté du numéraire | critique | `ReferenceSpec` obligatoire |
| biais d'optimisation | critique | domaine préenregistré, holdout, carte complète |
| explosion combinatoire de RiskMap | élevée | plans d'expérience versionnés et budgets explicites |
| schéma canonique appauvri | élevée | conserver payload brut hashé avec projection canonique |
| tests statistiques sans puissance | élevée | calibration sous contrôles vrais et domaine non testable |
| dépendance cachée à ccxt/pandas | moyenne | ports purs et extras optionnels |
| compatibilité prématurée avec l'ancien code | moyenne | adaptateurs de migration temporaires, non API cible |

### 12.1 Conditions de NO-GO

La fusion est arrêtée et réévaluée, sans passage automatique au gate suivant, si au moins une condition survient :

1. un invariant comptable requis est démontré contradictoire ou impossible pour les deux modèles de compte déclarés;
2. deux adaptateurs ne peuvent produire le même événement canonique sans perte d'une information nécessaire au domaine MVP;
3. la parité backtest/replay échoue après deux cycles Producteur–Contradictoire sur la même cause racine;
4. la provenance ou la licence interdit le portage d'un composant nécessaire;
5. un secret ou un ordre réel peut être déclenché par le chemin de test standard;
6. deux gates consécutifs restent `BLOCKED` trois cycles documentés pour la même dépendance externe;
7. maintenir la compatibilité legacy exige de violer un invariant normatif accepté.

Un NO-GO n'impose pas l'abandon de toute la recherche : il impose de publier le constat, réduire le périmètre ou proposer une nouvelle architecture dans une révision distincte. Modifier le critère après son déclenchement est interdit.

### 12.2 Provenance et licence des composants

Avant P3, chaque composant envisagé reçoit un enregistrement : dépôt et commit source, chemin, auteur/copyright disponible, licence détectée, compatibilité avec MIT, transformations et décision `PORT/REWRITE/REJECT/UNKNOWN`. L'absence de licence explicite signifie `UNKNOWN` et interdit la copie de code; seules les idées non protégeables peuvent être réimplémentées depuis une spécification indépendante, avec traçabilité.

## 13. Critères de succès finaux

La plateforme est recevable lorsque :

- deux fournisseurs différents peuvent alimenter le même flux canonique sans modifier le noyau;
- CSV, synthétique et live enregistré utilisent le même replay;
- spot et short ont des ledgers distincts et réconciliables;
- les trois stratégies sont des plugins sans I/O;
- toute métrique est versionnée et testée sur un oracle indépendant;
- le replay peut être réfuté par des tests de mutation;
- un `RunManifest` suffit à régénérer un `ResultBundle` identique dans l'environnement verrouillé;
- `RiskMap` publie zones gagnantes, perdantes, liquidées et non testables;
- la fidélité fournisseur est un résultat mesuré, jamais déduite du nom de l'adaptateur;
- aucune revendication de rentabilité ou d'universalité empirique n'est faite sans validation correspondante.

## 14. Décision proposée

**GO conditionnel pour une fusion contrôlée dans `paper-trading-codex-restored`.**

Le dépôt restauré doit rester le dépôt cible parce qu'il possède déjà la discipline scientifique, le packaging et la CI. `bitget-paper-trading` doit être traité comme une source de composants opérationnels, non comme le nouveau cœur.

Le premier incrément ne doit pas connecter Bitget. Il doit livrer les contrats canoniques, deux modèles de compte, un replay unique et la parité backtest/replay sur fixtures locales. L'indépendance fournisseur sera ensuite démontrée par deux adaptateurs interchangeables, pas déclarée par architecture seule.

Tant que P0–P2 ne sont pas franchies, le projet demeure **prototype de fusion**. Tant que P4 n'est pas franchie, il demeure **provider-neutral by design, unknown in practice**. Tant que P6 n'est pas franchie, il ne possède pas encore de cartographie avancée du risque validée.

## 15. Audit conceptuel réalisé avant fusion

État au 2026-08-06 : le cadrage documentaire initial est réalisé; aucune implémentation fusionnée n'est encore déclarée valide.

| Travail | Artefact | Résultat vérifié | Ce qui peut être intégré | Limite actuelle |
|---|---|---|---|---|
| archéologie du corpus | [`00_CORPUS_TRACEABILITY.md`](docs/fusion/00_CORPUS_TRACEABILITY.md) | dix intentions récurrentes et huit contradictions recensées | questions, scénarios et invariants historiques | les anciens chiffres ne sont pas des preuves |
| arbitrage conceptuel | [`01_CONCEPT_DECISION_REGISTER.md`](docs/fusion/01_CONCEPT_DECISION_REGISTER.md) | 30 décisions explicites et cinq inconnues | concepts `RETAIN` et intentions `REWRITE`, après gate | RFC non encore acceptées |
| référentiel | [`02_REFERENCE_MODEL.md`](docs/fusion/02_REFERENCE_MODEL.md) | unités, numéraire, prix, PnL et dix invariants définis | `ReferenceSpec` obligatoire | pas encore de schéma exécutable |
| risques | [`03_RISK_TAXONOMY.md`](docs/fusion/03_RISK_TAXONOMY.md) | risque distingué de zéro observé et de hors-modèle | statuts et exigences de données | calibration empirique absente |
| compatibilité | [`04_ENGINE_COMPATIBILITY.md`](docs/fusion/04_ENGINE_COMPATIBILITY.md) | spot et short ne partagent pas le même ledger | ports communs, comptes séparés | tests de caractérisation à écrire |
| RiskMap | [`05_RISKMAP_ORACLES.md`](docs/fusion/05_RISKMAP_ORACLES.md) | sept oracles préalables, dont Pareto et mutations | fixtures indépendantes du moteur | implémentation et calibration absentes |
| passage de phases | [`06_FUSION_GATES.md`](docs/fusion/06_FUSION_GATES.md) | P0–P7 ont critères, preuves et mutations | ordre de travail et règles de publication | P0 incomplet; P1+ non commencés |
| interfaces | [`CANONICAL_CONTRACT_RFCS.md`](docs/fusion/CANONICAL_CONTRACT_RFCS.md) | neuf RFC regroupées avec questions ouvertes | base de critique Producteur/Critique | statut documentaire seulement |

### 15.1 Calculs indépendants déjà fixés

- achat/revente spot de 100 USD à prix constant avec 0,1 % de frais par côté : perte attendue `0,1999 USD`;
- short linéaire : equity 1 000, allocation 30 %, levier 2, entrée 100, sortie 90 : marge `300`, notionnel `600`, quantité `6`, PnL brut `60 USD`;
- même détention de 10 SOL : rendement `0 %` en SOL mais `−50 %` en USD lorsque SOL passe de 100 à 50 USD;
- oracle Pareto O1 : `{A, B, D, E}` après déduplication sémantique;
- domaine cartésien O6 : `2 × 2 × 2 = 8` résultats terminaux attendus.

Ces valeurs sont des oracles préalables, pas des résultats du futur moteur. Celui-ci devra les reproduire, puis échouer sous les mutations prescrites.

### 15.2 Décision d'intégration actuelle

- **à intégrer après acceptation des RFC** : ports fournisseur, événements typés, manifeste immuable, journal append-only, comptes spot/short séparés et registre de métriques;
- **à réécrire avant intégration** : Risk Frontier historique, mocks temporels, checkpoints et événements legacy;
- **à rejeter** : faux Pareto par ratio, labels `safe/optimal` non calibrés, numéraire implicite, dépendance ccxt dans le cœur et `SELL` ambigu;
- **à différer** : L2/L3, paper live, multi-actif, monitoring et mesure empirique inter-exchange;
- **inconnu** : marge croisée universelle, corporate actions et méthode d'incertitude adaptée à chaque structure temporelle.

### 15.3 Prochaine preuve requise

Terminer P0 sans modifier le comportement métier : figer les révisions et environnements des deux dépôts, produire leurs hashes, exécuter leurs validations déclarées séparément et publier tous les `PASS`, `FAIL`, `SKIP` et `NON_TESTABLE`. P1 ne commencera qu'après cette baseline contradictoire et reproductible.

## 16. Gouvernance contradictoire des hypothèses

Le développement se fait depuis `fusion/controlled-merger`. Chaque hypothèse nouvelle utilise une branche `hypothesis/HNNN-slug-court` et un dossier probatoire propre. Sa fusion exige deux évaluations IA distinctes, l'une **Critique**, l'autre **Contradictoire**, selon [`PROTOCOL_CONTRADICTOIRE.md`](docs/fusion/PROTOCOL_CONTRADICTOIRE.md).

Les deux avis ne sont pas un vote et ne suffisent jamais seuls : oracles indépendants, tests mécaniques, mutations, manifeste et hashes restent obligatoires. Une réfutation ouverte, un verdict `NON_TESTABLE` ou une modification a posteriori de l'attendu bloque la fusion. Le statut des branches est conservé dans [`HYPOTHESIS_BRANCH_REGISTER.md`](docs/fusion/HYPOTHESIS_BRANCH_REGISTER.md).

Le cycle de faisabilité initial a reçu une dérogation humaine explicitement versionnée; elle autorise le travail de correction mais ne valide aucune hypothèse et ne modifie pas la règle générale.
