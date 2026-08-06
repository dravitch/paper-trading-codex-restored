# Rapport Contradictoire — Delta ca8de4f (réponse Producteur H1–H5)

## Objet examiné

Commit Producteur `ca8de4f` « docs: resolve contradictory findings H1-H5 », branche `correction/reconcile-l1-l12`. Portée : réponse aux constats H1–H5 de `CONTRADICTOIRE_DELTA_894B585.md`, conformément à `docs/fusion/REVIEW_REQUEST_H1_H5.md`.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `ca8de4f7e17625d3ef5aea6e19eff54930471693` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité

- Admission `894b585` réelle : commit `4b920b4` « docs: admit contradictory review of delta 894b585 », artefacts suivis.
- Delta purement documentaire; réexécution Nix sans objet.

## Réponses aux six réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Capacité temporelle accessible depuis l'allowlist P1 v1 ou son graphe transitif | **Échoue — aucune trouvée.** Allowlist purement stdlib non temporelle (`collections`, `dataclasses`, `decimal`, `enum`, `fractions`, `hashlib`, `json`, `math`, `operator`, `statistics`, `typing`…) ; `os`, `pathlib`, `time`, `datetime`, `importlib`, `numpy`, `pandas`, réseau/filesystem/provider explicitement rejetés. Réserve **J1** |
| 2 | Chemin P6 `PASS` avec O2/O4/O7 pending, rejeté ou non testable | **Direct fermé** — P6 exige mécaniquement « O2/O4/O7 sont `REVIEWED_ACCEPT` ou `REVIEWED_ACCEPT_WITH_LIMITS` sur leur révision courante »; mutation « remplacer un statut accepté par pending » ajoutée; pending/reject/non-testable bloquent. Réserve **J2** |
| 3 | Verdict ou modification d'oracle sans transition définie | **Échoue — aucune trouvée.** Transitions fermées : modifier `REVIEWED_*` → `SUPERSEDED_PENDING_REVIEW`; modifier `PENDING_REVIEW`/`SUPERSEDED_PENDING_REVIEW` → conservé; revoir → exactement l'un des quatre `REVIEWED_<VERDICT>` incluant `REVIEWED_NON_TESTABLE` |
| 4 | Trois cycles familiaux `UNATTRIBUTED` sans attribution, scission ou `STOP` | **Échoue** — `UNATTRIBUTED` compte dans le compteur de cycles bloqués de la famille; au troisième cycle familial, statut obligatoire `ATTRIBUTION_BLOCKED`, aucun quatrième cycle/`CONTINUE`/`REDUCE_SCOPE`; attribution/scission rétroactive ou `STOP`. Réserve **J3** |
| 5 | Cause multi-surface évitant le seuil malgré `root_cause_group_id`, ou deux causes forcées dans le même groupe | **Échoue pour la fuite de seuil** — la recherche de regroupement est obligatoire au plus tard au troisième cycle de la famille (compteur familial, pas par clé), donc une alternance de surfaces ne contourne pas; le seuil est évalué aussi sur le groupe. Risque résiduel : deux causes distinctes réunies par jugement (preuves/dépendance partagées) → réversible par scission versionnée. Réserve **J4** |
| 6 | Identifiants stables, non dérivés de messages/lignes, liés à une autorité de création | **Satisfaite** — formes `CMP/SYM/FM/RCG-NNN-slug`, immuabilité, règle « aucun message libre, ligne ou traceback ne devient un ID », autorité par type. Réserve **J5** |

## Constats

### J1 — Port `Clock` non défini et non importable sous l'allowlist (bloque l'implémentation P1)

La seule origine temporelle admise est « une dépendance explicite satisfaisant le port `Clock` », mais aucune définition du port n'existe : aucune classe/protocole `Clock` dans le dépôt (5 références en prose seulement : `CD-019`, `ReplayClock`/`LiveClock`, lignes P1, contrôle temporel, `FM-003`). Or l'allowlist v1 ne contient aucun module pouvant porter ce type et tout import externe hors allowlist est rejeté. Contre-exemple minimal : un module canonique annotant `clock: Clock` — l'import du module définissant `Clock` (nécessairement hors allowlist) est rejeté par le contrôle. **Effet : le mécanisme temporel autorisé est inconstructible tel que spécifié.** Action : définir le contrat du port `Clock` (méthodes, types) et son emplacement — module canonique sous `domain/` (graphe interne contrôlé) ou ajout d'un module dédié à l'allowlist — avant implémentation du contrôle.

### J2 — P6 : mutation asymétrique — l'élévation non fondée n'est pas testée (audit)

La mutation « remplacer un statut accepté par pending » teste la dégradation; la direction inverse (marquer un oracle `REVIEWED_ACCEPT_WITH_LIMITS` sans rapport de revue correspondant) n'a pas de mutant ni d'exigence de preuve dans le critère PASS, qui vérifie le statut enregistré mais pas l'existence d'un rapport `CONTRADICTOIRE_*` concordant. Contre-exemple minimal : O4 reste non revu mais son statut est édité en `REVIEWED_ACCEPT_WITH_LIMITS` → la lettre du critère P6 est satisfaite. **Effet : garde dépendante de l'honnêteté de l'édition, pas d'un contrôle.** Action : lier le statut accepté à la présence d'un rapport de revue versionné (chemin + verdict) dans la preuve P6, et ajouter le mutant « élever pending→accepté sans rapport ».

### J3 — NO-GO : `ATTRIBUTION_BLOCKED` hors vocabulaire des Statuts (documentaire)

La règle rend le statut `ATTRIBUTION_BLOCKED` obligatoire au troisième cycle familial, mais la section « Statuts » ne le déclare pas (`OPEN`, `CONTINUE`, `REDUCE_SCOPE`, `STOP`, `RESOLVED`). Contre-exemple minimal : un registre correct selon la règle porte un statut qui viole le vocabulaire déclaré. **Effet : vocabulaire et règle divergent.** Action : ajouter `ATTRIBUTION_BLOCKED` (et `UNATTRIBUTED` en tant que statut d'occurrence, distinct des statuts de cause) à la liste.

### J4 — NO-GO : classement de groupe `UNKNOWN` — effet sur le seuil non spécifié (documentaire/d'usage)

L'opérateur peut classer un groupe `UNKNOWN` « sans effacer leurs clés », mais l'effet de ce classement sur le seuil de répétition n'est pas défini. Contre-exemple minimal : une cause multi-surface classée `UNKNOWN` à chaque troisième cycle familial → si `UNKNOWN` exempte du seuil, la cause évite indéfiniment `REDUCE_SCOPE`/`STOP`. **Effet : fuite possible par réitération du classement.** Action : préciser que `UNKNOWN` compte comme cycles bloqués de la famille et ne suspend ni le compteur ni l'obligation; seul `RESOLVED` ou `STOP` clôt.

### J5 — Registre causal : cycle de vie des IDs et autorités (documentaire)

Les 10 IDs initiaux sont tous `RESERVED`; la transition vers un statut actif/utilisation n'est pas définie (que signifie `RESERVED` pour la signature `failure_signature` ?). Autorités lâches ou incohérentes : symbole = « API publique ou fonction normative » (toute fonction publique), et « introduit par modèle de référence » ou « invariant P1 » ne correspondent pas aux autorités déclarées (oracle ou mutation préenregistrée). **Effet : identité mécanique dépendante d'un artefact dont le statut d'utilisation est indéfini.** Action : définir le cycle `RESERVED`→actif et aligner les autorités de création sur les types déclarés.

## Verdict

**ACCEPT_WITH_LIMITS**

Les réfutations 1, 3, 4, 5 et 6 échouent : l'allowlist est pure, les transitions d'oracle sont fermées, le contournement `UNATTRIBUTED` est bloqué par `ATTRIBUTION_BLOCKED`, la fuite de seuil multi-surface est fermée par le compteur familial et le registre d'identifiants est stable et sourcé.

- **J1** bloque l'implémentation future du contrôle temporel P1 (port `Clock` à définir et rendre importable);
- **J2** à intégrer dans la preuve P6 avant son gate;
- **J3**, **J4**, **J5** documentaires.

Conformément à la portée : l'allowlist, l'analyse AST et les gardes P6 ne deviennent pas exécutables par cette revue; P1 et P6 restent interdits au statut `PASS`; O4/O7 demeurent `SUPERSEDED_PENDING_REVIEW`. Ce verdict ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
