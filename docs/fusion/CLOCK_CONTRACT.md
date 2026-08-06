# Contrat canonique `Clock`

## Types

`InstantNs` est un entier signé représentant des nanosecondes depuis l'époque Unix UTC. `DurationNs` est un entier signé de nanosecondes. Aucun objet `datetime`, timezone implicite ou flottant n'entre dans le domaine canonique.

## Port

Le futur module interne `paper_trading_codex.domain.clock` définit uniquement :

```python
from typing import Protocol, NewType

InstantNs = NewType("InstantNs", int)
DurationNs = NewType("DurationNs", int)

class Clock(Protocol):
    def now_ns(self) -> InstantNs: ...
```

Ce module n'importe aucune source temporelle. `Clock` est reçu explicitement par constructeur ou paramètre; aucune valeur par défaut n'est admise.

## Implémentations

- `ReplayClock` : vit sous `replay/`, commence à l'instant du manifeste et avance seulement par événement ou appel explicite `advance_to(InstantNs)`; retour arrière interdit.
- `FixedClock` : fixture de test retournant un instant préenregistré.
- `SystemClock` : vit uniquement sous un adaptateur `live/`, hors `domain/` et `replay/`; il convertit la source système en `InstantNs` avant injection.

## Invariants et mutants

1. mêmes événements + même instant initial → même séquence d'instants;
2. `ReplayClock` ne lit ni filesystem, ni réseau, ni horloge système;
3. un événement antérieur au dernier instant est rejeté ou traité par une politique d'ordre préenregistrée;
4. remplacer `Clock` par une construction implicite doit faire échouer P1;
5. placer `SystemClock` dans `domain/` ou `replay/` doit faire échouer l'allowlist.

## Limite

Le contrat exprime le temps logique du moteur; il ne prétend pas reproduire latence, dérive d'horloge ou temps de réception d'un fournisseur. Ces observations appartiennent aux événements F2+.
