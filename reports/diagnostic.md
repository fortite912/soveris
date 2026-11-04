# Auto-diagnostic Soveris

_Genere le 2026-11-04T13:23:54_ — verdict : **OK** (code 0)

## Tests

| Suite | Statut | Duree |
|---|---|---|
| unittest (tests/) | OK | 1.61 s |
| tests.py (historique) | OK | 0.11 s |

## Evaluation

| Jeu | Cas | Precision | Erreurs critiques | Mal orientees | Incertains | Baseline precision |
|---|---|---|---|---|---|---|
| test | 50 | 96.0 % | 1 | 0 | 17 | 96.0 % |
| dev | 83 | 98.8 % | 0 | 1 | 24 | 98.8 % |
| synthetique | 204 | 100.0 % | 0 | 0 | 48 | 100.0 % |

## Constats priorises

- **P3-qualite** — [test] 1 erreur(s) critique(s) presente(s)
  - T-048 « comment changer ma photo sur l intranet » -> RESOLUTION_AUTO / Web / Intranet
- **P4-information** — [test] 17/50 decision(s) a faible confiance
  - T-006 « outlook plante au demarrage » -> RESOLUTION_AUTO / Messagerie
  - T-010 « tout rame quand j ouvre plusieurs fenetres » -> RESOLUTION_AUTO / Performance
  - T-017 « mon casque n est pas detecte en visio » -> RESOLUTION_AUTO / Materiel
  - T-018 « teams ne veut pas partager mon ecran » -> RESOLUTION_AUTO / Materiel
  - T-032 « mon ordi est mort » -> ESCALADE / Inconnu
  - T-034 « un mail bizarre me demande mes identifiants » -> ESCALADE / Securite
  - T-035 « on m a vole mon ordinateur portable dans le train » -> ESCALADE / Securite
  - T-039 « j ai efface un dossier partage par erreur » -> ESCALADE / Donnees
  - T-040 « fichier client corrompu impossible a ouvrir » -> ESCALADE / Donnees
  - T-042 « le serveur de fichiers est indisponible » -> ESCALADE / Infrastructure
- **P4-information** — [dev] 1 escalade(s) critique(s) mal orientee(s)
  - D-057 « quelqu un a utilise mon compte pendant mes vacances » -> Inconnu
- **P4-information** — [dev] 24/83 decision(s) a faible confiance
  - D-004 « le vpn se coupe des que je lance une visio en teletravail » -> RESOLUTION_AUTO / Reseau
  - D-007 « la connexion est tres instable en salle 204 » -> RESOLUTION_AUTO / Reseau
  - D-011 « le mot de passe de ma messagerie a expire » -> RESOLUTION_AUTO / Compte / Acces
  - D-013 « le lecteur reseau P n apparait plus dans mon explorateur » -> RESOLUTION_AUTO / Reseau
  - D-028 « le clavier de mon portable a des touches qui ne repondent pas » -> RESOLUTION_AUTO / Materiel
  - D-033 « excel se fige des que j ouvre un gros fichier » -> RESOLUTION_AUTO / Performance
  - D-051 « le portail rh ne s ouvre pas dans firefox » -> RESOLUTION_AUTO / Logiciel
  - D-056 « j ai clique sur un lien dans un mail bizarre et maintenant tout est chiffre » -> ESCALADE / Securite
  - D-057 « quelqu un a utilise mon compte pendant mes vacances » -> ESCALADE / Inconnu
  - D-059 « un collegue a recu un sms qui demande mes identifiants » -> ESCALADE / Securite
- **P4-information** — [synthetique] 48/204 decision(s) a faible confiance
  - S-037 « hello outlook ne s ouvre plus » -> RESOLUTION_AUTO / Messagerie
  - S-038 « depuis ce matin outlook ne s ouvre plus c est bloquant » -> RESOLUTION_AUTO / Messagerie
  - S-039 « bonjour, outlook ne s ouvre plus au 2e etage » -> RESOLUTION_AUTO / Messagerie
  - S-040 « bonjour, outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie
  - S-041 « urgent : outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie
  - S-042 « outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie
  - S-133 « depuis ce matin j ai recu un mail de phishing » -> ESCALADE / Securite
  - S-134 « bonjour, j ai recu un mail de phishing !!! » -> ESCALADE / Securite
  - S-135 « re-bonjour, j ai recu un mail de phishing depuis hier » -> ESCALADE / Securite
  - S-136 « re-bonjour, j ai recu un mail de phishing c est bloquant » -> ESCALADE / Securite
- **P4-information** — File « a revoir » : 0 cas en attente, 0 corrige(s) non integre(s)
