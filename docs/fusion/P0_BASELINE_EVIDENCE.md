# Preuve Producteur P0 des deux baselines

## Statut

`PRODUCER_EVIDENCE_PENDING_INDEPENDENT_REVIEW`

Ce document rapporte des observations reproductibles. Il ne vaut ni admission humaine,
ni revue Critique/Contradictoire, ni `PASS` du gate P0.

## Périmètre

| Baseline | Révision examinée | Provenance distante observée |
|---|---|---|
| `paper-trading-codex-restored` | `5bac10bd0dd7b23d3554174477442df804df7f8d` | `refs/heads/correction/reconcile-l1-l12` |
| `bitget-paper-trading` | `f2e41890dd5950eb36456503b357bfb76be9ed47` | `refs/heads/claude/explore-code-cloud-Hm5n9` |

Les références ont été relues avec `git ls-remote` le 2026-08-07. Cette observation
prouve la concordance ponctuelle de la branche et du commit; elle ne prouve pas une
protection GitHub contre le force-push. P0 reste donc ouvert sur l'immuabilité distante.

## Environnement Bitget isolé

| Champ | Valeur observée |
|---|---|
| Hyperviseur | Proxmox, `192.168.100.200` |
| VM | VMID 110, `paper-trading-p0`, clone complet de VM 100 |
| OS | NixOS 26.05 « Yarara », `26.05.7006.445d861c6d31` |
| Système actif | `/nix/store/hkbv46rhi68c9ml9bk57mq50lga1wzr6-nixos-system-paper-trading-p0-26.05.7006.445d861c6d31` |
| Python | 3.11.15 |
| Pytest | 9.1.1 |
| NumPy / Pandas / CCXT | 1.26.4 / 2.3.3 / 4.5.71 |
| Réseau pendant les tests | bloqué par `systemd-run -p PrivateNetwork=yes` |
| Services en échec après exécution | aucun |

Le `shell.nix` historique a créé `.venv` et installé `requirements.txt` dans le clone
isolé. Le réseau n'a servi qu'à l'installation des dépendances; la collecte, les tests et
la couverture ont été exécutés hors réseau. Les contraintes du manifeste sont des
intervalles et non un lockfile : le manifeste `pip freeze` est donc une preuve nécessaire.

## Commandes et résultats Bitget

### Contrôle minimal d'import

Une collecte initiale avec seulement Python, Pytest et Loguru a échoué avant collecte :

```text
ModuleNotFoundError: No module named 'colorama'
exit code 2
```

Cause observée : importer `paper_trading.portfolio` exécute
`paper_trading/__init__.py`, qui importe avidement `engine`, puis les dépendances des
adaptateurs. Ce couplage est un constat de baseline; il n'a pas été corrigé dans la source.

Une collecte avec le venv complet mais sans l'environnement dynamique du `shell.nix` a
ensuite échoué sur :

```text
ImportError: libstdc++.so.6: cannot open shared object file
exit code 2
```

La collecte réussie utilise donc le `LD_LIBRARY_PATH` déclaré par le `shell.nix` :

```bash
systemd-run --wait --collect --pipe \
  -p PrivateNetwork=yes \
  -p User=netpulser \
  -p WorkingDirectory=/home/netpulser/baselines/bitget-paper-trading \
  -E LD_LIBRARY_PATH="${NIX_CC_LIB}/lib:${NIX_ZLIB}/lib" \
  .venv/bin/pytest --collect-only -q
```

Résultat observé : `9 tests collected`, code de sortie 0.

### Tests

La même unité isolée a exécuté `.venv/bin/pytest -v`.

```text
9 passed in 2.87s
exit code 0
```

### Couverture

`pytest-cov` 7.1.0 et Coverage.py 7.15.4 ont été installés après le gel du manifeste
historique, exclusivement comme instrumentation d'audit.

```text
paper_trading/portfolio.py  80 %
TOTAL                       38 %
9 passed in 8.58s
exit code 0
```

La suite historique est exécutable, mais la couverture globale ne satisfait pas le seuil
de publication de 70 %. Les neuf tests ne suffisent pas à valider le moteur, les métriques,
les adaptateurs ou la fidélité au marché.

## Empreintes Bitget

| Artefact | SHA-256 |
|---|---|
| manifeste des 22 fichiers Git suivis | `4a14e4785e364e82e4fa1394f83c2c8bb650ec1fecb8059f1c01e00a22b3b526` |
| `LICENSE` MIT | `dd10b10e2f68cef2e58683088bd1f3ff2194ba1151f15191cc60aed742365c83` |
| manifeste pip avant instrumentation | `18621128866d16f6bcca7bd72129a104ab1a0b1618d82a26edd8f43050989c8a` |
| manifeste pip avec instrumentation | `b8d5c2100eb93721874fde6cf4896551e88af08332c45336e6a8f190e9b45a44` |
| rapport Coverage XML | `845365692887558511bb65a7fe673ec097f6676edcb95756ef64d15ad0215402` |

Le fichier `.coverage` généré et le swap temporaire de construction ont été supprimés.
Le `git status --short` final du clone Bitget est vide.

## Baseline restaurée déjà reproduite

La preuve antérieure du dépôt restauré rapporte, sous Nix : Python 3.12.12, 68 tests
réussis, couverture 87,07 %, Ruff sans erreur, code de sortie 0. Cette preuve reste
distincte de l'exécution Bitget ci-dessus et ne doit pas être agrégée en un score commun.

## Licence et portage

Le commit Bitget examiné contient une licence MIT ajoutée explicitement et poussée au
dépôt distant. La décision Producteur peut donc passer de `BLOCKED_LICENSE` sur l'ancien
commit `adc1d275...` à `PORT_PENDING_REVIEW` pour les seuls fichiers du commit
`f2e41890...`. L'attribution et la conservation de la licence restent obligatoires.

## Nettoyage et limites

- Le swap temporaire `/var/lib/p0-build.swap` a été désactivé puis supprimé.
- `swapon --show` et `systemctl --failed --no-legend` sont vides après l'audit.
- La VM conserve le venv d'audit et le clone pour réexécution; ils ne sont pas des sources.
- La VM 110 a été arrêtée proprement après les vérifications; `qm status 110`
  rapporte `stopped`.
- Le snapshot Proxmox `pre-nixos-2605` est un retour d'infrastructure, pas une archive
  probatoire signée des dépôts.
- Aucune preuve de branch protection GitHub ou d'archive signée n'a encore été produite.
- Aucun résultat de performance financière n'est revendiqué.

## Publication KB

Le parcours d'infrastructure, les échecs intermédiaires et les preuves applicatives sont
publiés dans la KB :

<http://192.168.100.200:8000/projets/paper-trading-codex-restored/docs/kb001-vm-nixos-p0/>

Build KB : code 0. Contrôle HTTP local final au serveur : `200`, 46 811 octets. Commits KB
locaux : `ac3a3ee` (preuve applicative), puis `27fa89b` (arrêt de la VM). Le dépôt KB ne
possède pas de remote configuré; ces commits ne sont donc pas revendiqués comme publiés
sur un dépôt distant.

## Verdict Producteur P0

`PARTIAL` : les deux baselines disposent maintenant de résultats d'exécution séparés, la
licence MIT Bitget est observée et les révisions distantes concordent ponctuellement. P0 ne
peut pas passer avant preuve d'immuabilité distante conforme au protocole et revue
indépendante du présent dossier.

## Réponse Producteur aux revues admises

Les rapports Critique et Contradictoire ont été admis par l'opérateur le 2026-08-08 au
commit distinct `804002fbbcdb8ade13309e5f49cae9452e7b741a`. Les deux verdicts sont
`ACCEPT_WITH_LIMITS`.

### Chaîne d'import

La mention historique de `colorama` décrit le premier module absent dans l'environnement
minimal du Producteur, pas une séquence universelle. L'ordre observable dépend des paquets
déjà installés : `portfolio.py` exige d'abord Loguru; l'import avide de `engine` depuis
`paper_trading/__init__.py` expose ensuite notamment Colorama, Pandas, NumPy et CCXT. La
conclusion stable est le couplage transitif excessif, pas le nom du premier module absent.

Contradictoire a recollecté indépendamment la baseline restaurée : 68 tests collectés,
68 réussis, couverture 87,07 % et Ruff sans erreur, tous avec code de sortie 0. La réserve
Critique sur l'absence de recollecte est donc levée par la seconde revue.

### Périmètre de couverture

Le terme historique « 38 % global » est remplacé pour toute interprétation future par :

```text
pytest --cov=paper_trading : 465 statements, 175 covered, 38 %
paper_trading/portfolio.py : 80 %
pytest --cov sans cible    : 778 statements, 42 % (inclut les tests observés)
pytest --cov=.             : 898 statements, 36 % (mesure Critique)
```

La métrique P0 canonique de 38 % porte uniquement sur le paquet `paper_trading`. Elle ne
représente ni tout le dépôt, ni les adaptateurs, ni `core`, ni une couverture scientifique.

### Artefacts non canoniques

- Un `pip freeze` instrumenté est comparé comme ensemble de lignes normalisées par
  `LC_ALL=C sort -u`, jamais par le hash de l'ordre brut. La différence admise est exactement
  l'ajout de `coverage==7.15.4` et `pytest-cov==7.1.0`.
- `coverage.xml` contient un timestamp. Son hash brut identifie une exécution, mais n'est
  pas un attendu reproductible. L'oracle inter-exécutions est le tuple structurel
  `{lines-valid=465, lines-covered=175, line-rate=0.3763}` avec la commande et les versions.
- Avant fermeture, les manifestes normalisés et le rapport brut ou sa projection canonique
  doivent être versés dans un emplacement accessible et hashé.

### Statut après admission

Les limites de narration, recollecte et périmètre sont intégrées. Restent bloquants : la
mise à disposition des artefacts canoniques, puis une preuve de protection distante ou une
archive Git signée couvrant `d1ed53b...` et `f2e41890...`. P0 reste `PARTIAL`.
