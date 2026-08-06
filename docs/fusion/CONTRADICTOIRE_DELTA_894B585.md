# Rapport Contradictoire — Delta 894b585 (réponse Producteur G1–G4)

## Objet examiné

Commit Producteur `894b585` « docs: resolve contradictory findings G1-G4 », branche `correction/reconcile-l1-l12`. Portée : réponse aux constats G1–G4 de `CONTRADICTOIRE_DELTA_4225BC5.md`, conformément à `docs/fusion/REVIEW_REQUEST_G1_G4.md`.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `894b585b0738f8d2606476ef2b9a7c1286460ed5` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité

- Admission `4225bc5` réelle : commit `0d9bc06` « docs: admit contradictory review of delta 4225bc5 », artefacts suivis, `CONTRADICTOIRE_DELTA_4225BC5.md` hash `ef11a60f…` identique au mien.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux cinq réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Contourner le contrôle temporel (alias, import dynamique, `fromtimestamp`, `time_ns`, métadonnée fichier, alias indirect, réflexion, dépendance tierce) | **Échoue pour tous les cas nommés** — matcher par module source, liste d'appels élargie (`time_ns`, `fromtimestamp`, `utcfromtimestamp`, `st_*`), imports dynamiques et réflexion interdits, défaut conservateur. Réserve **H1** |
| 2 | Deux défauts indépendants, signatures normalisées différentes → même `cause_key` | **Échoue** — la signature `{component_id, symbol_id, failure_mode_id}` entre dans la clé; des signatures distinctes donnent des clés distinctes (collision SHA-256 non viable). Réserve **H4**, **H5** |
| 3 | Changement de ligne, message, traceback ou preuve modifie indûment la clé | **Échoue** — identité sur identifiants stables préenregistrés; ligne, traceback, révision, hash de preuve et descriptions exclus de l'identité |
| 4 | Transitions fermées des statuts ; chemin P6 `PASS` avec statut pending | **Partiellement — H2 trouvé** : le garde-fou est en prose seule; le critère P6 ne référence pas les statuts de revue. Plus H3 |
| 5 | Admission `8335ab0` effective et ancienne affirmation absente | **Confirmé** — `a1e9892` commité, fichiers suivis; « restent non suivis » absent du registre actif (ne subsiste que cité dans mon rapport `4225bc5`) |

## Constats

### H1 — P1 : « imports non allowlistés » sans liste blanche définie (bloque l'implémentation du contrôle)

`06_FUSION_GATES.md` interdit « les imports non allowlistés » dans `domain/`/`replay/`, mais aucune liste blanche n'est définie dans le delta ni ailleurs dans le dépôt (`grep` sans résultat). Sans elle, le contrôle est inconstructible : soit aucune importation n'est autorisée (impossible), soit la liste est à inventer par l'implémenteur (non figée). **Fragilité de conception** : si une future liste blanche admet une bibliothèque à capacité temporelle (ex. `numpy.datetime64("now")`, `pandas.Timestamp.now()`), la liste d'appels nommés ne la couvre pas — le conservatisme ne s'applique qu'aux provenances résolues. Contre-exemple minimal : `numpy.datetime64("now", "ns")` renvoie l'heure murale sans aucun des appels listés. **Effet : P1 implémenté à l'identique de la règle ne prouve pas l'absence d'horloge murale.** Action : définir et versionner la liste blanche avec un criblage de capacité temporelle, ou formuler l'autorisation comme « aucun import hors stdlib, et stdlib non temporelle », avec mutants correspondants.

### H2 — P6 : chemin `PASS` avec statut pending (bloque P6)

Le garde « Aucun statut pending n'autorise P6 `PASS` » (`05_RISKMAP_ORACLES.md`) est une affirmation de prose. Le critère PASS du gate P6 est « O1–O11 et paysages passent » (`06_FUSION_GATES.md`), sans référence aux statuts de revue. Contre-exemple minimal : O4 et O7 restent `SUPERSEDED_PENDING_REVIEW`; un implémenteur écrit les tests O1–O11 conformes à la règle, ils passent mécaniquement → la lettre du critère P6 est satisfaite, alors que les oracles définitionnels ne sont « acceptés » (05 : « ne deviennent acceptés qu'après revue Contradictoire »). La ligne 05:101 exprime l'exigence, le gate ne la rend pas mécanique. **Effet : P6 peut être revendiqué `PASS` avec O2/O4/O7 pending.** Action : ajouter au critère PASS de P6 l'exigence explicite « O2, O4 et O7 en `REVIEWED_*` » (ou un statut équivalent fermé), vérifiable par la preuve du gate.

### H3 — Statuts d'oracle : transitions non fermées (documentaire)

Le vocabulaire est défini (5 statuts) mais les transitions ne couvrent pas : `modifier(SUPERSEDED_PENDING_REVIEW)` → non spécifié (inférable, non clos); verdict `NON_TESTABLE` du protocole → aucun statut `REVIEWED_NON_TESTABLE` n'existe, la revue d'une révision concluant `NON_TESTABLE` ne peut s'enregistrer. Contre-exemple minimal : la Contradictoire conclut `NON_TESTABLE` pour O4 → aucune transition valide vers `REVIEWED_<verdict>` dans le vocabulaire. **Effet : vocabulaire non fermé vis-à-vis des verdicts admis.** Action : ajouter `REVIEWED_NON_TESTABLE` et spécifier `modifier(SUPERSEDED_PENDING_REVIEW)`.

### H4 — NO-GO : occurrences `UNATTRIBUTED` hors compteur (documentaire/d'usage)

« Une occurrence encore non diagnostiquée reçoit `UNATTRIBUTED` sous la famille et ne compte pas pour le seuil des trois cycles. » Rien ne force l'attribution au troisième cycle; l'opérateur peut laisser une cause non diagnostiquée indéfiniment et le déclencheur `REDUCE_SCOPE`/`STOP` du critère 6 n'atteint jamais son seuil. Contre-exemple minimal : un invariant bloqué sur trois cycles, chaque occurrence marquée `UNATTRIBUTED` → compteur à zéro, aucune obligation d'action. **Effet : la soupape de sécurité des trois cycles est contournable par non-attribution.** Action : régler qu'au troisième cycle, une famille à occurrences `UNATTRIBUTED` déclenche quand même l'obligation d'attribution ou de scission rétroactive, avec échéance.

### H5 — NO-GO : registre d'identifiants stables indéfini ; cause racine multi-surface scindée (documentaire)

La signature repose sur `component_id`, `symbol_id`, `failure_mode_id` « préenregistrés », mais aucun registre n'est défini ni versionné (même problème que H1). Par ailleurs, une cause racine unique observée à deux surfaces différentes (deux symboles/composants) produit deux `cause_key` : le compteur sous-compte par clé et un même défaut peut se répartir entre deux clés sans jamais atteindre le seuil. Contre-exemple minimal : un défaut de configuration propagé à deux fonctions → deux signatures, deux clés, une cause. La fusion opérateur versionnée (prévue) peut réconcilier, mais rien ne la rend obligatoire. **Effet : identité mécanique dépendante d'un artefact inexistant; causes racines scindables.** Action : créer le registre des identifiants et préciser quand la fusion est requise.

## Verdict

**ACCEPT_WITH_LIMITS**

Les réfutations 1, 2, 3 et 5 échouent : le contrôle temporel couvre tous les contre-exemples G1 nommés, la signature normalisée entre dans la clé, l'identité exclut ligne/traceback/preuve, et l'admission Git est réelle. H1–H5 sont les limites résiduelles.

- **H1** et **H2** bloquent l'implémentation future (contrôle AST P1, gate P6) : liste blanche à définir, critère P6 à rendre mécanique;
- **H3**, **H4**, **H5** documentaires : vocabulaire fermé des statuts, obligation d'attribution `UNATTRIBUTED`, registre d'identifiants stables.

Conformément à la limite de portée : ce verdict ne franchit ni P1 ni P6, O4/O7 restent pending et les contrôles exécutables ne sont pas implémentés. Il ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
