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
| delta `7039476` (`REV10`) | — | `ae5eb92` | `docs/fusion/CONTRADICTOIRE_DELTA_REV10.md` | `0a865294cdf651beae8aac3ee94cda1c5822ed989a547352ada764fb959b4470` | opérateur, 2026-08-06 |
| delta `3876fce` (`REV11bis`) | — | `102ce6a` | `docs/fusion/CONTRADICTOIRE_DELTA_REV11BIS.md` | `b6066082196fabc74e4e7657abf2fc076199a2b67d05c95965199c70697120cb` | opérateur, 2026-08-07; addendum `6f8c23695146a999a213b44ec056bea92e82e5238f3e251b1b62be82a4298e67` |
| P0 baseline, Critique | — | `804002fbbcdb8ade13309e5f49cae9452e7b741a` | `docs/fusion/CRITIQUE_P0_BASELINE.md` | `5a5df6466d4db66852163c2fb95008df3796d418f365fc9e569f6205f0c791cd` | opérateur, 2026-08-08; `ACCEPT_WITH_LIMITS` |
| P0 baseline, Contradictoire | — | `804002fbbcdb8ade13309e5f49cae9452e7b741a` | `docs/fusion/CONTRADICTOIRE_P0_BASELINE.md` | `c444e7e8c37a535afe8838e2b092ef9a0c4c2ca7828fa3aee11f6a041b4e4fb5` | opérateur, 2026-08-08; `ACCEPT_WITH_LIMITS` |

## Supersessions procédurales

| Artefact source | Remplacement admis | Motif | Manifeste |
|---|---|---|---|
| `REV09` non admis | `REV09bis` | cycle d'admission contaminé par une auto-revue Producteur rejetée; contenu scientifique indépendant inchangé | `docs/fusion/REV09_SUPERSESSION.md` au commit `4f281b7` |
| `REV11` non admis (`a837cea` invalidé) | `REV11bis` | décision opérateur liée aux hashes intermédiaires R1–R4, mais commit contenant les blobs finaux S1–S4; reprise contrôlée du contenu scientifique final inchangé | `docs/fusion/REV11_SUPERSESSION.md` au commit `102ce6a` |

## Admissions d'oracles

| Oracle ID | Commit d'admission | Rapport | SHA-256 admis | Verdict indexé | Commit d'indexation | Décision |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | aucune admission à ce jour |

Une ligne de cette table est ajoutée dans un commit d'indexation postérieur au commit d'admission. Elle doit référencer le même blob que la table générale et ne peut être déduite d'une preuve P6.

### Enregistrement machine d'un oracle

La table Markdown est une projection. La seule source machine est [`ORACLE_ADMISSIONS.json`](ORACLE_ADMISSIONS.json), jamais ce fichier Markdown ni un bloc de code. Le fichier contient exactement `{schema_version: 1, records: [...]}`. `records` est trié selon l'ordre fermé `O2`, `O4`, `O7`, contient au plus une entrée par oracle et n'accepte aucune autre clé racine ou d'enregistrement. Le JSON suit la sérialisation canonique définie dans `CAUSAL_ID_REGISTRY.md`; le blob présent est vide de toute admission.

Chaque objet de `records` se rend en exactement une ligne LF, sans CR ni espaces de début/fin :

```text
Oracle-Admission: {"admission_commit":"1111111111111111111111111111111111111111","admitted_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","oracle_id":"O2","report_path":"docs/fusion/CONTRADICTOIRE_O2.md","verdict":"ACCEPT"}
```

Grammaire de rendu : préfixe ASCII exact `Oracle-Admission: ` puis un objet JSON canonique sur une ligne, avec exactement les cinq clés montrées dans cet ordre canonique. `admission_commit` est `[0-9a-f]{40}`, `admitted_sha256` `[0-9a-f]{64}`, `oracle_id` `(O2|O4|O7)`, `report_path` `docs/fusion/[A-Za-z0-9_.-]+\.md`, `verdict` `(ACCEPT|ACCEPT_WITH_LIMITS|REJECT|NON_TESTABLE)`. Toute clé supplémentaire, doublon, échappement, chemin relatif, CR, oracle hors scope ou seconde entrée pour le même oracle invalide le fichier entier.

SHA-256 du vecteur, sans LF final : `7dcf174ee657868f5dc784973bf6cface2d62ef9ee1b51145139562f1be07067`. Le contrôleur parse uniquement `ORACLE_ADMISSIONS.json`, rejette les clés dupliquées avant construction d'objet, rend chaque entrée, exige l'égalité sémantique et recalcule ce hash. Mutants obligatoires : modifier un octet, permuter/dupliquer une clé dans l'entrée source, changer verdict/commit/hash/chemin, ajouter CR, réordonner `records` ou ajouter un doublon; tous bloquent P6.

### Évolution du registre machine

La genesis de `ORACLE_ADMISSIONS.json` est le blob vide créé au commit `3876fce12eb23daa78293a803a7a658afb5b10bc`, SHA-256 `246f867f77cfbe61fd392297925d4f498946eff28bcf3d66f62a6e22ed3c8209`. Pour une évaluation au commit `E`, la révision candidate `C` est l'unique sortie de `git rev-list --first-parent --max-count=1 E -- docs/fusion/ORACLE_ADMISSIONS.json`. Si `C` n'est pas la genesis, la révision précédente `P` est l'unique sortie de `git rev-list --first-parent --max-count=1 "C^1" -- docs/fusion/ORACLE_ADMISSIONS.json`.

Entre `P` et `C`, l'ensemble des `oracle_id` antérieurs est un sous-ensemble obligatoire du nouvel ensemble et chaque objet antérieur demeure sémantiquement identique dans sa sérialisation canonique. Une révision peut seulement ajouter un record nouvellement admis; retrait, modification, remplacement, seconde entrée du même oracle ou réintroduction produisent `ORACLE_ADMISSION_HISTORY_VIOLATION` et bloquent P6. L'ordre du tableau reste l'ordre fermé O2, O4, O7; l'ajout d'un oracle antérieur dans cet ordre peut donc déplacer un objet existant sans le modifier.

Un commit qui ne modifie pas le fichier n'est pas une nouvelle révision et valide le blob porté via son dernier `C`. Pour un merge, les blobs de tous les parents doivent être identiques au blob du premier parent et le merge ne peut modifier le fichier; sinon `ORACLE_ADMISSION_MERGE_CONFLICT`. Une union éventuelle est créée dans un commit linéaire ultérieur et doit satisfaire les règles d'ajout ci-dessus.

Mutants historiques obligatoires : retirer ou modifier un record antérieur, changer son verdict ou son ancre, dupliquer un oracle, traiter un commit non-révision comme `C`, sauter `P`, accepter des parents de merge divergents ou modifier le fichier dans un merge. Tous bloquent P6. Cette chaîne Git détecte les mutations dans l'histoire observée; elle ne remplace pas la preuve externe d'immuabilité exigée plus bas.

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
