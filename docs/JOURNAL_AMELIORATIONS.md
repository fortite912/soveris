# Journal des améliorations mesurées

Méthode (phase 3) : une hypothèse, un changement minimal, mesure sur **dev**,
vérification de non-régression sur le **jeu gelé** et les **synthétiques**, un
commit par changement conservé. Le jeu gelé n'a jamais servi à choisir un
changement. Toutes les valeurs proviennent de `python -m soveris evaluer`.

État de départ (`reports/baseline_initiale.json`, commit `a56a475`) :
dev 68/83 (81,9 %, 6 erreurs critiques) · gelé 46/50 (92,0 %, 1 critique) ·
synthétiques 204/204.

| # | Commit | Hypothèse / changement | Dev avant → après | Gelé avant → après | Synth. | Décision |
|---|---|---|---|---|---|---|
| 1 | `1144fa7` | Pluriels non appariés → suffixe `s`/`x` optionnel + un mot du ticket ne compte qu'une fois par article (`mail`/`mails`) | 68/83, 6 crit. → 72/83, 6 crit. | 46/50, 1 crit. → 47/50, 1 crit. | 204/204 | **Gardé** |
| 2 | `62168c9` | Un indice N2 spécifique perd contre deux indices N1 banals → `marge_n2 = 1.0` (le N2 gagne s'il est à moins d'un point) | 72/83, 6 crit. → 73/83, 5 crit. | 47/50 → 47/50 | 204/204 | **Gardé** |
| 3 | `f6cf1d4` | « partage d'ecran » ≠ « partage d ecran » → apostrophes et tirets normalisés en espaces | 73/83 → 74/83, 5 crit. | 47/50 → 47/50 | 204/204 | **Gardé** |
| 4 | `dd91ede` | Mots-clés génériques (`tout`, `personne`, `passe`, `disque`, `teletravail`) remplacés par des formes composées ; vocabulaire sécurité/données courant ajouté (`mdp`, `cheval de troie`, `malware`, `faux site`, `illisible`, `piratee`) | 74/83, 5 crit. → 82/83, 0 crit. | 47/50 → 48/50, 1 crit. | 204/204 | **Gardé** |
| 5 | — | Pondération des mots partagés (`poids_partage` + seuil 0,5), bonus multi-mots 1,5, `marge_n2` 1,5, `seuil_revue` 1,5 : testés séparément | 82/83 → 82/83 pour les quatre variantes | 48/50 → 48/50 | 204/204 | **Rejeté** (aucun gain de décision) |

Arrêt après 5 itérations (maximum fixé). Résultat final :

| Jeu | Avant | Après |
|---|---|---|
| Dev | 68/83 (81,9 %), 6 erreurs critiques, 3 escalades critiques mal orientées | 82/83 (98,8 %), 0 erreur critique, 1 mal orientée |
| Gelé | 46/50 (92,0 %), 1 erreur critique | 48/50 (96,0 %), 1 erreur critique |
| Synthétiques | 204/204 | 204/204 |
| Démo (verrou `tests.py`) | 7/10 | 7/10 |

Erreurs restantes sur le jeu gelé : « mon ordi est mort » (vocabulaire
familier, escalade conservatrice) et « comment changer ma photo sur l intranet »
(hors périmètre résolu à tort sur le seul mot « intranet »). Elles ne sont pas
corrigées volontairement : les traiter en ajoutant « ordi » ou en bloquant
« photo » reviendrait à coder le jeu de test.

Ajustement annexe (hors précision) : le signal « incertain » est passé de
`score ≤ seuil_revue` à `score < seuil_revue` (plus Inconnu et égalités). La
file « à revoir » passe de 52/83 cas signalés sur dev à 24/83, en couvrant
2 des 3 erreurs restantes (dev + gelé). `reports/baseline.json` a été refigé
sur l'état final (`reports/baseline_initiale.json` conserve le départ).

## Journal de la boucle automatique

Les entrées ci-dessous sont ajoutées par `python -m soveris calibrer --appliquer`
(voir `docs/AUTO_AMELIORATION.md`). Aucune pour l'instant.
