# Soveris

**Agent de triage et de résolution automatisée du support IT de niveau 1.**

![Python](https://img.shields.io/badge/Python-3.11%2B-1E2225)
![Dépendances](https://img.shields.io/badge/d%C3%A9pendances-0-9A7B4F)
![Souveraineté](https://img.shields.io/badge/traitement-100%25%20local-1E2225)
![Statut](https://img.shields.io/badge/statut-POC%20fonctionnel-8A8275)
![CI](https://github.com/fortite912/soveris/actions/workflows/ci.yml/badge.svg)

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
- [Évaluation, diagnostic et auto-amélioration](#évaluation-diagnostic-et-auto-amélioration)
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

**Principe de scoring.** Pour chaque demande, l'agent additionne les mots-clés de
chaque article de la base présents dans le texte (normalisation accents, casse,
apostrophes et tirets ; correspondance par **frontière de mot** avec tolérance au
pluriel). L'article au score le plus élevé l'emporte ; **un article N2 gagne dès
qu'il est à moins d'un point du meilleur N1** — à confiance comparable, l'agent
préfère escalader que répondre à tort. Chaque décision expose son score, son
niveau de confiance, un indicateur d'ambiguïté et son temps de traitement (de
l'ordre de la milliseconde, sans GPU). Les seuils et marges sont des paramètres
bornés (`soveris/parametres.json`), recalibrables automatiquement sous garde-fous.

## Démarrage rapide

Aucune installation. Python 3.11+ suffit.

```bash
git clone https://github.com/fortite912/soveris.git
cd soveris

# Démonstration automatique (jeu de tickets + tableau de bord)
python demo.py

# Mode interactif : saisissez vos propres incidents
python demo.py --interactif

# Interface web locale (ouvre http://127.0.0.1:8000 dans le navigateur)
python web.py

# Tests, évaluation, auto-diagnostic
python -m unittest discover -s tests -t .
python tests.py
python -m soveris evaluer --jeu dev
python -m soveris diagnose
```

Usage depuis Python :

```python
import soveris
r = soveris.analyser("je n'arrive plus a me connecter au wifi")   # analyse pure
r = soveris.traiter("...")   # analyse + journal local (sans donnée personnelle)
r["decision"], r["categorie"], r["niveau"], r["score"], r["confiance"], r["ambigu"]
```

> L'interface web est servie par `http.server` (bibliothèque standard) et
> n'écoute que sur **127.0.0.1** : rien n'est exposé au réseau, aucune donnée
> ne quitte la machine.

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

Chaque chiffre provient d'une exécution de `python -m soveris evaluer` ; les
rapports complets (par classe, matrice de confusion, erreurs) sont dans `reports/`.

| Jeu | Nature | État reçu | État actuel |
|---|---|---|---|
| Jeu de test **gelé** (50 tickets, empreinte protégée) | indépendant, jamais utilisé pour itérer | 46/50 (92,0 %), 1 fausse résolution hors périmètre | **48/50 (96,0 %)**, 1 fausse résolution hors périmètre |
| Jeu de **dev** (83 tickets rédigés pour la session) | sert à itérer | 68/83 (81,9 %), 6 fausses résolutions dont 4 critiques | **82/83 (98,8 %)**, 0 fausse résolution |
| Synthétiques (204 cas générés) | robustesse aux variantes | 204/204 | 204/204 |
| Jeu de démonstration (10 tickets) | illustration | 7/10 résolus auto | 7/10 résolus auto |
| Fausses résolutions **dangereuses** (sécurité, données, infrastructure) sur le jeu gelé | | 0 | 0 |
| Latence | | < 0,1 ms médiane | < 0,1 ms médiane |

Les quatre changements qui expliquent l'écart sont journalisés avec leur mesure
avant/après et leur commit dans
[docs/JOURNAL_AMELIORATIONS.md](docs/JOURNAL_AMELIORATIONS.md). Les deux erreurs
restantes du jeu gelé (« mon ordi est mort » escaladé ; « changer ma photo sur
l'intranet » résolu à tort) sont laissées telles quelles : les corriger
reviendrait à coder le jeu de test.

> Ces mesures portent sur des tickets rédigés ou générés, pas sur des données
> réelles. Le taux en production est inconnu (voir
> [docs/limites-et-risques.md](docs/limites-et-risques.md)).

## Évaluation, diagnostic et auto-amélioration

```bash
python -m soveris evaluer --jeu dev|test|synthetique|tous   # rapport JSON + Markdown
python -m soveris diagnose        # tests + évaluation + comparaison à reports/baseline.json
                                  # code de sortie 0 (OK) / 1 (régression ou test rouge) / 2 (erreur)
python -m soveris calibrer        # propose un recalibrage des paramètres sur dev (rien n'est écrit)
python -m soveris calibrer --appliquer --commit   # applique si les 6 garde-fous passent
python -m soveris integrer-revues # verse les cas corrigés de la file « à revoir » dans data/dev.json
```

- **Jeux séparés** : `data/test_gele.json` (gelé, protégé par empreinte SHA-256 dans
  les tests), `data/dev.json`, `data/synthetiques.json` (générés, marqués).
- **Journal local** : `soveris.traiter()` consigne chaque décision dans `journal/`
  (empreinte du texte, jamais le texte) et range les décisions incertaines dans une
  file « à revoir » pseudonymisée. Dossier ignoré par git.
- **Auto-amélioration** : recalibrage borné des paramètres sur dev, veto du jeu
  gelé, tests verts dont l'interdiction réseau, commit réversible, entrée au
  journal. Workflow hebdomadaire désactivé par défaut, auto-merge par un seul
  réglage. Détail : [docs/AUTO_AMELIORATION.md](docs/AUTO_AMELIORATION.md).
- **CI** : `.github/workflows/ci.yml` lance les tests et le diagnostic sur chaque
  push et pull request.

## Architecture du code

| Chemin | Rôle |
|---|---|
| `soveris/__init__.py` | Moteur : normalisation, scoring pondéré par frontière de mot, arbitrage N1/N2, `analyser` / `traiter` |
| `soveris/parametres.py` + `parametres.json` | Paramètres bornés du moteur (seuils, marge N2, tolérance pluriel) |
| `soveris/evaluation.py` | Jeux de données, verdicts, rapports, baseline |
| `soveris/diagnostic.py` | Auto-diagnostic priorisé avec code de sortie CI |
| `soveris/journal.py` | Journal local des décisions et file « à revoir » |
| `soveris/auto_amelioration.py` | Recalibrage contrôlé (garde-fous G1..G6) |
| `soveris/__main__.py` | Ligne de commande `python -m soveris` |
| `connaissances.py` | Base de connaissances déclarative (15 articles de support) |
| `database.py` | Persistance SQLite de démonstration + métriques |
| `demo.py`, `web.py` | Démonstrations terminal et web locale (127.0.0.1) |
| `validation.py` | Compatibilité : expose le jeu gelé au format historique |
| `data/`, `reports/`, `docs/` | Jeux étiquetés, rapports mesurés, documentation (architecture, diagnostic, journal, limites) |
| `tests/`, `tests.py` | 24 tests unittest + 19 vérifications historiques |

Le détail figure dans [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Choix techniques

- **Zéro dépendance externe** (`sqlite3`, `unicodedata` de la bibliothèque standard) :
  exécution immédiate, code intégralement auditable, surface d'attaque minimale.
- **Souveraineté des données** : traitement local, compatible déploiement on-premise
  en DSI — aucune donnée transmise à un tiers.
- **Base de connaissances déclarative** : un expert métier ajoute un cas de support
  sans modifier la logique de l'agent.
- **Décision traçable** : chaque arbitrage expose son score, son niveau de
  confiance, ses mots-clés reconnus et son temps de traitement.
- **Qualité vérifiée** : 24 tests unittest et 19 vérifications historiques,
  dont l'interdiction de tout appel réseau, l'empreinte du jeu gelé et des
  verrous de non-régression (démo 7/10, jeu gelé ≥ 46/50, zéro fausse
  résolution dangereuse).
- **Validation mesurée, pas proclamée** : jeux séparés (gelé / dev /
  synthétiques), rapports reproductibles, baseline figée et diagnostic qui
  échoue en CI à la moindre régression.

## Limites connues

Cas d'échec, risques, garde-fous et ce que le système ne garantit pas :
**[docs/limites-et-risques.md](docs/limites-et-risques.md)**. Le chemin
d'industrialisation (intégration, sécurité, conformité) reste décrit dans
[LIMITES.md](LIMITES.md).

## Feuille de route

- [x] Tolérance morphologique (pluriels), normalisation apostrophes/tirets
- [x] Évaluation reproductible, auto-diagnostic, recalibrage contrôlé
- [ ] Apprentissage de mots-clés depuis la file « à revoir » (avec relecture humaine)
- [ ] Gestion des synonymes et du vocabulaire familier (« ordi »)
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
