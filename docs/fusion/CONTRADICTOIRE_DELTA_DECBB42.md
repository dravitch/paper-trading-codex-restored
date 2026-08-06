# Rapport Contradictoire — Delta decbb42 (réponse Producteur K1–K5)

## Objet examiné

Commit Producteur `decbb42` « docs: resolve contradictory findings K1-K5 », branche `correction/reconcile-l1-l12`. Portée : réponse aux constats K1–K5 de `CONTRADICTOIRE_DELTA_58E11CB.md`, conformément à `docs/fusion/REVIEW_REQUEST_K1_K5.md`. Delta documentaire et Git : registre `REVIEW_ADMISSION_REGISTRY.md` créé (ancrage des rapports sur leurs blobs d'admission), mutants `Clock` ajoutés à P1, sanction des IDs non actifs, seuil du groupe candidat fixé, `NON_TESTABLE` compté comme cycle bloqué.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `decbb42cc79fb863e2eb4473d040c2855c8d2f1a` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité

- Admission `58e11cb` réelle : commit `1fdc5eb` « docs: admit contradictory review of delta 58e11cb », artefacts suivis, hash préservé.
- Delta purement documentaire (7 fichiers `.md`, aucun code); réexécution Nix sans objet.
- Réfutation 6 exécutée mécaniquement : les cinq `admitted_sha256` du registre recalculés depuis `git show <admission_commit>:<report_path>` correspondent exactement (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb); chaque commit d'admission est ancêtre de `decbb42` et ne contient que le rapport + son heartbit.

## Réponses aux six réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Réécrire rapport et preuve courante ensemble pour contourner l'ancre du commit d'admission | **Échoue — ancre immuable.** Le contrôleur recalcule le hash depuis le blob du commit d'admission, distinct et ancêtre, jamais depuis une valeur auto-déclarée de la preuve courante; réécrire rapport+preuve dans un commit ultérieur ne change pas le blob historique. Réécriture d'historique : déclarée invalidante (branche protégée ou archive signée exigée à la publication). Réserve **L4** (dépendance assumée) |
| 2 | Substituer chemin, commit, verdict ou rapport d'un autre oracle et faire passer P6 | **Échoue pour chemin/commit/verdict** — `admitted_sha256` ancré sur le blob du commit d'admission; mutations « modifier un octet du rapport », « recalculer seulement le hash courant », « changer le commit examiné ou d'admission », « substituer le rapport d'un autre oracle » répertoriées. Réserve **L1** (liaison oracle↔rapport non mécaniquement spécifiée) |
| 3 | Construire implicitement un `Clock` système ou déplacer `SystemClock` dans les modules canoniques sans échec P1 | **Échoue — mutants ajoutés.** Le contrôle injecte désormais la construction implicite d'un `Clock` système comme valeur par défaut et le déplacement de `SystemClock` sous `domain/` puis `replay/`; chaque mutant doit échouer avec fichier, ligne et règle. Constructeur implicite, singleton, défaut temporel et service locator restent interdits; l'allowlist rejette toute source temporelle dans `domain/`/`replay/`. |
| 4 | Employé un ID `RESERVED`, `DEPRECATED` ou `RETIRED` dans une nouvelle occurrence sans produire `NON_TESTABLE` et cycle bloqué | **Échoue — règle 7 étendue.** Ces trois états rendent le résultat `NON_TESTABLE` avec raison `INVALID_CAUSAL_ID_STATE` et le comptent comme cycle bloqué de la famille; pas d'activation/réactivation rétroactive. Réserve **L2** (définition mécanique de « nouvelle occurrence » absente) |
| 5 | Accumuler trois cycles d'un groupe candidat ou des résultats `NON_TESTABLE` sans décision obligatoire | **Échoue — compteurs fermés.** Seuil du groupe candidat = trois cycles bloqués, identique au seuil familial; tout `NON_TESTABLE` (y compris `INVALID_CAUSAL_ID_STATE`) compte pour sa famille et son groupe candidat; au troisième cycle, attribution/scission ou `STOP` est obligatoire; répéter un ID non actif ne remet ni compteur ni échéance à zéro. Réserve **L3** |
| 6 | Recalculer indépendamment les cinq hashes du registre depuis les blobs d'admission | **Satisfaite — vérifié.** Les cinq `admitted_sha256` correspondent aux blobs `git show <admission_commit>:<report_path>`; ancêtres vérifiés; commits d'admission sans la modification Producteur évaluée. |

## Constats

### L1 — P6 : liaison `oracle_id`↔rapport non mécaniquement spécifiée (substitution croisée résiduelle)

Le registre indexe par delta revu (pas par oracle) et le contrôleur vérifie que le rapport cite `reviewed_commit` et que son verdict égale `recorded_status`, mais aucune exigence ne lie l'`oracle_id` de la preuve au contenu du rapport. Contre-exemple minimal : pour un oracle O2, fournir le rapport admis d'O4 (chemin et `admission_commit` d'O4, blob concordant) — si le verdict d'O4 égale le `recorded_status` d'O2, la preuve passe sans que le rapport ne mentionne O2. **Effet : le mutant « substituer le rapport d'un autre oracle » est déclaré mais sa détection n'est pas spécifiée.** Action : exiger que le rapport nomme explicitement l'`oracle_id` (ou indexer le registre d'admission par oracle) et vérifier cette mention au contrôle.

### L2 — Registre : définition mécanique de « nouvelle occurrence » absente

La règle 7 sanctionne un ID non actif « utilisé dans une nouvelle occurrence », et `DEPRECATED` reste « lisible pour l'historique » — mais aucun critère ne distingue mécaniquement une occurrence nouvelle d'une occurrence historique (cycle ? clé causale déjà enregistrée ? timestamp ?). Contre-exemple minimal : une observation réutilisant un ID `DEPRECATED` qualifiée d'« historique » par l'opérateur → ni `NON_TESTABLE` ni cycle bloqué. **Effet : la distinction fondant la sanction est non décidable depuis la lettre du registre.** Action : définir « nouvelle occurrence » (par exemple occurrence dont la clé causale n'a jamais été enregistrée, ou horodatage du cycle courant).

### L3 — NO-GO : re-création d'un groupe candidat — héritage du compteur non normé

Le seuil du groupe candidat est fixé à trois cycles bloqués, mais la création d'un nouveau `RCG-NNN` couvrant des causes déjà comptées ne précise pas l'héritage des cycles antérieurs. Contre-exemple minimal : au deuxième cycle bloqué d'un groupe, l'opérateur crée un nouveau groupe candidat pour les mêmes causes → compteur repart à zéro si l'héritage n'est pas imposé; la requalification exige une décision versionnée mais son effet sur le compteur n'est pas spécifié. **Effet : remise à zéro possible par re-groupement.** Action : normer que tout nouveau groupe couvrant des causes déjà comptées hérite des cycles bloqués antérieurs (comme le renommage conserve l'ID et son historique).

### L4 — Dépendance assumée : immuabilité de l'historique Git (mitigée)

L'ancre repose sur l'absence de réécriture d'historique. Le registre le déclare et exige branche protégée ou archive signée à la publication. Dépendance assumée, non une faille nouvelle; à verrouiller (protection de branche) avant tout usage P6, pas seulement à la publication finale.

## Verdict

**ACCEPT_WITH_LIMITS**

Les six réfutations échouent : l'ancre des rapports est le blob immuable du commit d'admission (recalculé, jamais auto-déclaré), les mutants `Clock` sont injectés, les trois états d'ID non actifs sont sanctionnés avec cycle bloqué, le seuil du groupe candidat est fixé à trois, tout `NON_TESTABLE` compte, et les cinq hashes du registre ont été recalculés et concordent exactement avec les blobs d'admission.

Limites conditionnelles à intégrer avant tout gate P6 :

- **L1** — lier mécaniquement `oracle_id` au rapport (mention obligatoire de l'oracle dans le rapport, ou indexation du registre par oracle) pour rendre la substitution croisée détectable;
- **L2** — définir mécaniquement « nouvelle occurrence » (vs historique) pour la règle 7;
- **L3** — normer l'héritage des cycles bloqués pour tout nouveau groupe candidat couvrant des causes déjà comptées;
- **L4** — verrouiller l'immuabilité de l'historique (protection de branche / archive signée) avant toute utilisation de l'ancre en P6.

Conformément à la portée : cette revue documentaire et Git n'implémente aucun contrôleur P1/P6; P1 et P6 restent interdits au statut `PASS`; O4/O7 demeurent `SUPERSEDED_PENDING_REVIEW`. Ce verdict ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
