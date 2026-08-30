# H0004 — Observations protocolaires non normatives

1. Le langage canonique H0003 a suffi à construire les transitions spot sans dupliquer
   ses validateurs de contrats.
2. Le premier run antérieur aux mutants distingue une formule comptable directement
   compatible du code ensuite guidé vers les attendus.
3. Une sémantique de consommation monotone appartient au contrat observable du ledger,
   même lorsque le choix d'ordonnancement reste déféré au caller/P2.
4. La conservation gagne à être un validateur exécutable indépendant de la construction
   des événements : cela rend omission et double comptage directement falsifiables.
5. Un cumul informatif de frais doit rester séparé des écritures de balance pour éviter une
   double comptabilisation silencieuse.
6. Une conservation interne exacte ne prouve pas que l'état est muté sous le contexte
   contractuel qu'il annonce : les hashes sérialisés doivent être vérifiés à chaque frontière.
7. Une valeur neutralisée dans l'oracle (`contract_multiplier = 1`) peut masquer une
   convention ajoutée par le code; la faire varier reste une attaque nécessaire même lorsque
   tous les mutants préenregistrés passent.
8. Le premier paquet rejeté et son résultat doivent rester adressables séparément du candidat
   corrigé; la correction ne change ni le verdict historique ni l'antériorité du premier run.

Ces observations ne formalisent aucun protocole général et n'attribuent aucune hypothèse
suivante.
