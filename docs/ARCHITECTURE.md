# Architecture de Soveris

## 1. Vue d'ensemble

```
 demande (texte)
      │
      ▼
 soveris.analyser()  ── normalisation ─► scoring de chaque article ─► arbitrage
      │                                   (connaissances.py)          N1 / N2 / Inconnu
      ▼
 résultat structuré  {decision, categorie, niveau, score, confiance, ambigu,
                      mots_reconnus, solution, motif, temps_ms}
      │
      ├─► soveris.traiter()  : + journal local (journal/) et file « à revoir »
      ├─► database.py        : SQLite de démonstration (métriques ROI)
      └─► soveris.evaluation : rejoue les jeux étiquetés, produit les rapports
```

Tout est en Python standard. Aucun module du moteur n'importe de bibliothèque
réseau (`tests/test_reseau.py` le vérifie statiquement et dynamiquement).

## 2. Modules

| Chemin | Rôle |
|---|---|
| `soveris/__init__.py` | Moteur : `normaliser`, `scorer_article`, `analyser`, `est_incertain`, `traiter`. |
| `soveris/parametres.py` | Paramètres calibrables du moteur, chargés depuis `soveris/parametres.json` (phase 3). |
| `soveris/evaluation.py` | Chargement des jeux (`data/`), verdicts, rapport JSON/Markdown, baseline. |
| `soveris/diagnostic.py` | `python -m soveris diagnose` : tests + évaluation + comparaison baseline + constats priorisés, code de sortie CI. |
| `soveris/journal.py` | Journal des décisions (empreinte seulement), file « à revoir » pseudonymisée, intégration des corrections dans dev. |
| `soveris/auto_amelioration.py` | Recalibrage contrôlé des paramètres sur dev, garde-fous, application réversible (phase 5). |
| `soveris/__main__.py` | CLI : `evaluer`, `diagnose`, `calibrer`, `integrer-revues`, `demo`. |
| `connaissances.py` | Base de connaissances déclarative : liste d'articles `{id, categorie, niveau, mots_cles, solution}`. |
| `database.py` | Persistance SQLite de démonstration et métriques. |
| `demo.py`, `web.py` | Démonstrations terminal et web locale (127.0.0.1). Utilisent `soveris.traiter`. |
| `validation.py` | Compatibilité : expose le jeu gelé au format historique et le bilan `evaluer()` utilisé par `tests.py`. |
| `scripts/generer_synthetiques.py` | Génère `data/synthetiques.json` (déterministe). |

## 3. Données

| Fichier | Nature | Usage |
|---|---|---|
| `data/test_gele.json` | 50 tickets, `source: test_gele` | Vérification finale uniquement. Empreinte SHA-256 figée dans `tests/test_jeu_gele.py`. |
| `data/dev.json` | Tickets `source: dev` (rédigés) et `source: revue` (issus de la file) | Itération, calibration. |
| `data/synthetiques.json` | `source: generes` | Robustesse aux variantes de formulation. |

Format d'un cas :
```json
{"id": "D-001", "texte": "...", "attendu": "RESOLUTION_AUTO|ESCALADE",
 "categories": ["Reseau"], "critique": false, "source": "dev"}
```
`categories` liste les catégories acceptées (la première est la classe de
référence pour la précision par classe et la matrice de confusion). `critique`
marque les cas dont une résolution automatique serait dangereuse.

## 4. Décision

1. Chaque article reçoit un score (somme des poids des mots-clés reconnus par
   frontière de mot, après normalisation accents/casse).
2. Le meilleur score gagne ; à égalité, un article N2 bat un article N1.
3. Décision : `Inconnu` → escalade ; N2 → escalade avec contexte ; N1 sous le
   seuil → escalade par prudence ; sinon résolution automatique.
4. `ambigu` est vrai si un article d'une autre catégorie fait le même score ;
   `est_incertain()` combine Inconnu, score faible et ambiguïté pour alimenter la
   file « à revoir ».

## 5. Verdicts d'évaluation

`CORRECT`, `MANQUE` (escalade conservatrice), `MAL_CATEGORISE`,
`FAUSSE_DANGEREUSE`, `FAUSSE_HORS_PERIMETRE`. Les deux derniers sont les erreurs
critiques. Les escalades critiques orientées vers la mauvaise catégorie sont
comptées à part (`critiques_mal_orientees`).

## 6. Rapports

- `reports/baseline.json` : référence (résumés des trois jeux + commit).
- `reports/evaluation_<jeu>.{json,md}` : dernier rapport d'évaluation par jeu.
- `reports/diagnostic.{json,md}` : dernier auto-diagnostic.

## 7. Journal local

- `journal/decisions.jsonl` : une ligne par décision, sans texte (empreinte SHA-256 tronquée).
- `journal/a_revoir.jsonl` : décisions incertaines, texte pseudonymisé, champ `correction` à remplir par un humain.
- Ignoré par git.

## 8. Boucle d'amélioration

```
 production ─► file « à revoir » ─► correction humaine ─► integrer-revues ─► data/dev.json
                                                                                  │
 calibrer : recherche de paramètres sur dev ─► garde-fous (tests, réseau, test gelé) ─► parametres.json ─► PR
```
Détail dans `docs/AUTO_AMELIORATION.md`.
