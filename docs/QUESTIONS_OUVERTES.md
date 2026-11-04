# Questions ouvertes et hypothèses prises

Aucune question n'a été posée pendant la session ; chaque point ci-dessous est une
hypothèse prise faute d'information, à confirmer ou infirmer par le porteur du projet.

| # | Sujet | Hypothèse retenue |
|---|---|---|
| 1 | Bloc « CONTEXTE FOURNI » | Absent de la demande ; `docs/CONTEXTE.md` n'a donc pas été créé. |
| 2 | Jeu de test gelé | Le banc de 50 tickets de `validation.py` devient le jeu gelé (`data/test_gele.json`). Il est le seul jeu indépendant existant ; il n'est jamais utilisé pour itérer. |
| 3 | Données de dev | Aucune donnée de dev n'existait : un jeu `data/dev.json` a été rédigé pour la session (tickets nouveaux, formulations d'utilisateur, sans regarder les mots-clés au moment de l'écriture). Il est marqué `"source": "dev"`. |
| 4 | Verrou historique `46/50 == ` dans `tests.py` | Transformé en verrou de non-régression (`>= 46`) : un verrou d'égalité interdirait toute amélioration. Le jeu lui-même n'est pas modifié. |
| 5 | Données personnelles dans le journal | Le journal des décisions ne stocke qu'une empreinte SHA-256 tronquée du texte. La file « à revoir » conserve un texte **pseudonymisé** (e-mails, téléphones, suites de chiffres, URL masqués), car un humain doit pouvoir relire le cas. `database.py` (démo) conserve le texte brut comme avant : à aligner si la démo traite un jour des données réelles. |
| 6 | Décision « à faible confiance » | Score pondéré inférieur à `SEUIL_REVUE` (paramètre), ou égalité entre deux articles de catégories différentes, ou catégorie `Inconnu`. |
| 7 | Structure du code | `soveris.py` devient le paquet `soveris/` pour permettre `python -m soveris`. `import soveris; soveris.analyser(...)` reste identique. |
| 8 | Workflow planifié | GitHub Actions ne peut pas livrer un workflow « désactivé » nativement : la désactivation passe par une variable de dépôt (`vars.SOVERIS_AUTO_AMELIORATION`), absente par défaut. L'auto-merge est gouverné par `vars.SOVERIS_AUTO_MERGE`. |
| 9 | Erreur critique | Toute résolution automatique d'un cas étiqueté critique (sécurité, données, infrastructure), ou toute résolution automatique d'un cas hors périmètre. Une escalade conservatrice n'est jamais critique. |
| 10 | Python cible | 3.11+ (README). La session a tourné sous 3.13. |
