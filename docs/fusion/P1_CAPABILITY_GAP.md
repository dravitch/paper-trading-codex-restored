# P1 — Capability map et gap-to-gate après H0001 + H0002

## Objet

Ce diagnostic confronte uniquement les preuves admises H0001/H0002 au contrat P1 présent
dans `06_FUSION_GATES.md`, `02_REFERENCE_MODEL.md`, `CANONICAL_CONTRACT_RFCS.md`,
`CLOCK_CONTRACT.md` et `01_CONCEPT_DECISION_REGISTER.md`.

Il ne formule aucune H0003, ne modifie aucun code, ne franchit aucun gate et n'importe pas
les exigences P2/P6 dans P1.

## Ancres admises

| Preuve | Admission | Portée retenue |
|---|---|---|
| H0001 | `de946c1` | exactitude rationnelle d'un short P0 isolé, ouverture puis clôture totale |
| H0002 | `68ca8f8` | mêmes invariants sur cinq shorts isolés préenregistrés, ledger H0001 inchangé |

Les deux admissions sont `VALIDATED_WITH_PUBLISHED_LIMITS`. Elles ne valent pas `P1 PASS`.

## Contrat P1 réellement applicable

Le gate P1 exige cumulativement :

1. des événements canoniques exécutables;
2. des instruments canoniques exécutables;
3. deux ledgers séparés, spot et short;
4. des oracles comptables exacts;
5. l'absence de source temporelle directe dans les nouveaux modules `domain/`/`replay/`;
6. un port `Clock` explicitement injecté lorsque le temps est nécessaire;
7. le rejet mécanique des mutations frais, levier et sources temporelles directes ou
   aliasées;
8. les preuves de gate usuelles : commandes, environnement, manifeste, hashes, mutations,
   décision Producteur et deux revues admises.

Les RFC documentaires ajoutent les contraintes nécessaires pour rendre ces livrables non
ambigus : unités/devise/multiplicateur/arrondi, événements distincts, modèles de compte
séparés, somme des variations expliquée par événements et discriminants sérialisés.

## Capability map

| Capacité P1 | État | Preuve actuelle | Écart exact |
|---|---|---|---|
| Arithmétique exacte du short linéaire | `DEMONSTRATED_LIMITED` | H0001 + H0002 | démontrée seulement pour position isolée, ouverture et clôture totales |
| Frais maker/taker comme mouvements du ledger | `DEMONSTRATED_LIMITED` | H0001 + H0002, mutants frais | règlement H0001 en SOL; aucune politique canonique générale par `ReferenceSpec`/compte |
| Levier appliqué une seule fois | `DEMONSTRATED_LIMITED` | H0001 + H0002, mutants levier | quantité short seulement; aucun `AccountSpec` exécutable |
| Conservation des états aux observations | `DEMONSTRATED_LIMITED` | snapshots exacts H0001/H0002 | pas d'equity/PnL latent canonique ni de prix de valorisation paramétré |
| Indépendance vis-à-vis de la stratégie/provider/temps mural | `DEMONSTRATED_FOR_LEDGER_PATH` | imports purs, oracle séparé | ne prouve pas le contrôle temporel de tout `domain/`/`replay/` futur |
| `IsolatedLinearShortAccountModel` canonique | `PARTIAL` | `domain/ledger.py` | pas de classe/discriminant RFC-005, devise/unité/instrument/arrondi non portés par les types, pas de partie double conceptuelle générale |
| `SpotAccountModel` canonique | `ABSENT` | aucune | aucun code, événement de compte, oracle ou mutation spot |
| `InstrumentSpec` | `ABSENT` | RFC-001 documentaire | aucun schéma exécutable ni rejet tick/lot/type/unité |
| Événements canoniques | `ABSENT` | dataclasses H0001 spécialisées | absence de `MarketEvent`, `Fill`, `AccountEvent`, identité, instrument, temps canonique et ordre RFC-002/004 |
| `ReferenceSpec` exécutable | `ABSENT` | modèle documentaire | aucun type/hash/politique numérique ou rejet de référentiels incompatibles |
| Port `Clock` / `InstantNs` | `ABSENT` | contrat documentaire | aucun `domain.clock`, `Clock`, `FixedClock` ou injection testée |
| Contrôle temporel P1 | `ABSENT` | règle AST documentaire | aucun analyseur, allowlist exécutable ni mutants temporels |
| Oracles comptables exacts short | `DEMONSTRATED_LIMITED` | oracles H0001/H0002 | famille finie full-close; pas oracle du modèle short RFC-005 complet |
| Oracle comptable exact spot | `ABSENT` | calcul manuel documentaire seulement | l'oracle « spot à prix constant » n'est ni exécutable ni admis expérimentalement |
| Preuve de gate P1 complète | `ABSENT` | dossiers H0001/H0002 | aucune exécution intégrée de tous les critères P1, aucun manifeste/revues de gate |

## Ce que H0001 + H0002 démontrent désormais

Le ledger actuel possède un noyau algébrique crédible pour un short linéaire isolé :

```text
taille par marge × levier
        + frais d'entrée
        + PnL short signé
        + frais de sortie
        + règlement USD→SOL au prix de l'événement
        + observations sans réalisation
        = états exacts sur six configurations admises
```

H0002 établit que ce résultat n'est pas un ajustement au seul scénario fondateur : le même
blob de ledger passe directement les cinq nouveaux cas, sans convention A11/A12 ni logique
par `scenario_id`.

Cette preuve réduit fortement l'incertitude sur les formules du chemin short full-close.
Elle ne transforme pas ces dataclasses spécialisées en modèle de domaine P1 complet.

## Limites connues conservées

| Limite | Statut pour P1 | Traitement |
|---|---|---|
| A8, magnitudes positives + direction versus PnL/deltas signés | `DESIGN_DECISION_REQUIRED` | trancher avant de figer le schéma général d'`AccountEvent`; aucune correction H0001 |
| famille short finie/full-close | `PUBLISHED_LIMIT` | borne les preuves H0001/H0002; ne force pas à elle seule la prochaine hypothèse |
| revues/oracles non IV&V | `EVIDENCE_LIMIT` | publier; non bloquant pour le protocole actuel |
| mutants ciblés | `EVIDENCE_LIMIT` | publier; le gate P1 devra exécuter ses propres mutants obligatoires |
| garde de complétude des clés H0002 | `TOOLING_DEBT_NON_BLOCKING` | ne rouvre pas H0002; à corriger seulement si le runner est réutilisé comme infrastructure |

## Exigences souvent évoquées mais non automatiquement bloquantes

Le contrat actuel ne permet pas de transformer toute capacité financière intéressante en
condition P1 :

- multi-actif est explicitement `DEFER` par CD-025;
- fidélité exchange relève des providers/P4, pas de P1;
- replay multi-période et scheduler relèvent de P2;
- RiskMap, admission d'oracles et immuabilité distante relèvent de P6/P7;
- long dérivé, clôture partielle et multi-position ne sont pas nommés dans le critère PASS
  minimal P1.

Ils peuvent devenir nécessaires seulement si une décision explicite montre qu'un modèle
spot/short minimal conforme ne peut être défini sans eux. Ils ne sont pas importés ici par
prudence ou intérêt technique.

Liquidation, funding et marge réservée demandent une clarification plus étroite : RFC-005
nomme marge, funding et compte short, tandis que le modèle de référence impose que la
liquidation soit un événement du compte. Le gate condensé ne précise pas le profil minimal
exécutable. P1 doit donc déclarer explicitement soit leur comportement minimal, soit un
statut `UNSUPPORTED` sérialisé et réfutable; le silence n'est pas acceptable.

## Questions documentaires bloquant une revendication P1

Les cinq questions de `CANONICAL_CONTRACT_RFCS.md` restent `UNKNOWN`. Pour le noyau P1,
elles doivent être décidées ou explicitement différées sans hypothèse silencieuse :

1. politique numérique (`Fraction`/`Decimal`/binary64 et arrondi);
2. identité interne d'instrument;
3. ordre canonique sans séquence source;
4. représentation d'une censure de fin de replay — différable vers P2 si aucun événement
   P1 ne la requiert;
5. multi-devise dès P1 ou conversion obligatoire — CD-025 permet de viser mono-instrument,
   mais devise et numéraire restent obligatoires.

A8 rejoint cette liste comme décision de représentation des écritures signées.

## Gap-to-gate P1

### Bloqueurs certains

| Priorité logique | Bloc | Pourquoi P1 ne peut pas passer |
|---:|---|---|
| 1 | contrat P1 exécutable non borné | les RFC restent `DRAFT_FOR_CRITIQUE` et plusieurs choix nécessaires sont `UNKNOWN` |
| 2 | `InstrumentSpec` et événements canoniques absents | deux des trois livrables nommés par le gate n'existent pas |
| 3 | ledger spot absent | le gate exige explicitement des ledgers spot **et** short |
| 4 | modèle short RFC-005 seulement partiel | le noyau démontré ne porte pas toutes les unités, devises, discriminants et écritures exigées |
| 5 | `Clock` et contrôle temporel absents | la règle temporelle P1 est documentaire, sans port ni mutations exécutables |
| 6 | preuve intégrée P1 absente | aucun dossier ne teste cumulativement livrables, oracles et mutations du gate |

### Conclusion de diagnostic

```text
P1 = NOT_PASSED
cause = MISSING_EXECUTABLE_CANONICAL_CONTRACTS_AND_SPOT_LEDGER
short_full_close_accounting = DEMONSTRATED_LIMITED
clock_enforcement = ABSENT
next_hypothesis = NOT_ASSIGNED
```

H0001 et H0002 ont éliminé une incertitude importante mais étroite : les formules du short
isolé full-close résistent à une famille paramétrique. Elles n'ont pas éliminé la majorité
des surfaces explicitement nommées par le gate P1.

## Décision requise avant toute H0003

La prochaine étape n'est pas de choisir le mécanisme le plus intéressant. Il faut d'abord
borner un **profil minimal P1 exécutable** répondant à ces questions :

1. quels types exacts constituent « événements, instruments, ledgers spot/short »;
2. quel sous-ensemble minimal de RFC-005 est obligatoire pour le short et le spot;
3. quelles questions `UNKNOWN` doivent être tranchées maintenant et lesquelles relèvent
   explicitement de P2+;
4. quelle preuve unique montrera le gate P1, au-delà des hypothèses composantes.

Ce bornage doit produire une liste fermée de capacités et critères de réfutation. Ce n'est
qu'ensuite qu'un écart suffisamment étroit pourra recevoir l'identifiant H0003.
