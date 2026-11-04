# Diagnostic de l'état initial (Phase 1)

Toutes les valeurs ci-dessous proviennent d'exécutions réelles sur le code tel que
reçu (commit `a56a475`, moteur inchangé ; seule la tuyauterie d'évaluation a été
ajoutée). Référence figée dans `reports/baseline.json` ; rapports détaillés dans
`reports/evaluation_{test,dev,synthetique}.{json,md}`.

## 1. Tests

| Suite | Résultat |
|---|---|
| `python tests.py` (historique) | 19/19 verts |
| `python -m unittest discover -s tests` (ajoutée) | 14/14 verts |

## 2. Précision mesurée

| Jeu | Cas | Corrects | Précision | Erreurs critiques | Escalades critiques mal orientées | Décisions « incertaines » |
|---|---|---|---|---|---|---|
| Test gelé (50 tickets de l'ex-`validation.py`) | 50 | 46 | 92,0 % | 1 | 0 | 37 |
| Dev (rédigé pour la session, jamais vu par le moteur) | 83 | 68 | 81,9 % | 6 | 3 | 51 |
| Synthétiques (générés, graine 42) | 204 | 204 | 100 % | 0 | 0 | 150 |

Lecture : le 92 % annoncé est reproduit. Sur des formulations nouvelles (dev), la
précision tombe à 81,9 % et surtout **6 fausses résolutions** apparaissent,
dont 4 sur des cas critiques (sécurité, données). Les synthétiques sont à 100 %
par construction (leurs noyaux reprennent le vocabulaire couvert) : ils mesurent
la robustesse aux préfixes/suffixes, pas la précision réelle.

## 3. Précision par classe (jeu gelé puis dev)

| Classe | Gelé | Dev |
|---|---|---|
| Collaboration | 2/2 | 3/5 |
| Compte / Accès | 5/5 | 7/8 |
| Données | 2/2 | 3/5 |
| Inconnu (hors périmètre) | 7/8 | 8/10 |
| Infrastructure | 3/3 | 5/5 |
| Logiciel | 3/3 | 5/6 |
| Matériel | 6/7 | 9/10 |
| Messagerie | 2/3 | 4/6 |
| Performance | 1/2 | 4/5 |
| Réseau | 4/4 | 7/7 |
| Sécurité | 5/5 | 6/8 |
| Téléphonie | 3/3 | 4/4 |
| Web / Intranet | 3/3 | 3/4 |

## 4. Matrice de confusion (jeu gelé, attendu → prédit, hors diagonale)

- Messagerie → Inconnu : 1 (« emails », pluriel non apparié)
- Performance → Infrastructure : 1 (« tout rame » : le mot-clé « tout » de KB-102 est trop générique)
- Matériel → Inconnu : 1 (« ordi », vocabulaire familier)
- Inconnu → Web / Intranet : 1 (« changer ma photo sur l'intranet » : hors périmètre résolu à tort)

La matrice complète figure dans `reports/evaluation_test.md`.

## 5. Erreurs critiques observées

| Jeu | Cas | Obtenu | Cause |
|---|---|---|---|
| Gelé | « comment changer ma photo sur l intranet » | RESOLUTION_AUTO / Web | mot « intranet » seul suffit (seuil = 1) |
| Dev | « on m a piratee, mes contacts recoivent des mails de moi » | RESOLUTION_AUTO / Messagerie | « piratee » (féminin) absent, « mails » matche |
| Dev | « un faux site de la banque me demande mon mot de passe » | RESOLUTION_AUTO / Compte | « mot »+« passe » = 2 pts N1 contre 0 pour Sécurité (« demande mes identifiants » seulement) |
| Dev | « tous mes documents ont disparu du lecteur partage » | RESOLUTION_AUTO / Compte | « lecteur »+« partage » = 2 pts N1 contre « disparu » = 1 pt N2 |
| Dev | « mon disque dur fait un bruit bizarre et des fichiers sont illisibles » | RESOLUTION_AUTO / Compte | « disque » (KB-008) ; « fichiers » au pluriel ne matche pas KB-103 |
| Dev | « mon badge ne passe plus a l entree » | RESOLUTION_AUTO / Compte | « passe » seul (verbe) déclenche KB-002 |
| Dev | « je souhaite poser un jour de teletravail » | RESOLUTION_AUTO / Reseau | « teletravail » seul déclenche KB-007 (VPN) |

## 6. Causes d'échec identifiées (par fréquence)

1. **Pas de tolérance morphologique** : pluriels (« emails », « fichiers »,
   « imprimantes », « applis »), féminins (« piratee »), abréviations (« mdp »,
   « ordi »). Effet : escalades conservatrices, et parfois une catégorie N1
   gagne par défaut parce que le mot N2 n'a pas été vu.
2. **Mots-clés trop génériques ou polysémiques** : « tout », « personne » (KB-102),
   « passe » (verbe), « disque », « teletravail », « acces » et « connexion »
   partagés entre articles. Tous les mots pèsent 1 : un article à deux mots
   banals bat un article à un mot très spécifique (« disparu », « piratee »).
3. **Arbitrage N1/N2 uniquement à égalité stricte** : un indice N2 fort perd face
   à deux indices N1 faibles ; or l'erreur coûteuse est la fausse résolution.
4. **Seuil de résolution à un seul mot** (`SEUIL_CONFIANCE = 1`) : un mot isolé
   suffit à répondre automatiquement, ce qui produit les fausses résolutions hors
   périmètre.
5. **Signal de confiance peu informatif** : avec le score brut, 74 % des
   décisions du jeu gelé sont « incertaines » (score ≤ 1). Le signal doit
   devenir discriminant pour que la file « à revoir » soit exploitable.
6. **Égalités entre articles N1** tranchées par l'ordre de la base (D-045, D-051).

## 7. Latence

Médiane sous 0,1 ms par ticket sur tous les jeux (`latence_ms` dans les rapports) ;
non limitante.

## 8. Ce que le diagnostic n'a pas pu mesurer

- Aucun ticket réel : tous les jeux sont rédigés ou générés. La précision en
  production reste inconnue (voir `docs/limites-et-risques.md`).
