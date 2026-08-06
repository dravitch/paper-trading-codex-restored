# Protocole Contradictoire

## Objet

Toute nouvelle hypothèse de la fusion est développée sur une branche dédiée et ne rejoint `fusion/controlled-merger` qu'après production de preuves reproductibles et deux évaluations IA distinctes : une **Critique** et une **Contradictoire**.

Une approbation signifie que les preuves soumises soutiennent l'hypothèse dans son domaine déclaré. Elle ne prouve ni vérité universelle, ni fidélité à un marché non observé, ni performance future.

## Branches

| Usage | Convention | Base | Destination autorisée |
|---|---|---|---|
| intégration contrôlée | `fusion/controlled-merger` | `main` validée | `main`, après P7 |
| hypothèse | `hypothesis/HNNN-slug-court` | dernière fusion validée | `fusion/controlled-merger` |
| correction d'une hypothèse | même branche d'hypothèse | branche concernée | branche concernée |

Une branche n'est créée que lorsque son `HNNN` est attribué et que l'énoncé préalable existe. Les branches vides ou génériques sont interdites : elles ne permettent pas de savoir ce qui peut les réfuter.

## Dossier probatoire obligatoire

Chaque branche `hypothesis/HNNN-*` ajoute :

```text
docs/fusion/hypotheses/HNNN/
├── HYPOTHESIS.md
├── EVIDENCE.md
├── MANIFEST.json
├── CRITIQUE.md
└── CONTRADICTOIRE.md
```

`HYPOTHESIS.md` fixe avant exécution :

- l'énoncé mathématique ou logique;
- le domaine de validité et les unités;
- les données, seeds et configurations;
- l'oracle calculé indépendamment;
- le résultat attendu et sa tolérance;
- le critère de réfutation;
- les statuts possibles : `PASS`, `FAIL`, `BLOCKED`, `NON_TESTABLE`.

`EVIDENCE.md` consigne les commandes, résultats, contre-exemples, erreurs, couverture et mutations. `MANIFEST.json` identifie code, environnement, données, configuration, seeds et SHA-256.

## Rôles

### Producteur

Formule l'hypothèse, implémente le minimum nécessaire et fournit les preuves. Il ne valide pas sa propre branche.

### IA Critique

Vérifie définitions, calculs, code, tests, unités, domaine annoncé et reproductibilité. Elle recherche erreurs ordinaires, omissions et circularités.

### IA Contradictoire

Cherche activement à réfuter l'hypothèse par contre-exemples, mutations, changements de référentiel, cas limites et hypothèses alternatives. Elle ne reçoit pas la conclusion de la Critique avant d'avoir figé son premier verdict.

Les deux évaluations enregistrent au minimum : identité et version du modèle lorsque disponibles, date, révision Git, prompt ou mandat, fichiers examinés, commandes exécutées, verdict et objections ouvertes. Une simple mention « reviewed by AI » est invalide.

## Indépendance minimale

1. Critique et Contradictoire sont deux sessions ou agents distincts.
2. Chacune repart de l'énoncé préalable et du même dossier probatoire.
3. La Contradictoire produit son premier verdict sans lire le verdict de la Critique.
4. Aucun évaluateur ne modifie silencieusement l'attendu après observation.
5. Tout changement de l'hypothèse ou de l'oracle invalide les deux approbations antérieures.

Deux appels du même agent dans le même contexte ne comptent pas comme deux validations indépendantes.

## Verdicts de revue

Chaque rapport conclut par un seul statut :

- `ACCEPT` : aucune réfutation ouverte dans le domaine déclaré;
- `ACCEPT_WITH_LIMITS` : acceptable seulement après intégration explicite des limites;
- `REJECT` : contradiction ou défaut probatoire;
- `NON_TESTABLE` : les données ou l'oracle ne permettent pas de trancher.

## Gate de fusion d'une hypothèse

La fusion est autorisée uniquement si toutes les conditions suivantes sont vraies :

1. branche à jour avec `fusion/controlled-merger`;
2. hypothèse et attendu antérieurs à l'exécution;
3. tests déterministes, hors réseau et non circulaires;
4. mutations prescrites effectivement rejetées;
5. manifeste et hashes présents;
6. Critique = `ACCEPT` ou `ACCEPT_WITH_LIMITS`;
7. Contradictoire = `ACCEPT` ou `ACCEPT_WITH_LIMITS`;
8. toutes les limites conditionnant un `ACCEPT_WITH_LIMITS` sont intégrées aux documents et sorties utilisateur;
9. aucune objection bloquante ouverte;
10. historique conservé par merge non fast-forward ou pull request.

`REJECT`, `NON_TESTABLE`, absence d'un rapport ou désaccord non résolu bloque la fusion. Le résultat négatif reste publié dans la branche et le registre; il ne doit pas être effacé pour obtenir un historique artificiellement vert.

## Registre

Le registre canonique se trouve dans [`HYPOTHESIS_BRANCH_REGISTER.md`](HYPOTHESIS_BRANCH_REGISTER.md). Il est mis à jour à la création de la branche, à chaque verdict et à la décision de fusion.

## Surveillance locale

`scripts/watch_fusion_reviews.sh` surveille toutes les dix secondes les fichiers `HEARTBEAT_CONTRADICTOIRE*.md`, `HEARTBIT_CONTRADICTOIRE*.md`, `REVIEW_REQUEST_*.md` et `REVIEW_ADMISSION_REGISTRY.md`. Il conserve hors dépôt, dans `/tmp/codex-fusion-watch`, le dernier SHA-256 observé et un journal `NEW`/`MODIFIED`.

```bash
scripts/watch_fusion_reviews.sh baseline
scripts/watch_fusion_reviews.sh watch 10
scripts/watch_fusion_reviews.sh check
scripts/watch_fusion_reviews.sh stop
```

Le watcher n'exécute aucun heartbeat, ne fait aucun accès réseau et ne committe rien. Il détecte l'artefact; l'admission reste une décision explicite de l'opérateur.

## Limite du protocole

Deux IA peuvent partager les mêmes biais, données périmées ou erreurs de raisonnement. Le protocole augmente la contradiction documentée; il ne remplace ni oracle indépendant, ni test mécanique, ni revue humaine pour les décisions à conséquence financière.
