# H0004 — Mandat de revue du paquet corrigé

## Paquet

Les nouvelles revues examinent le paquet corrigé dont le manifeste est ancré au commit
`d60e96a`. Le commit portant ce mandat constitue l'enveloppe gelée.

Contexte historique obligatoire :

- paquet rejeté : `5967ee0`;
- rapports rejetants : `CRITIQUE.md` et `CONTRADICTOIRE.md`, commit `6f12875`;
- décision humaine rejetant le paquet et admettant F1/F2 : `830c0c0`;
- décision humaine sur le multiplicateur spot : `f2d45c9`;
- ancien résultat préservé : `RESULT_REJECTED_5967EE0.json`, SHA-256
  `cb6582a112e577b0508c39f15c2c2dc5107af7a11bd9124d6a76db3051402594`;
- nouveau résultat : `RESULT.json`, SHA-256
  `65adcc700a8021010c6e8a70121b54216c44f1dd11b2b7c63d5786330e780c72`.

## Mandat commun

Chaque reviewer doit vérifier mécaniquement le paquet complet puis tenter de réfuter
H0004. Il doit en particulier :

1. reproduire les contre-exemples originaux F1a/F1b/F2 et confirmer leurs codes;
2. vérifier que les rejets précèdent toute mutation et laissent l'état inchangé;
3. vérifier que `apply_initialization` contrôle toute liaison disponible sans changement
   d'API silencieux;
4. confirmer que la décision `contract_multiplier = 1/1 ONLY` est appliquée et que la
   formule préenregistrée reste `quantity × price`;
5. vérifier que scénario, oracle, six `AccountEvent`, S8 et M1–M19 n'ont pas régressé;
6. tenter de nouveaux context substitutions, variations neutralisées et attaques aux
   frontières relationnelles;
7. publier la limite de force de M18c si elle subsiste, sans la confondre avec S8 individuel;
8. maintenir `P1 = NOT_PASSED` et ne jamais réhabiliter rétroactivement `5967ee0`.

Verdicts autorisés : `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT`, `BLOCKED` ou
`NON_TESTABLE`, avec findings classés.

## Séparation

Le Critique et le Contradictoire sont deux agents/sessions distincts repartant du même
paquet. Les anciens rapports sont visibles aux deux. Le Contradictoire doit figer son
premier verdict sans lire ni recevoir le **nouveau** rapport ou verdict Critique.

Les nouvelles revues sont écrites dans `CRITIQUE_CORRECTION.md` et
`CONTRADICTOIRE_CORRECTION.md`. Les anciens rapports ne sont jamais modifiés.

La provenance qualifie l'indépendance `PROCEDURAL / ROLE-SEPARATED`, sans revendiquer
IV&V ni indépendance statistique.
