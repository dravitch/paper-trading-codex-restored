# H0003 — Observations protocolaires non normatives

1. Le premier blocage a empêché huit décisions invisibles d'entrer dans le code.
2. Une décision humaine distincte puis des vecteurs byte-exacts ont suffi à reprendre la
   même hypothèse sans effacer son état bloqué.
3. Une règle de compatibilité apparemment mineure (`fee_currency`) doit précéder le code
   dès qu'elle change un mutant ou un rejet.
4. Les vecteurs UTF-8/hash testent utilement le contrat au-delà des valeurs financières.
5. Les écarts d'allowlist doivent être classés par scope : la dépendance NFC ne réfute pas
   H0003, mais devra être décidée avant l'enforcement temporel P1.
6. M1–M11 tous verts n'épuisaient pas l'espace des réfutations : les revues ont trouvé
   des valeurs Python adverses et une validation relationnelle absente qui violaient
   directement l'énoncé. Les contre-exemples publiés deviennent des régressions
   permanentes, sans substitution par des variantes Producteur plus faciles.
7. Un paquet peut être `REJECTED` tout en autorisant un cycle correctif de la même
   hypothèse existentielle, si l'ancien résultat reste figé et si le correctif produit un
   nouveau paquet complet soumis à de nouvelles revues.

Ces observations ne modifient aucun protocole et n'attribuent aucune hypothèse suivante.
