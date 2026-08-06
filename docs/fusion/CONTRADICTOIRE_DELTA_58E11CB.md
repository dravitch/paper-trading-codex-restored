# Rapport Contradictoire — Delta 58e11cb (réponse Producteur J1–J5)

## Objet examiné

Commit Producteur `58e11cb` « docs: resolve contradictory findings J1-J5 », branche `correction/reconcile-l1-l12`. Portée : réponse aux constats J1–J5 de `CONTRADICTOIRE_DELTA_CA8DE4F.md`, conformément à `docs/fusion/REVIEW_REQUEST_J1_J5.md`. Delta documentaire : contrat `CLOCK_CONTRACT.md` créé, preuve de revue P6, vocabulaire NO-GO fermé, cycle de vie des identifiants causaux.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `58e11cbffe11fcf2bfdce60dc8df36fb0233329d` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité

- Admission `ca8de4f` réelle : commit `f8f0a2e` « docs: admit contradictory review of delta ca8de4f », artefacts `CONTRADICTOIRE_DELTA_CA8DE4F.md` et son heartbit suivis, hash préservé.
- Delta purement documentaire (8 fichiers `.md`, aucun code); réexécution Nix sans objet.

## Réponses aux six réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | `Clock` non importable, ambigu ou capable de lire implicitement le système depuis `domain/`/`replay/` | **Échoue — aucune trouvée.** `CLOCK_CONTRACT.md` définit `paper_trading_codex.domain.clock` (imports `typing` uniquement → graphe transitif sous l'allowlist v1) avec `InstantNs`/`DurationNs`/`Clock(now_ns)`; `SystemClock` confiné à `live/`, `ReplayClock` déterministe hors filesystem/réseau/horloge, `FixedClock` fixture; mutants 4–5 (construction implicite, `SystemClock` en `domain/`/`replay/`). Réserve **K2** |
| 2 | Élever un oracle pending/rejeté/non testable vers accepté sans rapport Git concordant et passer P6 | **Échoue — preuve P6 liée.** Preuve = `{oracle_id, reviewed_commit, report_path, report_sha256, report_verdict, recorded_status}`; le contrôleur exige fichier suivi, SHA-256 concordant, citation de `reviewed_commit` et verdict exactement égal au statut enregistré; mutants d'élévation ajoutés (pending→accepté sans rapport, rapport substitué, octet modifié, commit changé, `REJECT`/`NON_TESTABLE`→accepté). Réserve **K1** |
| 3 | État NO-GO légitime absent du vocabulaire fermé | **Échoue — vocabulaire clos.** Statuts de cause : `OPEN`, `CONTINUE`, `ATTRIBUTION_BLOCKED`, `REDUCE_SCOPE`, `STOP`, `RESOLVED`; statuts d'occurrence : `ATTRIBUTED`, `UNATTRIBUTED`; `UNKNOWN` explicitement requalifié en classement de relation causale, hors statuts. |
| 4 | `UNKNOWN` ou `UNATTRIBUTED` pour un quatrième cycle ou pour éviter attribution/scission/`STOP` | **Échoue — compteurs fermés.** `UNKNOWN` compte toujours comme cycle bloqué de la famille et du groupe candidat, ne suspend aucun compteur ni obligation; seuls `RESOLVED` et `STOP` clôturent; `UNATTRIBUTED` compte dans le compteur familial et le troisième cycle force `ATTRIBUTION_BLOCKED`. Réserve **K4** |
| 5 | ID `RESERVED` dans une cause observée, ou activation sans autorité versionnée | **Échoue — cycle fermé.** `RESERVED → ACTIVE → DEPRECATED → RETIRED`; `RESERVED` interdit dans une `failure_signature` observée; `ACTIVE` exige l'autorité acceptée; règle 6 (activation citant commit d'autorité, décision applicable et date); règle 7 (usage observé d'un `RESERVED` → résultat `NON_TESTABLE`, jamais d'activation rétroactive); règle 8 (lignes initiales `RESERVED`). Autorités alignées par espace (RFC, contrat canonique, oracle/mutation, décision opérateur). Réserve **K3**, **K5** |
| 6 | Dérive d'une même cause par changement de ligne/message/preuve, ou confluence de deux causes par le registre | **Échoue — identité sur IDs stables.** La signature = identifiants stables préenregistrés « jamais texte libre, numéro de ligne, traceback, révision ou hash de preuve »; `cause_key` = SHA-256 de `{cause_family_key, failure_signature}`; deux défauts distincts créent deux causes; fusion/scission/requalification soumise à décision versionnée citant preuves, anciennes et nouvelles clés. |

## Constats

### K1 — P6 : ancrage du `report_sha256` non nommé (preuve potentiellement auto-référentielle)

La preuve porte elle-même `report_sha256`, et « le contrôleur vérifie que son SHA-256 concorde » — concorde avec le champ de la preuve. Le mutant « modifier un octet du rapport » ne peut échouer de façon déterministe que si le contrôleur compare à une ancre non éditable par le même acteur que la preuve. Contre-exemple minimal : un acteur réécrivant à la fois le rapport (verdict accepté) et la preuve (`report_sha256` recalculé, `recorded_status` aligné) dans le même commit réécrit ferait passer le contrôle. **Effet : la concordance vérifiée est celle que la preuve s'attribue elle-même, sauf ancre externe.** Action : nommer l'ancre — `report_sha256` doit être validé contre le hash enregistré au commit d'admission du rapport, distinct de la preuve.

### K2 — P1 : mutants du contrat `Clock` non repris dans la liste de contrôle (couplage implicite)

Les invariants 4–5 de `CLOCK_CONTRACT.md` (remplacer `Clock` par une construction implicite; placer `SystemClock` dans `domain/`/`replay/`) exigent l'échec P1, mais la liste « Le test injecte au minimum » de `06_FUSION_GATES.md` ne les reprend pas; la liaison repose sur le caractère ouvert « au minimum » et sur l'exécution du contrat par le contrôleur. **Effet : deux mutants normatifs restent déclarés hors de la liste minimale injectée.** Action : lier explicitement les mutants du contrat dans la liste P1 avant implémentation du contrôle.

### K3 — Registre : usage `DEPRECATED`/`RETIRED` en nouvelle occurrence — conséquence non spécifiée

Le cycle interdit les nouvelles occurrences sous `DEPRECATED` et rend `RETIRED` terminal, mais la règle 7 ne définit la conséquence que pour `RESERVED` (résultat `NON_TESTABLE`). Contre-exemple minimal : un ID `DEPRECATED` réutilisé dans une nouvelle `failure_signature` — aucun statut ni blocage défini pour ce résultat. **Effet : les deux états interdits d'usage manquent de sanction documentée.** Action : étendre la règle 7 (ou une règle 9) aux usages `DEPRECATED` et `RETIRED`.

### K4 — NO-GO : seuil du « groupe candidat » non explicite

`UNKNOWN` compte comme cycle bloqué « de la famille et du groupe candidat », mais seul le seuil familial (troisième cycle) est chiffré; le texte antérieur indique seulement que « le seuil de répétition est évalué également sur ce groupe » sans valeur. Contre-exemple minimal : le nombre de cycles bloqués tolérables pour un groupe candidat avant décision n'est pas décidable depuis la lettre du registre. **Effet : seuil inférable mais non normé.** Action : fixer explicitement le seuil de cycles bloqués du groupe candidat (ou le déclarer identique au seuil familial).

### K5 — NO-GO/registre : effet d'un résultat `NON_TESTABLE` (règle 7) sur le compteur de cycles non spécifié

La règle 7 transforme en `NON_TESTABLE` tout résultat observé utilisant un ID `RESERVED`, mais ni le registre NO-GO ni les statuts ne disent si un résultat `NON_TESTABLE` compte comme cycle bloqué de la famille. Contre-exemple minimal : un opérateur cite des IDs `RESERVED` dans des observations répétées → chaque observation devient `NON_TESTABLE`; si `NON_TESTABLE` n'est pas compté comme cycle bloqué, le compteur familial n'avance pas et `ATTRIBUTION_BLOCKED`/`REDUCE_SCOPE`/`STOP` restent contournables par réitération. **Effet : échappatoire possible par le statut `NON_TESTABLE` introduit par la réponse.** Action : préciser que `NON_TESTABLE` compte comme cycle bloqué de la famille (ou est plafonné), et interdire l'usage répété d'IDs `RESERVED` comme classement d'évitement.

## Verdict

**ACCEPT_WITH_LIMITS**

Les six réfutations échouent : le port `Clock` est défini, importable et confiné; la preuve P6 lie statut, commit, rapport, hash et verdict; le vocabulaire NO-GO est clos avec `ATTRIBUTION_BLOCKED`; `UNKNOWN` et `UNATTRIBUTED` comptent dans les compteurs et ne suspendent rien; le cycle de vie des IDs est fermé avec autorités alignées; l'identité causale ne dérive pas des lignes/messages/preuves et les regroupements exigent une décision versionnée.

Limites conditionnelles à intégrer avant tout gate P1/P6 :

- **K1** — ancrer `report_sha256` sur le hash d'admission du rapport (preuve non auto-référentielle);
- **K2** — reprendre les mutants du contrat `Clock` dans la liste de contrôle P1;
- **K3** — sanctionner les usages `DEPRECATED`/`RETIRED` en nouvelle occurrence;
- **K4** — normer le seuil de cycles bloqués du groupe candidat;
- **K5** — compter `NON_TESTABLE` dans les cycles bloqués (ou le plafonner) pour fermer l'échappatoire par IDs `RESERVED`.

Conformément à la portée : cette revue documentaire n'implémente aucun module `Clock`, analyseur AST ni contrôleur P6; P1 et P6 restent interdits au statut `PASS`; O4/O7 demeurent `SUPERSEDED_PENDING_REVIEW`. Ce verdict ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
