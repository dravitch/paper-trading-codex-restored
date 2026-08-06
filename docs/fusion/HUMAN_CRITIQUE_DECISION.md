# Décision de la Critique humaine — cycle de faisabilité

## Décision

| Champ | Valeur |
|---|---|
| date | 2026-08-06 |
| rôle | Critique humaine et opérateur du projet |
| objet | admission de la revue Critique, de son addendum et conclusions du Producteur |
| décision | `ACCEPT_WITH_LIMITS` |
| effet | autorise le tour Producteur de consolidation et de correction |

La Critique humaine valide les constats suivants :

1. la revue IA Critique est utile mais son indépendance n'est pas garantie;
2. la restriction canadienne générale est documentée officiellement, tandis que le calendrier privé précis reste `UNKNOWN`;
3. le FAIL documentaire Bitget Demo `40099` demeure ouvert;
4. les limites L1–L12 doivent être traitées ou explicitement maintenues;
5. aucun gate ni aucune hypothèse métier n'est validé par cette décision seule.

## Dérogation limitée

Cette décision remplace, pour le seul cycle de cadrage de faisabilité, la seconde validation IA indépendante qui n'a pas pu être obtenue proprement. Elle ne doit pas être décrite comme une validation « par deux IA ».

Le [Protocole Contradictoire](PROTOCOL_CONTRADICTOIRE.md) reste applicable sans modification aux futures branches `hypothesis/HNNN-*`. Toute dérogation future exigera une nouvelle décision explicite et versionnée; celle-ci ne crée pas de dérogation permanente.

## Conditions du tour Producteur

Le Producteur peut maintenant :

- rapprocher la revue Contradictoire et la revue Critique;
- transformer chaque objection en correction, hypothèse ou limite;
- corriger les contradictions documentaires sans changer silencieusement le métier;
- ouvrir une branche dédiée lorsqu'une nouvelle hypothèse possède un énoncé, un oracle et un critère d'échec.

Le Producteur ne peut pas encore déclarer P0 `PASS`, fusionner une hypothèse dans la branche d'intégration, ni présenter la plateforme fusionnée comme validée.
