# Soveris — guide pour l'agent de développement

## But
Moteur Python de triage des demandes de support IT de niveau 1, **100 % local**
(zéro dépendance, zéro appel réseau à l'exécution). Il classe une demande en
langage naturel, la résout si elle est courante (N1) ou l'escalade (N2) avec
contexte. La prudence prime : en cas de doute, on escalade.

## Architecture (détail dans docs/ARCHITECTURE.md)
- `soveris/` : paquet moteur. `__init__.py` (normalisation, scoring, arbitrage),
  `evaluation.py` (jeux de données, métriques, rapports), `diagnostic.py`
  (auto-diagnostic), `journal.py` (journal local des décisions, file « à revoir »),
  `auto_amelioration.py` (recalibrage contrôlé), `parametres.py` (paramètres
  calibrables), `__main__.py` (CLI).
- `connaissances.py` : base de connaissances déclarative (articles N1/N2).
- `database.py`, `demo.py`, `web.py` : persistance SQLite, démo terminal, démo web.
- `data/` : `test_gele.json` (gelé, protégé par empreinte), `dev.json`
  (itération), `synthetiques.json` (générés par `scripts/generer_synthetiques.py`).
- `tests/` : tests unittest. `tests.py` : suite historique (toujours exécutée).
- `reports/` : `baseline.json` (référence), rapports d'évaluation et de diagnostic.

## Commandes
```bash
python -m unittest discover -s tests -v   # tests
python tests.py                            # suite historique
python -m soveris evaluer --jeu dev        # évaluation (dev | test | synthetique | tous)
python -m soveris diagnose                 # tests + évaluation + comparaison baseline (code de sortie CI)
python -m soveris calibrer                 # auto-amélioration contrôlée (propose, vérifie, applique si gain)
python -m soveris integrer-revues          # verse les cas corrigés de la file « à revoir » dans dev
python demo.py / python web.py             # démonstrations
```

## Règles
- Aucun appel réseau à l'exécution (test `tests/test_reseau.py` l'impose).
- Interdit : coder en dur des cas des jeux de test, modifier `data/test_gele.json`
  pour améliorer un score, écrire un secret dans le dépôt.
- Aucun chiffre dans la documentation sans exécution réelle qui le produit.
- Un commit par changement mesuré ; journal dans docs/JOURNAL_AMELIORATIONS.md.
- Documentation en français ; code, identifiants et noms de fichiers en français
  sans accents (convention du dépôt).
- Le jeu de test gelé ne sert qu'à vérifier l'absence de régression, jamais à itérer.

## Définition de « terminé »
1. `python -m unittest discover -s tests` et `python tests.py` verts.
2. `python -m soveris diagnose` renvoie 0 (aucune régression contre `reports/baseline.json`).
3. Le changement est journalisé (avant/après, hash de commit) s'il touche le moteur ou les données.
4. Documentation mise à jour si le comportement visible change.
