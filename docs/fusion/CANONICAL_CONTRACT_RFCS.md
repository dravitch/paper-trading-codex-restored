# RFC des contrats canoniques — version documentaire 0

## Statut commun

`DRAFT_FOR_CRITIQUE`. Aucun schéma n'est encore exécutable. Toute ambiguïté reste un blocage P1.

## RFC-001 — `InstrumentSpec`

Champs obligatoires : `instrument_id`, type, base, quote, settlement, multiplicateur, tick, lot, timezone, calendrier, politique d'arrondi. Rejet : unité absente, tick/lot non positifs, type inconnu.

## RFC-002 — `MarketEvent`

Champs : `event_id`, `source_id`, instrument, type, event_time, receive_time optionnel, séquence, payload canonique, hash brut, niveau F0–F4. Ordre canonique : `(event_time, sequence, source_id, event_id)`. Rejet : duplicate ID au contenu différent, temps absent, niveau supérieur aux données.

## RFC-003 — `StrategySpec` et `OrderIntent`

La stratégie reçoit état public + événements et retourne une intention sans effet de bord. Intentions : `OPEN_LONG`, `CLOSE_LONG`, `OPEN_SHORT`, `CLOSE_SHORT`, `CANCEL`, `HOLD`. Champs : instrument, direction, quantité ou règle de taille, type d'ordre, contraintes, hypothesis IDs. Rejet : `SELL` ambigu, appel provider, mutation ledger.

## RFC-004 — `ExecutionSpec`, `Order`, `Fill`

Déclare fill, spread, slippage, latence, impact, maker/taker, partial fills, priorité intra-barre, précision. Un fill porte quantité, prix, frais, temps et `order_id`. Rejet : frais sans devise, fill supérieur à quantité restante, ordre OHLCV sans politique double-barrière.

## RFC-005 — `AccountSpec` et ledger

Classes canoniques initiales : `SpotAccountModel` et `IsolatedLinearShortAccountModel`; discriminants sérialisés : `SPOT_CASH_V1` et `ISOLATED_LINEAR_SHORT_EDU_V1`. Écritures en partie double conceptuelle : cash, actif, marge, frais, PnL réalisé, funding. Invariant : somme des variations expliquée par événements. Rejet : levier sans marge, liquidation par stratégie, mélange de modèles ou alias de classe non déclaré.

## RFC-006 — `ReferenceSpec`

Défini par `02_REFERENCE_MODEL.md`. Son hash fait partie de toute clé de comparabilité. Rejet mécanique de toute agrégation aux hashes différents.

## RFC-007 — `HypothesisBundle`

Champs par Hn : énoncé, type `DEDUCE/ASSUME`, inputs, oracle, attendu pré-run, critère d'échec, tolérance/puissance, statut possible, limites. Rejet : attendu absent, test nommé sans oracle, PASS seul statut possible.

## RFC-008 — `RunManifest` et `ResultBundle`

Le manifeste fixe code, données, specs, RNG, versions et commande. Le bundle contient event log, ledger, métriques, anomalies, verdicts et hashes. Le SHA-256 sémantique porte sur une sérialisation canonique bit-exacte; les tolérances d'oracle sont enregistrées séparément et ne modifient jamais le hash. NaN/infini sont détectés avant sérialisation : le run devient `ERROR`, la valeur est remplacée par un objectif absent et une anomalie finie portant le token lexical observé. Rejet : secret, chemin machine comme identité, timestamp non pertinent dans hash sémantique, NaN/infini brut, résultat sans manifeste.

## RFC-009 — `RiskMap`

Défini par `CONTROLLED_MERGER_FEASIBILITY.md §9` et `05_RISKMAP_ORACLES.md`. Comparabilité par hash de référentiel/scénario; Pareto formel; toutes combinaisons conservées. Rejet : top-N appelé frontière, exclusion d'échecs, interpolation présentée comme run, point sans taille d'échantillon.

## Questions ouvertes avant P1

1. Decimal arbitraire ou binary64 avec arrondi explicite?
2. Identité d'instrument interne : UUID de spec ou chaîne sémantique?
3. Ordre canonique si une source ne fournit aucune séquence?
4. Représentation d'une censure de fin de replay?
5. Ledger multi-devise dès P1 ou conversion obligatoire?

Ces questions restent `UNKNOWN`; aucune réponse ne doit être codée implicitement.
