# Evaluation — jeu `dev`

_Genere le 2026-11-04T13:23:54_

| Indicateur | Valeur |
|---|---|
| Cas | 83 |
| Decisions correctes | 82 (98.8 %) |
| Erreurs critiques (fausse resolution) | 0 |
| Escalades critiques mal orientees | 1 |
| Decisions incertaines | 24 |
| Latence mediane / p95 / max (ms) | 0.591 / 0.717 / 0.943 |

## Verdicts

| Verdict | Nombre |
|---|---|
| CORRECT | 82 |
| MAL_CATEGORISE | 1 |

## Precision par classe attendue

| Classe | Cas | Corrects | Precision |
|---|---|---|---|
| Collaboration | 5 | 5 | 100.0 % |
| Compte / Acces | 8 | 8 | 100.0 % |
| Donnees | 5 | 5 | 100.0 % |
| Inconnu | 10 | 10 | 100.0 % |
| Infrastructure | 5 | 5 | 100.0 % |
| Logiciel | 6 | 6 | 100.0 % |
| Materiel | 10 | 10 | 100.0 % |
| Messagerie | 6 | 6 | 100.0 % |
| Performance | 5 | 5 | 100.0 % |
| Reseau | 7 | 7 | 100.0 % |
| Securite | 8 | 8 | 100.0 % |
| Telephonie | 4 | 4 | 100.0 % |
| Web / Intranet | 4 | 3 | 75.0 % |

## Matrice de confusion (attendu en ligne, predit en colonne)

| attendu \ predit | Collaboration | Compte / Acces | Donnees | Inconnu | Infrastructure | Logiciel | Materiel | Messagerie | Performance | Reseau | Securite | Telephonie | Web / Intranet |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Collaboration | 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| Compte / Acces |  | 7 |  |  |  |  |  |  |  | 1 |  |  |  |
| Donnees |  |  | 5 |  |  |  |  |  |  |  |  |  |  |
| Inconnu |  |  |  | 9 | 1 |  |  |  |  |  |  |  |  |
| Infrastructure |  |  |  |  | 5 |  |  |  |  |  |  |  |  |
| Logiciel |  |  |  |  |  | 6 |  |  |  |  |  |  |  |
| Materiel |  |  |  |  |  |  | 10 |  |  |  |  |  |  |
| Messagerie |  |  |  |  |  |  |  | 6 |  |  |  |  |  |
| Performance |  |  |  |  |  |  |  |  | 5 |  |  |  |  |
| Reseau |  |  |  |  |  |  |  |  |  | 7 |  |  |  |
| Securite |  |  |  | 1 |  |  |  |  |  |  | 7 |  |  |
| Telephonie |  |  |  |  |  |  |  |  |  |  |  | 4 |  |
| Web / Intranet |  |  |  |  |  | 1 |  |  |  |  |  |  | 3 |

## Erreurs

| Id | Texte | Attendu | Obtenu | Verdict |
|---|---|---|---|---|
| D-051 | le portail rh ne s ouvre pas dans firefox | RESOLUTION_AUTO / Web / Intranet | RESOLUTION_AUTO / Logiciel | MAL_CATEGORISE |

## Escalades critiques mal orientees

- D-057 « quelqu un a utilise mon compte pendant mes vacances » : attendu Securite, obtenu Inconnu

## Decisions incertaines (a revoir)

- D-004 « le vpn se coupe des que je lance une visio en teletravail » -> RESOLUTION_AUTO / Reseau (score 1.0, CORRECT)
- D-007 « la connexion est tres instable en salle 204 » -> RESOLUTION_AUTO / Reseau (score 1.0, CORRECT)
- D-011 « le mot de passe de ma messagerie a expire » -> RESOLUTION_AUTO / Compte / Acces (score 1.0, CORRECT)
- D-013 « le lecteur reseau P n apparait plus dans mon explorateur » -> RESOLUTION_AUTO / Reseau (score 1.0, CORRECT)
- D-028 « le clavier de mon portable a des touches qui ne repondent pas » -> RESOLUTION_AUTO / Materiel (score 1.0, CORRECT)
- D-033 « excel se fige des que j ouvre un gros fichier » -> RESOLUTION_AUTO / Performance (score 1.0, CORRECT)
- D-051 « le portail rh ne s ouvre pas dans firefox » -> RESOLUTION_AUTO / Logiciel (score 1.0, MAL_CATEGORISE)
- D-056 « j ai clique sur un lien dans un mail bizarre et maintenant tout est chiffre » -> ESCALADE / Securite (score 1.0, CORRECT)
- D-057 « quelqu un a utilise mon compte pendant mes vacances » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-059 « un collegue a recu un sms qui demande mes identifiants » -> ESCALADE / Securite (score 1.0, CORRECT)
- D-060 « mon ordinateur portable a ete vole ce week end » -> ESCALADE / Securite (score 1.0, CORRECT)
- D-061 « je recois des mails d arnaque au president » -> ESCALADE / Securite (score 1.0, CORRECT)
- D-062 « on m a piratee, mes contacts recoivent des mails de moi » -> ESCALADE / Securite (score 1.0, CORRECT)
- D-063 « un faux site de la banque me demande mon mot de passe » -> ESCALADE / Securite (score 1.0, CORRECT)
- D-073 « mon disque dur fait un bruit bizarre et des fichiers sont illisibles » -> ESCALADE / Donnees (score 1.0, CORRECT)
- D-074 « je voudrais commander une nouvelle chaise » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-075 « a quelle heure ferme le parking » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-076 « mon badge ne passe plus a l entree » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-077 « je souhaite poser un jour de teletravail » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-078 « il n y a plus de gobelets a la machine a cafe » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-079 « comment faire une note de frais » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-080 « je voudrais une formation powerpoint » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-082 « quel est le numero de la medecine du travail » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- D-083 « pouvez vous changer la photo de mon profil sur l annuaire » -> ESCALADE / Inconnu (score 0.0, CORRECT)
