# Registre de décisions conceptuelles

## Règle de décision

| Statut | Critère |
|---|---|
| RETAIN | nécessaire, défini et compatible avec la finalité |
| REWRITE | intention utile, implémentation ou définition invalide |
| REJECT | contradiction, promesse trompeuse ou couplage interdit |
| DEFER | pertinent mais non nécessaire au premier noyau validable |
| UNKNOWN | preuves insuffisantes pour décider |

## Décisions

| ID | Concept | Décision | Ce qui est trouvé/vérifié | Intégration attendue | Réfutation de la décision |
|---|---|---|---|---|---|
| CD-001 | moteur unique replay/backtest | RETAIN | les divergences historiques ont produit des bugs comptables | `ReplayScheduler` unique | besoin démontré de sémantiques incompatibles |
| CD-002 | provider interchangeable | RETAIN | CSV, mocks et ccxt fournissent tous des observations de marché | port `MarketDataSource` | modification du domaine nécessaire pour changer de provider |
| CD-003 | ccxt dans le noyau | REJECT | dépendance fournisseur/réseau | extra d'adaptateur uniquement | aucune |
| CD-004 | stratégie modifie le portefeuille | REJECT | couple décision/comptabilité et empêche replay indépendant | `Strategy -> OrderIntent` | aucune |
| CD-005 | événement canonique | RETAIN | vocabulaires TP/SL/MTM/BUY/SELL incompatibles | `MarketEvent`, `OrderIntent`, `Fill`, `AccountEvent` distincts | schéma incapable de représenter un cas réel documenté |
| CD-006 | `SELL` générique | REJECT | signifie close-long ou short selon le moteur | intentions directionnelles explicites | aucune |
| CD-007 | ledger unique spot/futures | REJECT | cash spot et marge short ont des invariants différents | modèles de compte séparés | preuve algébrique d'invariants identiques |
| CD-008 | checkpoint JSON | RETAIN/REWRITE | reprise opérationnelle utile | schéma versionné mutable | reprise démontrée inutile |
| CD-009 | checkpoint = manifeste | REJECT | état courant ≠ preuve immuable | artefacts séparés | aucune |
| CD-010 | métriques normatives | RETAIN | Sortino/Calmar historiques ambigus ont changé le verdict | registre versionné | métrique sans décision utilisateur possible |
| CD-011 | numéraire implicite | REJECT | SOL/USD a inversé des lectures | `ReferenceSpec.numeraire` obligatoire | aucune |
| CD-012 | benchmark universel | REJECT | Buy/Hold et Sell/Hold dépendent du produit et des frictions | benchmark plugin + spec | aucune |
| CD-013 | risk frontier historique | REWRITE | table de levier ou top ratio, non-Pareto | `RiskMap` + dominance formelle | anciens oracles démontrent une vraie dominance |
| CD-014 | labels green/yellow/red | REJECT comme verdict | aucune calibration externe; green a liquidé | labels descriptifs historiques seulement | calibration préenregistrée et confirmée |
| CD-015 | zone de survie | RETAIN/REWRITE | intention pertinente | probabilité/fréquence, horizon et scénario obligatoires | impossibilité de définir survie sans arbitraire |
| CD-016 | configuration optimale | REJECT | sélection in-sample et voisinage non contrôlé | Pareto + stabilité + holdout | protocole d'optimalité préenregistré |
| CD-017 | heatmaps | RETAIN | valeur pédagogique réelle | vue de `RiskMap`, jamais preuve seule | graphique ne reflète pas le bundle source |
| CD-018 | seed globale | REJECT | état caché et interférence | RNG local nommé | aucune |
| CD-019 | horloge murale dans replay | REJECT | sortie non déterministe | `Clock` injectée | aucune |
| CD-020 | slippage constant | RETAIN comme modèle F0/F1 | scénario simple falsifiable | `ExecutionSpec`, statut ASSUME | présentation comme réalité exchange |
| CD-021 | modèle L2 | DEFER | données et priorité non disponibles | extension F3 | besoin du MVP démontré |
| CD-022 | paper live | DEFER | impossible à valider avant P0–P4 | après enregistrement canonique | parité replay déjà disponible |
| CD-023 | stratégies RSI/MA | DEFER/PORT | utiles pour neutralité de stratégie, non validées | port après contrats | oracles de signaux inexistants |
| CD-024 | grid short | RETAIN comme plugin | seul modèle actuellement normé partiellement | jamais cœur universel | dépendance du domaine au grid |
| CD-025 | multi-actif | DEFER | utile mais complexifie calendrier/cross-margin | après deux modèles mono-actif | besoin minimal prouvé |
| CD-026 | MIF « certification » | REJECT | aucune autorité ni procédure réglementaire démontrée | remplacer par contrôles de qualité nommés | certification externe vérifiée |
| CD-027 | monitoring | DEFER | utile en live, inutile pour prouver le noyau | dérive données/modèle après P5 | aucune |
| CD-028 | tests comme spec | RETAIN | protège les intentions | tests écrits depuis RFC/oracles | test dérivé du code |
| CD-029 | rôle Producteur/Critique | RETAIN | réduit confirmation circulaire | revue et artefacts séparés | aucune |
| CD-030 | publication des FAIL | RETAIN | condition d'honnêteté | `ResultBundle` conserve réfutations | aucune |

## Concepts encore UNKNOWN

- modèle de marge croisée universalisable;
- représentation canonique d'un carnet L3;
- politique commune des corporate actions multi-actifs;
- mesure de fidélité empirique inter-exchange;
- méthode d'incertitude adaptée à chaque dépendance temporelle.

Aucun de ces concepts ne doit bloquer le noyau F0/F1 mono-instrument.
