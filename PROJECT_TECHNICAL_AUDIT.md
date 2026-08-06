# Audit technique final

## Structure

Paquet Python stable `paper_trading_codex`, sept fichiers de tests, quatre configurations, trois exemples, scripts de statut/reproductibilité, environnement Nix verrouillé, CI et documentation normative.

## Corrections appliquées

| Domaine | Correction |
|---|---|
| métriques | Sortino défini avec downside deviation; Calmar avec CAGR |
| comptabilité | suppression du double débit des frais d'achat |
| short | quantité contractuelle explicite; levier appliqué une fois |
| liquidation | formule simplifiée dérivée et assomption de perte séparée |
| audit | identifiants publics, TP/SL/MTM, échec sur zéro paire |
| événements | MTM et liquidation inclus dans les statistiques de clôture |
| RNG | générateur local seedable |
| packaging | licence MIT incluse dans wheel/sdist |
| documentation | hypothèses, méthodes, limites, statut et révision ajoutés |

## Résultats

- Pytest : 68 réussis, 0 échec, 0 skip;
- couverture : 87,07 % lignes et branches;
- Ruff : zéro erreur;
- build : wheel et sdist réussis;
- wheel hors dépôt : 68 tests réussis;
- Nix : environnement Python 3.12.12 utilisé;
- réseau : bloqué pendant tous les tests.

## Erreurs restantes

Aucune erreur technique bloquante observée dans le périmètre testé. Restent des limites de modèle et une CI distante non observée, documentées dans `LIMITATIONS.md` et l'audit de publication.
