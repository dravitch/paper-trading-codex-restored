# REV13 — Réponse Producteur T1–T3

## Portée

Réponse aux trois limites du rapport Contradictoire
`docs/fusion/CONTRADICTOIRE_DELTA_REV12.md`, admis avec le verdict
`ACCEPT_WITH_LIMITS`. Cette révision modifie uniquement les contrats documentaires. Elle
n'implémente aucun contrôleur, n'exécute aucun oracle et ne change le statut d'aucun gate.

## Corrections

| Constat | Défaut observé | Contrat après correction | Mutant falsifiable attendu |
|---|---|---|---|
| T1 | un unique « manifeste » devait à la fois préenregistrer le run et contenir le hash d'un rapport futur | `PRE_RUN.json` est ancré avant exécution; `MANIFEST.json` est une annexe post-run; P6 référence les deux et leur ancrage | créer ou modifier `PRE_RUN.json` après le début du run, omettre l'annexe ou substituer le hash du rapport doit rendre le run `NON_TESTABLE` |
| T2 | seuls les parents de `C` étaient inspectés, donc un merge transparent divergent entre `C` et `E` pouvait disparaître du walk limité au chemin | tous les merges de la première parenté genesis→`E` sont inspectés indépendamment de l'historique du chemin | un merge `-s ours` dont le second parent porte un autre blob doit produire le conflit de registre fermé |
| T3 | l'unicité de consommation d'une décision était déclarée sans recherche croisée | le contrôleur construit un index injectif `decision_commit → supersession_id` sur tout le registre | deux supersessions référençant le même `decision_commit` doivent produire `REGISTRY_HISTORY_VIOLATION` |

## T1 — cycle de vie fermé du manifeste de run

Le terme ambigu « manifeste du run » est séparé en deux artefacts :

1. `reports/runs/<run_id>/PRE_RUN.json`, engagement fermé et ancré dans un commit Git
   strictement antérieur à l'exécution;
2. `reports/runs/<run_id>/MANIFEST.json`, annexe post-run qui lie l'engagement au rapport
   `reports/input_validation/<run_id>.json` effectivement produit.

Le `run_id` est dérivé du contenu canonique de l'engagement, et non choisi après
observation. Le manifeste P6 doit référencer le chemin, le hash et le commit d'ancrage de
l'engagement ainsi que le chemin et le hash de l'annexe. Le SHA-256 du rapport est donc
explicitement postérieur à l'exécution; aucune préconnaissance circulaire n'est revendiquée.

## T2 — merges transparents

Le walk des révisions du fichier reste utile pour résoudre `C` et `P`, mais il ne constitue
plus le walk des merges. Le contrôleur doit parcourir séparément chaque merge de la
première parenté depuis la genesis du registre jusqu'à `E`, comparer le blob de tous les
parents à celui du premier parent, puis comparer le blob du merge à ce même blob. Un
fichier absent est comparé comme une valeur distincte.

Cette règle capture le contre-exemple `git merge -s ours` : même si le merge ne modifie pas
le chemin dans son arbre final et reste invisible à `rev-list ... -- <fichier>`, le blob
divergent de son parent secondaire déclenche le code de conflit propre au registre.

## T3 — consommation d'une décision

Chaque supersession porte déjà `decision_commit`. L'invariant devient mécanique sans
modifier le schéma JSON : sur la totalité de `supersessions`, la projection
`decision_commit → supersession_id` doit être une fonction injective. La seconde
utilisation du même commit est invalide, même si elle vise une autre occurrence ou emploie
une autre raison. Le contrôle historique du diff au commit décisionnel reste obligatoire.

## Vérifications Producteur

Les vérifications syntaxiques et documentaires à exécuter sur le commit de réponse sont :

```text
git diff --check <parent>..<commit-réponse>
python -m pytest tests -q
ruff check paper_trading_codex tests examples
```

Elles prouvent seulement l'absence de régression du dépôt existant et la cohérence de
forme. Les trois mutants ci-dessus restent `PENDING_IMPLEMENTATION` tant que le contrôleur
P6 n'existe pas.

## Statut

- T1 : `RESOLVED_SPEC_PENDING_REVIEW`;
- T2 : `RESOLVED_SPEC_PENDING_REVIEW`;
- T3 : `RESOLVED_SPEC_PENDING_REVIEW`;
- P6 : `BLOCKED_IMMUTABILITY`;
- gates franchis par cette réponse : aucun.

