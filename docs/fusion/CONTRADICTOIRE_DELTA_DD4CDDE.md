# Rapport Contradictoire — Delta dd4cdde (réponse Producteur L1–L4)

## Objet examiné

Commit Producteur `dd4cdde133af1bdc266c21ca943a6401b13dec30` « docs: resolve contradictory findings L1-L4 », branche `correction/reconcile-l1-l12`. Portée : réponse aux constats L1–L4 de `CONTRADICTOIRE_DELTA_DECBB42.md` (admis au commit `02775ce`), documentée dans `REV06.md`, conformément à `docs/fusion/REVIEW_REQUEST_L1_L4.md`. Delta documentaire : `REV06.md` et `PROGRESSION.md` créés; `06_FUSION_GATES.md`, `CAUSAL_ID_REGISTRY.md`, `NO_GO_REGISTER.md`, `REVIEW_ADMISSION_REGISTRY.md`, `LIMIT_RESOLUTION_REGISTER.md` modifiés.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `dd4cdde133af1bdc266c21ca943a6401b13dec30` |
| indépendance | aucune conclusion Critique de ce delta lue avant le gel du verdict |

## Vérifications préalables d'intégrité et sortie attendue

- Admission `decbb42` réelle : commit `02775ce` « docs: admit contradictory review of delta decbb42 », puis indexée au commit `3df7209`.
- Delta purement documentaire (7 fichiers `.md`, aucun code); réexécution Nix sans objet.
- Réfutation 5 exécutée mécaniquement. Commandes : `git show <admission_commit>:<report_path> | sha256sum` et `git show <admission_commit>:<report_path> | grep -c "Oracle scope:"`. Résultat : les six SHA-256 concordent exactement (a1e9892, 0d9bc06, 4b920b4, f8f0a2e, 1fdc5eb, 02775ce) et aucun blob admis ne contient le marqueur `Oracle scope:` (0 occurrence pour chacun). Code de sortie 0 sur toutes les vérifications de concordance.

## Réponses aux six réfutations du mandat

| # | Réfutation | Verdict |
|---|---|---|
| 1 | Substituer à O2 un rapport admis visant O4 avec le même verdict | **Échoue — double appartenance.** Le contrôleur exige `oracle_id ∈ Oracle scope` indexé **et** marqueur `Oracle scope: <oracle_id>` extrait du blob d'admission (jamais de la preuve courante). O2 ∉ {O4} bloqué à l'index comme au blob; modifier l'index seul ne change pas le blob. Réserve **M1** |
| 2 | Accepter comme historique une occurrence créée après dépréciation, dupliquée, modifiée ou sans ascendance | **Échoue partiellement.** Création après dépréciation, duplication sous nouvel `occurrence_id` et ascendance falsifiée sont bloquées (règles 9–10, `INVALID_CAUSAL_ID_STATE`/`INVALID_OCCURRENCE_HISTORY`, sans temps mural). **Modification causale sous le même `occurrence_id` historique non détectable** → Réserve **M2** |
| 3 | Recréer/fusionner/scinder un groupe et obtenir un compteur < union dédupliquée | **Échoue.** Le compteur est la cardinalité de l'union des `cycle_id`; omission d'un prédécesseur/cycle → `NON_TESTABLE INCOMPLETE_GROUP_HISTORY` + cycle bloqué; pas de remise à zéro. `\|{A,B}∪{B,C}\| = 3` satisfait. Réserve **M3** |
| 4 | Revendiquer P6 sans protection distante hashée ni archive signée | **Échoue.** Preuve d'immuabilité obligatoire avant tout contrôle P6, SHA-256 dans le manifeste; absence → `BLOCKED_IMMUTABILITY` même si les blobs concordent. L4 honnêtement `RESOLVED_SPEC_OPEN_PROOF_EXTERNAL`, aucune preuve affirmée. |
| 5 | Vérifier les six SHA-256 et l'inéligibilité des revues `Oracle scope = —` | **Satisfaite — vérifié.** Six hashes concordants avec les blobs d'admission; les six revues admises portent `—` et aucun blob ne contient le marqueur → aucune ne peut accepter O2/O4/O7. |
| 6 | Contradiction entre `REV06.md`, les registres modifiés et les critères P6 | **Une tension réelle trouvée** entre `REV06.md` L2 et la règle 9 de `CAUSAL_ID_REGISTRY.md` → Réserve **M2**; voir constat. |

## Constats

### M1 — L1 : syntaxe normative du marqueur `Oracle scope` non définie (robustesse du contrôleur)

Le marqueur est spécifié en prose (« le blob admis doit contenir `Oracle scope: <oracle_id>` ») sans bloc normatif dédié. Contre-exemple minimal : un rapport contenant une phrase négative « O2 est hors Oracle scope » contient la sous-chaîne `Oracle scope: O2`; un extracteur sous-chaîne naïf, associé à un index opérateur fautif, ferait passer l'appartenance. **Effet : l'appartenance aux deux sources dépend d'une extraction non normée.** Action : définir un champ normatif unique (ligne ou bloc d'en-tête exact, un marqueur par oracle et son verdict), non ambigu et vérifiable par expression déterministe.

### M2 — L2 : mutation causale sous un `occurrence_id` historique réutilisé — non détectable (tension `REV06.md`/règle 9)

La règle 9 qualifie d'« historique » toute occurrence dont l'`occurrence_id` existe dans un ancêtre antérieur à la désactivation — sans vérifier l'égalité du contenu. La règle 10 impose de créer un nouvel `occurrence_id` en cas de modification causale, mais aucune détection de la violation n'est définie (pas de comparaison blob actuel vs blob au `first_recorded_commit`, ni hash des champs causaux). Contre-exemple minimal : reprendre un `occurrence_id` enregistré avant dépréciation, réécrire ses champs causaux dans un commit ultérieur → classé « historique » par la règle 9, sans sanction. **Effet : `REV06.md` L2 (« toute modification causale est nouvelle ») contredit le critère mécanique de la règle 9 en cas de non-conformité; le but L2 est contournable.** Action : le contrôleur doit vérifier que le blob courant d'une occurrence historique égale le blob au `first_recorded_commit` (ou le hash canonique de ses champs causaux); toute divergence = nouvelle occurrence.

### M3 — L3 : source autoritaire d'énumération des `cycle_id` non définie (le contrôleur ne peut pas recomputer l'union)

Le compteur d'un groupe est la cardinalité de l'union des `cycle_id` hérités, et l'omission produit `INCOMPLETE_GROUP_HISTORY` — mais le registre NO-GO est vide (aucune cause enregistrée) et les décisions versionnées sont documentaires. Contre-exemple minimal : sans registre machine des `cycle_id` par cause/famille, le contrôleur ne peut ni recomputer l'union ni distinguer une omission réelle d'une cause réellement neuve (compteur 0 légitime). **Effet : la détection `INCOMPLETE_GROUP_HISTORY` suppose un registre de cycles exécutable qui n'existe pas.** Action : définir le format machine du registre des `cycle_id` (ou son équivalent) avant que le contrôleur de groupe soit implémentable.

### M4 — Registre : `occurrence_id` et codes de raison hors des vocabulaires fermés

L'`occurrence_id` (règles 9–10) est un nouvel espace d'identité sans forme ni autorité de création, hors des espaces fermés `CMP/SYM/FM/RCG`, alors que le NO-GO déclare « les identifiants stables proviennent de `CAUSAL_ID_REGISTRY.md` ». Les codes de raison (`INVALID_CAUSAL_ID_STATE`, `INVALID_OCCURRENCE_HISTORY`, `INCOMPLETE_GROUP_HISTORY`) ne figurent dans aucun vocabulaire fermé déclaré. **Effet : vocabulaire ouvert par ajout non contrôlé.** Action : déclarer forme/autorité de l'`occurrence_id` et vocabulaire fermé des codes de raison.

## Verdict

**ACCEPT_WITH_LIMITS**

Les six réfutations échouent dans leur forme directe : la substitution oracle est bloquée par l'index et le marqueur du blob, l'occurrence créée/dupliquée/privée d'ascendance est sanctionnée, le regroupement ne peut produire un compteur inférieur à l'union, P6 est `BLOCKED_IMMUTABILITY` sans preuve d'immuabilité, les six hashes concordent et aucune revue admise n'est admissible pour O2/O4/O7.

Limites conditionnelles à intégrer avant toute implémentation des contrôleurs P6 :

- **M1** — normer la syntaxe du marqueur `Oracle scope` (bloc normatif, un marqueur par oracle);
- **M2** — vérifier l'immuabilité du contenu des occurrences historiques (blob ou hash canonique au `first_recorded_commit`) pour détecter la mutation sous ID réutilisé — résout la tension `REV06.md` L2 vs règle 9;
- **M3** — définir le registre machine des `cycle_id` nécessaire à la recomputation des unions de groupes;
- **M4** — déclarer forme/autorité de l'`occurrence_id` et vocabulaire fermé des codes de raison.

Effet sur les gates : **aucun**. P6 reste bloqué (`BLOCKED_IMMUTABILITY`, L4 `OPEN_PROOF_EXTERNAL`, aucun rapport admis ne couvre O2/O4/O7) et P0 garde ses blocages connus (baseline Bitget, licence). Cette revue documentaire ne réévalue aucune performance financière et ne valide aucune hypothèse `hypothesis/HNNN-*`.
