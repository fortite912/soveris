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
| 11 | Baseline de référence | `reports/baseline.json` est refigée sur l'état final de la phase 3 (sinon le diagnostic ne détecterait jamais une régression par rapport à l'état livré) ; `reports/baseline_initiale.json` conserve l'état reçu. |
| 12 | Vocabulaire ajouté en phase 3 | Les mots ajoutés (`mdp`, `cheval de troie`, `malware`, `faux site`, `illisible`, `piratee`, formes composées pour `tout`/`personne`) sont du vocabulaire métier générique motivé par les erreurs de **dev**. « ordi » n'a volontairement pas été ajouté : seul le jeu gelé l'exige. |
| 13 | Jeu de démonstration | `TICKETS_DEMO` (10 tickets) reste verrouillé à 7/10 dans `tests.py` ; il n'a pas été intégré aux jeux d'évaluation (c'est une vitrine, pas une mesure). |
| 14 | Auto-merge | Mis en œuvre par `gh pr merge --auto`, qui exige que l'auto-merge soit autorisé dans les réglages du dépôt et qu'une protection de branche existe ; sans cela la commande échoue et la PR reste ouverte (comportement voulu : jamais de fusion silencieuse). |
| 15 | Vitesse des tests | La suite unittest dure ~30 s à cause de la recherche sur grille (144 combinaisons) dans `tests/test_auto_amelioration.py` ; jugé acceptable pour une CI, à réduire si gênant. |
