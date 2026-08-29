# H0003 — Mandat de revue du paquet corrigé

## Paquet

Les nouvelles revues examinent exclusivement le paquet corrigé descendant du manifeste
`5d883f107c1e26bfc44575829d4b34fff5c7aff7`. Le commit d'enveloppe gelé est le commit
portant le présent mandat.

Contexte historique obligatoire :

- paquet rejeté : `44893b0061f13e8a03c4a27f4d299b8b65b5943c`;
- rapports rejetants : `CRITIQUE.md` et `CONTRADICTOIRE.md`, commit `04a5a1f`;
- décision humaine autorisant le correctif : `HUMAN_REJECTION_DECISION.md`, commit
  `426781e`;
- ancien résultat figé : `RESULT_REJECTED_44893B0.json`, SHA-256
  `f13814dee86a98d75c28b6dc697f29d8b1185208501bd46996f47376abe7c87d`;
- nouveau résultat : `RESULT.json`, SHA-256
  `7acb225a68c0d77ba4ed42dd3f435e1bc93ee24d1a32a66b22fc593c01ef5dd2`.

## Mandat commun

Chaque reviewer doit vérifier mécaniquement le paquet complet, puis tenter de réfuter
H0003. Il doit en particulier :

1. reproduire les anciens contre-exemples C4/F1/F2 et confirmer leurs codes de rejet;
2. vérifier que R1–R3 n'ont ajouté aucune convention B1–B8/B5a ni capacité hors scope;
3. vérifier que M1–M11, vecteurs, round-trips, hashes et suite globale restent valides;
4. chercher de nouveaux contre-exemples aux frontières de types, à la grille instrument et
   aux validations relationnelles;
5. maintenir `P1 = NOT_PASSED` et la note `unicodedata` dans son scope publié.

Verdicts autorisés : `ACCEPT`, `ACCEPT_WITH_LIMITS`, `REJECT`, `BLOCKED` ou
`NON_TESTABLE`, motivé par des findings classés.

## Séparation

Le Critique et le Contradictoire sont deux agents/sessions distincts repartant du même
paquet. Les anciens rapports sont visibles aux deux. Le Contradictoire doit figer son
premier verdict sans lire ni recevoir le **nouveau** rapport ou verdict Critique. Les
nouveaux rapports doivent être écrits dans `CRITIQUE_CORRECTION.md` et
`CONTRADICTOIRE_CORRECTION.md`; les anciens rapports ne sont jamais modifiés.

La provenance doit qualifier l'indépendance `PROCEDURAL / ROLE-SEPARATED`, sans revendiquer
IV&V ni indépendance statistique.
