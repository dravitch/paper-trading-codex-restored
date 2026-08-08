# Registre de provenance des composants

## Règle

`PORT` autorise une copie adaptée seulement si la licence et les obligations sont établies. `CLEAN_REIMPLEMENT` autorise une réimplémentation depuis une spécification publique sans copier l'expression du code source. `BLOCKED_LICENSE` interdit tout portage tant que le titulaire ou une licence vérifiable ne l'autorise pas.

## Sources initiales

| Source | Révision observée | Licence observée | Composants envisagés | Décision actuelle |
|---|---|---|---|---|
| `paper-trading-codex-restored` | base `bd1a9d5` | MIT (`LICENSE`) | tests, métriques, packaging, contrats locaux | `PORT`, sous historique Git |
| `dravitch/bitget-paper-trading` | `adc1d27508c1789d185d28109df2b854449b418a` | aucun `LICENSE*`, `COPYING*` ou `NOTICE*` trouvé à profondeur 2 le 2026-08-06 | CLI, mock, spot portfolio, RSI/MA, checkpoint | `BLOCKED_LICENSE` pour copie; `CLEAN_REIMPLEMENT` depuis RFC seulement |
| `dravitch/bitget-paper-trading` | `f2e41890dd5950eb36456503b357bfb76be9ed47` | MIT (`LICENSE`, SHA-256 `dd10b10e...`) ajoutée et observée sur la branche distante le 2026-08-07 | mêmes composants, sous examen fichier par fichier | `PORT_PENDING_REVIEW`; ne rétroagit pas sur l'ancien commit non licencié |
| archives Codex | révisions multiples/unknown | hétérogène ou unknown | intentions, contre-exemples, vocabulaire | idées seulement; aucune copie sans examen par fichier |

## Champs requis avant P3

Pour chaque composant : source URL, commit, chemin, blob SHA-256, auteur/copyright disponible, licence SPDX ou `UNKNOWN`, obligations, fichier cible, transformation, tests de caractérisation, décision et approbateur.

## Conséquence immédiate

Aucun code de `bitget-paper-trading` ne doit encore être copié sur la branche de fusion. La licence MIT est établie pour la révision `f2e41890...`, mais chaque portage exige toujours les champs P3, une revue indépendante et l'admission humaine. Les comportements utiles continuent d'être reformulés comme contrats et oracles jusqu'à cette admission.
