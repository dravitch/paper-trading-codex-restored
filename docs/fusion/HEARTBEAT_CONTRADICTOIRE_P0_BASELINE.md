# HEARTBEAT_CONTRADICTOIRE_P0_BASELINE

Date : 2026-08-08
Role : IA Contradictoire independante (gate P0, baselines restored + Bitget)
Commit examine : d1ed53b1b63d3b6d06ad8edcf64dc4655a3574da (branche correction/reconcile-l1-l12)
Baseline Bitget reexecutee : f2e41890dd5950eb36456503b357bfb76be9ed47
Independance : aucun CRITIQUE_*, docs/deepsearch/*, REVUE_CRITIQUE_* ni
  CONTRADICTOIRE_DELTA_REV12/HEARTBEAT_*_REV12 lus ; aucune commande Git mutante
Environnement : VM dediee VMID 140 paper-trading-p0-review, NixOS 26.05
  (26.05.7006.445d861c6d31), IP 192.168.100.105/24, 0 unite en echec

## Verification mecanique (reexecutable, code de sortie 0)
- Manifeste Bitget (22 fichiers Git suivis, git ls-tree) : 4a14e478...b3b526 REPRODUIT
- LICENSE MIT Bitget : dd10b10e...365c83 REPRODUIT
- Blob docs/fusion/P0_BASELINE_EVIDENCE.md : d615010629ded11b4ac88c05169fee3125131afe6f4cce223a3e9d4f8c018cc3 identique au workspace
- git status --porcelain : 0 dans les deux clones (avant/après execution, apres nettoyage)
- Restored 68 tests : collecte 68 in 6.81s, 68 passed in 3.42s, exit 0
- Restored couverture : TOTAL 545 stmts, 49 missed, 87% ; "Total coverage: 87.07%", exit 0
- Restored Ruff : "All checks passed!", exit 0
- Bitget hors reseau (PrivateNetwork=yes) : 9 tests collected in 2.29s ; 9 passed in 2.26s ; exit 0
- Bitget couverture --cov=paper_trading : TOTAL 465/290 = 38%, portfolio.py 80% ; 9 passed, exit 0
- Sonde reseau : dans l'unite -> Network is unreachable (exit 1) ; sur l'hote -> SONDE_NET_OK (exit 0)
- Echec colorama : ModuleNotFoundError: No module named 'colorama' REPRODUIT (venv minimal)
- Echec libstdc++ : ImportError: libstdc++.so.6 cannot open shared object file REPRODUIT (exit 2)
- LD_LIBRARY_PATH : /nix/store/7vafhlh0lmcvi75jfyy09qwr4m3x1ks3-gcc-15.2.0-lib/lib:/nix/store/483x61iy35irm4wr2b7dwzihljhp6da2-zlib-1.3.2/lib (identique KB)
- Recalculs manuels : qty 0.02, cash 8999, PnL vente 49.45 > 0, PnL metriques 197.8 > 0, win rate 100.0

## Hashes des artefacts
- pip freeze avant instrumentation : 18621128866d16f6bcca7bd72129a104ab1a0b1618d82a26edd8f43050989c8a (REPRODUIT)
- pip freeze avec instrumentation (pip 25.3) : 012fb968502b2c6bec43beae1647284550d05970c0a2073e524f5750ef539297 (annonce b8d5c210... : contenu identique, ordre non canonique)
- coverage.xml VM 140 : 0ae24b5b0f4d37111940c6f91c0c0149ae8ecb6adea5d468fb2011169887a788 (annonce 84536569... : structure 465/175/0.3763 identique, timestamp dans le XML)

## Refutations du mandat (10)
Toutes NOT_REFUTED : hashes, commits/refs distantes, collecte+tests+couverture hors reseau,
sonde reseau, echecs colorama/libstdc++, integrite fichiers Git, inspection 9 tests,
recalculs manuels, dependance du perimetre --cov (42% sans / 38% avec), licence MIT sans retroaction.

## Verdict
ACCEPT_WITH_LIMITS

## Objections ouvertes (limites)
1. FAIBLE : pip freeze avec instrumentation non reproductible octet-a-octet (ordre non canonique)
2. FAIBLE : coverage.xml non reproductible octet-a-octet (timestamp)
3. MOYENNE : 38% valable uniquement pour --cov=paper_trading (42% sans perimetre) - commande figee dans la preuve Producteur
4. MOYENNE : immuabilite distante non prouvee (concordance ls-remote != protection force-push) - partagee avec le Producteur

## Fermeture P0 (conditions)
Admission humaine des deux rapports sur d1ed53b ; integration des limites ; preuve
d'immuabilite distante (protection ou archive signee hashée) ; ancrage et indexation
des blobs admis ; controle final ancetres + SHA-256 ; aucune limite bloquante restante.

## Sorties
- docs/fusion/CONTRADICTOIRE_P0_BASELINE.md
- docs/fusion/HEARTBEAT_CONTRADICTOIRE_P0_BASELINE.md

## Etat des gates
- P0 : PARTIAL inchange (immuabilite distante + admission des deux revues restent ouvertes)
- Aucune re-evaluation financiere ; aucune validation d'hypothese hypothesis/HNNN-*
