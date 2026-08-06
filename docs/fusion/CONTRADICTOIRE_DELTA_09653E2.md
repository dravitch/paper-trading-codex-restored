# Rapport Contradictoire — Delta 09653e2 (REV05, consolidation L1–L12)

## Objet examiné

Commit Producteur `09653e2` « docs: reconcile contradictory limits L1-L12 » sur branche `correction/reconcile-l1-l12`, base `e413867`, candidat à la fusion dans `fusion/controlled-merger`. Objet = consolidation des limites L1–L12 de la revue Contradictoire de faisabilité et des objections Critique C1–C3, conformément à `docs/fusion/REVIEW_REQUEST_REV05.md`.

## Identité et contexte

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| modèle | `opencode/big-pickle` (version de publication non disponible) |
| date | 2026-08-06 |
| révision examinée | `09653e2f1d66d41bcf20f21f907aa47ca0dfc686` |
| HEAD de la branche au moment de la revue | `273046a3fb635a3999f02aff5f495b426531cb7c` |
| indépendance | aucun rapport Critique de ce delta lu avant le gel du verdict; seuls le delta, le mandat `REVIEW_REQUEST_REV05.md` et mes vérifications mécaniques ont fondé ce verdict |

## Fichiers examinés (delta uniquement)

- `CONTROLLED_MERGER_FEASIBILITY.md` (§8, §9.4, §9.7, §12.1, §12.2, §16)
- `docs/fusion/02_REFERENCE_MODEL.md`, `04_ENGINE_COMPATIBILITY.md`, `05_RISKMAP_ORACLES.md`, `06_FUSION_GATES.md`, `CANONICAL_CONTRACT_RFCS.md`, `README.md`
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md`, `docs/fusion/COMPONENT_PROVENANCE.md`, `REV05.md`
- `paper_trading_codex/core/data_fetcher.py`, `paper_trading_codex/core/exchange_simulator.py` (modifications de docstrings/messages)
- Vérifications externes : `ARCHIVES/02_BIGET_PAPERTRADING/bitget-paper-trading` (pin, licence), tests du dépôt restauré

## Commandes exécutées

```text
git show 09653e2 / 273046a  (lecture du delta et du mandat)
nix develop --no-write-lock-file -c bash -lc \
  'pytest -q --cov=paper_trading_codex --cov-report=term-missing && ruff check .'
   -> 68 passed in 1.87s ; coverage 87.07% ; ruff : All checks passed! ; Python 3.12.12
git cat-file -t adc1d27508c1789d185d28109df2b854449b418a   -> commit (pin vérifié)
find bitget-paper-trading -maxdepth 2 \( -iname LICENSE -o -iname COPYING -o -iname NOTICE \) -> 0
python3 (calculs O8/O10/O11 et mutation <-> <=)
grep -rn "now()\|IsolatedShortModel\|IsolatedMarginModel\|rsi\|signal_generator" (état résiduel)
```

## Preuve Nix annoncée — statut

La commande exacte du registre a été **réexécutée, pas recopiée** : `exit 0`, `68 passed`, `87.07 %`, `All checks passed!`, Python `3.12.12`. Seul le temps diffère (1,87 s vs 2,26 s), sans portée probatoire (charge machine). **L11 (dépôt restauré) : REPRODUCED.**

## Vérifications mécaniques indépendantes

| Assertion du delta | Vérification | Verdict |
|---|---|---|
| O8 : P `(2,0)` domine Z `(0,0)` sur le seul rendement | dominance recalculée : **P est non dominé** (Z est dominé par P) | **confirmé** |
| O10 : X `(6,3)` domine Y `(6,4)` sur le seul drawdown | dominance stricte calculée | **confirmé** |
| O10 mutation `<`→`<=` fait échouer O1 | ensemble sémantique O1 devient `{A,D,E}` ≠ `{A,B,D,E}` | **confirmé** (mutation efficace) |
| O11 : Q `(4,1)` et R `(8,5)` mutuellement non dominés | calculé | **confirmé** |
| pin Bitget `adc1d27…` | commit existe dans le clone local; remote `dravitch/bitget-paper-trading` | **confirmé** |
| « aucun LICENSE* à profondeur 2 » | 0 fichier `LICENSE/COPYING/NOTICE` hors `.venv` | **confirmé** |
| C1 : 40099 retiré du code | une occurrence historique **qualifiée** subsiste volontairement dans `data_fetcher.py:27` (« fournisseur 40099 non datée et non reproduite »); plus aucun énoncé de permanence; endpoints privés lèvent toujours `NotImplementedError`; `match="PortfolioManager|ExchangeSimulator"` satisfait (68 verts) | **confirmé** |
| L10 : nom unique | `IsolatedLinearShortAccountModel` seul dans les documents actifs; seuls reliquats = ma source contradictoire (attendue) | **confirmé** |
| L9 : aucune copie Bitget | aucun code RSI/signal_generator dans `paper_trading_codex/` ni `tests/` (les occurrences « rsi » sont des sous-chaînes) | **confirmé** |
| C2 : mutation « Sell & Hold = plafond » ajoutée à P7 | présente dans `06_FUSION_GATES.md` | **confirmé** |

Les 12 mutations documentaires minimales du mandat (`REVIEW_REQUEST_REV05.md`) sont chacune couvertes par un texte figé du delta (O2 univoque, `point_id` exclu et tri imposé en O7, NaN interdit O9/RFC-008, rayon O4 figé, hash≠tolérance §8, `now()` P1, provider P3, NO-GO §12.1, `BLOCKED_LICENSE`, alias rejeté RFC-005, baseline Bitget non présentée comme reproduite, O2/O4/O7 soumis à revue tierce).

## Tentatives de réfutation — issues

| # | Attaque | Issue |
|---|---|---|
| T1 | L5 (hash bit-exact) est irréalisable : les calculs en binary64 ne sont pas reproductibles entre processus | Non réfutée : l'environnement est verrouillé (flake), la sérialisation canonique exclut timestamps/chemins/NaN et la tolérance est séparée du hash. Cohérent |
| T2 | L7 (convention de frais) : un règlement en actif de base changerait l'oracle 0,1999 | Non réfutée : `fee_settlement` USD/gross_notional/per_fill reproduit exactement 0,1999; le règlement en base est explicitement exclu de cet oracle |
| T3 | L1 (liquidation = contrainte dure) contredit §9.4 « point liquidé à rendement élevé » | Non réfutée : O2 conserve le point dans `FailureMap` avec métriques descriptives; cohérent avec §9.4/§9.8 |
| T4 | La clé O7 n'est pas réellement invariante par permutation | Non réfutée dans son domaine déclaré (les six points O1) : exclusion de `point_id`/ordre/timestamp + tri lexicographique ⇒ invariance par construction |
| T5 | La mutation O10 ne ferait pas échouer O1 | Réfutée (par recalcul) : la mutation change l'ensemble sémantique, donc l'attendu O1 |
| T6 | Le commit « docs: » modifie du code | **Partiellement fondée** : `data_fetcher.py`/`exchange_simulator.py` modifiés (messages d'exception). Aucun calcul métier touché, tests verts. Voir R5 |

## Limites résiduelles (conditions du verdict)

Chaque limite nomme fichier, énoncé, contre-exemple et effet sur les gates.

**À intégrer avant P1/P6 :**

- **R1 — `05_RISKMAP_ORACLES.md` (O7).** La clé canonique n'inclut en résultat que `(G, D, liquidated)`. Utilisée comme clé de déduplication générale d'un `RiskMap` multi-axes (ES, turnover, funding, §9.5), elle fusionnerait des points distincts ayant même `(G,D)` mais d'autres métriques différentes. Contre-exemple : deux runs `(G=6,D=3)` avec ES différents seraient dédupliqués. Effet : P6 pourrait perdre des points sans échec. Action : déclarer la clé O7 limitée au domaine de l'oracle, ou l'étendre aux métriques mandatées.
- **R2 — `05_RISKMAP_ORACLES.md` (O7).** `reference_hash` est référencé dans la clé mais sa dérivation n'est pas spécifiée (sérialisation canonique de quel objet ?). Effet : P6 ne peut pas évaluer O7 sans définition. Action : une ligne — `reference_hash = SHA-256` de la sérialisation canonique du `ReferenceSpec`.
- **R3 — `06_FUSION_GATES.md` (P1).** La mutation « réintroduire `now()` » n'a pas de périmètre de modules défini. Or la branche contient encore 4 `datetime.now()` légitimes dans le code legacy (`grid_bot.py:408`, `portfolio_manager.py:66,157`, `exchange_simulator.py:90` — ce dernier dans un fichier touché par le delta), que P0 interdit de modifier. Contre-exemple : une mutation portant sur toute la package échouerait sur la baseline elle-même. Effet : P1 bloqué ou mutation tronquée. Action : scoper la mutation aux modules du domaine ou planifier la purge des fallbacks legacy dans P1.
- **R7 — `05_RISKMAP_ORACLES.md` (O9) / RFC-008.** Le point `I=(G=+inf)` est un *input* à classer `ERROR NON_FINITE_OBJECTIVE`, mais la sérialisation canonique interdit NaN/±inf. Le chemin de représentation en mémoire du point non fini (avant exclusion) n'est pas spécifié. Effet : P6 risque de rejeter le point sans produire le statut attendu. Action : détection à l'entrée, consignation dans `anomalies` du `ResultBundle`, jamais sérialisé.

**Items de processus (à enregistrer, ne bloquent pas le delta) :**

- **R4 — `05_RISKMAP_ORACLES.md`.** Les oracles O2/O4/O7 sont déclarés « acceptés après revue Contradictoire d'une révision figée », sans champ de statut/révision par oracle. Action : marquer leur acceptation (révision `09653e2`) une fois le présent delta figé.
- **R5 — type de commit.** Un commit étiqueté `docs:` modifie des messages d'exception (comportement observable). Hygiène : séparer les changements de code des changements documentaires.
- **R6 — `05_RISKMAP_ORACLES.md` (O4).** Seul le point 3 a un attendu individuel figé; les statuts des points 1, 2, 5 sont dérivables de la règle, donc moins indépendants. Acceptable, à noter.
- **R8 — §12.1 NO-GO.** « deux gates consécutifs BLOCKED trois cycles documentés » : « cycle » non défini; aucun opérateur d'application ni registre des constats NO-GO. Effet sur gates : faible, mais la falsifiabilité annoncée exige un mécanisme d'enregistrement.

## Réfutations rejetées

- La preuve Nix annoncée serait « non reproductible » : **reproduite à l'identique** (chiffres exacts).
- Le delta modifierait un calcul métier : diff = docstrings/commentaires/messages seulement; 68 tests verts; aucun seuil, frais ou formule touché.
- La consolidation serait une « modification de l'attendu après observation » : le registre interdit de réécrire la source contradictoire (respecté) et fige les attendus par des textes datés (respecté).

## Verdict

**ACCEPT_WITH_LIMITS**

Le delta `09653e2` résout effectivement les limites L1–L12 au niveau spécification et preuve : O2 univoque, O7 opérationnalisé, O8–O11 ajoutés et vérifiés par recalcul, hash séparé de la tolérance, frais réglés en numéraire, mutations P1/P3/P7 présentes, NO-GO définis, provenance/licence encadrée (`BLOCKED_LICENSE`), nom de compte unifié, preuve Nix reproduite.

La fusion du delta dans `fusion/controlled-merger` est autorisée sous les conditions suivantes : les limites **R1, R2, R3, R7** sont intégrées aux documents avant le franchissement des gates **P1** et **P6**; les items **R4, R5, R6, R8** sont enregistrés dans le registre de résolution. Aucune de ces limites ne bloque le retour du delta lui-même.

Ce verdict ne valide aucune hypothèse `hypothesis/HNNN-*` ni aucun gate; la baseline Bitget de L11 et les mutations exécutables de L6 restent `OPEN_PROOF`.
