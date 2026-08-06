# REV05 — Consolidation Producteur L1–L12

## AVANT

La revue Contradictoire avait accepté le cadrage sous douze limites. O2 autorisait deux politiques, O4 et O7 dépendaient de règles absentes, certains cas Pareto n'avaient aucun oracle, hash et tolérance étaient confondus, et aucun NO-GO ou audit de licence n'encadrait le portage.

Le code présentait aussi une ancienne erreur Bitget Demo `40099` et une commission comme propriétés actuelles du fournisseur, sans preuve datée.

## APRÈS

- politique de liquidation MVP unique;
- clé canonique O7 et voisinage O4 fixés;
- oracles O8–O11 ajoutés avant implémentation;
- reproductibilité bit-exacte séparée de l'équivalence numérique;
- règlement des frais explicite;
- mutations horloge/provider ajoutées aux gates;
- nom `IsolatedLinearShortAccountModel` unifié;
- sept conditions de NO-GO;
- provenance/licence obligatoire avant copie;
- revendications Bitget legacy retirées sans activer d'endpoint privé;
- registre L1–L12 créé.

## Justification

Chaque changement répond directement à une ambiguïté, contradiction ou absence de réfutabilité identifiée dans les deux revues. Aucun calcul métier du moteur existant n'est modifié.

## Tests et preuves

- attendus O2 et O4 désormais univoques;
- O8 : P `(2,0)` domine Z `(0,0)` sur le seul rendement;
- O9 : valeur absente = `NON_TESTABLE`, non finie = `ERROR`;
- O10 : X `(6,3)` domine Y `(6,4)` sur le seul drawdown;
- O11 : Q `(4,1)` et R `(8,5)` restent tous deux non dominés;
- Nix : Python 3.12.12, 68 tests passés en 2,26 s, couverture 87,07 %, Ruff zéro erreur.

## Statut

Branche de correction seulement. L9, la baseline Bitget de L11, L12 et les mutations exécutables restent ouvertes. Aucun gate franchi; revue Contradictoire du delta requise avant fusion.

## Réponse Producteur aux limites résiduelles

Après la revue du delta `09653e2`, R1–R8 sont intégrées ou enregistrées : identité RiskMap généralisée, dérivation de `reference_hash`, périmètre de mutation temporelle, statuts des oracles, dette de commit, table complète O4, ingestion des non-finis et registre NO-GO. O7 étant modifié, sa revue précédente est marquée `SUPERSEDED_PENDING_REVIEW`. Aucun gate n'est franchi par cette réponse.

La revue suivante du delta `8335ab0` a produit F1–F5. La réponse Producteur corrige O4, généralise le conflit O7 au `RiskPoint` sémantique complet, remplace le simple motif `datetime.now()` par un contrôle AST des sources temporelles et donne au NO-GO une clé causale canonique. O4 et O7 restent `PENDING_REVIEW`; le contrôle AST n'est pas encore implémenté.
