# Registre d'admission des revues

## Ancre normative

L'ancre d'un rapport est le blob Git contenu dans son **commit d'admission distinct**, approuvé par l'opérateur avant toute réponse Producteur. Le registre est un index vérifiable, pas l'autorité du hash.

Contrôle : `admission_commit` doit être ancêtre du commit évalué; `git show admission_commit:report_path` doit exister; son SHA-256 doit égaler `admitted_sha256`; le commit d'admission ne contient pas la modification Producteur qu'il évalue. Modifier ensemble rapport et preuve dans un commit ultérieur ne change donc pas le blob historique ancré.

## Admissions

`Oracle scope` est un ensemble fermé d'identifiants (`O2`, `O4`, `O7`) explicitement nommés par le rapport. `—` signifie que la revue historique ne constitue aucune preuve d'oracle. Une preuve P6 n'est admissible que si son `oracle_id` appartient exactement à cette colonne et à la table **Admissions d'oracles** ci-dessous, et si le blob admis contient exactement une ligne normative ancrée de forme `Oracle-Review: oracle_id=O2; verdict=ACCEPT`. L'expression complète est `^Oracle-Review: oracle_id=(O2|O4|O7); verdict=(ACCEPT|ACCEPT_WITH_LIMITS|REJECT|NON_TESTABLE)$`, en ASCII, sans espaces supplémentaires.

Le blob est découpé uniquement sur l'octet LF (`0A`). Une **ligne candidate** commence à l'octet 0 par les 14 octets ASCII `Oracle-Review:`. Une ligne indentée, citée ou préfixée n'est pas candidate. Il doit exister exactement une candidate et elle doit correspondre entièrement à l'expression normative; toute candidate supplémentaire ou mal formée invalide le rapport. Tout CR (`0D`) sur une candidate l'invalide; aucune normalisation CRLF n'est effectuée.

Le verdict extrait doit égaler `Verdict indexé` dans le blob du registre au `registry_commit` fourni par la preuve P6. Ce commit doit être distinct, postérieur au commit d'admission, ancêtre du commit P6 et contenir une ligne `{oracle_id, admission_commit, report_path, admitted_sha256, verdict}` concordante. La preuve contient aussi `registry_blob_sha256`, recalculé par le contrôleur. Changer ultérieurement le verdict indexé, utiliser un autre commit de registre ou indexer un verdict divergent bloque P6; `recorded_status` courant ne fait jamais autorité.

| Objet revu | Oracle scope | Commit d'admission | Rapport | SHA-256 admis | Décision |
|---|---|---|---|---|---|
| delta `8335ab0` | — | `a1e9892` | `docs/fusion/CONTRADICTOIRE_DELTA_8335AB0.md` | `5bec97caed707a5171269c4731c322ac8e0a5c844f5174c15dd3886a1ea1bade` | opérateur, 2026-08-06 |
| delta `4225bc5` | — | `0d9bc06` | `docs/fusion/CONTRADICTOIRE_DELTA_4225BC5.md` | `ef11a60f949ab12e019c11605624ca08a9bf3162b8a5679cac7b2f45eb6550d1` | opérateur, 2026-08-06 |
| delta `894b585` | — | `4b920b4` | `docs/fusion/CONTRADICTOIRE_DELTA_894B585.md` | `db87ec2a649c3f88cc46b38a7f26e9ea66575b49658181e5bef75186f3e0e74d` | opérateur, 2026-08-06 |
| delta `ca8de4f` | — | `f8f0a2e` | `docs/fusion/CONTRADICTOIRE_DELTA_CA8DE4F.md` | `ef29e9dbd87e411a75f17955ded3b53f121ffe19b0552fa40afae80690bb73d0` | opérateur, 2026-08-06 |
| delta `58e11cb` | — | `1fdc5eb` | `docs/fusion/CONTRADICTOIRE_DELTA_58E11CB.md` | `1ba611239e075910603a10d70a40b762a7b2f595e443dfdcdc467ba42cce1e99` | opérateur, 2026-08-06 |
| delta `decbb42` | — | `02775ce` | `docs/fusion/CONTRADICTOIRE_DELTA_DECBB42.md` | `97cb352468a4e828b78ce6af5078f50ee2c54e71200f0b1a9cc6781183cfb2d1` | opérateur, 2026-08-06 |
| delta `dd4cdde` | — | `5a8ebe2` | `docs/fusion/CONTRADICTOIRE_DELTA_DD4CDDE.md` | `ede8f51e082327e3a6e886cd716f4dcc027bc283bd43669fa7998f86f967257b` | opérateur, 2026-08-06 |
| delta `f14546f` | — | `cf6aa7a` | `docs/fusion/CONTRADICTOIRE_DELTA_F14546F.md` | `3ec01a4ee0082e59b77a6d2616f06e90162c9ffdc63d01fbfa82cdd0051fbf0d` | opérateur, 2026-08-06 |
| delta `930b0f9` (`REV08`) | — | `a7c8a69` | `docs/fusion/CONTRADICTOIRE_DELTA_REV08.md` | `30ac34a795b1404ee416941f5fa06ad38aeee8bc1ec76cbee72c16cc60b65a64` | opérateur, 2026-08-06 |
| delta `6867a2d` (`REV09bis`) | — | `4f281b7` | `docs/fusion/CONTRADICTOIRE_DELTA_REV09BIS.md` | `981e5b083e7382087f1f3153fe144c98348a0bb1e77c15ffb910ce36675f7085` | opérateur, 2026-08-06; addendum `77c75221b779092c1712a75e2411a79873fd046189752c062bae733c8693a42a` |

## Supersessions procédurales

| Artefact source | Remplacement admis | Motif | Manifeste |
|---|---|---|---|
| `REV09` non admis | `REV09bis` | cycle d'admission contaminé par une auto-revue Producteur rejetée; contenu scientifique indépendant inchangé | `docs/fusion/REV09_SUPERSESSION.md` au commit `4f281b7` |

## Admissions d'oracles

| Oracle ID | Commit d'admission | Rapport | SHA-256 admis | Verdict indexé | Commit d'indexation | Décision |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | aucune admission à ce jour |

Une ligne de cette table est ajoutée dans un commit d'indexation postérieur au commit d'admission. Elle doit référencer le même blob que la table générale et ne peut être déduite d'une preuve P6.

### Enregistrement machine d'un oracle

La table Markdown est une projection. L'enregistrement autoritaire est exactement une ligne LF, sans CR ni espaces de début/fin :

```text
Oracle-Admission: {"admission_commit":"1111111111111111111111111111111111111111","admitted_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","oracle_id":"O2","report_path":"docs/fusion/CONTRADICTOIRE_O2.md","verdict":"ACCEPT"}
```

Grammaire : préfixe ASCII exact `Oracle-Admission: ` puis un objet JSON canonique sur une ligne, avec exactement les cinq clés montrées dans cet ordre canonique. `admission_commit` est `[0-9a-f]{40}`, `admitted_sha256` `[0-9a-f]{64}`, `oracle_id` `(O2|O4|O7)`, `report_path` `docs/fusion/[A-Za-z0-9_.-]+\.md`, `verdict` `(ACCEPT|ACCEPT_WITH_LIMITS|REJECT|NON_TESTABLE)`. Toute clé supplémentaire, doublon, échappement, chemin relatif, CR ou seconde ligne pour le même oracle invalide l'index.

SHA-256 du vecteur, sans LF final : `7dcf174ee657868f5dc784973bf6cface2d62ef9ee1b51145139562f1be07067`. Le contrôleur reconstruit la ligne depuis les champs parsés, exige l'égalité octet-pour-octet puis recalcule ce hash. Mutants obligatoires : modifier un octet, permuter/dupliquer une clé, changer verdict/commit/hash/chemin, ajouter CR ou une seconde ligne; tous bloquent P6.

## Mutations bloquantes

- rapport courant différent du blob admis;
- commit d'admission non ancêtre;
- chemin absent au commit d'admission;
- hash indexé différent du blob;
- admission et réponse Producteur dans le même commit;
- verdict/statut enregistré différent du rapport ancré.
- `oracle_id` absent du scope indexé ou de l'unique ligne normative exacte du rapport.
- enregistrement `Oracle-Admission` absent, non canonique, dupliqué ou divergent du rapport.

Toute réécriture d'historique invalide les admissions jusqu'à nouvelle décision opérateur. **Avant toute exécution ou revendication de P6**, le Producteur doit fournir l'une des preuves suivantes : règle de protection distante interdisant force-push et suppression sur la branche contenant les admissions, exportée et hashée; ou archive Git signée couvrant les commits d'admission, avec identité du signataire et commande de vérification. Sans artefact vérifiable, P6 est `BLOCKED_IMMUTABILITY`, même si tous les hashes concordent. La même preuve reste obligatoire pour la publication finale.
