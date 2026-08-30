# Registre des branches d'hypothèse

## Statuts

`DRAFT`, `TESTING`, `IN_REVIEW`, `REFUTED`, `NON_TESTABLE`, `VALIDATED`, `MERGED`.

## Registre

| ID | Branche | Énoncé court | Gate | Critique | Contradictoire | Statut | Commit de fusion |
|---|---|---|---|---|---|---|---|
| H0001 | `hypothesis/H0001-canonical-ledger-equivalence` | équivalence comptable canonique du scénario P0 | P1 | `ACCEPT_WITH_LIMITS` | `ACCEPT_WITH_LIMITS` | `VALIDATED` | — |
| H0002 | `hypothesis/H0002-short-ledger-generalization` | conservation comptable du short sur une famille préenregistrée | P1 | `ACCEPT_WITH_LIMITS` | `ACCEPT_WITH_LIMITS` | `VALIDATED` | — |
| H0003 | `hypothesis/H0003-canonical-contract-foundation` | suffisance exécutable du socle canonique P1 | P1 | `ACCEPT_WITH_LIMITS` | `ACCEPT_WITH_LIMITS` | `VALIDATED` | — |
| H0004 | `hypothesis/H0004-minimal-spot-ledger` | conservation comptable d'un compte spot cash canonique | P1 | `REJECT` | `REJECT` | `TESTING` | — |

## Règle

Une ligne est créée en même temps que la branche. `VALIDATED` exige les deux rapports indépendants définis par le [Protocole Contradictoire](PROTOCOL_CONTRADICTOIRE.md). `MERGED` exige en plus l'identifiant du commit de fusion.

Pour H0001, `VALIDATED` signifie `VALIDATED_WITH_PUBLISHED_LIMITS` dans le seul domaine
préenregistré. Les rapports sont ancrés au commit `e4ff866`; leur admission et leurs hashes
sont consignés dans [`HUMAN_ADMISSION.md`](hypotheses/H0001/HUMAN_ADMISSION.md). Elle ne
vaut pas `P1 PASS`.

Pour H0002, `VALIDATED` signifie également `VALIDATED_WITH_PUBLISHED_LIMITS` dans la
famille préenregistrée seulement. Les rapports sont ancrés au commit `5658a8b`; leur
admission et leurs hashes sont consignés dans
[`HUMAN_ADMISSION.md`](hypotheses/H0002/HUMAN_ADMISSION.md). Elle ne vaut pas `P1 PASS`.

Le premier préenregistrement H0003 `ed2731d` a conclu `BLOCKED_SPEC_AMBIGUITY`. Les
décisions humaines `0fe5610` et `d817a16` ont fermé B1–B8/B5a avant code; les vecteurs ont
été gelés à `0e105c2`. Le premier paquet Producteur `44893b0` a reçu deux verdicts
`REJECT`, admis dans [`HUMAN_REJECTION_DECISION.md`](hypotheses/H0003/HUMAN_REJECTION_DECISION.md).
Le paquet initial `44893b0` reste rejeté et n'est jamais réhabilité. R1–R3 et les
contre-exemples admis ont ensuite été matérialisés dans le paquet corrigé `d3134e6`. Ses
deux rapports `ACCEPT_WITH_LIMITS`, ancrés à `ec7ae4b`, sont admis dans
[`HUMAN_ADMISSION.md`](hypotheses/H0003/HUMAN_ADMISSION.md). H0003 signifie donc
`VALIDATED_WITH_PUBLISHED_LIMITS` pour le paquet corrigé seulement; elle ne vaut pas
`P1 PASS`.

Le préenregistrement H0004 part du diagnostic post-H0003 `9c3b758`. Les mathématiques et
le scénario spot ont été gelés avant code à `044406f`. La décision humaine `8aa05bc` ferme
S1–S7 et permet de regeler les écritures et états exacts, mais le second préenregistrement
identifie S8 : détecter toute réapplication sans mémoire cachée exige une règle de
progression des fills. La décision humaine `cef58c5` ferme S8 par progression strictement
croissante des clés locales `Fill`. Le troisième préenregistrement est
`READY_FOR_IMPLEMENTATION`; H0004 passe au statut opérationnel `TESTING`, sans code encore
écrit et sans effet sur `P1`. Le Producteur a ensuite gelé un premier run nominal antérieur
aux mutants, un paquet complet M1–M19 et un résultat `PASS_PENDING_INDEPENDENT_REVIEW`.
H0004 est désormais `IN_REVIEW`; `P1` reste non passé.

Le paquet `5967ee0` a ensuite reçu deux verdicts `REJECT`, admis dans
[`HUMAN_REJECTION_DECISION.md`](hypotheses/H0004/HUMAN_REJECTION_DECISION.md). Le paquet
est rejeté mais l'hypothèse de faisabilité reste corrigeable : H0004 revient en
`TESTING / CORRECTION_REQUIRED` pour F1/F2, sans effet sur P1.
