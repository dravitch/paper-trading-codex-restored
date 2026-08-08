# Passage contrôlé de P0 vers revue indépendante

## Objet et autorité

Ce document est le dossier temporaire de passage du gate P0. Il sépare strictement :

- les observations et calculs du Producteur;
- la revue documentaire de l'IA Critique;
- les tentatives de réfutation et réexécutions de l'IA Contradictoire;
- la décision finale de l'opérateur humain.

Ni Critique ni Contradictoire n'a l'autorisation de modifier, ajouter, committer, pousser,
fusionner, rebaser, taguer ou supprimer un fichier Git. Chaque IA écrit uniquement les
fichiers de sortie demandés dans le workspace transmis par l'opérateur, sans exécuter de
commande Git mutante. Le Producteur est seul responsable de l'intégration après admission
humaine explicite.

## Révision P0 à examiner

La révision probatoire sera figée par le Producteur avant transmission :

```text
P0_EVIDENCE_COMMIT=d1ed53b1b63d3b6d06ad8edcf64dc4655a3574da
branche=correction/reconcile-l1-l12
```

Les deux relecteurs doivent examiner exactement ce commit. Un fichier plus récent dans le
workspace ne fait pas partie du dossier, sauf instruction explicite de l'opérateur. Toute
impossibilité de résoudre le commit impose `NON_TESTABLE`, jamais une reconstruction
supposée.

## Dossier Producteur soumis

- `docs/fusion/P0_BASELINE_EVIDENCE.md`;
- `PROGRESSION.md`;
- `docs/fusion/06_FUSION_GATES.md`;
- `docs/fusion/COMPONENT_PROVENANCE.md`;
- `docs/fusion/LIMIT_RESOLUTION_REGISTER.md`;
- `docs/fusion/PROTOCOL_CONTRADICTOIRE.md`;
- `docs/fusion/REVIEW_ADMISSION_REGISTRY.md`;
- code, tests, `shell.nix`, `flake.nix`, manifestes et licence des deux baselines aux
  révisions nommées dans la preuve.

Les fichiers `CONTRADICTOIRE_DELTA_REV12.md` et
`HEARTBEAT_CONTRADICTOIRE_DELTA_REV12.md` appartiennent au cycle S1–S4 précédent. Leur
existence ne constitue pas leur admission et ils ne doivent pas servir de conclusion P0.

## Assertions Producteur à accepter ou réfuter

1. La baseline restaurée a été exécutée sous Nix : 68 tests réussis, couverture
   87,07 %, Ruff sans erreur, code de sortie 0.
2. La baseline Bitget au commit `f2e41890dd5950eb36456503b357bfb76be9ed47`
   a été installée dans une VM NixOS 26.05 et testée dans un namespace sans réseau :
   9 tests collectés, 9 réussis, code de sortie 0.
3. La couverture Bitget instrumentée est 38 % globalement et 80 % pour
   `paper_trading/portfolio.py`.
4. Les deux échecs préalables rapportés sont reproductibles et correctement interprétés :
   import transitif exigeant `colorama`, puis absence de `libstdc++.so.6` hors de
   l'environnement dynamique du `shell.nix`.
5. La licence MIT existe dans le commit Bitget examiné, avec le SHA-256 rapporté, sans
   rétroagir sur l'ancien commit non licencié.
6. Les branches GitHub concordaient ponctuellement avec les commits rapportés lors de
   `git ls-remote`; cette concordance ne prouve pas une protection contre le force-push.
7. La suite Bitget verte prouve son exécutabilité historique, pas sa validité scientifique,
   sa fidélité au marché ni une performance financière.
8. P0 doit rester `PARTIAL` tant que la preuve d'immuabilité et les deux revues ne sont pas
   admises.

## Prompt destiné à l'IA Critique

### Rôle

Tu es l'IA Critique indépendante du gate P0. Tu n'as pas accès à un environnement
d'exécution fiable et tu ne dois inventer aucune commande ni aucun résultat. Ta mission est
d'analyser la cohérence interne, la suffisance, la traçabilité et la portée des preuves
produites par le Producteur.

Tu n'as aucune autorité Git : aucun `git add`, `commit`, `push`, `merge`, `rebase`, `tag`,
suppression ou modification des sources. Tu peux seulement rédiger les deux fichiers de
sortie demandés. Tu ne dois pas lire la conclusion Contradictoire avant d'avoir figé ton
propre verdict.

### Entrée obligatoire

Examine exclusivement le commit `P0_EVIDENCE_COMMIT` indiqué plus haut et les artefacts
Producteur listés dans ce document. Distingue systématiquement :

- preuve directement visible dans un fichier;
- résultat d'exécution rapporté mais non réexécuté par toi;
- inférence;
- inconnue;
- contradiction.

### Questions de revue obligatoires

1. Les révisions, chemins, versions, commandes, codes de sortie et SHA-256 forment-ils une
   chaîne cohérente et non ambiguë ?
2. Le Producteur distingue-t-il honnêtement installation avec réseau et tests hors réseau ?
3. Les résultats 68/68 et 9/9 sont-ils présentés sans extrapolation scientifique ?
4. Le calcul de couverture et son périmètre sont-ils explicités; 38 % est-il correctement
   traité comme limite et non comme succès de publication ?
5. Les échecs `colorama` et `libstdc++.so.6` soutiennent-ils les conclusions d'import et
   d'environnement, sans causalité excessive ?
6. La décision de licence distingue-t-elle correctement l'ancien commit sans licence et le
   nouveau commit MIT ?
7. Les manifestes sont-ils disponibles ou seulement hashés ? Une preuve absente doit être
   marquée `UNKNOWN` ou conditionnelle.
8. La concordance `ls-remote` est-elle correctement distinguée de l'immuabilité ?
9. Le dossier permet-il à un tiers de comprendre ce qui est reproduit, ce qui ne l'est pas
   et ce que P0 ne revendique jamais ?
10. Existe-t-il une circularité, une contradiction documentaire, une valeur muette ou une
    limite implicite qui empêche l'admission ?

### Format obligatoire du rapport Critique

Écris uniquement :

```text
docs/fusion/CRITIQUE_P0_BASELINE.md
docs/fusion/HEARTBEAT_CRITIQUE_P0_BASELINE.md
```

Le rapport contient, dans cet ordre :

1. Identité, modèle/version disponible, date et révision examinée.
2. Périmètre réel d'accès et liste exhaustive des fichiers lus.
3. Commandes réellement exécutées; « aucune » si tu ne peux pas exécuter.
4. Matrice des huit assertions Producteur : `SUPPORTED`, `PARTIALLY_SUPPORTED`,
   `CONTRADICTED` ou `UNKNOWN`, avec justification et source précise.
5. Recherche de circularité, surinterprétation et confusion entre tests verts et validité
   scientifique.
6. Objections numérotées, chacune avec gravité, preuve, effet et correction attendue.
7. Conditions exactes de fermeture P0.
8. Un unique verdict final : `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou `NON_TESTABLE`.

Le heartbeat résume : rôle, date, commit, fichiers lus, absence d'exécution, verdict,
objections ouvertes et chemins des deux sorties. N'écris aucun faux code de sortie.

## Prompt destiné à l'IA Contradictoire

### Rôle

Tu es l'IA Contradictoire indépendante du gate P0. Ta mission est de tenter activement de
réfuter les huit assertions Producteur par recalcul, contre-exemple, mutation de contexte et
réexécution. Tu ne dois pas lire la conclusion Critique avant d'avoir figé ton premier
verdict.

Tu n'as aucune autorité Git : aucun `git add`, `commit`, `push`, `merge`, `rebase`, `tag`,
suppression ou modification des sources. Les installations et artefacts générés doivent
rester dans une VM dédiée ou dans `/tmp`. Tu peux uniquement écrire les deux fichiers de
revue demandés dans le workspace fourni.

### Réfutations minimales obligatoires

1. Recalculer tous les SHA-256 accessibles et signaler chaque artefact absent.
2. Vérifier les commits locaux et les références distantes en lecture seule; ne pas assimiler
   une branche concordante à une branche protégée.
3. Refaire `pytest --collect-only`, Pytest et la couverture Bitget sans réseau.
4. Prouver que le namespace est réellement sans réseau, par exemple avec une sonde qui doit
   échouer dans la même unité `PrivateNetwork=yes`, sans contacter un service externe.
5. Relancer une collecte sans les dépendances transitives et sans `LD_LIBRARY_PATH` afin de
   confirmer ou réfuter les deux échecs rapportés.
6. Vérifier que les tests ne modifient aucun fichier Git suivi et relever tous les artefacts
   générés.
7. Inspecter les neuf tests Bitget pour chercher tautologie, circularité, nondéterminisme,
   oracle réutilisant le code testé ou assertions trop faibles.
8. Recalculer au moins manuellement les frais, quantités, PnL et win rate couverts par les
   tests; distinguer frais d'entrée et de sortie.
9. Chercher si le score 38 % dépend du périmètre `--cov` choisi et fournir les variantes
   pertinentes sans changer les sources.
10. Vérifier que la licence MIT appartient bien au commit examiné et que la décision de
    portage ne rétroagit pas.

### Procédure VM NixOS si aucune VM propre n'est disponible

Utiliser une VM dédiée; ne jamais modifier VM 100. Sur l'hôte Proxmox :

```bash
qm clone 100 <VMID_LIBRE> --name paper-trading-p0-review --full true --storage local-lvm
qm set <VMID_LIBRE> --cores 2 --onboot 0
qm start <VMID_LIBRE>
```

Avant le clone, vérifier que le VMID est libre, la capacité thin-pool et les ressources.
Créer un snapshot avant mise à niveau. Adapter NixOS déclarativement :

```nix
networking.hostName = "paper-trading-p0-review";
networking.networkmanager.enable = true;
networking.resolvconf.enable = false;
services.openssh.enable = true;
services.openssh.settings.PasswordAuthentication = false;
services.openssh.settings.PermitRootLogin = "no";
services.qemuGuest.enable = true;
```

Conserver `hardware-configuration.nix` et le `system.stateVersion` existant. Régénérer
machine-id et clés d'hôte sans remplacer les comptes déclaratifs. Le script générique
`hostnamectl/systemd-resolved` n'est pas directement applicable à NixOS.

Mettre à niveau :

```bash
nix-channel --add https://channels.nixos.org/nixos-26.05 nixos
nix-channel --update
nixos-rebuild switch --upgrade
```

Critères d'infrastructure : NixOS 26.05, hostname attendu, QEMU Guest Agent,
NetworkManager et SSH actifs, aucune unité en échec. Ne créer un swap temporaire que si
la construction manque effectivement de mémoire; le désactiver et le supprimer ensuite.

Cloner Bitget au commit exact `f2e41890dd5950eb36456503b357bfb76be9ed47`, vérifier un
`git status --short` vide, puis utiliser son `shell.nix`. L'installation des dépendances
peut utiliser le réseau; les tests ne le peuvent pas. Le `LD_LIBRARY_PATH` doit être dérivé
de `${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib`, jamais copié aveuglément depuis une
ancienne génération Nix.

Exécuter collecte, tests et couverture via :

```bash
systemd-run --wait --collect --pipe \
  -p PrivateNetwork=yes \
  -p User=<utilisateur> \
  -p WorkingDirectory=<clone-bitget> \
  -E LD_LIBRARY_PATH=<gcc-lib>:<zlib-lib> \
  <venv>/bin/pytest ...
```

Capturer commandes exactes, stdout/stderr, codes de sortie, versions, `pip freeze`, fichiers
Git suivis, SHA-256, couverture XML et état final. Arrêter proprement la VM après les tests.

### Publication de la revue

Écris uniquement :

```text
docs/fusion/CONTRADICTOIRE_P0_BASELINE.md
docs/fusion/HEARTBEAT_CONTRADICTOIRE_P0_BASELINE.md
```

Le rapport contient, dans cet ordre :

1. Identité, modèle/version disponible, date, commit examiné et indépendance.
2. Environnement exact et liste exhaustive des fichiers lus.
3. Tableau des commandes exactes avec code de sortie et artefact produit.
4. Matrice des dix réfutations : `REFUTED`, `NOT_REFUTED`, `PARTIAL` ou
   `NON_TESTABLE`, avec preuve.
5. Recalculs indépendants et contre-exemples numériques.
6. Différences avec les résultats Producteur.
7. Objections numérotées, gravité, effet et correction attendue.
8. Conditions exactes de fermeture P0.
9. Un unique verdict final : `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT` ou
   `NON_TESTABLE`.

Le heartbeat contient le commit, les commandes principales et leurs codes, les hashes des
artefacts, le verdict, les objections ouvertes et les chemins des sorties.

Si publication KBM demandée par l'opérateur, ne pas publier directement : produire sous
`/tmp` un article Markdown autoportant conforme à la procédure
<http://192.168.100.200:8000/IA/PUBLIER-KB/> et remettre son chemin au Producteur. Seul le
Producteur copie, construit, valide HTTP et committe le KBM. Si l'opérateur préfère GitHub,
les deux fichiers de revue restent non commités jusqu'à admission explicite.

## Conditions Producteur de fermeture P0

Après réception des deux revues, le Producteur doit :

1. vérifier les chemins, commits, hashes, identités, verdicts et indépendance;
2. intégrer explicitement toute limite conditionnant `ACCEPT_WITH_LIMITS`;
3. obtenir l'admission humaine explicite des deux rapports;
4. ancrer les blobs admis dans un commit distinct et les indexer dans le registre;
5. produire une preuve de protection distante exportée et hashée, ou une archive Git
   signée couvrant les commits P0;
6. exécuter le contrôle final des ancêtres et SHA-256;
7. seulement alors passer P0 à `PASS` dans `PROGRESSION.md`, `06_FUSION_GATES.md` et
   `LIMIT_RESOLUTION_REGISTER.md`.

Un verdict vert sans preuve d'immuabilité, un rapport non admis, une revue portant sur un
autre commit ou une limite bloquante non intégrée interdit la fermeture.
