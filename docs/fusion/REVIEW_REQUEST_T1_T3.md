# Demande de revue indépendante — réponse T1–T3

## Révision à examiner

La revue porte exclusivement sur le commit Producteur ci-dessous et son delta par rapport
à son premier parent. Le présent fichier est l'enveloppe de transmission ancrée après ce
commit; sa version `PENDING` dans le commit examiné ne fait pas partie du contenu
scientifique à évaluer.

```text
PRODUCTEUR_COMMIT=01b138eb672882f14a6801c31886bcdca34ef36c
branche=work/continuation-2026-08-28
```

Parent Producteur : `7c322a812cc7308d1045c53bd34fa854d0e5bbb4`.

## Artefacts obligatoires

- `REV13.md`;
- `docs/fusion/CAUSAL_ID_REGISTRY.md`;
- `docs/fusion/NO_GO_REGISTER.md`;
- `docs/fusion/REVIEW_ADMISSION_REGISTRY.md`;
- `docs/fusion/06_FUSION_GATES.md`;
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md`;
- `PROGRESSION.md`.

## Empreintes du dossier au commit Producteur

Les SHA-256 portent sur les octets retournés par
`git show 01b138eb672882f14a6801c31886bcdca34ef36c:<chemin>`.

| Artefact | Blob Git | SHA-256 |
|---|---|---|
| `REV13.md` | `c8e3a67f766933f69b264b0961fb99bfe5fca70b` | `c9753992f30227e959f02c3b6f1d3b7fa88c0f47befab6ade027fab051c86122` |
| `docs/fusion/CAUSAL_ID_REGISTRY.md` | `907c7e9f2c96076eef296015400fc92f305c851d` | `4969e92f5cf09c989e5eaf18ec84e99b96c4f061a9fd10cfb90ceff52a0ab628` |
| `docs/fusion/NO_GO_REGISTER.md` | `b4beef6c66c3c55cd9fca5478a5a1af268ea8564` | `0d91ad4058b628b3fb4e0109cce1ff486639ef2748294cbf5e47a4a21bb1e2e2` |
| `docs/fusion/REVIEW_ADMISSION_REGISTRY.md` | `681f1e8f7f50c936bbe4f75a2d05367c8bcee765` | `23ed1d43a8a1f0d81a7c2d7bdaacbe1fb0d09fa87c15fa39c822fa3b7bca1dc2` |
| `docs/fusion/06_FUSION_GATES.md` | `ae17843015b45a7b6527993df63979c76488dfa2` | `52d0ead162138b3b0aa35d2ab6d70b56b27ad0bbbc952dc919cb7c7755b1e8eb` |
| `docs/fusion/LIMIT_RESOLUTION_REGISTER.md` | `ecc7fd28c44e1c4916923439faf08222c1f12cdc` | `f0af27fca486c01fa2a33863e65cdd03b8124b75f33c8c5a04dd28f2b91c2452` |
| `PROGRESSION.md` | `a5a49d1da4287e51377a152afcc0d15768f8eb1b` | `c89f076ccdb72dfdd6511e48b6790426fd88b4f3b5af6ae91275964f656d3b1c` |

Commande de contrôle :

```bash
git diff --name-status 7c322a812cc7308d1045c53bd34fa854d0e5bbb4 \
  01b138eb672882f14a6801c31886bcdca34ef36c
```

## Réfutations obligatoires

1. Construire une chronologie où le même artefact prétend encore être pré-run tout en
   contenant le hash d'un rapport futur; chercher aussi un `run_id` choisissable après
   observation ou une collision traitée opportunistement.
2. Reproduire un merge transparent `-s ours` avec un parent secondaire divergent et
   déterminer si le walk normé le détecte même lorsque l'historique limité au chemin ne
   retourne pas le merge.
3. Construire deux supersessions qui consomment le même `decision_commit`, avec mêmes puis
   différentes occurrence et raison; les deux variantes doivent être rejetées.
4. Vérifier la cohérence des chemins, schémas, domaines de hashes, ancres Git, codes
   d'erreur et mutants entre tous les artefacts obligatoires.
5. Vérifier que la réponse ne revendique ni implémentation, ni résultat de mutant, ni
   `PASS` de P1/P6.

## Sortie attendue

Produire un rapport Critique et un rapport Contradictoire dans deux contextes indépendants,
avec commit exact, modèle/session, commandes et codes de sortie, contre-exemples minimaux,
verdict unique (`ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`) et effet
explicite sur les gates. La Contradictoire fige son premier verdict sans lire celui de la
Critique. L'admission reste une décision humaine explicite.
