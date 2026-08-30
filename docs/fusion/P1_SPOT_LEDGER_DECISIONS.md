# P1 — Décisions humaines du ledger spot minimal

## Autorité et portée

```text
decision_authority = HUMAN
supersedes_ambiguities_detected_at = 044406f38116658864ebe07ce3fa14a3a08d5f20
implementation_started = false
effect_on_H0004 = AUTHORIZED_FOR_REPREREGISTRATION_ONLY
effect_on_P1 = NOT_PASSED
```

Ces décisions ferment exactement S1–S7 du premier préenregistrement H0004. Elles ne
modifient pas H0003, ne créent aucun moteur d'exécution et n'autorisent le code H0004
qu'après un second préenregistrement démontrant qu'aucune autre convention exécutable
n'est nécessaire.

## S1 — Identité des `AccountEvent` dérivés

Pour un `AccountEvent` produit à partir d'un `Fill` :

```text
derivation_identity = {
  account_model,
  source_id,
  source_event_id = fill_id,
  kind,
  account
}

account_event_id =
  "ae:" + sha256(canonical_json(derivation_identity))
```

Les cinq clés portent exactement ces noms et la sérialisation est celle de H0003. Aucun
compteur, UUID, RNG, timestamp courant ou état global n'est autorisé. Une même identité
source et un même rôle produisent le même ID. Un contenu divergent sous cette identité
reste soumis à `DUPLICATE_DIVERGENT` selon H0003.

**Statut : `RESOLVED`.**

## S2 — Provenance et séquence des écritures d'un fill

Toute écriture dérivée d'un fill hérite exactement :

```text
source_id       = Fill.source_id
source_event_id = Fill.fill_id
event_time      = Fill.event_time
sequence        = Fill.sequence
```

Les trois écritures partagent temps et séquence; leur `account_event_id` les distingue
dans la clé locale B6. Aucun sous-compteur artificiel n'est créé.

**Statut : `RESOLVED`.**

## S3 — Initialisation explicite

Le `SpotAccountModel` part conceptuellement de balances nulles. Son état initial observable
est établi par des `AccountEvent(kind=INITIALIZE)` explicitement préenregistrés comme
inputs.

Le ledger ne crée ni leur ID ni leur provenance. Il les valide, les applique avant tout
fill et rejette toute nouvelle initialisation après le début des fills. Une balance nulle
peut être rendue explicite par un delta canonique `"0/1"`.

**Statut : `RESOLVED`.**

## S4 — `fees_by_currency`

```text
fees_by_currency[currency] >= 0
fees_by_currency[currency] += Fill.fee_amount
```

Ce champ est un cumul informatif de magnitudes acquittées. Il n'est pas une balance,
n'entre jamais une seconde fois dans la conservation et ne porte pas le signe du mouvement
comptable. L'écriture correspondante reste :

```text
AccountEvent(kind=FEE).delta = -Fill.fee_amount
```

**Statut : `RESOLVED`.**

## S5 — `last_event_key`

Le champ conserve la clé typée du dernier input ayant modifié le compte :

```text
(
  object_type,
  event_time,
  sequence,
  source_id,
  object_id
)

object_type = ACCOUNT_EVENT | FILL
```

Après une initialisation, la clé désigne l'`AccountEvent` input. Après application d'un
fill, elle désigne le `Fill` input, jamais les écritures dérivées. Ce pointeur de provenance
n'introduit aucun ordre canonique inter-types et ne constitue pas un scheduler P2.

**Statut : `RESOLVED`.**

## S6 — Réapplication d'un fill

Le ledger ne possède aucun registre caché de fills consommés. La déduplication H0003
`same identity + same bytes → IDEMPOTENT_DEDUPLICATE` reste une opération sur collection
explicite avant application.

Une tentative d'appliquer individuellement un fill à un état auquel ce fill a déjà été
appliqué est rejetée avec un code stable. Elle n'est ni réappliquée ni transformée en no-op.
Aucun `seen_fill_ids`, singleton, cache ou état non sérialisé n'est autorisé.

**Statut : `RESOLVED` au niveau de la sémantique; mécanisme à vérifier au second
préenregistrement.**

## S7 — Devise des frais de `SPOT_CASH_V1`

Le sous-profil positif H0004 accepte uniquement :

```text
Fill.fee_currency
== ReferenceSpec.fee_settlement_currency
== InstrumentSpec.quote
```

Une devise structurellement valide selon H0003 mais différente de `quote` est rejetée par
le ledger spot minimal avec :

```text
SPOT_FEE_CURRENCY_UNSUPPORTED
```

H0004 ne définit aucune algèbre de frais en base. H0003 continue de définir la compatibilité
structurelle générale; H0004 borne le sous-ensemble comptable effectivement supporté.

**Statut : `RESOLVED`.**

## Règle d'arrêt

Si le second préenregistrement découvre une décision supplémentaire modifiant balances,
écritures, bytes, IDs, rejets ou état sérialisé, il conserve
`H0004 = BLOCKED_SPEC_AMBIGUITY` et publie cette décision manquante. Le présent document
n'autorise aucune invention Producteur.
