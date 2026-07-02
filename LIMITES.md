# Limites connues & chemin d'industrialisation

> Soveris est un **prototype validé** (92 % de décisions correctes sur banc de
> validation, zéro fausse résolution dangereuse), **pas un produit industriel**.
> Ce document liste sans complaisance ce qui sépare ce POC d'un déploiement
> réel en DSI. Ces limites sont connues, documentées et assumées.

## 1. Moteur de décision
- Le matching est **lexical** (mots-clés + frontières de mots), pas sémantique :
  il ne « comprend » pas la demande, il la reconnaît.
- Pluriels, synonymes et langage familier partiellement couverts — exemples
  réels relevés par le banc de validation : « je ne reçois plus mes *emails* »
  (pluriel non apparié), « mon *ordi* est mort » (vocabulaire familier).
  Comportement en cas d'échec : **escalade conservatrice** (jamais de réponse
  devinée) — c'est un choix de conception.
- Améliorations identifiées : normalisation morphologique, dictionnaire de
  synonymes, pondération des mots-clés ; à terme, couche NLP **locale**
  optionnelle (sans introduire de dépendance dans le cœur).

## 2. Base de connaissances
- 15 articles rédigés à la main. Un déploiement réel en demanderait des
  **centaines**, avec un outil d'édition pour les techniciens et une
  gouvernance (qui valide une solution avant qu'elle soit servie ?).
- Pas encore d'apprentissage depuis les tickets résolus (boucle
  d'enrichissement manuelle).

## 3. Intégration au système d'information
- **Aucun connecteur** vers les outils réels (GLPI, ServiceNow, messagerie,
  Teams) : aujourd'hui, la demande est saisie manuellement. C'est le chantier
  le plus lourd avant tout pilote.
- Point souvent mal compris : l'architecture 100 % locale est un **atout**
  face aux politiques de sécurité — aucun flux sortant à faire ouvrir sur le
  pare-feu. Le vrai coût d'intégration est ailleurs : compte de service et
  droits sur l'API du ticketing interne, validation du logiciel par l'équipe
  sécurité (revue de code, environnement de test), et maintenance dans le
  temps.

## 4. Sécurité & conformité
- L'interface web de démonstration est en HTTP local, **sans
  authentification** — choix assumé pour un usage mono-poste sur 127.0.0.1,
  insuffisant en entreprise (il faudrait : comptes, TLS, journal d'audit,
  gestion des secrets, durcissement).
- Aucune donnée réelle n'a jamais été traitée (validation exclusivement sur
  tickets synthétiques). Tout traitement de données réelles exigerait une mise
  en conformité RGPD formalisée (registre de traitement, durées de rétention).

## 5. Données & persistance
- SQLite mono-fichier : parfait pour le POC, inadapté à la volumétrie et à la
  concurrence d'une DSI. La couche de persistance est isolée : migration
  PostgreSQL prévue le jour où un pilote le justifie.

## 6. Déploiement & exploitation
- Pas d'installeur ni d'image (Dockerfile en feuille de route), pas de
  mécanisme de mise à jour, pas de supervision de l'agent lui-même.

## 7. Portée des mesures
- **70 %** = jeu de démonstration (10 tickets) ; **92 %** = banc de validation
  interne (50 tickets variés). Le taux réel en production est **inconnu** tant
  qu'aucun pilote encadré n'a tourné — et il n'est jamais présenté autrement.

---

**Position du porteur.** Ce projet est mené dans le cadre du Statut National
Étudiant-Entrepreneur, en parallèle d'une formation initiale qui reste
prioritaire. L'industrialisation (connecteurs, sécurité, exploitation) ne
serait engagée qu'avec un cadre adapté : pilote borné, accompagnement du
réseau Pépite, et montée en compétences préalable. Documenter ces limites
fait partie de la méthode : un chiffre n'a de valeur que si l'on sait
exactement ce qu'il mesure.
