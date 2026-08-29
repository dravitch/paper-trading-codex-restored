# H0001 — Observations non normatives pour le futur Hypothesis Protocol

## Statut

Notes issues de la première exécution. Elles ne modifient pas le protocole général et ne
constituent pas un gate.

## Observations

1. **Deux artefacts préalables suffisent pour commencer.** L'énoncé et l'oracle indépendant
   doivent précéder le code. Le manifeste final, les preuves et les observations gagnent à
   être écrits après l'exécution réelle.
2. **Les inputs et les réponses historiques doivent être physiquement séparés.** Un oracle
   dont le fichier d'entrée contient aussi la projection attendue reste contestable, même
   s'il promet de ne pas lire ce champ.
3. **L'égalité comptable et la reproduction historique sont deux assertions.** H0001
   compare d'abord ledger et oracle exactement, puis seulement sa projection au résultat P0.
4. **Les unités doivent être portées par les invariants.** Le mutant USD-as-SOL est détecté
   parce que le règlement impose explicitement `fee_usd / event_price`.
5. **Une métadonnée revendiquée doit apparaître dans les états testés.** La marge `300 USD`
   a dû être ajoutée aux snapshots; la laisser seulement dans l'événement aurait permis un
   `PASS` incomplet.
6. **Les rationnels récurrents exposent les tolérances prématurées.** Le premier run
   `Decimal` a échoué. Conserver l'oracle exact a conduit à `Fraction`; la tolérance reste
   limitée à la projection binary64 P0.
7. **Les mutants ont plus de valeur avec un code d'invariant stable.** Les six mutations ne
   sont pas seulement rouges : chacune indique la règle comptable violée.
8. **Aucune revue intermédiaire n'était nécessaire.** Le Producteur a pu aller de
   l'hypothèse préenregistrée au dossier probatoire complet; les deux revues commencent sur
   ce paquet figé.
9. **Le scope empêche la contamination de roadmap.** T1–T3 restent une dette P6 sur une
   branche sœur et n'ont pas été importés dans H0001.
10. **Un plan préenregistré doit être consommé ou comparé intégralement.** Vérifier seulement
    les numéros de séquence laissait `kind` et `price` sans autorité effective; M7 a fermé
    cette voie avant revue.
11. **Un commit déclaré par l'appelant n'est pas une provenance.** Le runner doit résoudre
    lui-même le HEAD exécuté; le manifeste peut ensuite lier ce résultat au dossier.
12. **A8 révèle un choix de représentation encore ouvert.** H0001 fonctionne avec des
    PnL/deltas signés alors que l'énoncé parlait de magnitudes positives + direction. Cette
    tension est non bloquante ici mais doit rester visible avant généralisation P1.

Ces observations devront être confrontées à d'autres hypothèses avant toute formalisation
du futur Hypothesis Protocol.
