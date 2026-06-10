# Soveris

**Agent de triage et de résolution automatisée du support IT de niveau 1.**

![Python](https://img.shields.io/badge/Python-3.11%2B-1E2225)
![Dépendances](https://img.shields.io/badge/d%C3%A9pendances-0-9A7B4F)
![Souveraineté](https://img.shields.io/badge/traitement-100%25%20local-1E2225)
![Statut](https://img.shields.io/badge/statut-POC%20fonctionnel-8A8275)

Soveris intercepte une demande de support exprimée en langage naturel, la qualifie,
la résout lorsqu'elle est courante, ou l'escalade vers un ingénieur avec un contexte
enrichi. Le tout en **Python standard, sans aucune dépendance externe**, et en
**traitement 100 % local** : aucune donnée ne quitte le système d'information.

---

## Sommaire

- [Le problème](#le-problème)
- [La solution](#la-solution)
- [Fonctionnement](#fonctionnement)
- [Démarrage rapide](#démarrage-rapide)
- [Exemple de sortie](#exemple-de-sortie)
- [Indicateurs mesurés](#indicateurs-mesurés)
- [Architecture du code](#architecture-du-code)
- [Choix techniques](#choix-techniques)
- [Feuille de route](#feuille-de-route)
- [Genèse du projet](#genèse-du-projet)
- [Licence](#licence)

---

## Le problème

Dans toute infrastructure d'entreprise, le support de niveau 1 (N1) concentre la
majorité du volume de tickets pour une valeur ajoutée marginale : réinitialisations
de mots de passe, incidents de connectivité, demandes d'accès, pannes récurrentes
déjà documentées. Ce flux répétitif mobilise un temps d'ingénieur coûteux, dégrade
les délais de prise en charge et alimente le turnover des équipes support.

## La solution

Soveris automatise le traitement **à l'entrée du flux** :

- **résout** automatiquement les incidents courants (N1) ;
- **escalade** les cas sensibles (N2) vers un ingénieur, avec un contexte de
  qualification déjà constitué ;
- **trace** chaque décision et produit des indicateurs de pilotage (ROI).

## Fonctionnement

```
            Demande en langage naturel
                       │
        ┌──────────────▼──────────────┐
        │  1. CLASSIFICATION           │   catégorie + niveau (N1 / N2)
        ├──────────────────────────────┤
        │  2. RÉSOLUTION               │   appariement base de connaissances
        ├──────────────────────────────┤
        │  3. ARBITRAGE                │   résolution auto │ escalade enrichie
        ├──────────────────────────────┤
        │  4. TRAÇABILITÉ              │   journalisation + métriques (ROI)
        └──────────────────────────────┘
```

**Principe de scoring.** Pour chaque demande, l'agent compte les mots-clés de chaque
article de la base présents dans le texte (normalisation des accents + correspondance
par **frontière de mot** pour éliminer les faux positifs). L'article au score le plus
élevé l'emporte ; **à score égal, l'article N2 gagne** — à confiance équivalente,
l'agent préfère escalader que répondre à tort. Chaque décision expose son niveau de
confiance et son temps de traitement (de l'ordre de la milliseconde, sans GPU).

## Démarrage rapide

Aucune installation. Python 3.11+ suffit.

```bash
git clone https://github.com/fortite912/soveris.git
cd soveris

# Démonstration automatique (jeu de tickets + tableau de bord)
python demo.py

# Mode interactif : saisissez vos propres incidents
python demo.py --interactif
```

## Exemple de sortie

```
Ticket #1 : Je n'arrive plus a me connecter au wifi
   RESOLU AUTO   Categorie : Reseau (N1)   Confiance : HAUTE   0.3 ms
  Mots reconnus : wifi, connecter

Ticket #8 : J'ai recu un mail suspect de phishing
    ESCALADE     Categorie : Securite (N2)   Confiance : HAUTE

════════════════════════════════════════════════════════════════
 TABLEAU DE BORD  -  indicateurs de pilotage (R.O.I.)
════════════════════════════════════════════════════════════════
  Tickets traites            : 10
  Resolus automatiquement    : 7
  Taux de resolution auto    : █████████████████████░░░░░░░░░ 70.0 %
  Temps moyen de traitement  : 0.5 ms / ticket
  ≈ 70 min de temps ingenieur N1 preserve (hypothese 10 min/ticket)
════════════════════════════════════════════════════════════════
```

> Affichage en couleurs ANSI natives (aucune librairie) — désactivable en
> définissant la variable d'environnement `NO_COLOR`.

## Indicateurs mesurés

| Banc | Résultat |
|---|---|
| Jeu de démonstration (10 tickets) | **70 %** de résolution automatique |
| Validation indépendante (50 tickets variés, pièges et hors périmètre inclus) | **92 %** de décisions correctes |
| Fausses résolutions dangereuses (sécurité, données, infrastructure) | **0** |
| Temps de traitement | ~0,5 ms / ticket (déterministe, sans GPU) |

Les erreurs résiduelles du banc de validation sont **conservatrices** (l'agent
escalade au lieu de deviner) et documentées — limites connues : pluriels non
appariés, vocabulaire familier (« ordi »). Leur traitement est en feuille de route.

## Architecture du code

| Fichier | Rôle |
|---|---|
| `connaissances.py` | Base de connaissances déclarative (15 articles de support) |
| `soveris.py` | Moteur : normalisation, scoring par frontière de mot, arbitrage |
| `database.py` | Persistance SQLite + calcul des métriques |
| `demo.py` | Démonstration automatique et mode interactif (couleurs ANSI natives) |
| `validation.py` | Banc de validation indépendant : 50 tickets étiquetés, mesure des fausses résolutions |
| `tests.py` | Suite de tests automatisés (19 vérifications, `python tests.py`) |

Chaque module est exécutable seul (`python soveris.py`, `python database.py`…) pour
en tester le comportement isolément.

## Choix techniques

- **Zéro dépendance externe** (`sqlite3`, `unicodedata` de la bibliothèque standard) :
  exécution immédiate, code intégralement auditable, surface d'attaque minimale.
- **Souveraineté des données** : traitement local, compatible déploiement on-premise
  en DSI — aucune donnée transmise à un tiers.
- **Base de connaissances déclarative** : un expert métier ajoute un cas de support
  sans modifier la logique de l'agent.
- **Décision traçable** : chaque arbitrage expose son score, son niveau de
  confiance, ses mots-clés reconnus et son temps de traitement.
- **Qualité vérifiée** : suite de 19 tests automatisés (`python tests.py`)
  couvrant décisions, prudence, robustesse du matching, persistance, et des
  verrous de non-régression sur le jeu de démonstration (70 %) et sur le banc
  de validation (92 %, zéro fausse résolution dangereuse).
- **Validation mesurée, pas proclamée** : le banc `validation.py` rejoue
  50 tickets rédigés du point de vue utilisateur (formulations vagues, fautes,
  cas hors périmètre) et mesure aussi les *fausses résolutions* — la métrique
  de confiance d'une DSI.

## Feuille de route

- [ ] Pondération des mots-clés et gestion des synonymes
- [ ] Couche NLP optionnelle (LLM local, on-premise)
- [ ] Connecteur vers les outils de ticketing existants (GLPI, ServiceNow)
- [ ] Tableau de bord web des métriques
- [ ] Mesure de l'impact « Green IT » (réduction des requêtes redondantes)

## Genèse du projet

Le moteur de Soveris réutilise l'architecture (scoring sémantique, machine à états,
persistance transactionnelle) d'un premier prototype d'automatisation que j'ai conçu
en autonomie. Le pivot vers le support IT n'est donc pas une hypothèse théorique,
mais la transposition d'un socle technique déjà éprouvé.

## Licence

© 2026 Sean Fritsch. Tous droits réservés.
Dépôt public à fins de démonstration. Toute réutilisation est soumise à autorisation.
