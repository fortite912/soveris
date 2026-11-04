# Auto-amélioration contrôlée

## 1. Mécanismes envisagés

Le moteur est lexical : une base de connaissances déclarative (mots-clés par
article), un score par article, un arbitrage N1/N2 gouverné par quelques
paramètres (`soveris/parametres.json`). Trois mécanismes d'auto-amélioration
sont compatibles avec cette architecture et restent 100 % locaux :

| Mécanisme | Principe | Ce qu'il modifie | Simplicité | Risque |
|---|---|---|---|---|
| **A. Recalibrage des paramètres** | Recherche exhaustive, déterministe et bornée (144 combinaisons) des paramètres sur les données de dev ; application si tous les garde-fous passent. | Un seul fichier JSON (6 valeurs bornées). | Très simple, entièrement vérifiable, réversible par `git revert`. | Faible : l'espace est fermé, aucune valeur hors plage, aucun cas appris par cœur. |
| **B. Apprentissage de mots-clés depuis la file « à revoir »** | Pour chaque cas corrigé par un humain, proposer les mots du ticket absents de l'article correct ; retenir ceux qui apparaissent dans plusieurs corrections et dans aucun autre article. | `connaissances.py` (vocabulaire). | Moyenne : nécessite un volume de corrections et une relecture humaine des mots proposés (risque de mots-clés parasites : « bonjour », « urgent »). | Moyen : un mot mal choisi crée des fausses résolutions ; impossible à borner a priori. |
| **C. Pondération apprise des mots-clés** | Estimer un poids par mot-clé (fréquence dans les corrections / dans les erreurs). | Une table de poids par mot. | Complexe : des dizaines de valeurs libres, sur-apprentissage quasi certain avec 83 cas de dev. | Élevé. |

## 2. Choix : A, alimenté par la file « à revoir »

Le mécanisme A est retenu parce qu'il est le plus simple à auditer et le seul
dont l'espace de modification est **fermé et borné** (`parametres.PLAGES`).
Il n'est utile que si les données de dev évoluent : c'est le rôle de la file
« à revoir ». Les corrections humaines des cas incertains sont versées dans
`data/dev.json` (`source: "revue"`) par `python -m soveris integrer-revues`,
puis la calibration ré-explore les paramètres sur ce dev enrichi. La boucle
complète est donc :

```
 production ──► journal/a_revoir.jsonl ──► correction humaine (champ "correction")
                                                   │
                        python -m soveris integrer-revues
                                                   ▼
                                            data/dev.json (source: revue)
                                                   │
                        python -m soveris calibrer --appliquer --commit
                                                   ▼
            parametres.json + baseline.json + journal ──► pull request hebdomadaire
```

Le mécanisme B n'est pas implémenté : il est documenté comme prochaine étape,
à n'activer qu'avec une revue humaine des mots proposés. Le mécanisme C est écarté.

## 3. Objectif optimisé (sur dev uniquement)

Ordre lexicographique, à maximiser :
1. moins d'erreurs critiques (fausses résolutions dangereuses ou hors périmètre) ;
2. plus de décisions correctes ;
3. moins d'escalades critiques mal orientées.

À objectif égal, la configuration courante est conservée ; parmi des candidats à
gain égal, celui qui change le moins de paramètres l'emporte. Le seuil de revue
(`seuil_revue`) est choisi séparément : couvrir le plus d'erreurs de dev avec le
moins de cas signalés.

## 4. Garde-fous (tous obligatoires avant application)

| Garde-fou | Vérification |
|---|---|
| G1 | Gain **strict** de l'objectif sur dev. |
| G2 | Jeu **gelé** : décisions correctes ≥ avant et erreurs critiques ≤ avant. Le jeu gelé n'intervient jamais dans le choix, seulement dans le veto. |
| G3 | Synthétiques : mêmes conditions. |
| G4 | Chaque paramètre dans sa plage (`parametres.valider`). |
| G5 | Les deux suites de tests passent avec les nouveaux paramètres, dont `tests/test_reseau.py` (aucun appel réseau) et `tests/test_jeu_gele.py` (empreinte du jeu gelé intacte). En cas d'échec, l'ancien fichier est restauré. |
| G6 | Entrée ajoutée à `docs/JOURNAL_AMELIORATIONS.md` (avant/après par jeu, paramètres changés) et `reports/baseline.json` refigée. |

Le changement tient dans un commit (`--commit`) touchant trois fichiers
(`parametres.json`, `baseline.json`, journal) : `git revert` suffit à l'annuler.

## 5. Ce que la boucle ne fait jamais

- Modifier le code, la base de connaissances ou un jeu de données.
- Lire ou utiliser `data/test_gele.json` pour choisir un paramètre.
- Appeler le réseau. Le workflow GitHub Actions ne fait que lancer les commandes
  locales et ouvrir une pull request avec les fichiers produits.
- Fusionner seule : l'auto-merge est désactivé par défaut (voir § 6).

## 6. Workflow planifié (désactivé par défaut)

`.github/workflows/auto-amelioration.yml` tourne chaque lundi à 06:17 UTC et à la
demande. Il ne fait rien tant que la variable de dépôt
`SOVERIS_AUTO_AMELIORATION` ne vaut pas `true` (Settings → Secrets and
variables → Actions → Variables). Quand il est actif :

1. `python -m soveris diagnose` (rapport joint à la PR) ;
2. `python -m soveris calibrer --appliquer` ;
3. ouverture (ou mise à jour) d'une pull request `auto/amelioration` avec les
   rapports et, le cas échéant, les paramètres recalibrés.

L'auto-merge est gouverné par **un seul réglage** : la variable
`SOVERIS_AUTO_MERGE=true`. Il ne s'applique que si la calibration a appliqué un
changement, et la fusion reste conditionnée au passage de la CI (tests +
diagnostic) et aux règles de protection de la branche. Par défaut, la PR attend
une relecture humaine.

## 7. État mesuré

Sur l'état final de la phase 3, `python -m soveris calibrer` parcourt 144
combinaisons et conclut « aucun changement : les paramètres courants sont déjà
optimaux sur dev ». Le mécanisme a été validé de bout en bout sur une copie du
dépôt remise aux paramètres historiques : il a retrouvé `tolerance_pluriel` et
`marge_n2 = 1.0` (dev 77/83 → 82/83, gelé 47/50 → 48/50), passé les six
garde-fous et produit un commit réversible. Ce résultat figure dans
`tests/test_auto_amelioration.py` (gain retrouvé depuis les défauts, sans
régression sur le gelé).
