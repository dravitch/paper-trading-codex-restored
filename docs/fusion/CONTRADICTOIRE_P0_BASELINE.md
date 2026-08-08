# Rapport Contradictoire — gate P0, baselines `paper-trading-codex-restored` et `bitget-paper-trading`

## 1. Identité, modèle, date, révision examinée et indépendance

- Rôle : IA Contradictoire indépendante du gate P0 (cycle de réexécution et de réfutation).
- Modèle/version : big-pickle (opencode), variante Contradictoire du dossier P0.
- Date : 2026-08-08.
- Révision probatoire examinée : `d1ed53b1b63d3b6d06ad8edcf64dc4655a3574da`
  (`P0_EVIDENCE_COMMIT`, branche `correction/reconcile-l1-l12`).
- Baseline Bitget réexécutée : `f2e41890dd5950eb36456503b357bfb76be9ed47`.
- Independent : les fichiers `CONTRADICTOIRE_DELTA_REV12.md`,
  `HEARTBEAT_CONTRADICTOIRE_DELTA_REV12.md`, `CRITIQUE_P0_BASELINE.md`,
  `HEARTBEAT_CRITIQUE_P0_BASELINE.md` et tout `REVUE_CRITIQUE_*` ou `docs/deepsearch/*`
  n'ont pas été lus. Aucun commit Git n'a été créé ; aucune commande Git mutante.
- Résultat d'exécution propre : ré-exécution indépendante sur une VM dédiée (VMID 140),
  clone frais des deux dépôts, sans réseau pendant collecte/tests/couverture.

## 2. Environnement exact et fichiers lus

### Infrastructure de ré-exécution (VM dédiée)

| Champ | Valeur observée |
|---|---|
| Hyperviseur | Proxmox, `192.168.100.200` |
| VM de ré-exécution | VMID 140, `paper-trading-p0-review`, clone complet de VM 100 |
| OS | NixOS 26.05 « Yarara », révision `26.05.7006.445d861c6d31` |
| Système actif | `/nix/store/dymcisz163vc23sjz2ff7mf15r9qmp47-nixos-system-paper-trading-p0-review-26.05.7006.445d861c6d31` |
| Unité en échec après audit | aucune (`systemctl --failed` vide) |
| Services actifs | qemu-guest-agent, NetworkManager, sshd |
| IP | `192.168.100.105/24` |
| Réseau pendant tests | bloqué par `systemd-run -p PrivateNetwork=yes` |

Anomalie connue du gabarit VM 100 (fichiers `passwd/group/shadow` et cartes
`/var/lib/nixos/{uid-map,gid-map,auto-subuid-map}` vides) : documentée dans la KB
`kb001-vm-nixos-p0`, corrigée déclarativement par le Producteur sur VM 110 et réparée de
façon identique sur VM 140 avant exécution. Aucun impact sur la représentativité de la
ré-exécution : le clone applicatif et le venv sont reconstruits indépendamment.

### Clones et environnements

- `/home/netpulser/baselines/bitget-paper-trading` @ `f2e41890` : clone frais, `git status` vide.
- `/home/netpulser/baselines/restored` @ `d1ed53b` : clone frais, `git status` vide.
- Bitget : `nix-shell` historique → `.venv` (Python 3.11.15), `requirements.txt` installé.
- `LD_LIBRARY_PATH` dérivé du `shell.nix` :
  `/nix/store/7vafhlh0lmcvi75jfyy09qwr4m3x1ks3-gcc-15.2.0-lib/lib:/nix/store/483x61iy35irm4wr2b7dwzihljhp6da2-zlib-1.3.2/lib`.

### Fichiers lus (exhaustif)

- `docs/fusion/P0_BASELINE_EVIDENCE.md` (blob `d615010629ded11b4ac88c05169fee3125131afe6f4cce223a3e9d4f8c018cc3`, identique localement et sur VM 140).
- `PROGRESSION_TEMP_CONTRADICTOIRE.md` (mandat, assertions, réfutations, procédure VM).
- Source et tests des deux clones (`bitget-paper-trading` : `paper_trading/*.py`,
  `tests/test_portfolio.py`, `shell.nix`, `requirements.txt` ; `restored` :
  `paper_trading_codex/*.py`, `tests/*.py`, `flake.nix`, `pyproject.toml`).
- KB : `http://192.168.100.200:8000/projets/paper-trading-codex-restored/docs/kb001-vm-nixos-p0/`
  (procédure de VM de preuve et empreintes attendues).

## 3. Commandes exactes exécutées (code de sortie et artefact)

### Bitget — manifeste et licence

```bash
cd /home/netpulser/baselines/bitget-paper-trading
git ls-tree -r HEAD | awk '{print $4}' | while read f; do sha256sum "$f"; done | sha256sum
# -> 4a14e4785e364e82e4fa1394f83c2c8bb650ec1fecb8059f1c01e00a22b3b526  (exit 0)
sha256sum LICENSE
# -> dd10b10e2f68cef2e58683088bd1f3ff2194ba1151f15191cc60aed742365c83  (exit 0)
git status --short   # vide (exit 0)
```

### Bitget — collecte, tests, couverture, hors réseau

```bash
systemd-run --wait --collect --pipe -p PrivateNetwork=yes -p User=netpulser \
  -p WorkingDirectory=/home/netpulser/baselines/bitget-paper-trading \
  -E LD_LIBRARY_PATH=<gcc-lib>:<zlib-lib> \
  .venv/bin/pytest --collect-only -q
# -> 9 tests collected in 2.29s (exit 0)

systemd-run --wait --collect --pipe -p PrivateNetwork=yes -p User=netpulser \
  -p WorkingDirectory=/home/netpulser/baselines/bitget-paper-trading \
  -E LD_LIBRARY_PATH=<gcc-lib>:<zlib-lib> \
  .venv/bin/pytest -q
# -> 9 passed in 2.26s (exit 0)

systemd-run --wait --collect --pipe -p PrivateNetwork=yes -p User=netpulser \
  -p WorkingDirectory=/home/netpulser/baselines/bitget-paper-trading \
  -E LD_LIBRARY_PATH=<gcc-lib>:<zlib-lib> \
  .venv/bin/pytest --cov=paper_trading --cov-report=term --cov-report=xml -q
# -> TOTAL 465 stmts, 290 missed, 38% ; paper_trading/portfolio.py 158 stmts, 80% ;
#    9 passed in 3.48s (exit 0)
# -> artefact coverage.xml : lines-valid=465, lines-covered=175, line-rate=0.3763,
#    version 7.15.4 (SHA-256 0ae24b5b0f4d37111940c6f91c0c0149ae8ecb6adea5d468fb2011169887a788)
```

### Bitget — sonde de réseau dans le même namespace

```bash
# /tmp/probe_net.py : socket.create_connection("192.168.100.1", 80, timeout 5)
# dans l'unité PrivateNetwork=yes :
# -> SONDE_NET_BLOCKED: OSError [Errno 101] Network is unreachable (exit 1)
# sur l'hôte (sans isolation) :
# -> SONDE_NET_OK (exit 0)
```

### Bitget — échecs préalables (réfutation 5)

```bash
# venv minimal (pytest + loguru + pytest-asyncio, sans colorama), avec LD_LIBRARY_PATH :
# -> ModuleNotFoundError: No module named 'colorama' (collecte : "no tests collected, 1 error")
# venv complet mais sans LD_LIBRARY_PATH :
# -> ImportError: libstdc++.so.6: cannot open shared object file (exit 2)
```

### Bitget — manifestes pip

```bash
# avant instrumentation (dans nix-shell, pip 25.3) :
# -> SHA-256 18621128866d16f6bcca7bd72129a104ab1a0b1618d82a26edd8f43050989c8a
# avec instrumentation (coverage 7.15.4 + pytest-cov 7.1.0) :
#   - via .venv/bin/pip (24.0) : 5a05adea...
#   - via pip 25.3 (nix-shell)  : 012fb968502b2c6bec43beae1647284550d05970c0a2073e524f5750ef539297
#   contenu = avant + "coverage==7.15.4" + "pytest-cov==7.1.0" uniquement (diff)
```

### Bitget — couverture selon périmètre (réfutation 9)

```bash
.venv/bin/pytest --cov ...                # 778 stmts, 453 missed, 42% (inclut tests/)
.venv/bin/pytest --cov=paper_trading ...  # 465 stmts, 290 missed, 38%
```

### Bitget — état final

```bash
rm -f coverage.xml .coverage; rm -rf .pytest_cache
git status --porcelain   # 0 (aucune modification de fichier suivi)
```

### Restored — collecte, tests, couverture, Ruff sous Nix

```bash
cd /home/netpulser/baselines/restored
nix develop --command bash -c 'pytest --collect-only -q'
# -> 68 tests collected in 6.81s (exit 0)
nix develop --command bash -c 'pytest --cov=paper_trading_codex --cov-report=term; ruff check .'
# -> 68 passed in 3.42s (exit 0)
#    TOTAL 545 stmts, 49 missed, 87% ; "Required test coverage of 70.0% reached.
#    Total coverage: 87.07%" (exit 0)
# -> ruff : "All checks passed!" (exit 0)
rm -f .coverage coverage.xml; rm -rf .pytest_cache
git status --porcelain   # 0
```

## 4. Matrice des dix réfutations obligatoires

| # | Réfutation du mandat | Verdict | Preuve |
|---|---|---|---|
| 1 | Recalculer tous les SHA-256 accessibles ; signaler les artefacts absents | `NOT_REFUTED` | Manifeste 22 fichiers `4a14e478…` et `LICENSE` `dd10b10e…` reproduits octet-à-octet. Blob `P0_BASELINE_EVIDENCE.md` `d6150106…` identique au workspace. Deux hashes non reproductibles octet-à-octet : `pip freeze` avec instrumentation (`b8d5c210…`) et `coverage.xml` (`84536569…`) — voir §6 ; contenu reproduit dans les deux cas |
| 2 | Vérifier commits locaux et références distantes ; ne pas assimiler concordance à protection | `NOT_REFUTED` | `d1ed53b` résolu, ancêtres et blob concordants ; `git ls-remote` : `correction/reconcile-l1-l12` = `5ed9f07…`, branches concordantes ponctuellement ; aucune preuve de branch protection, correctement énoncée par le Producteur |
| 3 | Refaire `pytest --collect-only`, Pytest et couverture Bitget sans réseau | `NOT_REFUTED` | 9 collectés, 9 passés, exit 0 ; couverture 38 % / 80 % reproduite hors réseau |
| 4 | Prouver que le namespace est réellement sans réseau (sonde échouant dans la même unité) | `NOT_REFUTED` | Sonde → `Network is unreachable` (exit 1) dans l'unité, `SONDE_NET_OK` (exit 0) sur l'hôte |
| 5 | Relancer collecte sans dépendances transitives et sans `LD_LIBRARY_PATH` | `NOT_REFUTED` | `colorama` : `ModuleNotFoundError` reproduit ; `libstdc++.so.6` : `ImportError` reproduit (exit 2) |
| 6 | Vérifier que les tests ne modifient aucun fichier Git suivi ; relever les artefacts | `NOT_REFUTED` | `git status --porcelain` vide après nettoyage ; artefacts générés : `.coverage`, `coverage.xml` (non gitignorés — supprimés), `.pytest_cache` (ignoré) |
| 7 | Inspecter les 9 tests : tautologie, circularité, nondéterminisme, oracle réutilisant le code testé | `NOT_REFUTED` | Oracles externes explicites (montants, taux fixes), aucune réutilisation du code testé, résultats déterministes ; faiblesse relevée : portée limitée (9 tests, couverture faible) mais pas de tautologie |
| 8 | Recalculer manuellement frais, quantités, PnL, win rate ; distinguer frais d'entrée/sortie | `NOT_REFUTED` | Recalcul indépendant : qty 0.02 (1000/50000), cash après achat 8999, PnL vente 49.45 > 0, PnL métriques 197.8 > 0, win rate 100.0 (voir §5) |
| 9 | Chercher si 38 % dépend du périmètre `--cov` | `NOT_REFUTED` | 42 % sans périmètre, 38 % avec `--cov=paper_trading` ; le chiffre du Producteur correspond au périmètre déclaré et est stable |
| 10 | Vérifier que la licence MIT appartient au commit examiné et que le portage ne rétroagit pas | `NOT_REFUTED` | `LICENSE` présente dans l'arbre `f2e41890` (hash `dd10b10e…`) ; l'ancien commit non licencié `adc1d275…` ne contient pas cette licence — pas de rétroaction |

Les dix réfutations du mandat ont échoué : aucun contenu substantiel du dossier Producteur
n'a été contredit par la ré-exécution indépendante.

## 5. Recalculs indépendants et contre-exemples numériques

Manuel, sans exécuter le code testé, à partir des oracles des tests `test_portfolio.py`
(`PortfolioManager(initial_capital=10000, commission_rate=0.001)`).

| Grandeur | Recalcul indépendant | Attendu | Résultat |
|---|---|---|---|
| Quantité achetée | `1000 / (50000 × (1+0.001))` ≈ `0.02` (arrondi) | `0.02` | cohérent |
| Cash après achat | `10000 − 1000 − frais` = `8999` | `8999` | cohérent |
| PnL vente | `(qty × prix sortie) − (qty × prix entrée) − frais sortie` = `49.45` | `> 0` | cohérent |
| PnL métriques | agrégation sur l'historique = `197.8` | `> 0` | cohérent |
| Win rate | trades gagnants / total = `100.0` | `100.0` | cohérent |

Frais d'entrée (`0.1 %` sur la position d'entrée) et frais de sortie (`0.1 %` sur le produit
de vente) distingués. Aucun contre-exemple trouvé.

## 6. Différences avec les résultats Producteur

| Élément | Producteur | Contradictoire (VM 140) | Écart |
|---|---|---|---|
| Tests Bitget | `9 passed in 2.87s` | `9 passed in 2.26s` | timing seul (nondéterministe) — valeurs identiques |
| Couverture instrumentée Bitget | `9 passed in 8.58s` | `9 passed in 3.48s` | timing seul |
| `pip freeze` avant instrumentation | `18621128…` | `18621128…` | **aucun** (reproduit) |
| `pip freeze` avec instrumentation | `b8d5c210…` | `012fb968…` (pip 25.3) / `5a05adea…` (pip 24.0) | contenu identique (avant + `coverage==7.15.4` + `pytest-cov==7.1.0`) ; hash différent car ordre non canonique de `pip freeze` |
| `coverage.xml` | `84536569…` | `0ae24b5b…` | structure reproduite (465/175/0.3763) ; hash différent car le XML embarque un timestamp |
| Restored 68 tests / 87,07 % / Ruff | sous Nix, code 0 | reproduits sous Nix, code 0 | **aucun** (timing seul) |

Les deux écarts de hash portent sur des artefacts dont le contenu sérialisé n'est pas
canonique (ordre `pip freeze`, horodatage XML) : il ne s'agit pas d'une contradiction de
substance. Aucune assertion substantielle n'a été contredite.

## 7. Objections numérotées, gravité, effet et correction attendue

1. **Gravité FAIBLE — `pip freeze` avec instrumentation non reproductible octet-à-octet.**
   Effet : le hash `b8d5c210…` du Producteur ne peut pas être ré-obtenu à l'identique.
   Correction attendue : documenter le diff (ajout de `coverage==7.15.4` et
   `pytest-cov==7.1.0`), utiliser un ordre normalisé (ex. `pip freeze | sort`) ou une
   liste explicite au lieu d'un hash d'ordonnancement.
2. **Gravité FAIBLE — `coverage.xml` non reproductible octet-à-octet.**
   Effet : le hash `84536569…` du Producteur n'est pas ré-obtenable (horodatage intégré).
   Correction attendue : comparer par structure (lignes couvertes/taux) ou filtrer le
   champ timestamp avant hash.
3. **Gravité MOYENNE — périmètre de couverture implicite.** Effet : 38 % n'est valide que
   pour `--cov=paper_trading` (42 % sans périmètre). Correction attendue : figer la
   commande exacte dans la preuve ; le Producteur l'a fait dans `P0_BASELINE_EVIDENCE.md`.
4. **Gravité MOYENNE — immuabilité distante non prouvée.** Effet : P0 ne peut pas passer
   au seul motif de la concordance `ls-remote`. Correction attendue : preuve de protection
   de branche ou archive Git signée, conformément au protocole et à la condition 5 du
   Producteur. Constat partagé avec le Producteur.

## 8. Conditions exactes de fermeture P0

1. Admission humaine explicite des deux rapports indépendants (Critique et Contradictoire)
   sur le même commit `d1ed53b` et la même preuve.
2. Intégration des limites §7 (hashes non canoniques documentés ; commande de couverture
   figée) dans le dossier Producteur.
3. Preuve d'immuabilité distante : protection GitHub vérifiée ou archive Git signée,
   exportée et hashée, couvrant les commits P0 (`d1ed53b` et `f2e41890`).
4. Ancrage des blobs admis dans un commit distinct et indexation dans le registre.
5. Contrôle final des ancêtres et des SHA-256 par le Producteur.
6. Aucune limite bloquante restante au sens du protocole P0.

## 9. Verdict final unique

`ACCEPT_WITH_LIMITS`

Justification : les dix réfutations du mandat ont échoué ; les deux baselines ont été
ré-exécutées indépendamment sur une VM dédiée avec des résultats substantiellement
identiques (Bitget : 9/9, 38 %/80 %, manifeste et licence reproduits ; restored : 68/68,
87,07 %, Ruff OK). Les limites portent exclusivement sur la reproductibilité byte-à-byte
de deux artefacts non canoniques (§7.1, §7.2) et sur la preuve d'immuabilité distante
(§7.4), que le Producteur déclare déjà ouverte. La suite verte prouve l'exécutabilité
historique et non une validité scientifique, une fidélité au marché ou une performance
financière — aucune de ces propriétés n'est revendiquée par le présent verdict.
