# Rapport Contradictoire — delta REV09bis (reprise procédurale de REV09)

## Provenance de la reprise

Copie contrôlée par le Producteur du rapport Contradictoire indépendant `CONTRADICTOIRE_DELTA_REV09.md`. Le contenu scientifique, la cible `6867a2d`, le verdict et les limites P1–P4 sont inchangés. Cette copie ne constitue pas une seconde revue et ne crée aucune indépendance supplémentaire. `REV09` est supersédé uniquement comme objet d'admission à cause de l'échec procédural antérieur; il reste conservé comme source historique non admise.

## Objet examiné

Commit Producteur `6867a2db063321cd39636f87a741452396d93ca7` « docs: resolve contradictory findings O1-O4 », branche `correction/reconcile-l1-l12`, cible `fusion/controlled-merger`. Portée : réponse aux constats O1–O4 de `CONTRADICTOIRE_DELTA_REV08.md` (admis au commit `a7c8a69`), documentée dans `REV09.md`, conformément à `docs/fusion/REVIEW_REQUEST_O1_O4.md`. Delta documentaire : `REV09.md` créé; `PROGRESSION.md`, `docs/fusion/06_FUSION_GATES.md`, `CAUSAL_ID_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md`, `NO_GO_CYCLE_REGISTRY.json`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md` modifiés. Aucun contrôleur n'est implémenté.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `6867a2db063321cd39636f87a741452396d93ca7` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict (aucun fichier `CRITIQUE_*` relatif à `REV09` consulté) |

## Vérifications préalables d'intégrité et sortie attendue

- Admission `a7c8a69` réelle : contenu limité au rapport + heartbit, ancêtre de `6867a2d` (vérifié par `git merge-base --is-ancestor`), `6867a2d` ancêtre de la révision courante `608493b`, non ancêtre de `a7c8a69`.
- Réfutation 5 exécutée mécaniquement. Commandes : `git show <admission_commit>:<report_path> | sha256sum` pour les neuf lignes du registre; `python3 -m json.tool docs/fusion/NO_GO_CYCLE_REGISTRY.json`; sérialisation canonique récursive (tri des clés à tous les niveaux) en Python pour les deux vecteurs; `git show 930b0f9:docs/fusion/NO_GO_CYCLE_REGISTRY.json | sha256sum` pour la genesis; comparaison de `previous_blob_sha256` au SHA du blob au `parent_registry_commit`.
- Résultat : **les neuf SHA-256 concordent exactement** (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb, 02775ce, 5a8ebe2, cf6aa7a, a7c8a69), le JSON est valide (`schema_version:1`, `genesis_commit`/`parent_registry_commit` = `930b0f9`, `previous_blob_sha256` = `4ff3bef1…`), le blob au commit `930b0f9` a bien pour SHA-256 `4ff3bef1ba8d0005dcacdc0dd381d523e821a1c9d28549ebc847a74f6db046fb` (= `previous_blob_sha256` courant), le vecteur canonique produit `51857ebbbcc0155f75bf33ae635a6f865a17e74cd324a7cd063c1ef3b47375e6` et le vecteur étendu `eacf3f8071439cd6315c7693159449aeb6f9988a727eba234ab063da9f7e7563`. Code de sortie 0 sur toutes les vérifications.
- Table **Admissions d'oracles** vide (`aucune admission à ce jour`) → aucune preuve P6 admissible; `Oracle scope` = `—` pour les neuf blobs admis.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Faire accepter une candidate citée/préfixée, deux candidates, ou modifier rétroactivement le verdict indexé sans blocage P6 | **Échoue.** « Une ligne candidate commence à l'octet 0 par les 14 octets ASCII `Oracle-Review:` »; une ligne indentée, citée ou préfixée n'est pas candidate → zéro candidate rend le rapport invalide (exactement une candidate exigée); toute candidate supplémentaire ou mal formée invalide. Le `Verdict indexé` est lu dans le blob du registre au `registry_commit` fourni par la preuve (distinct, postérieur à l'admission, ancêtre du commit P6, recalculé par le contrôleur); « changer ultérieurement le verdict indexé, utiliser un autre commit de registre ou indexer un verdict divergent bloque P6 » et `recorded_status` courant ne fait jamais autorité. Réserve **P1** |
| 2 | Produire un encodage canonique alternatif conforme pour NFC, slash, contrôles ou Unicode; recalculer les deux vecteurs | **Échoue.** NFC exigé, surrogate rejeté (jamais normalisé silencieusement), échappements exhaustifs (`"`, `\`, `\b`, `\t`, `\n`, `\f`, `\r`, autres U+0000–U+001F en `\u00xx` minuscule), `/` jamais échappé, non-ASCII NFC direct en UTF-8, sans BOM ni fin de ligne. Les deux vecteurs recalculés concordent exactement (`51857e…75e6` et `eacf3f…7563`); NFD et slash échappé produisent des octets différents du vecteur attendu → rejetés. Réserve **P2** |
| 3 | Contester la chaîne genesis `930b0f9` → blob courant, retirer une entrée, ou réinitialiser via migration de schéma | **Échoue comme exploit, linéarité du chaînage non close.** Genesis explicitement ancrée : blob au commit `930b0f9`, SHA `4ff3bef1…`, vérifié égal au blob réel de ce commit; le successeur la cite dans `genesis_commit`, `parent_registry_commit` et `previous_blob_sha256`; le blob courant `a7ad22af…` chaîne exactement (`parent_registry_commit` = `930b0f9`, `previous_blob_sha256` = `4ff3bef1…` = SHA du blob parent). `f14546f` déclaré pré-genesis documentaire sans données. Retrait : listes vides + sous-ensembles obligatoires + identité octet-pour-octet → `REGISTRY_HISTORY_VIOLATION`. Migration : `schema_version` immuable dans une chaîne, manifeste revu reliant genesis source et cible, conservation exhaustive des identités, jamais de réinitialisation. Réserve **P3** |
| 4 | Superséder une occurrence en réutilisant son ID, en supprimant l'ancienne ou en créant un trou sans rejet | **Échoue.** Une correction référence un `occurrence_id` existant dans `supersedes_occurrence_id` (référence ≠ proposition d'ID neuf); le contrôleur vérifie l'existence puis alloue au remplacement le prochain ID contigu; l'ancienne entrée demeure immuable, compte dans `len(occurrences)`, devient `SUPERSEDED` par événement annexe append-only, son suffixe n'est jamais libéré; réutilisation, suppression ou trou → séquence exacte violée. Réserve **P4** |
| 5 | Vérifier le JSON, les neuf hashes d'admission, les hashes genesis/vecteurs et les contradictions inter-documents | **Satisfaite — vérifié.** JSON valide; neuf hashes concordants; genesis `4ff3bef1…` et vecteurs `51857e…`/`eacf3f…` concordants; chaîne parent valide; admission `a7c8a69` ancêtre, distincte et limitée au rapport + heartbit; aucune contradiction bloquante inter-documents (REV09 ↔ registre JSON ↔ NO_GO_REGISTER ↔ CAUSAL_ID_REGISTRY ↔ LIMIT_RESOLUTION_REGISTER ↔ PROGRESSION) |

## Constats

### P1 — Registre des verdicts : la ligne de la table d'oracles n'a pas de grammaire mécanique

Le verdict indexé est ancré (commit distinct, postérieur, ancêtre, blob recalculé), mais la « ligne `{oracle_id, admission_commit, report_path, admitted_sha256, verdict}` concordante » que le contrôleur doit lire dans le blob du registre au `registry_commit` n'a aucune syntaxe formelle : séparateur de table Markdown, ordre des colonnes, espaces, échappement du chemin, forme du verdict. Aucun vecteur ni mutation (modifier un octet de la ligne du registre) n'est prescrit. **Effet : le même défaut que celui fermé pour le marqueur du rapport (O1) se déplace vers la ligne du registre — deux implémentations peuvent parser différemment un même blob.** Action : donner une grammaire et un vecteur à cette ligne, ajouter la mutation octet.

### P2 — Vecteurs : clés non ASCII, échappements `\u00xx` et rejets NFC/surrogate non falsifiés

Le contrat de sérialisation est désormais complet et déterministe, et les deux vecteurs concordent. Mais le vecteur étendu ne couvre ni une clé non-ASCII (donc le tri par valeur scalaire Unicode n'est pas éprouvé sur des clés non NFC-equivalentes), ni un contrôle U+0000–U+001F autre que `\n` (le codage `\u00xx` minuscule n'est pas vectorisé), ni un cas de rejet (entrée NFD ou contenant un surrogate — le texte dit « rejetée, jamais normalisée silencieusement » mais aucune fixture de rejet n'est définie). **Effet : le contrat est énoncé mais non falsifié pour ces trois cas.** Action : étendre le vecteur (clé non-ASCII, `\u0000`/`\u001f`) et prescrire au moins un test de rejet NFC/surrogate.

### P3 — Registre : la linéarité du chaînage entre deux révisions Git n'est pas close

Genesis et premier successeur sont explicitement ancrés et vérifiés. Mais `parent_registry_commit` est déclaré librement : « nomme le commit exact dont le blob est chaîné » sans exiger qu'il soit la **révision du registre immédiatement précédente** dans l'historique Git du fichier. Un blob ultérieur pourrait citer une genesis antérieure comme parent (sous-ensembles vides trivials, `previous_blob_sha256` correct), sautant les écritures intermédiaires du registre et les retirant de fait de la chaîne, sans déclencher `REGISTRY_HISTORY_VIOLATION`. « Append-only entre deux révisions Git » est ambigu : deux commits quelconques ou deux révisions consécutives du fichier ? **Effet : le retrait d'une écriture intermédiaire par « saut de parent » n'est pas mécaniquement fermé.** Action : exiger `parent_registry_commit` = dernier commit antérieur ayant modifié le fichier (ou champ `parent_blob_sha256` vérifié contre l'historique), et un mutant de saut.

### P4 — Supersession : l'« événement annexe append-only » `SUPERSEDED` n'a ni schéma ni emplacement

La règle 9 des occurrences (`occurrence_id`, `first_recorded_commit`, `cycle_id`, `causal_payload_sha256`) ne contient ni champ `status` ni champ `supersedes_occurrence_id`. La supersession « prend le statut terminal `SUPERSEDED` par un événement annexe append-only » sans définir ce qu'est cet événement : format JSON, fichier, rattachement à la chaîne d'immuabilité du registre, jonction par le contrôleur, et comment le remplacement référence l'ID antérieur. **Effet : le comportement de rejet est correct, la représentation machine est indéfinie — un contrôleur ne peut pas l'implémenter déterministiquement.** Action : normer l'événement annexe (schéma, emplacement, chaîne) ou étendre le schéma JSON des occurrences.

## Verdict

**ACCEPT_WITH_LIMITS**

Les cinq réfutations échouent dans leur périmètre : candidate citée/préfixée et deux candidates rejetées, verdict indexé ancré au `registry_commit` (modification rétroactive bloquée), encodage canonique NFC/échappements exhaustifs avec les deux vecteurs recalculés et concordants, genesis `930b0f9`/`4ff3bef1…` vérifiée et chaîne courante exacte, retrait/migration non ouvrants, supersession avec ID réutilisé/supprimé/trou rejetée, et le JSON, les neuf hashes d'admission, les hashes genesis/vecteurs et la chaîne parent sont vérifiés concordants.

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs :

- **P1** — donner une grammaire et un vecteur à la ligne de la table d'admissions d'oracles lue au `registry_commit`, ajouter la mutation octet;
- **P2** — étendre le vecteur (clé non-ASCII, `\u00xx`) et prescrire un test de rejet NFC/surrogate;
- **P3** — exiger `parent_registry_commit` = révision du registre immédiatement précédente (ou preuve d'adjacence), avec mutant de saut;
- **P4** — normer l'événement annexe `SUPERSEDED` (schéma, emplacement, chaîne) ou le champ `supersedes_occurrence_id` dans le schéma JSON.

Effet sur les gates : **aucun**. Le registre machine est vide (aucun cycle exécuté), la table d'admissions d'oracles est vide (aucun oracle admissible), la preuve d'immuabilité externe reste absente → P6 reste `BLOCKED_IMMUTABILITY`; P0 garde ses blocages connus. Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
