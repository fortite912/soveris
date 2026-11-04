# Auto-diagnostic Soveris

_Genere le 2026-11-04T13:20:23_ — verdict : **OK** (code 0)

## Evaluation

| Jeu | Cas | Precision | Erreurs critiques | Mal orientees | Incertains | Baseline precision |
|---|---|---|---|---|---|---|
| test | 50 | 92.0 % | 1 | 0 | 37 | 92.0 % |
| dev | 83 | 81.9 % | 6 | 3 | 51 | 81.9 % |
| synthetique | 204 | 100.0 % | 0 | 0 | 150 | 100.0 % |

## Constats priorises

- **P3-qualite** — [test] 1 erreur(s) critique(s) presente(s)
  - T-048 « comment changer ma photo sur l intranet » -> RESOLUTION_AUTO / Web / Intranet
- **P3-qualite** — [dev] 6 erreur(s) critique(s) presente(s)
  - D-062 « on m a piratee, mes contacts recoivent des mails de moi » -> RESOLUTION_AUTO / Messagerie
  - D-063 « un faux site de la banque me demande mon mot de passe » -> RESOLUTION_AUTO / Compte / Acces
  - D-071 « tous mes documents ont disparu du lecteur partage » -> RESOLUTION_AUTO / Compte / Acces
  - D-073 « mon disque dur fait un bruit bizarre et des fichiers sont illisibles » -> RESOLUTION_AUTO / Compte / Acces
  - D-076 « mon badge ne passe plus a l entree » -> RESOLUTION_AUTO / Compte / Acces
  - D-077 « je souhaite poser un jour de teletravail » -> RESOLUTION_AUTO / Reseau
- **P4-information** — [test] 37/50 decision(s) a faible confiance
  - T-001 « le wifi coupe sans arret dans la salle de reunion » -> RESOLUTION_AUTO / Reseau
  - T-004 « compte bloque apres plusieurs essais » -> RESOLUTION_AUTO / Compte / Acces
  - T-005 « je ne recois plus mes emails depuis hier » -> ESCALADE / Inconnu
  - T-006 « outlook plante au demarrage » -> RESOLUTION_AUTO / Messagerie
  - T-009 « mon pc est super lent depuis la mise a jour » -> RESOLUTION_AUTO / Performance
  - T-010 « tout rame quand j ouvre plusieurs fenetres » -> ESCALADE / Infrastructure
  - T-011 « le vpn refuse de se connecter depuis chez moi » -> RESOLUTION_AUTO / Reseau
  - T-014 « ma souris ne repond plus » -> RESOLUTION_AUTO / Materiel
  - T-015 « ecran noir au demarrage du poste » -> RESOLUTION_AUTO / Materiel
  - T-016 « le clavier tape des caracteres bizarres » -> RESOLUTION_AUTO / Materiel
- **P4-information** — [dev] 3 escalade(s) critique(s) mal orientee(s)
  - D-056 « j ai clique sur un lien dans un mail bizarre et maintenant tout est chiffre » -> Infrastructure
  - D-057 « quelqu un a utilise mon compte pendant mes vacances » -> Inconnu
  - D-058 « l antivirus a trouve un cheval de troie » -> Inconnu
- **P4-information** — [dev] 51/83 decision(s) a faible confiance
  - D-001 « bonjour le wifi de mon bureau ne fonctionne plus depuis ce matin » -> RESOLUTION_AUTO / Reseau
  - D-007 « la connexion est tres instable en salle 204 » -> RESOLUTION_AUTO / Reseau
  - D-009 « mon compte est verrouille apres 3 tentatives » -> RESOLUTION_AUTO / Compte / Acces
  - D-013 « le lecteur reseau P n apparait plus dans mon explorateur » -> RESOLUTION_AUTO / Reseau
  - D-015 « pouvez vous reinitialiser mon mdp svp » -> ESCALADE / Inconnu
  - D-016 « outlook ne se synchronise plus » -> RESOLUTION_AUTO / Messagerie
  - D-018 « mes courriels arrivent avec plusieurs heures de retard » -> ESCALADE / Inconnu
  - D-021 « je ne recois plus les emails de mes collegues » -> ESCALADE / Inconnu
  - D-024 « impossible d imprimer depuis mon poste, le document reste en attente » -> RESOLUTION_AUTO / Materiel
  - D-025 « le scanner ne numerise plus en recto verso » -> RESOLUTION_AUTO / Materiel
- **P4-information** — [synthetique] 150/204 decision(s) a faible confiance
  - S-001 « svp le wifi ne marche plus merci » -> RESOLUTION_AUTO / Reseau
  - S-002 « bonjour, le wifi ne marche plus » -> RESOLUTION_AUTO / Reseau
  - S-003 « le wifi ne marche plus !!! » -> RESOLUTION_AUTO / Reseau
  - S-004 « depuis ce matin le wifi ne marche plus c est bloquant » -> RESOLUTION_AUTO / Reseau
  - S-005 « depuis ce matin le wifi ne marche plus !!! » -> RESOLUTION_AUTO / Reseau
  - S-006 « depuis ce matin le wifi ne marche plus » -> RESOLUTION_AUTO / Reseau
  - S-007 « bonjour, plus d internet !!! » -> RESOLUTION_AUTO / Reseau
  - S-008 « urgent : plus d internet merci » -> RESOLUTION_AUTO / Reseau
  - S-009 « plus d internet pouvez vous m aider » -> RESOLUTION_AUTO / Reseau
  - S-010 « urgent : plus d internet !!! » -> RESOLUTION_AUTO / Reseau
- **P4-information** — File « a revoir » : 0 cas en attente, 0 corrige(s) non integre(s)
