# Rapport Contradictoire — delta REV10 (réponse Producteur P1–P4)

## Objet examiné

Commit Producteur `70394762fc1f8fae7246d389ba3d1974ef98060b` « docs: resolve contradictory findings P1-P4 », branche `correction/reconcile-l1-l12`, cible `fusion/controlled-merger`. Portée : réponse aux constats P1–P4 de `CONTRADICTOIRE_DELTA_REV09BIS.md` et de l'addendum (admis au commit `4f281b7`), documentée dans `REV10.md`, conformément à `docs/fusion/REVIEW_REQUEST_P1_P4.md`. Delta documentaire : `REV10.md` créé; `PROGRESSION.md`, `docs/fusion/CAUSAL_ID_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md`, `NO_GO_CYCLE_REGISTRY.json`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md` modifiés. Aucun contrôleur n'est implémenté.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `70394762fc1f8fae7246d389ba3d1974ef98060b` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict (aucun fichier `CRITIQUE_*` ni `docs/deepsearch/*` consulté); le Producteur n'a déclenché aucune auto-revue pour ce cycle |

## Vérifications préalables d'intégrité et sortie attendue

- Admission `4f281b7` réelle : contenu limité aux artefacts de revue (rapport, reprise, heartbits, addendum), ancêtre de `7039476` (vérifié par `git merge-base --is-ancestor`), `7039476` ancêtre de la révision courante `7a33956`, non ancêtre de `4f281b7`.
- Réfutation 5 exécutée mécaniquement. Commandes : `git show <admission_commit>:<report_path> | sha256sum` pour les dix lignes du registre; `python3 -m json.tool docs/fusion/NO_GO_CYCLE_REGISTRY.json`; calcul SHA-256 de la ligne `Oracle-Admission` et des quatre vecteurs; `git rev-list --first-parent "C^" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json`; `git show` des blobs aux commits de la chaîne.
- Résultat : **les dix SHA-256 concordent exactement** (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb, 02775ce, 5a8ebe2, cf6aa7a, a7c8a69, `4f281b7` = `981e5b08…`; addendum = `77c75221…`), le JSON est valide (`schema_version:1`, `genesis_commit` `930b0f9`, `parent_registry_commit` `6867a2d`, `previous_blob_sha256` `a7ad22af…`, `supersessions:[]`), la ligne machine produit `7dcf174ee657868f5dc784973bf6cface2d62ef9ee1b51145139562f1be07067`, les quatre vecteurs/hashes historiques produisent `51857e…75e6`, `eacf3f…7563`, `5ab872…feee`, `7dcf17…067` (tous exacts). Code de sortie 0 sur toutes les vérifications.
- Chaîne du registre : `git rev-list --first-parent "7039476^" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json` renvoie en premier `6867a2d` (= `parent_registry_commit`); blob à `6867a2d` = `a7ad22af…` (= `previous_blob_sha256`); blob courant `9e626d79…`. Genesis `4ff3bef1…` à `930b0f9`. `f14546f` pré-genesis documentaire.
- Table **Admissions d'oracles** vide → aucune preuve P6 admissible; `Oracle scope` = `—` pour les dix blobs admis.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Faire accepter une ligne `Oracle-Admission` avec octet, ordre, clé, verdict, commit, hash ou chemin divergent; recalculer le vecteur `7dcf17…` | **Échoue.** Grammaire fermée : préfixe ASCII exact `Oracle-Admission: `, objet JSON canonique sur une ligne, exactement cinq clés dans l'ordre canonique, regex par champ (`[0-9a-f]{40}`, `[0-9a-f]{64}`, `(O2|O4|O7)`, `docs/fusion/[A-Za-z0-9_.-]+\.md`, verdicts fermés). Vecteur recalculé = `7dcf17…067` (attendu). Le contrôleur reconstruit la ligne depuis les champs parsés, exige l'égalité octet-pour-octet puis recalcule le hash. Toute mutation (octet, permutation/duplication de clé, verdict/commit/hash/chemin, CR, seconde ligne) bloque P6. Réserve **Q1** |
| 2 | Produire un encodage alternatif conforme du vecteur `5ab872…`, ou faire accepter NFD, surrogate ou clé dupliquée sans `NON_CANONICAL_CAUSAL_JSON` | **Échoue.** Vecteur de couverture `{"a":"\u0000\u001f","é":[1,true]}` recalculé = `5ab872…feee` (attendu) : clé NFC non ASCII, entier, booléen, U+0000 et U+001F. NFC exigé, surrogates rejetés, échappements exhaustifs. Fixtures de rejet obligatoires (clé/valeur NFD, surrogate isolé, paire de surrogates, clé dupliquée après décodage) → `NON_CANONICAL_CAUSAL_JSON`; normaliser puis accepter = mutation qui doit échouer. Code ajouté à la table fermée. Réserve **Q2** |
| 3 | Faire pointer le registre vers un ancêtre autre que sa dernière révision first-parent sans `REGISTRY_HISTORY_VIOLATION`; vérifier le parent `6867a2d`/blob `a7ad22…` | **Échoue.** Pour un commit candidat `C`, le parent autoritaire est le premier commit renvoyé par `git rev-list --first-parent "C^" -- docs/fusion/NO_GO_CYCLE_REGISTRY.json`; aucun ancêtre plus ancien n'est accepté même si le hash concorde. Vérifié : pour `C=7039476` le premier résultat est `6867a2d`, blob `a7ad22af…` = `previous_blob_sha256` déclaré; chaîne `4ff3bef1…` → `a7ad22af…` → `9e626d79…` exacte. Mutant obligatoire : successeur pointant vers la genesis en sautant une révision → doit produire `REGISTRY_HISTORY_VIOLATION`. Réserve **Q3** |
| 4 | Superséder par suppression, réutilisation, branche, cycle ou référence absente sans rejet; vérifier que `supersessions` a un schéma déterministe | **Échoue.** Tableau machine `supersessions` ajouté au schéma JSON (vide). Entrée de forme exacte `{supersession_id, superseded_occurrence_id, replacement_occurrence_id, reason_code, decision_commit}`; les deux occurrences existent et sont distinctes, le remplacement est le prochain `OCC` de la même transaction; ancienne occurrence immuable, comptée dans `len`, statut dérivé `SUPERSEDED`; au plus une supersession entrante et une sortante, chaîne acyclique. Suppression, réutilisation, référence absente, branche ou cycle → `REGISTRY_HISTORY_VIOLATION`. Réserve **Q4** |
| 5 | Vérifier JSON, les dix hashes d'admission, quatre vecteurs/hashes historiques et cohérence inter-documents | **Satisfaite — vérifié.** JSON valide; dix hashes concordants; quatre vecteurs/hashes (`51857e`, `eacf3f`, `5ab872`, `7dcf17`) concordants; chaîne et parent first-parent vérifiés; admission `4f281b7` ancêtre, distincte, limitée aux artefacts de revue; `REV09` absent du registre (supersédé non admis, cohérent). Aucune contradiction bloquante inter-documents (REV10 ↔ registre JSON ↔ NO_GO_REGISTER ↔ CAUSAL_ID_REGISTRY ↔ REVIEW_ADMISSION_REGISTRY ↔ LIMIT_RESOLUTION_REGISTER ↔ PROGRESSION) |

## Constats

### Q1 — Ligne machine `Oracle-Admission` : localisation physique dans le blob non définie

La grammaire, le hash et les mutants sont fermés. Mais le registre est un fichier Markdown : aucune règle ne dit où la ligne autoritaire doit vivre (ligne brute au niveau du fichier, hors bloc de code) ni ce qu'est une « candidate » dans ce blob — contrairement au marqueur du rapport, qui exige une ligne candidate à l'octet 0. Une ligne `Oracle-Admission: …` située à l'intérieur d'une zone de documentation (fence ```) du même fichier matcherait la grammaire et pourrait être lue comme un enregistrement réel. Enfin, rien ne régit plusieurs enregistrements pour des oracles distincts (numérotation, décompte, invalidation par oracles hors scope). **Effet : deux implémentations peuvent différer sur l'emplacement de lecture dans un même blob.** Action : définir la localisation (ligne brute, hors fence) et les règles multi-oracles, au besoin par un vecteur dans le fichier réel.

### Q2 — `NON_CANONICAL_CAUSAL_JSON` : sémantique comptable ambiguë (cycle bloqué ou rejet pré-validation)

Le code est ajouté à la table fermée des codes de raison, qui rend les résultats `NON_TESTABLE` (comptés comme cycles bloqués de la famille et du groupe candidat). Or un échec de canon se produit **au calcul de `causal_payload_sha256`, avant qu'une occurrence n'existe** : rien ne précise s'il produit une entrée de registre (cycle bloqué, occurrence) ou un rejet pré-validation sans entrée machine. Les deux lectures (fixture de rejet sans enregistrement vs résultat `NON_TESTABLE` enregistré) restent non départagées. **Effet : le compteur de cycles d'une famille dépend de la lecture choisie.** Action : préciser si `NON_CANONICAL_CAUSAL_JSON` est enregistré dans le registre machine et comment il affecte le compteur.

### Q3 — Parent first-parent : cas limites du `git rev-list` non régulés

La règle de révision immédiatement précédente est vérifiée sur la chaîne réelle. Restent non régulés : (a) un commit candidat `C` de fusion (le `C^` first-parent ignore les révisions du registre présentes sur la branche fusionnée → parent déclaré possiblement divergent du blob fusionné, `REGISTRY_HISTORY_VIOLATION` faussement positif); (b) le résultat vide de `git rev-list` (fichier jamais modifié avant `C` — seuls genesis et pré-genesis sont traités, sans énoncer la condition d'exemption d'un blob sans `parent_registry_commit`); (c) l'ordre de renvoi de `git rev-list` (premier = plus récent) est une garantie d'implémentation, non épinglée. **Effet : comportement correct sur la chaîne actuelle, indéfini sur ces cas.** Action : réguler merges, résultat vide et ordre de `rev-list`, et l'exemption de la genesis.

### Q4 — Espace `SUP-NNNNNN` sous-normé et `reason_code` non énuméré

`supersession_id` suit `SUP-NNNNNN` « alloué de façon contiguë comme OCC », mais aucune des règles OCC (regex `^OCC-[0-9]{6}$`, domaine, séquence exacte `000001..len`, rejet de tout ID proposé par l'appelant, allocation exclusive par le contrôleur) n'est étendue à `SUP`. `reason_code` appartient à un « vocabulaire fermé » non énuméré (les cinq codes causaux ne décrivent pas une raison de supersession). `decision_commit` n'est qu'une chaîne `[0-9a-f]{40}` sans exigence d'existence ni d'ancestralité. **Effet : les injections sur `supersession_id` (SUP-000000, trou, doublon, ID appelant) ne sont pas mécaniquement fermées comme elles le sont pour `OCC`.** Action : étendre les règles OCC à `SUP`, énumérer `reason_code`, valider `decision_commit`.

## Verdict

**ACCEPT_WITH_LIMITS**

Les cinq réfutations échouent dans leur périmètre : ligne `Oracle-Admission` fermée (grammaire, champs, hash `7dcf17…` vérifié, mutants bloquant P6), canon Unicode avec vecteur `5ab872…` vérifié et fixtures de rejet `NON_CANONICAL_CAUSAL_JSON`, parent autoritaire first-parent vérifié (`6867a2d`/`a7ad22af…`, chaîne `4ff3bef1…→a7ad22af…→9e626d79…`), supersession avec schéma machine `{supersession_id, superseded_occurrence_id, replacement_occurrence_id, reason_code, decision_commit}` et invariants (distinct, contigu, acyclique, ≤1 entrante/sortante), et le JSON, les dix hashes d'admission, les quatre vecteurs/hashes historiques et la cohérence inter-documents vérifiés concordants.

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs :

- **Q1** — définir la localisation physique de la ligne `Oracle-Admission` dans le blob (ligne brute hors fence) et les règles multi-oracles;
- **Q2** — préciser si `NON_CANONICAL_CAUSAL_JSON` est enregistré dans le registre machine et son effet sur le compteur de cycles;
- **Q3** — réguler merges, résultat vide et ordre de `git rev-list --first-parent`, et l'exemption de la genesis;
- **Q4** — étendre les règles OCC à `SUP-NNNNNN` (regex, domaine, séquence, allocation exclusive), énumérer `reason_code`, valider `decision_commit`.

Effet sur les gates : **aucun**. Le registre machine est vide (aucun cycle exécuté), la table d'admissions d'oracles est vide (aucun oracle admissible), la preuve d'immuabilité externe reste absente → P6 reste `BLOCKED_IMMUTABILITY`; P0 garde ses blocages connus. Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
