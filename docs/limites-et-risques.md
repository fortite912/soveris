# Limites et risques

Ce document dit ce que Soveris **ne garantit pas**. Il complète `LIMITES.md`
(chemin d'industrialisation) et `docs/DIAGNOSTIC.md` (mesures).

## 1. Cas d'échec connus

| Cas | Comportement | Gravité |
|---|---|---|
| Vocabulaire familier ou abrégé non listé (« ordi », « mon pc est mort ») | Escalade `Inconnu` (conservatrice) | Faible : un humain reprend |
| Demande hors périmètre contenant un mot technique (« changer ma photo sur l'intranet ») | Résolution automatique à tort | Moyenne : réponse inutile envoyée à l'utilisateur |
| Deux articles N1 à égalité sans mot discriminant (« le portail rh ne s'ouvre pas dans firefox ») | Le premier article de la base gagne | Faible : mauvaise catégorie N1, décision correcte |
| Incident de sécurité formulé sans aucun mot du lexique (« quelqu'un a utilisé mon compte pendant mes vacances ») | Escalade `Inconnu` au lieu de `Securite` | Moyenne : escalade correcte mais non priorisée |
| Négations et contexte (« ce n'est pas un problème de wifi ») | Le mot compte quand même | Moyenne : fausse résolution possible |
| Plusieurs incidents dans un même ticket | Un seul article retenu | Faible à moyenne |
| Fautes d'orthographe au-delà du pluriel (« imprimente ») | Non reconnu | Faible : escalade |
| Texte long et bavard | Plus de mots déclencheurs, risque de catégorie parasite | Moyenne |

## 2. Risques

- **Fausse résolution d'un cas critique.** C'est le risque principal. Il est
  mesuré à 0 sur les jeux gelé et dev *actuels*, mais ces jeux sont rédigés : un
  attaquant ou un utilisateur créatif peut formuler un incident de sécurité
  sans aucun mot du lexique, ou avec deux mots N1 forts. La marge N2 réduit ce
  risque sans l'éliminer.
- **Sur-apprentissage des données de dev.** Les paramètres et le vocabulaire
  ont été choisis sur 83 cas. Le jeu gelé sert de veto, pas de preuve de
  généralisation : 50 cas donnent une précision à ± 5 points près.
- **Dérive du vocabulaire.** Un nouvel outil interne, un nouveau nom de
  produit : la base ne le connaît pas tant qu'un humain ne l'ajoute pas.
- **Boucle automatique.** Elle ne touche qu'aux paramètres bornés, mais un dev
  enrichi par des corrections humaines erronées orienterait la calibration dans
  le mauvais sens. D'où la relecture de la PR hebdomadaire et l'auto-merge
  désactivé par défaut.
- **Données personnelles.** Le journal ne stocke que des empreintes ; la file
  « à revoir » stocke un texte pseudonymisé par expressions régulières, ce qui
  ne couvre pas tout (noms sans majuscule, identifiants internes, lieux). La
  base SQLite de démonstration conserve le texte brut.
- **Pas de données réelles traitées.** Toute mesure ici est obtenue sur des
  tickets rédigés ou générés.

## 3. Garde-fous en place

- Escalade par défaut : `Inconnu`, score sous le seuil, N2 à moins d'un point
  d'un N1.
- Jeu gelé protégé par empreinte SHA-256 ; verrous de non-régression dans les
  deux suites de tests ; diagnostic qui échoue en CI à la moindre régression.
- Interdiction de tout appel réseau, vérifiée statiquement (imports) et
  dynamiquement (sockets) à chaque exécution des tests.
- Calibration automatique bornée (`parametres.PLAGES`), gain strict exigé sur
  dev, veto du gelé et des synthétiques, tests verts, journal, commit unique
  réversible, workflow désactivé par défaut, auto-merge désactivé par défaut.
- Aucune donnée de ticket dans le dépôt : `journal/` et `*.db` sont ignorés.

## 4. Ce que le système ne garantit pas

- Il ne comprend pas la demande : il reconnaît des mots. Toute formulation
  hors lexique est escaladée ou, plus rarement, mal orientée.
- Il ne garantit pas l'absence de fausse résolution en production.
- Il ne détecte ni les négations, ni l'ironie, ni les demandes multiples.
- Il ne garantit pas l'anonymat complet des textes de la file « à revoir ».
- Il ne remplace pas la gouvernance de la base de connaissances : qui valide
  une solution avant qu'elle soit servie reste une question humaine.

## 5. Signaux à surveiller en exploitation

- Hausse de la part de décisions `Inconnu` (vocabulaire qui dérive).
- File « à revoir » qui grossit sans être traitée.
- Diagnostic hebdomadaire avec des constats P3 récurrents sur une même classe.
