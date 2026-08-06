# Cadrage de la fusion contrôlée

## Finalité

Ce dossier transforme le corpus historique Codex en propositions réfutables avant toute fusion de code. Il ne certifie ni un moteur universel, ni une fidélité d'exchange, ni une performance financière.

## Ordre de lecture

1. [Corpus et traçabilité](00_CORPUS_TRACEABILITY.md) — ce qui a été trouvé et ses limites probatoires.
2. [Registre de décisions](01_CONCEPT_DECISION_REGISTER.md) — ce qui est retenu, réécrit, rejeté, différé ou inconnu.
3. [Modèle de référence](02_REFERENCE_MODEL.md) — unités, numéraire, valorisation et invariants.
4. [Taxonomie des risques](03_RISK_TAXONOMY.md) — ce qui est mesurable et ce qui reste hors modèle.
5. [Compatibilité des moteurs](04_ENGINE_COMPATIBILITY.md) — écarts entre les modèles existants et cible.
6. [Oracles RiskMap](05_RISKMAP_ORACLES.md) — résultats attendus calculés avant implémentation.
7. [Gates de fusion](06_FUSION_GATES.md) — conditions de passage falsifiables.
8. [RFC des contrats canoniques](CANONICAL_CONTRACT_RFCS.md) — propositions à critiquer avant codage.
9. [Protocole Contradictoire](PROTOCOL_CONTRADICTOIRE.md) — branches, preuves et double revue IA.
10. [Registre des branches d'hypothèse](HYPOTHESIS_BRANCH_REGISTER.md) — état canonique des validations.
11. [Décision de la Critique humaine](HUMAN_CRITIQUE_DECISION.md) — dérogation limitée permettant le tour Producteur.
12. [Consolidation L1–L12](LIMIT_RESOLUTION_REGISTER.md) — décisions Producteur et preuves restant ouvertes.
13. [Provenance des composants](COMPONENT_PROVENANCE.md) — licence, décisions de portage et blocages.
14. [Registre NO-GO](NO_GO_REGISTER.md) — causes, cycles et décisions d'arrêt ou réduction.
15. [Registre des identifiants causaux](CAUSAL_ID_REGISTRY.md) — composants, symboles, modes d'échec et groupes racines.
16. [Contrat Clock](CLOCK_CONTRACT.md) — temps canonique, horloges replay/test/live et invariants.
17. [Registre d'admission](REVIEW_ADMISSION_REGISTRY.md) — commits et hashes immuables des revues acceptées.

## Hiérarchie des preuves

| Niveau | Ce qu'il permet d'affirmer | État actuel |
|---|---|---|
| observation du corpus | une idée ou contradiction existe dans les archives | documenté |
| dérivation indépendante | un attendu simple est calculable sans le moteur | documenté pour les oracles listés |
| RFC documentaire | une interface proposée est critiquable | documenté, non accepté |
| schéma et test exécutable | une contrainte est mécaniquement vérifiée | absent |
| replay reproductible | mêmes entrées et manifeste donnent le même bundle | non démontré |
| validation empirique | un profil de fidélité est confronté à des observations | non démontré |

## Statut au 2026-08-06

- phase active : préparation de `P0 Baselines`;
- branche d'intégration : `fusion/controlled-merger`;
- documentation normative initiale : produite;
- décisions irréversibles : aucune;
- code de fusion : non commencé;
- verdict de publication de la plateforme fusionnée : **pas prête**.

Les évolutions de ce cadrage sont consignées dans [REV04](../../REV04.md). Le rapport directeur reste [CONTROLLED_MERGER_FEASIBILITY](../../CONTROLLED_MERGER_FEASIBILITY.md).
