# PAMD — Principe → Artefact → Mécanisation → Durcissement
## Hypothèse v0.1 — non certifiée, un seul cas observé

---

## 1. Objectif

Un principe déclaré en prose se dégrade silencieusement dès qu'aucun mécanisme
ne peut le contredire : il est réinterprété, contourné, oublié, ou respecté en
apparence sans l'être en fait.

PAMD répond à un problème étroit et falsifiable : réduire l'écart entre ce
qu'un principe prétend garantir et ce qu'un tiers peut vérifier sans relire
tout l'historique de la décision.

**Condition de non-application** : PAMD n'a de valeur que si cet écart a un
coût réel. Un principe jamais violé, ou dont la violation est sans
conséquence, ne justifie pas le coût du déploiement. Ne pas appliquer PAMD à
tout — c'est un critère d'échec du diagnostic autant qu'un critère de succès
de l'outil.

---

## 2. Les quatre étapes

### Étape 1 — Principe

Une phrase normative, assignable, avec un domaine de validité explicite.
Forme : *"Dans [contexte], [acteur] ne doit jamais [action] sans [condition]."*

Le principe reste à ce stade tant qu'il n'est pas falsifiable en théorie —
c'est-à-dire tant qu'aucun état du monde imaginable ne pourrait le contredire.
S'il n'existe aucun cas de violation concevable, ce n'est pas une règle, c'est
un vœu.

**Exemple générique** : *"Un enregistrement, une fois écrit dans le registre,
ne peut jamais être modifié — seulement remplacé par un nouvel enregistrement
qui référence l'ancien."*

### Étape 2 — Artefact

Le principe reçoit une forme pointable : un fichier, un schéma, un champ nommé
que deux parties peuvent désigner sans ambiguïté ("le principe est à telle
ligne, tel fichier").

Sortie de l'étape : l'artefact doit être lisible sans son auteur. Un tiers qui
n'a pas participé à sa rédaction doit pouvoir dire ce qu'il exige, sans
contexte conversationnel supplémentaire.

**Exemple générique — schéma minimal d'un registre append-only** :
```json
{
  "record_id": "REC-000042",
  "content": { "...": "..." },
  "previous_record_hash": "a3f5...",
  "created_at_commit": "d82fb3a"
}
```
La règle "ne jamais modifier" devient ici un *champ obligatoire*
(`previous_record_hash`) plutôt qu'une instruction dans une doc.

### Étape 3 — Mécanisation

Un prédicat exécutable teste la conformité à l'artefact sans intervention
humaine.

Sortie de l'étape : le prédicat doit avoir **au moins une mutation connue qui
le fait échouer** — un cas construit exprès pour violer le principe, utilisé
pour vérifier que le mécanisme sait dire NON. Sans mutation testée, un
mécanisme qui dit toujours PASS n'a jamais été vérifié — il est décoratif.

**Exemple générique — le prédicat pour l'artefact ci-dessus** :
```
Test de conformité :
  pour chaque nouveau record R :
    calculer H = hash(dernier_record_connu)
    vérifier R.previous_record_hash == H
    si faux → REJETÉ

Mutation obligatoire (doit échouer) :
  soumettre un record dont previous_record_hash pointe vers un
  ancêtre qui N'EST PAS le dernier connu (tentative de réécriture
  de branche) → le test DOIT rejeter ce record.
```
Le principe "ne jamais modifier" n'est plus une phrase : c'est une commande
qui retourne 0 ou 1.

### Étape 4 — Durcissement

Le mécanisme de l'étape 3 est exposé, de façon répétée, à une critique
adversariale — un autre agent, une autre session, un regard qui cherche
activement une faille dans le *prédicat lui-même*, pas dans ce qu'il mesure.

Il n'y a pas de sortie propre à cette étape : le durcissement est
asymptotique. C'est ce qui distingue PAMD d'une checklist écrite une fois.

**Prédiction testable (non confirmée)** : contrairement aux étapes 1 à 3, qui
peuvent être planifiées à l'avance dans le même document fondateur, l'étape 4
tend à ne pas être anticipée — elle se découvre à mesure qu'un mécanisme
"complet" révèle une faille imprévue (ex. : un cas où deux parents peuvent
légitimement pointer vers le même ancêtre — mutation non couverte à l'étape
3). Si cette prédiction se confirme sur un second cas indépendant, elle
devient un trait structurel de PAMD plutôt qu'une observation isolée.

---

## 3. Catalogue de mécanismes réutilisables (étape 3, indépendant du domaine)

Pour qu'une IA ou un humain puisse *construire* l'étape 3 sans redécouvrir la
roue, voici des mécanismes génériques, transposables hors informatique quand
c'est indiqué :

| Mécanisme | Ce qu'il empêche | Transposable hors code |
|---|---|---|
| **Hash chaîné** (chaque record référence le hash du précédent) | Réécriture silencieuse de l'historique | Oui — numérotation notariale, cahier relié |
| **Statut fermé à 3-4 valeurs** (jamais texte libre) | Ambiguïté d'interprétation d'un verdict | Oui — tout système de décision à trancher |
| **ID stable préenregistré, pas de texte libre en clé** | Confusion entre "nouvelle occurrence" et "même cause renommée" | Oui — nomenclature de cas en droit, en médecine |
| **Mutation obligatoire par prédicat** | Mécanisme de vérification jamais testé (théâtre de conformité) | Oui — audit "et si on essayait de tricher" |
| **Verdict figé avant lecture croisée** | Contamination de l'indépendance entre deux jugements | Oui — double correction d'examen à l'aveugle |
| **Seuil de répétition avant décision obligatoire** | Report indéfini d'un problème récurrent non résolu | Oui — règle des trois retards avant sanction |

---

## 4. Critères objectifs de valeur (falsifiables)

| Critère | Question testable | Mesure |
|---|---|---|
| Capture d'état | Un tiers sans accès à l'historique peut-il reconstruire le principe depuis l'Artefact seul ? | Écart entre reconstruction et original |
| Détection de divergence | Le mécanisme détecte-t-il des mutations *non vues* à sa conception ? | Taux de détection sur jeu adversarial neuf |
| Traçabilité | Peut-on remonter d'un état donné à la chaîne de décisions sans trou ? | Nombre de sauts non expliqués |
| Transport de contexte | Un nouvel agent avec l'Artefact seul prend-il les mêmes décisions qu'avec l'historique complet ? | Écart de décision avec/sans historique |
| Coût marginal | Le coût de PAMD est-il inférieur à la valeur du principe protégé ? | Temps/tokens ajoutés vs. incidents évités |

### Condition d'échec de l'hypothèse

PAMD est réfutée dans un contexte donné si, après déploiement des étapes 1–3
seulement : (a) le coût marginal dépasse la valeur mesurée, (b) le mécanisme
ne détecte aucune mutation construite pour le tester, ou (c) un tiers sans
accès à l'historique ne peut pas reconstruire le principe depuis l'Artefact
seul. Ces échecs sont des résultats, pas des ratés à cacher.

---

---

# MISSION — PAMD-001 — Suivi des critères objectifs de valeur

## 0. Métadonnées
Mission ID : PAMD-001
Date de création : [À REMPLIR]
Auteur / Agent : [À REMPLIR]
Projet : [NOM DU PROJET CANDIDAT — indépendant du corpus d'origine]
Statut : ACTIF
Source de vérité : ce fichier + le dossier de sortie de la mission

## 1. Contexte

On teste si un déploiement minimal de PAMD (étapes 1–3 uniquement, sans
attendre le Durcissement) apporte une valeur mesurable sur un principe réel
du projet désigné ci-dessus — pas un principe fictif choisi pour bien
marcher.

**Contrainte impérative** : le principe testé doit déjà exister dans le
projet, énoncé en prose, sans artefact ni mécanisme associé aujourd'hui. Ne
pas inventer un principe nouveau pour l'occasion — cela biaiserait le test
en confondant la valeur de PAMD avec la valeur du principe.

## 2. Objectif général

Produire une mesure AVANT/APRÈS sur les cinq critères de valeur, suffisante
pour trancher : PAMD apporte-t-il un gain net dans ce contexte, ou son coût
dépasse-t-il sa valeur ?

## 3. Objectifs détaillés

- Sélectionner UN SEUL principe existant, non encore mécanisé
- Construire l'Artefact (étape 2) qui le porte
- Construire le prédicat de mécanisation (étape 3) AVEC au moins une
  mutation adversariale
- Mesurer les cinq critères de valeur AVANT (état actuel, principe en
  prose seul) et APRÈS (principe + Artefact + prédicat)
- Documenter tout échec de la même manière qu'un succès

## 4. Protocole à observer

### Setup
Choisir le principe. L'écrire sous la forme "Dans [contexte], [acteur] ne
doit jamais [action] sans [condition]." Vérifier qu'il est falsifiable :
décrire par écrit UN cas concret qui le violerait, avant de continuer.

### Métriques à capter (mesure AVANT, sur le principe en prose seul)
1. Capture d'état — donner le principe en prose à un agent naïf sans autre
   contexte, lui demander de citer un cas où il s'appliquerait. Noter
   l'écart avec l'intention réelle.
2. Détection de divergence — impossible à mesurer avant mécanisation
   (noter N/A explicitement, ne pas inventer un score)
3. Traçabilité — chercher dans l'historique existant si une violation
   passée du principe est identifiable a posteriori. Noter le temps requis.
4. Transport de contexte — donner le principe en prose à un second agent
   sans l'historique de la décision qui l'a motivé ; comparer sa décision
   à celle prise avec l'historique complet.
5. Coût marginal — N/A avant mécanisation (aucun coût encore engagé)

### Métriques à capter (mesure APRÈS, avec Artefact + prédicat)
Refaire les cinq mesures ci-dessus avec l'Artefact et le prédicat en place.
Pour le critère 2 (détection de divergence), construire au minimum une
mutation NON anticipée à la conception du prédicat et vérifier si elle est
détectée.

## 5. Ce que l'agent doit faire

1. Écrire le principe sélectionné et son cas de falsification AVANT toute
   autre action
2. Produire les cinq mesures AVANT, avec preuve horodatée (pas d'estimation
   a posteriori)
3. Construire Artefact + prédicat + au moins une mutation
4. Produire les cinq mesures APRÈS, avec preuve
5. Calculer l'écart AVANT/APRÈS sur chaque critère
6. Rendre un verdict explicite : GAIN NET / GAIN MARGINAL / PAS DE GAIN /
   COÛT SUPÉRIEUR AU GAIN — avec le calcul qui y mène, pas une impression

## 6. Critères de succès

- [ ] Un principe réel et préexistant a été choisi et documenté avec son
      cas de falsification
- [ ] Les cinq mesures AVANT sont produites avec preuve, y compris les N/A
- [ ] L'Artefact et le prédicat sont produits et fonctionnels
- [ ] Au moins une mutation adversariale non anticipée a été testée contre
      le prédicat
- [ ] Les cinq mesures APRÈS sont produites avec preuve
- [ ] Un verdict chiffré est rendu, y compris s'il est négatif

## 7. Interdictions

- Ne pas choisir un principe fictif ou trivial pour garantir un bon score
- Ne pas construire un prédicat sans lui soumettre au moins une mutation
  qu'il n'a pas été conçu pour anticiper
- Ne pas convertir un résultat négatif ou mitigé en conclusion positive par
  reformulation — un GAIN MARGINAL ou un COÛT SUPÉRIEUR AU GAIN est un
  résultat valide et doit être rapporté tel quel
- Ne pas passer à un second principe avant d'avoir clôturé la mesure
  complète du premier

## 8. Format attendu

Rapport de mission : `mission-PAMD-001-journal.md`
Livrables : principe + cas de falsification, Artefact, prédicat + mutation,
tableau des 10 mesures (5 avant / 5 après), verdict chiffré avec calcul
