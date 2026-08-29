# P1 — Profil minimal exécutable fermé

## Statut et objet

Ce document borne le plus petit profil permettant, après implémentation et preuves, de
revendiquer `P1 PASS`. Il applique le gate P1 et les contrats normatifs existants à la
capability map admise après H0001/H0002.

Il ne crée aucune hypothèse, ne constitue aucune preuve exécutable et ne change pas le
statut courant :

```text
P1 = NOT_PASSED
next_hypothesis = NOT_ASSIGNED
```

## Frontière de responsabilité

P1 définit des valeurs, événements et transitions comptables canoniques. Il reçoit des
fills explicites; il ne décide pas comment les produire ni dans quel ordre un replay les
planifie.

| Responsabilité | Gate |
|---|---|
| types instrument/référentiel/temps | P1 |
| événements de marché, fills et écritures de compte comme données canoniques | P1 |
| transitions des comptes spot et short | P1 |
| stratégie → `OrderIntent` | P3 |
| génération/simulation des ordres et fills | hors profil P1; à borner avec P2/P3 selon l'usage |
| ordre global et scheduler de replay | P2 |
| adaptation fournisseur et fidélité exchange | P4 |
| RiskMap et chaîne probatoire associée | P6 |

Un `Fill` P1 est donc un fait d'entrée préenregistré, jamais une affirmation de fidélité à
un exchange.

## 1. Types exécutables minimaux

Chaque type ci-dessous est relié à une exigence P1 existante. Aucun autre type public n'est
requis par ce profil.

| Type | Exigence source | Champs minimaux et rôle | Rejets minimaux |
|---|---|---|---|
| `InstrumentSpec` | gate « instruments », RFC-001 | `instrument_id`, `instrument_type`, `base`, `quote`, `settlement`, `contract_multiplier`, `tick_size`, `lot_size`, `rounding_policy` | identifiant/devise/unité absents; multiplicateur, tick ou lot non positifs; type/politique inconnus |
| `ReferenceSpec` | RFC-006, modèle de référence | `numeraire`, `valuation_price`, `fee_settlement_currency`, `numeric_policy`, `rounding_policy`; hash canonique | numéraire/prix/politique absents; référentiels incompatibles agrégés |
| `MarketEvent` | gate « événements », RFC-002 | `event_id`, `source_id`, `instrument_id`, `event_type`, `event_time: InstantNs`, `sequence`, `price`, `raw_hash`, `fidelity_level` | temps/ID/instrument absents; doublon divergent; prix non positif; niveau non justifié |
| `Fill` | RFC-004, entrée des ledgers | `fill_id`, `order_id`, `instrument_id`, `side`, `quantity`, `price`, `fee_amount`, `fee_currency`, `liquidity_role`, `event_time`, `sequence` | quantité/prix non positifs; frais négatifs ou sans devise; instrument inconnu; side ambigu |
| `AccountEvent` | RFC-005, invariant d'explication | `account_event_id`, `account_model`, `instrument_id`, `kind`, `event_time`, `sequence`, montants signés et devises | kind/modèle/devise inconnus; doublon divergent; mouvement inexpliqué |
| `SpotAccountModel` | gate « ledger spot », RFC-005/CD-007 | état quote/base, application de fills spot, écritures et valorisation | solde insuffisant; vente supérieure au base; modèle mélangé |
| `IsolatedLinearShortAccountModel` | gate « ledger short », RFC-005/CD-007 | collatéral, position short isolée, marge déclarée, frais, PnL réalisé/latent, application full-close | levier/marge incohérents; mauvais signe/unité; modèle mélangé |
| `InstantNs`, `DurationNs`, `Clock` | contrôle temporel P1, `CLOCK_CONTRACT.md` | types entiers et port `now_ns()` sans source système | flottant/datetime implicite; Clock par défaut; source directe |

Les états, positions, balances et écritures peuvent être des valeurs internes immuables de
ces modèles. Ils ne créent pas de nouvelles capacités de gate et n'exigent pas un RFC
séparé.

### Types explicitement non requis par P1

- `OrderIntent` et stratégie : P3;
- scheduler/journal de replay : P2;
- provider/adaptateur live : P4/P5;
- `RiskPoint`/`RiskMap` : P6;
- `ExecutionSpec` comme moteur générateur de fills : non requis pour appliquer des fills
  P1 explicites;
- ordre, carnet, latence, slippage ou impact réalistes : hors profil P1.

## 2. Décisions P1 fermées

Les seules sorties employées sont `REQUIRED_IN_P1`, `DEFERRED_TO_P2+` et
`UNSUPPORTED_IN_P1_PROFILE`.

| Sujet | Décision | Règle fermée |
|---|---|---|
| politique numérique | `REQUIRED_IN_P1` | écritures et oracles utilisent des rationnels exacts réduits; sérialisation canonique `numerator/denominator`; aucune tolérance interne; arrondi seulement à une frontière nommée par `InstrumentSpec`/`ReferenceSpec` |
| identité d'instrument | `REQUIRED_IN_P1` | `instrument_id` est une chaîne sémantique non vide; la compatibilité exige aussi le SHA-256 canonique de l'`InstrumentSpec`; aucun UUID implicite |
| ordre canonique | `REQUIRED_IN_P1` | clé locale P1 `(event_time, sequence, source_id, event_id)`; une source sans séquence est rejetée dans ce profil, jamais réparée silencieusement |
| censure de fin de replay | `DEFERRED_TO_P2+` | aucune censure n'est créée ou interprétée par P1; un input qui en dépend est rejeté par le profil P1 |
| devise / numéraire | `REQUIRED_IN_P1` | chaque montant porte une devise; un `ReferenceSpec.numeraire` est obligatoire; un compte est mono-instrument avec base/quote/settlement déclarés; aucune conversion implicite |
| multi-devise de compte | `UNSUPPORTED_IN_P1_PROFILE` | balance ou écriture dans une devise hors spec rejetée avec code stable |
| A8, représentation des signes | `REQUIRED_IN_P1` | quantité, prix, notionnel, marge et frais sont non négatifs; les mouvements de balance, PnL et deltas de collatéral sont signés; `kind`/`side` donne le sens économique; aucune double négation |
| absence de séquence source | `UNSUPPORTED_IN_P1_PROFILE` | rejet mécanique; synthèse/ordre intersource relève de P2 ou d'un adaptateur futur |

Cette politique rationnelle formalise le mécanisme déjà admis par H0001/H0002. Une
conversion binary64 peut exister hors du noyau, mais ne décide jamais une égalité P1.

## 3. Profil comptable spot minimal

### Discriminant et état

```text
account_model = SPOT_CASH_V1
state = {
  instrument_spec_hash,
  reference_spec_hash,
  quote_balance,
  base_balance,
  fees_by_currency,
  last_event_key
}
```

Le profil accepte un événement d'initialisation explicite puis des fills `BUY` ou `SELL`.
Les deux balances commencent aux valeurs rationnelles préenregistrées. Dette, marge et
solde négatif sont interdits.

### Transitions minimales

Pour un fill de quantité base `q`, prix quote/base `p` et frais quote `f` :

```text
BUY:
  base_delta  = +q
  quote_delta = -(q × p + f)

SELL:
  base_delta  = -q
  quote_delta = +(q × p - f)
```

Le fill porte déjà sa quantité; P1 ne déduit pas un fill d'un budget ou d'un ordre. Le cas
manuel normatif « débit total 100 USD à 20 avec 0,1 USD de frais » est représenté par
`q=4,995`, `q×p=99,9` et `f=0,1`.

### Écritures et conservation

Chaque fill produit des `AccountEvent` séparant au minimum mouvement base, mouvement quote
et frais. Pour chaque transition :

```text
new_balance = old_balance + somme(account_event.delta de cette balance)
```

La valorisation au prix déclaré `v` est une projection, jamais une écriture :

```text
equity_quote = quote_balance + base_balance × v
```

L'oracle minimal obligatoire couvre achat puis revente au même prix avec frais et retrouve
exactement `99,8001 USD` depuis `100 USD` selon le calcul de référence.

### Hors profil spot P1

`UNSUPPORTED_IN_P1_PROFILE` et rejetés explicitement : short via vente sans base, crédit,
marge, borrow/intérêt, corporate actions, plusieurs instruments ou devises, partial fill
reconstruit depuis un ordre, carnet, slippage et fidélité exchange.

## 4. Profil comptable short minimal

### Discriminant et état

```text
account_model = ISOLATED_LINEAR_SHORT_EDU_V1
state = {
  instrument_spec_hash,
  reference_spec_hash,
  collateral_balance,
  position?,
  fees_by_currency,
  realized_pnl,
  last_event_key
}
```

Une position porte quantité base, prix d'entrée, notionnel quote, marge déclarée quote et
levier. Une seule position isolée et une clôture totale sont supportées.

### Capacités requises

Le modèle H0001/H0002 devient conforme au profil P1 seulement lorsque :

1. chaque quantité et montant porte instrument, unité et devise via les specs;
2. les discriminants `ISOLATED_LINEAR_SHORT_EDU_V1` et hashes de specs sont sérialisés;
3. ouverture, observation/valorisation et clôture sont des événements canoniques ordonnés;
4. chaque variation du collatéral, frais et PnL est expliquée par un `AccountEvent`;
5. `notional = quantity × price × contract_multiplier`;
6. `notional = declared_margin × leverage` et le levier n'affecte pas une seconde fois le
   PnL;
7. les frais déclarent base, devise, moment et compte de règlement;
8. le PnL latent est une projection réversible au prix de valorisation déclaré et ne mute
   pas le collatéral réalisé;
9. la clôture totale produit PnL réalisé, frais et position absente;
10. les oracles exacts H0001/H0002 restent vrais après passage par ces types canoniques.

### Décisions sur les mécanismes non démontrés

| Mécanisme | Décision | Comportement obligatoire |
|---|---|---|
| réservation/restitution de marge | `UNSUPPORTED_IN_P1_PROFILE` | `AccountSpec.margin_reservation = UNSUPPORTED`; marge déclarée validée mais non débitée, conformément à H0001 A3; toute demande de réservation est rejetée |
| liquidation | `UNSUPPORTED_IN_P1_PROFILE` | aucune liquidation silencieuse ou par stratégie; un événement/configuration exigeant liquidation est rejeté avec code stable |
| funding | `UNSUPPORTED_IN_P1_PROFILE` | taux ou événement funding non nul rejeté avec code stable |
| clôture partielle | `UNSUPPORTED_IN_P1_PROFILE` | quantité de clôture différente de la position rejetée |
| positions simultanées | `UNSUPPORTED_IN_P1_PROFILE` | seconde ouverture avant clôture rejetée |

Ces exclusions sont des discriminants sérialisés du profil, pas des omissions. Les ajouter
exigera une autre preuve mais leur absence ne bloque pas le P1 minimal ainsi borné.

## 5. Profil temporel minimal

P1 n'implémente aucun scheduler.

### Types et injection

- `InstantNs` et `DurationNs` sont des entiers signés en nanosecondes Unix UTC;
- `Clock` expose seulement `now_ns() -> InstantNs` et n'importe aucune source temporelle;
- un composant P1 qui n'a pas besoin du temps reçoit les `event_time` explicitement et ne
  reçoit pas artificiellement un `Clock`;
- un composant P1 qui crée réellement un instant reçoit `Clock` explicitement, sans valeur
  par défaut, singleton ou service locator;
- `FixedClock` est une fixture de test; `SystemClock` est interdit sous `domain/` et
  `replay/`.

### Enforcement obligatoire

Un contrôle AST parcourt récursivement `paper_trading_codex/domain/` et
`paper_trading_codex/replay/`, applique l'allowlist P1 v1 et suit les alias simples. Il doit
rejeter avec fichier, ligne et règle au minimum :

- `datetime.now()` et `datetime.now(timezone.utc)`;
- `from datetime import datetime as dt; dt.now()`;
- `time.time()` et `time.monotonic()`;
- fonctions temporelles assignées puis appelées;
- imports dynamiques de `time`;
- temps de fichiers par `os.stat`/`Path.stat`;
- `Clock` système implicite ou par défaut;
- `SystemClock` placé sous `domain/` ou `replay/`.

Les fallbacks legacy hors de ces répertoires ne sont pas une preuve P1 et ne bloquent pas
ce profil avant migration. Aucune exemption n'est permise pour le premier PASS P1 minimal.

## 6. Définition fermée de `P1 PASS`

| Capability | Statut | Preuve exécutable requise |
|---|---|---|
| `InstrumentSpec` | `REQUIRED_IN_P1` | tests de construction/sérialisation + mutants unité, type, multiplicateur, tick, lot, arrondi |
| `ReferenceSpec` et hash canonique | `REQUIRED_IN_P1` | tests exacts + rejet champ absent, hash incompatible, politique inconnue |
| `InstantNs`, `DurationNs`, `Clock` | `REQUIRED_IN_P1` | tests du port, injection explicite et absence de source système |
| `MarketEvent` | `REQUIRED_IN_P1` | tests du schéma, identité, ordre local, doublon divergent et temps obligatoire |
| `Fill` | `REQUIRED_IN_P1` | tests unités/devise/frais/side/temps et mutants correspondants |
| `AccountEvent` | `REQUIRED_IN_P1` | tests du discriminant, montants signés, devise et somme des variations expliquée |
| `SpotAccountModel / SPOT_CASH_V1` | `REQUIRED_IN_P1` | oracle exact achat/vente/frais/valorisation + mutants frais, solde, unité et conservation |
| `IsolatedLinearShortAccountModel / ISOLATED_LINEAR_SHORT_EDU_V1` | `REQUIRED_IN_P1` | oracles exacts H0001/H0002 via types canoniques + mutants frais, levier, signe, unité, conservation et capacités unsupported |
| contrôle AST temporel/allowlist | `REQUIRED_IN_P1` | tous les mutants directs, aliasés, dynamiques, filesystem et `SystemClock` rejetés |
| sérialisation rationnelle canonique | `REQUIRED_IN_P1` | vecteurs bit-exacts, fractions réduites, hashes stables, NaN/infini impossibles |
| manifeste et résultat intégrés P1 | `REQUIRED_IN_P1` | code/données/specs/commandes/hashes/environnement + résultat reproductible |
| Critique + Contradictoire + admission humaine du paquet P1 | `REQUIRED_IN_P1` | deux rapports conformes sur la même révision puis décision explicite |
| `OrderIntent`/stratégie | `DEFERRED_TO_P2+` | aucune preuve P1; attribution réelle P3 |
| scheduler/journal/replay | `DEFERRED_TO_P2+` | aucune preuve P1; attribution P2 |
| censure de fin de replay | `DEFERRED_TO_P2+` | aucune preuve P1 |
| provider/fidélité exchange | `DEFERRED_TO_P2+` | aucune preuve P1; attribution réelle P4 |
| live/checkpoint | `DEFERRED_TO_P2+` | aucune preuve P1; attribution réelle P5 |
| RiskMap/Pareto | `DEFERRED_TO_P2+` | aucune preuve P1; attribution réelle P6 |
| multi-actif/multi-devise/cross-margin | `UNSUPPORTED_IN_P1_PROFILE` | tests de rejet stable, aucune implémentation positive exigée |
| funding/liquidation/partial close/multi-position | `UNSUPPORTED_IN_P1_PROFILE` | tests de rejet stable et discriminants sérialisés |

### Règle de décision

> **P1 ne peut être déclaré `PASS` que lorsque chaque ligne `REQUIRED_IN_P1` possède sa
> preuve exécutable admise, que chaque capacité `UNSUPPORTED_IN_P1_PROFILE` est rejetée
> mécaniquement et sérialisée comme telle, et qu'aucune décision dont P1 dépend ne reste
> `UNKNOWN`.**

Un succès Hn isolé ne remplace pas cette preuve intégrée. Une capacité différée ne peut
être utilisée implicitement par un composant P1.

## NEXT EXPERIMENT CANDIDATES

Les écarts restants sont ordonnés par dépendance logique, sans identifiant d'hypothèse :

1. **socle de contrats canoniques exécutables** — politique rationnelle, `InstrumentSpec`,
   `ReferenceSpec`, temps scalaire et événements; dépendance de tous les ledgers;
2. **ledger spot minimal** — première capacité explicitement exigée mais entièrement
   absente, construite sur les contrats;
3. **projection du short démontré vers le profil canonique** — conserver H0001/H0002 en
   ajoutant specs, événements, discriminants et écritures expliquées;
4. **port `Clock` et enforcement temporel** — port minimal puis mutants AST sur le graphe
   canonique réel;
5. **preuve intégrée du gate P1** — exécution cumulative, manifeste, mutations, deux revues
   et admission.

L'ordre 2–4 peut être réévalué uniquement si le socle du point 1 démontre une dépendance
différente. Aucun de ces candidats n'est attribué comme H0003 dans ce document.

## Signal d'arrêt atteint

Le profil répond sans interprétation à « quoi construire et prouver pour `P1 PASS` » : les
types, décisions, comportements spot/short, exclusions, temps, preuves et règle finale sont
fermés. La prochaine action peut donc être la sélection humaine du premier écart
falsifiable; elle n'est pas réalisée ici.
