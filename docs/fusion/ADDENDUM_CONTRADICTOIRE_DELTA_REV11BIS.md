# Addendum Contradictoire — traitement de REV11bis (reprise finale de REV11)

## Objet

Traitement par l'IA Contradictoire du candidat d'admission `CONTRADICTOIRE_DELTA_REV11BIS.md` et `HEARTBEAT_CONTRADICTOIRE_DELTA_REV11BIS.md`, créés par le Producteur en application de `REV11_SUPERSESSION.md` et à la demande de `REVIEW_REQUEST_REV11BIS_ADDENDUM.md` (incident : la session indépendante `dde43829` a signalé prématurément une version intermédiaire R1–R4; la version finale S1–S4 a été admise par erreur sous `a837cea` puis invalidée par `3415cb3`).

## Vérifications mécaniques

- `diff docs/fusion/CONTRADICTOIRE_DELTA_REV11.md docs/fusion/CONTRADICTOIRE_DELTA_REV11BIS.md` : seule la ligne 1 (titre) diffère et la section « Provenance de la reprise » (5 lignes) est ajoutée. Aucune valeur, aucun hash, aucune conclusion, aucun verdict ni aucune limite S1–S4 modifiés.
- `diff` des heartbits : titre et note de reprise (3 lignes), libellé « Objet », lien « Rapport : » seulement. Aucun champ de verdict, limite ou gate modifié.
- Contenu scientifique de REV11bis = contenu de la version finale REV11 (blobs `7e6f3e6d…`/`8d0e9a76…`), qui sont aussi les blobs du commit `a837cea` (vérifié : `git show a837cea:<file> | sha256sum` = `7e6f3e6d…` et `8d0e9a76…`).
- Hashs de la décision opérateur (`a1966b62…`/`d1fab028…`) ≠ blobs committés (`7e6f3e6d…`/`8d0e9a76…`) → motif d'invalidation cohérent. Aucune ligne REV11 au registre d'admission (vérifié par `grep`).
- Cible (`3876fce`), verdict (`ACCEPT_WITH_LIMITS`), limites finales (S1–S4) et contenu des réfutations : identiques entre REV11 final et REV11bis.

## Indépendance

Aucun fichier Contradictoire autre que les deux candidats REV11bis et les documents procéduraux Produits n'a été lu pour ce traitement. La conclusion gelée reste celle du rapport indépendant `REV11` (version finale S1–S4), inchangée; aucune auto-revue n'a été utilisée.

## Position Contradictoire

- R1–R4 est bien une version intermédiaire du même run indépendant (`dde43829`), signalée prématurément; S1–S4 en est la version finale. Les deux sont issues de la même session indépendante, et non de deux revues distinctes.
- Le contenu scientifique de `REV11bis` est **identique** à celui du rapport Contradictoire indépendant final : cible, vérifications, valeurs, verdict `ACCEPT_WITH_LIMITS` et limites S1–S4 inchangés.
- La reprise est **procéduralement recevable à l'admission** : elle n'ajoute aucune indépendance, ne modifie aucune conclusion, ne fausse aucune vérification. Conformément à la demande, elle ne prétend pas à une nouvelle revue.
- L'admission reste une décision opérateur explicite; l'IA Contradictoire ne committe rien.
- Aucun gate n'est franchi : P6 reste `BLOCKED_IMMUTABILITY` (registre machine vide, table d'admissions d'oracles vide, preuve d'immuabilité externe absente).

## Note d'orchestration

Cet addendum se substitue à l'ancien heartbeat du run interrompu (qui mentionnait des limites R1–R4). Toute admission future de REV11bis devra vérifier les hashes des blobs stables avant décision, conformément à la correction procédurale de `REV11_SUPERSESSION.md`.
