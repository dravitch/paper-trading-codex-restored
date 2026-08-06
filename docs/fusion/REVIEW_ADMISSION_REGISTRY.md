# Registre d'admission des revues

## Ancre normative

L'ancre d'un rapport est le blob Git contenu dans son **commit d'admission distinct**, approuvé par l'opérateur avant toute réponse Producteur. Le registre est un index vérifiable, pas l'autorité du hash.

Contrôle : `admission_commit` doit être ancêtre du commit évalué; `git show admission_commit:report_path` doit exister; son SHA-256 doit égaler `admitted_sha256`; le commit d'admission ne contient pas la modification Producteur qu'il évalue. Modifier ensemble rapport et preuve dans un commit ultérieur ne change donc pas le blob historique ancré.

## Admissions

`Oracle scope` est un ensemble fermé d'identifiants (`O2`, `O4`, `O7`) explicitement nommés par le rapport. `—` signifie que la revue historique ne constitue aucune preuve d'oracle. Une preuve P6 n'est admissible que si son `oracle_id` appartient exactement à cette colonne et si le blob admis contient exactement une ligne normative ancrée de forme `Oracle-Review: oracle_id=O2; verdict=ACCEPT`, où l'ID appartient à `{O2,O4,O7}` et le verdict à `{ACCEPT,ACCEPT_WITH_LIMITS,REJECT,NON_TESTABLE}`. L'expression complète est `^Oracle-Review: oracle_id=(O2|O4|O7); verdict=(ACCEPT|ACCEPT_WITH_LIMITS|REJECT|NON_TESTABLE)$`, en ASCII, sans espaces supplémentaires. Une phrase, citation ou sous-chaîne ne correspond pas. Le verdict extrait doit être celui indexé pour cet oracle. Le contrôleur lit le blob au commit d'admission; la preuve courante ne fait pas autorité.

| Objet revu | Oracle scope | Commit d'admission | Rapport | SHA-256 admis | Décision |
|---|---|---|---|---|---|
| delta `8335ab0` | — | `a1e9892` | `docs/fusion/CONTRADICTOIRE_DELTA_8335AB0.md` | `5bec97caed707a5171269c4731c322ac8e0a5c844f5174c15dd3886a1ea1bade` | opérateur, 2026-08-06 |
| delta `4225bc5` | — | `0d9bc06` | `docs/fusion/CONTRADICTOIRE_DELTA_4225BC5.md` | `ef11a60f949ab12e019c11605624ca08a9bf3162b8a5679cac7b2f45eb6550d1` | opérateur, 2026-08-06 |
| delta `894b585` | — | `4b920b4` | `docs/fusion/CONTRADICTOIRE_DELTA_894B585.md` | `db87ec2a649c3f88cc46b38a7f26e9ea66575b49658181e5bef75186f3e0e74d` | opérateur, 2026-08-06 |
| delta `ca8de4f` | — | `f8f0a2e` | `docs/fusion/CONTRADICTOIRE_DELTA_CA8DE4F.md` | `ef29e9dbd87e411a75f17955ded3b53f121ffe19b0552fa40afae80690bb73d0` | opérateur, 2026-08-06 |
| delta `58e11cb` | — | `1fdc5eb` | `docs/fusion/CONTRADICTOIRE_DELTA_58E11CB.md` | `1ba611239e075910603a10d70a40b762a7b2f595e443dfdcdc467ba42cce1e99` | opérateur, 2026-08-06 |
| delta `decbb42` | — | `02775ce` | `docs/fusion/CONTRADICTOIRE_DELTA_DECBB42.md` | `97cb352468a4e828b78ce6af5078f50ee2c54e71200f0b1a9cc6781183cfb2d1` | opérateur, 2026-08-06 |
| delta `dd4cdde` | — | `5a8ebe2` | `docs/fusion/CONTRADICTOIRE_DELTA_DD4CDDE.md` | `ede8f51e082327e3a6e886cd716f4dcc027bc283bd43669fa7998f86f967257b` | opérateur, 2026-08-06 |

## Mutations bloquantes

- rapport courant différent du blob admis;
- commit d'admission non ancêtre;
- chemin absent au commit d'admission;
- hash indexé différent du blob;
- admission et réponse Producteur dans le même commit;
- verdict/statut enregistré différent du rapport ancré.
- `oracle_id` absent du scope indexé ou de l'unique ligne normative exacte du rapport.

Toute réécriture d'historique invalide les admissions jusqu'à nouvelle décision opérateur. **Avant toute exécution ou revendication de P6**, le Producteur doit fournir l'une des preuves suivantes : règle de protection distante interdisant force-push et suppression sur la branche contenant les admissions, exportée et hashée; ou archive Git signée couvrant les commits d'admission, avec identité du signataire et commande de vérification. Sans artefact vérifiable, P6 est `BLOCKED_IMMUTABILITY`, même si tous les hashes concordent. La même preuve reste obligatoire pour la publication finale.
