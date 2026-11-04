# Evaluation — jeu `test`

_Genere le 2026-11-04T13:17:55_

| Indicateur | Valeur |
|---|---|
| Cas | 50 |
| Decisions correctes | 46 (92.0 %) |
| Erreurs critiques (fausse resolution) | 1 |
| Escalades critiques mal orientees | 0 |
| Decisions incertaines | 37 |
| Latence mediane / p95 / max (ms) | 0.296 / 0.396 / 2.283 |

## Verdicts

| Verdict | Nombre |
|---|---|
| CORRECT | 46 |
| FAUSSE_HORS_PERIMETRE | 1 |
| MANQUE | 3 |

## Precision par classe attendue

| Classe | Cas | Corrects | Precision |
|---|---|---|---|
| Collaboration | 2 | 2 | 100.0 % |
| Compte / Acces | 5 | 5 | 100.0 % |
| Donnees | 2 | 2 | 100.0 % |
| Inconnu | 8 | 7 | 87.5 % |
| Infrastructure | 3 | 3 | 100.0 % |
| Logiciel | 3 | 3 | 100.0 % |
| Materiel | 7 | 6 | 85.7 % |
| Messagerie | 3 | 2 | 66.7 % |
| Performance | 2 | 1 | 50.0 % |
| Reseau | 4 | 4 | 100.0 % |
| Securite | 5 | 5 | 100.0 % |
| Telephonie | 3 | 3 | 100.0 % |
| Web / Intranet | 3 | 3 | 100.0 % |

## Matrice de confusion (attendu en ligne, predit en colonne)

| attendu \ predit | Collaboration | Compte / Acces | Donnees | Inconnu | Infrastructure | Logiciel | Materiel | Messagerie | Performance | Reseau | Securite | Telephonie | Web / Intranet |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Collaboration | 1 |  |  |  |  |  | 1 |  |  |  |  |  |  |
| Compte / Acces |  | 5 |  |  |  |  |  |  |  |  |  |  |  |
| Donnees |  |  | 2 |  |  |  |  |  |  |  |  |  |  |
| Inconnu |  |  |  | 7 |  |  |  |  |  |  |  |  | 1 |
| Infrastructure |  |  |  |  | 3 |  |  |  |  |  |  |  |  |
| Logiciel |  |  |  |  |  | 3 |  |  |  |  |  |  |  |
| Materiel |  |  |  | 1 |  |  | 6 |  |  |  |  |  |  |
| Messagerie |  |  |  | 1 |  |  |  | 2 |  |  |  |  |  |
| Performance |  |  |  |  | 1 |  |  |  | 1 |  |  |  |  |
| Reseau |  |  |  |  |  |  |  |  |  | 4 |  |  |  |
| Securite |  |  |  |  |  |  |  |  |  |  | 5 |  |  |
| Telephonie |  |  |  |  |  |  |  |  |  |  |  | 3 |  |
| Web / Intranet |  |  |  |  |  |  |  |  |  |  |  |  | 3 |

## Erreurs

| Id | Texte | Attendu | Obtenu | Verdict |
|---|---|---|---|---|
| T-005 | je ne recois plus mes emails depuis hier | RESOLUTION_AUTO / Messagerie | ESCALADE / Inconnu | MANQUE |
| T-010 | tout rame quand j ouvre plusieurs fenetres | RESOLUTION_AUTO / Performance | ESCALADE / Infrastructure | MANQUE |
| T-032 | mon ordi est mort | RESOLUTION_AUTO / Materiel, Performance | ESCALADE / Inconnu | MANQUE |
| T-048 | comment changer ma photo sur l intranet | ESCALADE / Inconnu | RESOLUTION_AUTO / Web / Intranet | FAUSSE_HORS_PERIMETRE |

## Decisions incertaines (a revoir)

- T-001 « le wifi coupe sans arret dans la salle de reunion » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- T-004 « compte bloque apres plusieurs essais » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- T-005 « je ne recois plus mes emails depuis hier » -> ESCALADE / Inconnu (score 0, MANQUE)
- T-006 « outlook plante au demarrage » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- T-009 « mon pc est super lent depuis la mise a jour » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- T-010 « tout rame quand j ouvre plusieurs fenetres » -> ESCALADE / Infrastructure (score 1, MANQUE)
- T-011 « le vpn refuse de se connecter depuis chez moi » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- T-014 « ma souris ne repond plus » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- T-015 « ecran noir au demarrage du poste » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- T-016 « le clavier tape des caracteres bizarres » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- T-017 « mon casque n est pas detecte en visio » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- T-018 « teams ne veut pas partager mon ecran » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- T-020 « impossible d ouvrir l application de compta » -> RESOLUTION_AUTO / Logiciel (score 1, CORRECT)
- T-023 « chrome ne charge aucune page » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- T-024 « l intranet est inaccessible depuis mon poste » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- T-025 « le site de l entreprise ne s affiche pas » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- T-026 « mon telephone pro ne recoit plus d appels » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- T-027 « la carte sim n est pas reconnue » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- T-028 « le portable de service ne s allume plus » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- T-031 « session windows verrouillee impossible de rentrer » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- T-032 « mon ordi est mort » -> ESCALADE / Inconnu (score 0, MANQUE)
- T-033 « je crois que j ai un virus sur mon poste » -> ESCALADE / Securite (score 1, CORRECT)
- T-034 « un mail bizarre me demande mes identifiants » -> ESCALADE / Securite (score 1, CORRECT)
- T-035 « on m a vole mon ordinateur portable dans le train » -> ESCALADE / Securite (score 1, CORRECT)
- T-036 « ransomware detecte par l antivirus » -> ESCALADE / Securite (score 1, CORRECT)
- T-038 « la prod est tombee tout le monde est bloque » -> ESCALADE / Infrastructure (score 1, CORRECT)
- T-039 « j ai efface un dossier partage par erreur » -> ESCALADE / Donnees (score 2, CORRECT)
- T-040 « fichier client corrompu impossible a ouvrir » -> ESCALADE / Donnees (score 1, CORRECT)
- T-041 « je pense que mon compte a ete pirate » -> ESCALADE / Securite (score 1, CORRECT)
- T-043 « ou se trouve la machine a cafe » -> ESCALADE / Inconnu (score 0, CORRECT)
- T-044 « je veux poser mes conges la semaine prochaine » -> ESCALADE / Inconnu (score 0, CORRECT)
- T-045 « le badge de la porte ne fonctionne plus » -> ESCALADE / Inconnu (score 0, CORRECT)
- T-046 « quelle est la date de la prochaine reunion d equipe » -> ESCALADE / Inconnu (score 0, CORRECT)
- T-047 « ma chaise de bureau est cassee » -> ESCALADE / Inconnu (score 0, CORRECT)
- T-048 « comment changer ma photo sur l intranet » -> RESOLUTION_AUTO / Web / Intranet (score 1, FAUSSE_HORS_PERIMETRE)
- T-049 « il fait trop chaud dans l open space » -> ESCALADE / Inconnu (score 0, CORRECT)
- T-050 « besoin d une formation sur excel » -> ESCALADE / Inconnu (score 0, CORRECT)
