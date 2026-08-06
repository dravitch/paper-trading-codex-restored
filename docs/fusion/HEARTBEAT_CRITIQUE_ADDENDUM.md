# Heartbeat — IA Critique, addendum de métadonnées

## Provenance

Ce fichier transcrit l'addendum fourni par l'IA Critique. Une adresse email destinataire a été retirée avant publication : elle n'ajoutait aucune preuve et constituait une donnée personnelle.

## Identité et contexte déclarés

- rôle : IA Critique;
- modèle : Claude, interface de chat Anthropic;
- version exacte : `UNKNOWN`, non communicable de façon fiable par auto-déclaration;
- date de session : 2026-08-06;
- révision Git examinée : `UNKNOWN`;
- accès déclaré : documents transmis en conversation, sans clone ni accès direct au dépôt;
- statut maintenu : `ADMITTED_AS_REVIEW_WITH_LIMITS`.

## Exécution déclarée

Aucun `pytest`, Ruff ou autre contrôle n'a été exécuté contre le dépôt réel. L'IA déclare une recherche filesystem sans résultat et des recalculs manuels documentés dans la revue. Les mentions de résultats globaux de tests ou lint provenaient donc des rapports du Producteur et non d'une reproduction indépendante.

## Indépendance déclarée

L'IA Critique confirme avoir reçu et lu `CONTRADICTOIRE_FEASIBILITY.md` avant son premier verdict. Elle conclut elle-même : **indépendance non garantie pour ce cycle**. Une nouvelle revue Critique, sans rapport Contradictoire dans son contexte initial et avec accès réel au dépôt, est requise si l'indépendance stricte conditionne la fusion.

## Correction sur Bitget et le Canada

La formulation antérieure « indisponible après le 15 août » est retirée comme fait établi. Une pièce privée transférée, datée du 30 juin 2026, décrit :

- 15 août 2026, 00:00 CST : fermeture et retraits uniquement;
- 30 août 2026, 23:59 CST : date limite de retrait;
- 31 août 2026, 00:00 CST : fermeture du compte.

Cette pièce n'a pas été authentifiée par en-têtes SMTP, DKIM/SPF ou second canal officiel. Son calendrier reste donc `β=B`, source unique non authentifiée, et ne doit pas être gravé dans une norme.

Vérification Producteur du 2026-08-06 : les [Conditions d'utilisation officielles Bitget](https://www.bitget.com/en-CA/support/articles/360014944032-terms-of-use), indiquées comme mises à jour le 16 juin 2026, incluent le Canada dans les « Prohibited Countries ». Cette source confirme la restriction juridictionnelle générale, mais ne confirme pas les dates du 15, 30 et 31 août. Le calendrier précis demeure `UNKNOWN`.

## FAIL `40099`

Le verdict Critique demeure inchangé : `data_fetcher.py` et `exchange_simulator.py` présentent l'erreur Bitget Demo `40099` comme permanente sans date ni provenance. Il s'agit d'un défaut de traçabilité documentaire, indépendamment de tout calendrier canadien.

## Effet procédural

L'addendum améliore l'honnêteté de la provenance, mais ne fournit ni SHA Git examiné, ni exécution reproductible, ni indépendance de lecture. Il ne transforme donc pas la revue initiale en seconde validation conforme et ne franchit aucun gate.
