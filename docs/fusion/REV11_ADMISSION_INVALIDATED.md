# Invalidation de l'admission REV11

## Motif

La décision opérateur portait sur les blobs vérifiés suivants :

- rapport : `a1966b629b3a0d90f86f2447531d646ab2dd79ce37f90b87700e94ca0fea2816`;
- heartbeat : `d1fab028e88d92833d4c43e39e177c132a21b2c5aaa3225f3ee5bd47c22f3c3a`.

Avant le commit `a837cea`, les fichiers ont été modifiés par un processus concurrent. Les blobs effectivement committés sont :

- rapport : `7e6f3e6dbc7edc5f362d29bc790da2530b40f21447cbff67bf9425210f93b1ef`;
- heartbeat : `8d0e9a76a4d9880e96b4f31f5a5b9e442df61fad5500b231cd37e7ec4b11adba`.

Les hashes ne concordent pas avec la décision. Le commit `a837cea` est donc conservé comme tentative d'admission invalide, n'est pas indexé dans `REVIEW_ADMISSION_REGISTRY.md` et ne peut servir de preuve. Une nouvelle admission explicite des blobs courants est obligatoire.

Cette invalidation ne modifie aucun verdict et ne franchit aucun gate.
