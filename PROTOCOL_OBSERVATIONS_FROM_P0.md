# Protocol Observations from P0

**Date** : 2026-08-17
**Statut** : Notes non normatifs pour le futur Hypothesis Protocol et Admission Protocol

## Observation 1 — Le protocole Contradictoire fonctionne comme structure

Le cycle L1–L12, puis R1–R8, puis F1–F5, ... jusqu'à S1–S4 a produit une documentation d'une rigueur exceptionnelle. Chaque itération a forcé le Producteur à expliciter ses hypothèses, et chaque réponse a été traçable. **Le mécanisme de double revue (Critique + Contradictoire) avec blind review a fonctionné** : les deux rapports P0 ont identifié des limites réelles (narration causale imprécise, périmètre de couverture ambigu, artefacts hors dépôt) sans contredire les résultats fondamentaux.

**Pour le futur Hypothesis Protocol** : garder la séparation Critique/Contradictoire. Elle est supérieure à un critique unique qui fait tout.

## Observation 2 — La boucle méthodologique a un coût

Le nombre de cycles (L1–L12 + R1–R8 + F1–F5 + G1–G4 + H1–H5 + J1–J5 + K1–K5 + L1–L4 + M1–M4 + N1–N4 + O1–O4 + P1–P4 + Q1–Q4 + S1–S4 = **14 séries de constats**) est disproportionné par rapport à la taille du code (545 lignes, 11 fichiers). Chaque cycle a produit de la valeur documentaire, mais le ratio document/code est très élevé.

**Pour le futur Hypothesis Protocol** : il faut un mécanisme de "merge threshold" — au-delà d'un certain nombre de cycles sans new finding substantiel, la boucle doit pouvoir se fermer. Sinon on risque une récursion méthodologique infinie.

## Observation 3 — `status × impact × scope` est essentiel

La distinction "ce que je sais" vs "ce que cet inconnu m'empêche de faire" a résolu le problème fondamental de L12 : un oracle non revu (OPEN_PROOF) bloque P6 mais ne bloque pas P0. Sans cette distinction, P0 serait resté ouvert indéfiniment.

**Pour le futur Admission Protocol** : cette grille est obligatoire. Elle doit être le moteur de la décision d'admission, pas une succession de conditions textuelles.

## Observation 4 — Les artefacts hors dépôt créent une asymétrie

La baseline Bitget a été exécutée sur une VM Proxmox dédiée avec `pip freeze`, `coverage.xml` et un dépôt KB local. Ces artefacts ne sont pas vérifiables par un tiers sans accès à la VM. Le protocole a bien identifié cette limite (objets O3), mais elle crée une asymétrie : le dépôt restauré est entièrement reproductible depuis Git, tandis que la baseline Bitget dépend d'infrastructures externes.

**Pour le futur Admission Protocol** : les preuves doivent être reproductibles depuis le dépôt seul, ou l'infrastructure doit être documentée et reproductible (Nix le fait bien pour le dépôt restauré).

## Observation 5 — Le document de capacité manquait

`P0_PAPER_TRADING_CAPABILITY_MAP.md` n'existait pas avant cet audit. Sans lui, on pouvait clôturer P0 en se focalisant sur hashes et gates, sans savoir ce que le système fait réellement comme paper trader. C'est le document le plus important pour la transition vers P1.

**Pour le futur Admission Protocol** : chaque gate doit inclure une capability map qui répond à "qu'est-ce que ce système sait réellement faire ?"

## Observation 6 — Le protocole a du mal à s'arrêter

Le principal risque méthodologique n'est pas l'erreur, c'est la récursion. Les 14 séries de constats ont chacune produit de la valeur, mais à un moment il faut décider que "assez c'est assez" et clôturer. Le protocole n'avait pas de mécanisme d'arrêt explicite pour la phase documentaire.

**Pour le futur Hypothesis Protocol** : définir un nombre maximum de cycles ou un critère d'arrêt ("plus de new findings substantiels sur N cycles") avant de commencer.

## Observation 7 — Le contrôleur absent crée un angle mort

Toute la chaîne NO-GO, les registres causaux, les schémas JSON et les mutants sont spécifiés mais pas implémentés. La chaîne documentaire est cohérente, mais aucun code ne la valide mécaniquement. C'est un risque pour P1+.

**Pour le futur Admission Protocol** : l'admission ne devrait pas dépendre de contrôleur absent. Soit le contrôleur est implémenté avant l'admission, soit l'admission est manuelle et documentée.

## Observation 8 — Deux protocoles distincts, pas un

L'analyse comparative La Barre/Fusion montre que la "production de connaissance" (Fusion) et l'"admission opérationnelle" (La Barre) sont deux choses distinctes. Forcer un seul protocole à tout faire crée de la complexité. Le noyau commun minimal (Producteur, Critique, Contradictoire, preuve, historique) est suffisant.

**Pour la suite** : ne pas chercher à fusionner les deux protocoles. Les laisser évoluer séparément avec un noyau partagé.
