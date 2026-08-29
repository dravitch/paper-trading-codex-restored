# H0003 — Revue Contradictoire indépendante

## Verdict figé

`REJECT`

Les vecteurs préenregistrés, leurs hashes, les round-trips et M1–M11 sont effectivement
verts. Deux contre-exemples publics restent néanmoins acceptés : des valeurs binary64/bool
entrent silencieusement dans les champs rationnels, et un prix de `MarketEvent` hors grille
B1 ne dispose d'aucune validation contre l'instrument. Ces écarts touchent l'énoncé exact
du socle canonique, pas une généralisation future.

Ce verdict ne déclare ni H0003 admise/validée, ni `P1 PASS`.

## Identité, révision et indépendance

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire |
| identité/version du moteur | `UNKNOWN` |
| date | `2026-08-29` (`America/Toronto`) |
| branche | `hypothesis/H0003-canonical-contract-foundation` |
| paquet gelé | `44893b0061f13e8a03c4a27f4d299b8b65b5943c` |
| mandat | réfutation contradictoire de H0003 uniquement |
| indépendance | `PROCEDURAL / ROLE-SEPARATED` |

Le premier verdict a été figé sans ouvrir, lire ou modifier
`docs/fusion/hypotheses/H0003/CRITIQUE.md` et sans recevoir son verdict. Cette séparation
ne revendique ni IV&V organisationnelle, ni indépendance statistique, ni indépendance des
modèles ou auteurs.

## Fichiers examinés

- `HYPOTHESIS.md`, `ORACLE_VECTORS.json`, `RESULT.json`, `EVIDENCE.md`, `MANIFEST.json`,
  `H0003_PROTOCOL_OBSERVATIONS.md` et le placeholder antérieur de `CONTRADICTOIRE.md`;
- `docs/fusion/P1_CANONICAL_CONTRACT_DECISIONS.md`,
  `P1_MINIMAL_EXECUTABLE_PROFILE.md`, `CLOCK_CONTRACT.md` et la section allowlist de
  `06_FUSION_GATES.md`;
- `paper_trading_codex/domain/contracts.py` et `domain/__init__.py`;
- `tests/hypotheses/H0003/test_canonical_contract_foundation.py` et
  `run_experiment.py`;
- objets et différences Git de la chaîne de provenance.

`CRITIQUE.md` n'a pas été lu et a été explicitement exclu des commandes de recherche et
de diff.

## Provenance vérifiée

La chaîne demandée est linéaire et chaque arc est ancestral :

```text
ed2731d → 0fe5610 → 0e105c2 → d817a16 → be6678a
         → 5676de8 → 9a8f318 → 5bd95dd → 44893b0
```

- `ed2731d` conserve le blocage pré-code;
- `0fe5610` ferme humainement B1–B8;
- `0e105c2` fige les vecteurs avant code;
- `d817a16` ferme B5a avant code;
- `be6678a` aligne le préenregistrement encore sans implémentation;
- `5676de8` introduit seulement ensuite contrats, exports, tests et runner;
- `9a8f318` corrige la garde Unicode déjà normative;
- `5bd95dd` enregistre les preuves;
- `44893b0` gèle le paquet examiné.

Les SHA-256 recalculés de la décision, hypothèse, vecteurs, contrats, exports, tests,
runner, résultat, preuves, observations, statut et environnement concordent tous avec
`MANIFEST.json`. Le SHA-256 réel de `RESULT.json` est
`f13814dee86a98d75c28b6dc697f29d8b1185208501bd46996f47376abe7c87d`.

## Commandes et résultats

| Contrôle | Résultat | Code |
|---|---|---:|
| `git rev-parse HEAD` | `44893b0061f13e8a03c4a27f4d299b8b65b5943c` | 0 |
| `git merge-base --is-ancestor` sur chaque arc | filiation complète | 0 |
| `sha256sum` des artefacts manifestés | concordance complète | 0 |
| `nix develop --command pytest tests/hypotheses/H0003 -q` | `29 passed in 0.07s` | 0 |
| `nix develop --command just check` | Ruff OK; `125 passed`; couverture `90.92 %`; `contracts.py` 95 % | 0 |
| contre-exemple types numériques via constructeur public | bool/float acceptés et convertis en `Fraction` | 0 |
| contre-exemple prix marché hors grille | `MarketEvent(price=20001/200)` construit sans rejet | 0 |

Le contre-exemple numérique a notamment produit :

```text
InstrumentSpec.contract_multiplier=True  → Fraction(1, 1)
Fill.quantity=0.1                         → 3602879701896397/36028797018963968
Fill.price=100.005                        → 879653282685911/8796093022208
Fill.fee_amount=False                     → Fraction(0, 1)
```

Aucun de ces appels n'a levé `ContractValidationError`.

## Examen de M1–M11

| Famille | Résultat contradictoire |
|---|---|
| M1–M3 | rejets ciblés observés pour non-positivité et devises testées |
| M4 | textes non canoniques rejetés; `Fraction(2,4)` sérialisée `1/2` |
| M5 | incompatibilités identité et hash rejetées |
| M6 | champ `sequence` absent rejeté |
| M7 | doublon idempotent dédupliqué, divergent rejeté |
| M8–M9 | frais et signes testés rejetés avec codes stables |
| M10 | ordre des clés sans effet sur bytes/hash |
| M11 | cinq round-trips bit-identiques |

Les mutations prescrites sont correctement réalisées, mais elles ne suffisent pas à
établir le critère 6 (types/unités incompatibles rejetés) ni le critère 8 (aucune convention
supplémentaire silencieuse), réfutés ci-dessous.

## Findings bloquants

### F1 — Coercition silencieuse de binary64 et bool vers le rationnel canonique

```text
status = FAIL
impact = BLOCKING_H0003
scope = CANONICAL_NUMERIC_CONSTRUCTION
```

Les `__post_init__` appellent `Fraction(value)` sans exiger que l'entrée soit déjà un
`Fraction` ou un entier non-bool. Python traite `bool` comme entier et convertit un float
en son rationnel binary64 exact. Un objet public peut donc accepter `True`, `False`, `0.1`
ou `100.005`, puis publier des bytes rationnels qui donnent à cette coercition l'apparence
d'une donnée canonique.

Cette acceptation est une convention non préenregistrée. Le profil dit que le noyau utilise
des rationnels exacts réduits et qu'une conversion binary64 peut exister **hors** du noyau;
il exige également les rejets de types incompatibles. L'écart concerne directement
`InstrumentSpec`, `MarketEvent`, `Fill` et `AccountEvent`. Les vecteurs M4 ne testent que
la syntaxe textuelle et ne le détectent pas.

**Effet exact :** la revendication « contrats canoniques avec validation de construction,
sans convention numérique supplémentaire » est fausse pour le paquet gelé.

### F2 — `REJECT_OFF_GRID` n'est pas applicable à `MarketEvent.price`

```text
status = FAIL
impact = BLOCKING_H0003
scope = B1 / MARKET_EVENT_COMPATIBILITY
```

B1 ferme la règle : toute quantité hors `lot_size` ou tout prix hors `tick_size` est
rejeté. Le code fournit `validate_fill_compatibility`, qui applique la grille au prix du
fill, mais ne fournit aucun validateur équivalent pour `MarketEvent`. Un
`MarketEvent(price=20001/200)` est accepté pour l'instrument oracle dont le tick vaut
`1/100`, alors que `100.005 / 0.01` n'est pas entier.

Ce n'est pas seulement une validation différée : aucune API du paquet ne permet d'agréger
ce `MarketEvent` avec `InstrumentSpec` pour appliquer B1. M2 vérifie seulement que le tick
et le lot eux-mêmes sont positifs; le contrôle additionnel hors grille ne couvre que
`Fill`.

**Effet exact :** un contrat événementiel incompatible avec l'instrument est accepté, en
contradiction avec la décision B1 réutilisée et les critères de réfutation H0003.

## Autres tentatives de réfutation

- Les bytes UTF-8, NFC, échappements, clés triées, absence de BOM/newline et hashes des
  vecteurs ont été recalculés sans divergence.
- Les surrogates Unicode et collisions de clés après NFC sont rejetés avec codes stables.
- Les rationnels textuels non réduits, zéros alternatifs, dénominateurs négatifs/nuls,
  décimaux et exposants sont rejetés.
- Les identités typées, l'ordre local et l'interdiction d'ordre inter-types correspondent
  à B6/B7; aucune mémoire globale cachée n'a été trouvée.
- Les compatibilités instrument/référence/frais et compte/devise couvertes par B5/B5a/B4
  fonctionnent sur les chemins testés.
- `Clock` est un port pur sans source temporelle; `InstantNs` et `DurationNs` suivent la
  représentation `NewType` explicitement prescrite par `CLOCK_CONTRACT.md`. L'enforcement
  AST reste hors portée H0003.

## Note `unicodedata`

```text
status = OPEN_TOOLING_NOTE
impact_on_H0003 = NON_BLOCKING
scope = P1_CLOCK_ENFORCEMENT / ALLOWLIST_V1
impact_before_P1_PASS = BLOCKING_UNTIL_ALLOWLIST_DECISION
```

`unicodedata` est nécessaire à la règle NFC de H0003 mais absent de l'allowlist P1 v1.
H0003 exclut explicitement l'enforcement AST et démontre correctement les bytes NFC; cette
dépendance ne cause donc ni F1 ni F2 et ne réfute pas isolément H0003. En revanche, la
règle d'allowlist interdit tout ajout sans décision préenregistrée, audit transitif et
mutant. La note doit rester ouverte et bloquer toute future revendication `P1 PASS` tant
que cette décision n'existe pas.

## Portée finale

Le paquet est testable et sa provenance est cohérente; `NON_TESTABLE` ne convient pas.
Les deux écarts ne sont pas des limites hors profil : ils acceptent des valeurs
incompatibles au cœur des contrats que H0003 affirme fermer. Le verdict contradictoire est
donc `REJECT` malgré la réussite de M1–M11 et des vecteurs positifs.

Ce rapport n'ordonne aucune correction en cours de revue, ne modifie aucun artefact
Producteur, ne statue pas sur une hypothèse suivante et ne produit ni admission humaine ni
`P1 PASS`.
