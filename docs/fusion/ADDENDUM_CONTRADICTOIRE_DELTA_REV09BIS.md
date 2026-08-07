# Addendum Contradictoire — traitement de REV09bis (reprise procédurale)

## Objet

Traitement par l'IA Contradictoire du candidat d'admission `CONTRADICTOIRE_DELTA_REV09BIS.md` et `HEARTBEAT_CONTRADICTOIRE_DELTA_REV09BIS.md`, créés par le Producteur en application de `REV09_SUPERSESSION.md` (décision opérateur : `REV09` supersédé `SUPERSEDED_PROCEDURAL`, non admis; `REV09bis` = copie contrôlée seule admise à l'admission).

## Vérifications mécaniques

- `diff docs/fusion/CONTRADICTOIRE_DELTA_REV09.md docs/fusion/CONTRADICTOIRE_DELTA_REV09BIS.md` : la seule différence est le titre (ligne 1) et l'ajout de la section « Provenance de la reprise » (5 lignes). Aucune valeur numérique, aucun hash, aucune conclusion, aucun verdict ni aucune limite P1–P4 modifiés.
- `diff` des heartbits : titre, ligne « Provenance », libellé « Objet » et lien « Rapport complet » seulement.
- Cohérence avec la revendication Producteur : « les ajouts se limitent à l'identité de reprise, à la provenance et aux liens de fichiers » — **confirmé**.
- `REV09` non admis : le registre d'admission compte neuf entrées (jusqu'à `a7c8a69`/`REV08`); aucun rapport `REV09` n'y figure. Statut `SUPERSEDED_PROCEDURAL` cohérent.

## Indépendance

Aucun fichier de la contamination n'a été lu : ni les artefacts `docs/deepsearch/*` (auto-revues Producteur, dont `qwen_fail_jenerepondpasauxquestions.md`), ni les `CRITIQUE_*`. Le verdict gelé reste exclusivement celui du rapport indépendant `REV09`, inchangé.

## Position Contradictoire

- Le contenu scientifique de `REV09bis` est **identique** à celui du rapport Contradictoire indépendant.
- Verdict inchangé : **ACCEPT_WITH_LIMITS** avec les limites P1–P4 (grammaire de la ligne du registre des verdicts; couverture des vecteurs; linéarité du chaînage du registre; schéma de l'événement `SUPERSEDED`).
- La reprise est **procéduralement valide** : elle n'ajoute aucune indépendance, ne modifie aucune conclusion et ne fausse aucune vérification. `REV09bis` peut être soumis à l'admission.
- L'admission reste une décision opérateur explicite; l'IA Contradictoire ne committe rien.
- Aucun gate n'est franchi : P6 reste `BLOCKED_IMMUTABILITY` (table d'admissions d'oracles vide, preuve d'immuabilité externe absente).

## Note d'orchestration

Le watcher local a été abandonné (surveillance par script inefficace). Un orchestrateur externe (type `rublo`) est requis pour déclencher les cycles : détection des nouveaux `REVIEW_REQUEST_*`, admission, et réveil de l'IA Contradictoire.
