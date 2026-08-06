# Compatibilité des moteurs et artefacts d'état

## Matrice

| Concept | Projet restauré | Projet Bitget | Contrat cible |
|---|---|---|---|
| ordre | événements grid implicites | buy/sell | `OrderIntent` directionnel |
| position | short avec quantité contractuelle | long spot | `SpotAccountModel` / `IsolatedLinearShortAccountModel` |
| equity | collatéral SOL valorisé | cash USDT + actifs | ledger dans numéraire déclaré |
| temps | timestamps injectés, quelques fallbacks | nombreux `now()`/sleep | `ReplayClock` / `LiveClock` |
| hasard | RNG local dans simulateur corrigé | `hash(symbol)` + RNG | `RandomSpec` |
| données | CSV/synthétique | mock/ccxt | `MarketDataSource` |
| état | manifeste | pickle/JSON portefeuille | `Checkpoint` distinct |
| événements | OPEN/CLOSE/LIQ | BUY/SELL | événements canoniques typés |
| métriques | registre normé | résumé portefeuille | `MetricRegistry` |

## Checkpoint, manifeste et journal

| Artefact | Mutable | Finalité | Peut prouver un résultat |
|---|---:|---|---:|
| `Checkpoint` | oui | reprendre un processus | non |
| `EventLog` | append-only | rejouer ce qui a été reçu | avec provenance complète |
| `RunManifest` | non | décrire l'expérience | oui, avec bundle |
| `ResultBundle` | non | porter résultats et verdicts | oui |

Invariant de reprise : le dernier `event_id` validé est enregistré; tout événement déjà appliqué est rejeté comme doublon. Invariant de replay : un `EventLog` fermé et hashé produit le même `ResultBundle` sous le même manifeste.

## Adaptateurs temporaires autorisés

- ancien trade Grid → `AccountEvent` avec statut `LEGACY_TRANSLATED`;
- trade spot Bitget → fills canoniques;
- CSV close-only → événements F0;
- OHLCV → événements F1.

Un événement traduit conserve le payload brut et ne peut recevoir un profil supérieur à sa source.
