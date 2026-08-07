# Supersession procédurale REV11 → REV11bis

## Incident

La session Contradictoire indépendante `dde43829` a écrit une version intermédiaire R1–R4 et signalé prématurément sa disponibilité à `00:13:58` EDT. Elle a poursuivi son analyse puis écrit la version finale S1–S4 à `00:26:19–00:27:52`.

L'opérateur avait admis les hashes de la version intermédiaire. Le commit `a837cea` contient les blobs finaux, différents des blobs admis; `3415cb3` invalide donc cette tentative et aucune ligne REV11 n'existe dans le registre d'admission.

## Décision

| Artefact | Statut |
|---|---|
| version intermédiaire REV11 R1–R4 | `SUPERSEDED_INCOMPLETE`, non admise |
| commit `a837cea` | `INVALID_ADMISSION_HASH_MISMATCH`, non indexé |
| version finale REV11 S1–S4 | source historique conservée |
| REV11bis S1–S4 | candidat à admission après addendum Contradictoire |

REV11bis reprend la version finale sans changement scientifique. Seuls le titre, la provenance, l'objet du heartbeat et son lien de rapport sont adaptés. Cette supersession ne vaut ni admission ni franchissement de gate.

## Correction procédurale requise

Les futurs producteurs Contradictoires écrivent sous noms temporaires, publient le heartbeat en dernier par renommage atomique et ne signalent la revue qu'après gel et arrêt de la session. Le Producteur vérifie deux hashes stables avant de demander l'admission.
