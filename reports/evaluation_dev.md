# Evaluation — jeu `dev`

_Genere le 2026-11-04T13:17:55_

| Indicateur | Valeur |
|---|---|
| Cas | 83 |
| Decisions correctes | 68 (81.9 %) |
| Erreurs critiques (fausse resolution) | 6 |
| Escalades critiques mal orientees | 3 |
| Decisions incertaines | 51 |
| Latence mediane / p95 / max (ms) | 0.313 / 0.402 / 0.625 |

## Verdicts

| Verdict | Nombre |
|---|---|
| CORRECT | 68 |
| FAUSSE_DANGEREUSE | 4 |
| FAUSSE_HORS_PERIMETRE | 2 |
| MAL_CATEGORISE | 2 |
| MANQUE | 7 |

## Precision par classe attendue

| Classe | Cas | Corrects | Precision |
|---|---|---|---|
| Collaboration | 5 | 3 | 60.0 % |
| Compte / Acces | 8 | 7 | 87.5 % |
| Donnees | 5 | 3 | 60.0 % |
| Inconnu | 10 | 8 | 80.0 % |
| Infrastructure | 5 | 5 | 100.0 % |
| Logiciel | 6 | 5 | 83.3 % |
| Materiel | 10 | 9 | 90.0 % |
| Messagerie | 6 | 4 | 66.7 % |
| Performance | 5 | 4 | 80.0 % |
| Reseau | 7 | 7 | 100.0 % |
| Securite | 8 | 6 | 75.0 % |
| Telephonie | 4 | 4 | 100.0 % |
| Web / Intranet | 4 | 3 | 75.0 % |

## Matrice de confusion (attendu en ligne, predit en colonne)

| attendu \ predit | Collaboration | Compte / Acces | Donnees | Inconnu | Infrastructure | Logiciel | Materiel | Messagerie | Performance | Reseau | Securite | Telephonie | Web / Intranet |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Collaboration | 3 | 1 |  |  | 1 |  |  |  |  |  |  |  |  |
| Compte / Acces |  | 6 |  | 1 |  |  |  |  |  | 1 |  |  |  |
| Donnees |  | 2 | 3 |  |  |  |  |  |  |  |  |  |  |
| Inconnu |  | 1 |  | 7 | 1 |  |  |  |  | 1 |  |  |  |
| Infrastructure |  |  |  |  | 5 |  |  |  |  |  |  |  |  |
| Logiciel |  |  |  | 1 |  | 5 |  |  |  |  |  |  |  |
| Materiel |  |  |  | 1 |  |  | 9 |  |  |  |  |  |  |
| Messagerie |  |  |  | 2 |  |  |  | 4 |  |  |  |  |  |
| Performance |  |  |  |  | 1 |  |  |  | 4 |  |  |  |  |
| Reseau |  |  |  |  |  |  |  |  |  | 7 |  |  |  |
| Securite |  | 1 |  | 2 | 1 |  |  | 1 |  |  | 3 |  |  |
| Telephonie |  |  |  |  |  |  |  |  |  |  |  | 4 |  |
| Web / Intranet |  |  |  |  |  | 1 |  |  |  |  |  |  | 3 |

## Erreurs

| Id | Texte | Attendu | Obtenu | Verdict |
|---|---|---|---|---|
| D-015 | pouvez vous reinitialiser mon mdp svp | RESOLUTION_AUTO / Compte / Acces | ESCALADE / Inconnu | MANQUE |
| D-018 | mes courriels arrivent avec plusieurs heures de retard | RESOLUTION_AUTO / Messagerie | ESCALADE / Inconnu | MANQUE |
| D-021 | je ne recois plus les emails de mes collegues | RESOLUTION_AUTO / Messagerie | ESCALADE / Inconnu | MANQUE |
| D-031 | les imprimantes du 3e ne repondent plus | RESOLUTION_AUTO / Materiel | ESCALADE / Inconnu | MANQUE |
| D-035 | tout est lent sur mon pc aujourd hui | RESOLUTION_AUTO / Performance | ESCALADE / Infrastructure | MANQUE |
| D-042 | les applis se ferment toutes seules | RESOLUTION_AUTO / Logiciel | ESCALADE / Inconnu | MANQUE |
| D-044 | personne ne m entend en visio | RESOLUTION_AUTO / Collaboration | ESCALADE / Infrastructure | MANQUE |
| D-045 | le partage d ecran ne fonctionne pas sur zoom | RESOLUTION_AUTO / Collaboration | RESOLUTION_AUTO / Compte / Acces | MAL_CATEGORISE |
| D-051 | le portail rh ne s ouvre pas dans firefox | RESOLUTION_AUTO / Web / Intranet | RESOLUTION_AUTO / Logiciel | MAL_CATEGORISE |
| D-062 | on m a piratee, mes contacts recoivent des mails de moi | ESCALADE / Securite | RESOLUTION_AUTO / Messagerie | FAUSSE_DANGEREUSE |
| D-063 | un faux site de la banque me demande mon mot de passe | ESCALADE / Securite | RESOLUTION_AUTO / Compte / Acces | FAUSSE_DANGEREUSE |
| D-071 | tous mes documents ont disparu du lecteur partage | ESCALADE / Donnees | RESOLUTION_AUTO / Compte / Acces | FAUSSE_DANGEREUSE |
| D-073 | mon disque dur fait un bruit bizarre et des fichiers sont illisibles | ESCALADE / Donnees, Materiel | RESOLUTION_AUTO / Compte / Acces | FAUSSE_DANGEREUSE |
| D-076 | mon badge ne passe plus a l entree | ESCALADE / Inconnu | RESOLUTION_AUTO / Compte / Acces | FAUSSE_HORS_PERIMETRE |
| D-077 | je souhaite poser un jour de teletravail | ESCALADE / Inconnu | RESOLUTION_AUTO / Reseau | FAUSSE_HORS_PERIMETRE |

## Escalades critiques mal orientees

- D-056 « j ai clique sur un lien dans un mail bizarre et maintenant tout est chiffre » : attendu Securite, obtenu Infrastructure
- D-057 « quelqu un a utilise mon compte pendant mes vacances » : attendu Securite, obtenu Inconnu
- D-058 « l antivirus a trouve un cheval de troie » : attendu Securite, obtenu Inconnu

## Decisions incertaines (a revoir)

- D-001 « bonjour le wifi de mon bureau ne fonctionne plus depuis ce matin » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- D-007 « la connexion est tres instable en salle 204 » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- D-009 « mon compte est verrouille apres 3 tentatives » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- D-013 « le lecteur reseau P n apparait plus dans mon explorateur » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- D-015 « pouvez vous reinitialiser mon mdp svp » -> ESCALADE / Inconnu (score 0, MANQUE)
- D-016 « outlook ne se synchronise plus » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- D-018 « mes courriels arrivent avec plusieurs heures de retard » -> ESCALADE / Inconnu (score 0, MANQUE)
- D-021 « je ne recois plus les emails de mes collegues » -> ESCALADE / Inconnu (score 0, MANQUE)
- D-024 « impossible d imprimer depuis mon poste, le document reste en attente » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-025 « le scanner ne numerise plus en recto verso » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-026 « mon deuxieme ecran reste noir » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-027 « ma souris sans fil ne reagit plus » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-028 « le clavier de mon portable a des touches qui ne repondent pas » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-029 « la webcam n est pas detectee » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-030 « ma cle usb n est pas reconnue » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- D-031 « les imprimantes du 3e ne repondent plus » -> ESCALADE / Inconnu (score 0, MANQUE)
- D-032 « mon ordinateur est devenu tres lent » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- D-033 « excel se fige des que j ouvre un gros fichier » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- D-034 « mon poste rame enormement depuis la derniere mise a jour » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- D-035 « tout est lent sur mon pc aujourd hui » -> ESCALADE / Infrastructure (score 1, MANQUE)
- D-036 « le ventilateur tourne a fond et le pc est lent » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- D-037 « word plante a chaque ouverture » -> RESOLUTION_AUTO / Logiciel (score 1, CORRECT)
- D-041 « message d erreur au lancement d acrobat » -> RESOLUTION_AUTO / Logiciel (score 1, CORRECT)
- D-042 « les applis se ferment toutes seules » -> ESCALADE / Inconnu (score 0, MANQUE)
- D-044 « personne ne m entend en visio » -> ESCALADE / Infrastructure (score 1, MANQUE)
- D-045 « le partage d ecran ne fonctionne pas sur zoom » -> RESOLUTION_AUTO / Compte / Acces (score 1, MAL_CATEGORISE)
- D-047 « je n arrive pas a rejoindre la reunion en ligne » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- D-048 « l intranet ne charge pas » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- D-049 « chrome affiche une page blanche sur tous les sites » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- D-051 « le portail rh ne s ouvre pas dans firefox » -> RESOLUTION_AUTO / Logiciel (score 1, MAL_CATEGORISE)
- D-052 « mon telephone fixe n a plus de tonalite » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- D-053 « le softphone ne sonne plus » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- D-054 « je ne peux plus passer d appels depuis mon mobile pro » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- D-056 « j ai clique sur un lien dans un mail bizarre et maintenant tout est chiffre » -> ESCALADE / Infrastructure (score 1, CORRECT)
- D-057 « quelqu un a utilise mon compte pendant mes vacances » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-058 « l antivirus a trouve un cheval de troie » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-059 « un collegue a recu un sms qui demande mes identifiants » -> ESCALADE / Securite (score 1, CORRECT)
- D-060 « mon ordinateur portable a ete vole ce week end » -> ESCALADE / Securite (score 1, CORRECT)
- D-061 « je recois des mails d arnaque au president » -> ESCALADE / Securite (score 1, CORRECT)
- D-062 « on m a piratee, mes contacts recoivent des mails de moi » -> RESOLUTION_AUTO / Messagerie (score 1, FAUSSE_DANGEREUSE)
- D-073 « mon disque dur fait un bruit bizarre et des fichiers sont illisibles » -> RESOLUTION_AUTO / Compte / Acces (score 1, FAUSSE_DANGEREUSE)
- D-074 « je voudrais commander une nouvelle chaise » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-075 « a quelle heure ferme le parking » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-076 « mon badge ne passe plus a l entree » -> RESOLUTION_AUTO / Compte / Acces (score 1, FAUSSE_HORS_PERIMETRE)
- D-077 « je souhaite poser un jour de teletravail » -> RESOLUTION_AUTO / Reseau (score 1, FAUSSE_HORS_PERIMETRE)
- D-078 « il n y a plus de gobelets a la machine a cafe » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-079 « comment faire une note de frais » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-080 « je voudrais une formation powerpoint » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-081 « la climatisation est en panne au 2e etage » -> ESCALADE / Infrastructure (score 1, CORRECT)
- D-082 « quel est le numero de la medecine du travail » -> ESCALADE / Inconnu (score 0, CORRECT)
- D-083 « pouvez vous changer la photo de mon profil sur l annuaire » -> ESCALADE / Inconnu (score 0, CORRECT)
