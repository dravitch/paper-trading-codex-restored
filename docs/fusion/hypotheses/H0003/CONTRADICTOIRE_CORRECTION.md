# H0003 — Revue Contradictoire du paquet corrigé

## Verdict figé

`ACCEPT_WITH_LIMITS`

Les contre-exemples admis C4/F1/F2 sont fermés avec leurs entrées et codes exacts. Les
corrections R1–R3 restent dans la décision humaine du cycle correctif et ne modifient ni
B1–B8/B5a, ni les vecteurs antérieurs, ni le périmètre fonctionnel H0003. Aucune nouvelle
réfutation bloquante n'a été trouvée.

Ce verdict porte sur le paquet corrigé `d3134e6` seulement. Il ne réhabilite pas le paquet
`44893b0`, ne constitue pas une admission humaine et ne déclare pas `P1 PASS`.

## Identité, mandat et indépendance

| Champ | Valeur |
|---|---|
| rôle | IA Contradictoire — cycle correctif |
| identité/version du moteur | `UNKNOWN` |
| date | `2026-08-29` (`America/Toronto`) |
| branche | `hypothesis/H0003-canonical-contract-foundation` |
| paquet corrigé gelé | `d3134e63362693b4ca47d61229d1307edf7daca5` |
| manifeste corrigé | `5d883f107c1e26bfc44575829d4b34fff5c7aff7` |
| code Producteur exécuté | `729a138a6db010ac320ff9d056e9591f336f8575` |
| indépendance | `PROCEDURAL / ROLE-SEPARATED` |

Le mandat `CORRECTION_REVIEW_REQUEST.md` a été lu intégralement. Les anciens rapports
`CRITIQUE.md` et `CONTRADICTOIRE.md` ainsi que `HUMAN_REJECTION_DECISION.md` ont été lus
comme contexte historique obligatoire. Le nouveau `CRITIQUE_CORRECTION.md` et son verdict
n'ont été ni ouverts, ni lus, ni demandés, ni reçus avant fixation du présent verdict.
Cette séparation ne revendique ni IV&V organisationnelle, ni indépendance statistique, ni
indépendance des modèles/auteurs.

## Paquet et provenance examinés

Fichiers lus :

- `CORRECTION_REVIEW_REQUEST.md`, anciens rapports et décision humaine de rejet;
- `HYPOTHESIS.md`, `ORACLE_VECTORS.json`, `EVIDENCE.md`, `MANIFEST.json`, `RESULT.json`,
  `RESULT_REJECTED_44893B0.json` et `H0003_PROTOCOL_OBSERVATIONS.md`;
- `P1_CANONICAL_CONTRACT_DECISIONS.md`, `P1_MINIMAL_EXECUTABLE_PROFILE.md`,
  `CLOCK_CONTRACT.md` et l'allowlist de `06_FUSION_GATES.md`;
- `paper_trading_codex/domain/contracts.py`, ses exports, les tests H0003 et le runner;
- `STATUS.md`, `flake.lock`, `pyproject.toml` et les objets Git nécessaires.

La filiation corrective est valide :

```text
44893b0 paquet rejeté
→ 04a5a1f anciens rapports
→ 426781e décision humaine de rejet et autorisation R1–R3
→ 34dc2b7 correction des contrats
→ 729a138 régressions et runner corrigé
→ f2455f9 preuves Producteur
→ 5d883f1 manifeste corrigé
→ d3134e6 enveloppe de revue
```

Les fichiers normatifs `HYPOTHESIS.md`, `ORACLE_VECTORS.json` et
`P1_CANONICAL_CONTRACT_DECISIONS.md` conservent leurs hashes antérieurs. Le correctif
n'est donc pas obtenu par réécriture postérieure de l'hypothèse ou des réponses.

## Contrôles exécutés

| Contrôle | Résultat | Code |
|---|---|---:|
| `git rev-parse HEAD` | paquet exact `d3134e63362693b4ca47d61229d1307edf7daca5` | 0 |
| `git merge-base --is-ancestor` sur chaque arc correctif | filiation complète | 0 |
| `sha256sum` des artefacts manifestés | concordance complète | 0 |
| blobs `contracts.py`/runner au commit `729a138` | hashes manifestés exacts | 0 |
| ancien résultat depuis le blob `44893b0` | `f13814de...7c87d`, inchangé | 0 |
| nouveau résultat depuis le commit de preuves | `7acb225a...f5dd2`, exact | 0 |
| `nix develop --command pytest tests/hypotheses/H0003 -q` | `39 passed in 0.09s` | 0 |
| `nix develop --command just check` | Ruff OK; `135 passed`; couverture `90.97 %`; contrats 95 % | 0 |
| `nix develop --command python scripts/update_status.py --check` | `STATUS.md is current` | 0 |

Les cinq bytes/hashes préenregistrés et leurs cinq round-trips restent identiques. Les
M1–M11 continuent à produire les rejets ou invariances annoncés.

## Reproduction de C4/F1/F2

### C4 / R1 — scalaires temporels

Les entrées historiques exactes sont rejetées :

```text
InstantNs("not-an-int") → INSTANT_NS_TYPE_INVALID
DurationNs(True)        → DURATION_NS_TYPE_INVALID
```

Les variantes adverses `float` et `datetime` ont également été rejetées. Les deux types
sont des sous-classes immuables de `int`; leur constructeur exige désormais
`type(value) is int`. Les événements acceptent un `int` exact ou un `InstantNs` déjà
validé et refusent `bool`/float/objet implicite.

```text
status = CLOSED
impact = SUPPORTING
scope = R1 / H0003_TEMPORAL_SCALARS
```

### F1 / R2 — frontière rationnelle

Les quatre entrées historiques exactes sont rejetées avec
`RATIONAL_VALUE_TYPE_INVALID` :

```text
contract_multiplier=True
quantity=0.1
price=100.005
fee_amount=False
```

Une attaque supplémentaire avec `Decimal("0.5")` est également rejetée. La frontière
publique accepte uniquement les types exacts `int` et `Fraction`; `bool`, binary64,
`Decimal` et sous-types numériques ne sont plus convertis silencieusement. Les chemins de
désérialisation continuent à exiger les chaînes rationnelles B8 canoniques.

```text
status = CLOSED
impact = SUPPORTING
scope = R2 / CANONICAL_NUMERIC_BOUNDARY
```

### F2 / R3 — compatibilité `MarketEvent`

Le prix historique `20001/200` contre un tick `1/100` est rejeté par `PRICE_OFF_GRID`.
Une identité d'instrument différente est rejetée par
`MARKET_EVENT_INSTRUMENT_INCOMPATIBLE`. Le chemin nominal préenregistré est accepté.

```text
status = CLOSED
impact = SUPPORTING
scope = R3 / MARKET_EVENT_INSTRUMENT_COMPATIBILITY
```

## Absence d'expansion ou de convention nouvelle

R1 exécute la règle antérieure « entiers signés » et la décision humaine exigeant
`type(value) == int`. R2 matérialise la frontière rationnelle exacte déjà normative. R3
applique directement B1 et la décision humaine à l'identité et au tick du `MarketEvent`.

Le diff correctif de production se limite à ces types/validations et à leur export. Aucun
ledger, modèle de compte, replay, scheduler, stratégie, provider, réseau, filesystem,
source temporelle ou enforcement AST n'a été ajouté. Les régressions conservent exactement
les contre-exemples publiés plutôt que de leur substituer des variantes plus faibles.

## Recherche de nouvelles réfutations

Les attaques suivantes n'ont pas produit de divergence :

- `bool`, float, `Decimal`, texte et datetime aux frontières temporelles/rationnelles;
- entier signé négatif et grand entier pour les scalaires temporels;
- rationnels textuels non réduits, zéro alternatif, dénominateur négatif/nul, décimal et
  exposant;
- JSON non canonique, clés dupliquées avant/après NFC, surrogate Unicode, BOM/newline et
  ordre de construction;
- instrument différent, prix et quantité hors grille, devise de frais/référence/compte
  incompatible;
- séquence absente ou booléenne, ordre local, ordre inter-types et doublon divergent;
- round-trip et hashes après passage par les nouveaux types temporels.

Aucune convention B1–B8/B5a manquante n'a été nécessaire pour exécuter ces contrôles.

## Limites publiées

| ID | Statut | Impact | Scope | Effet exact |
|---|---|---|---|---|
| L1 | `OPEN_TOOLING_NOTE` | non bloquant H0003; bloquant avant P1 PASS | `P1_CLOCK_ENFORCEMENT / ALLOWLIST_V1` | `unicodedata` reste nécessaire à NFC mais absent de l'allowlist. H0003 exclut l'enforcement AST; aucune extension silencieuse n'est admise. |
| L2 | `PUBLISHED_LIMIT` | non bloquant | validations relationnelles | Comme pour Fill et AccountEvent, la compatibilité de MarketEvent est une fonction explicite : un consommateur doit l'appeler à la frontière d'agrégation. H0003 démontre le validateur, pas un registre global ni un pipeline de replay. |
| L3 | `PUBLISHED_SCOPE_LIMIT` | non bloquant | P1 | H0003 ne prouve ni ledgers spot/short conformes, ni enforcement temporel, replay, provider ou fidélité exchange. |

L1 reprend exactement la classification publiée :

```text
status = OPEN_TOOLING_NOTE
impact_on_H0003 = NON_BLOCKING
scope = P1_CLOCK_ENFORCEMENT
impact_before_P1_PASS = BLOCKING_UNTIL_ALLOWLIST_DECISION
```

## Verdict et effet

Le paquet corrigé est testable, ses preuves sont cohérentes et les trois motifs admis du
rejet précédent sont fermés sans contamination de scope. Les limites restantes sont
explicites et ne réfutent pas l'énoncé H0003 dans son périmètre.

Le verdict contradictoire corrigé est donc `ACCEPT_WITH_LIMITS`. Il doit être soumis avec
la nouvelle revue Critique à une décision humaine distincte. Il ne modifie pas le statut
rejeté de `44893b0`, ne constitue aucune admission et maintient `P1 = NOT_PASSED`.
