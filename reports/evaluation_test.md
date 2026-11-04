# Evaluation — jeu `test`

_Genere le 2026-11-04T13:23:54_

| Indicateur | Valeur |
|---|---|
| Cas | 50 |
| Decisions correctes | 48 (96.0 %) |
| Erreurs critiques (fausse resolution) | 1 |
| Escalades critiques mal orientees | 0 |
| Decisions incertaines | 17 |
| Latence mediane / p95 / max (ms) | 0.608 / 0.721 / 6.172 |

## Verdicts

| Verdict | Nombre |
|---|---|
| CORRECT | 48 |
| FAUSSE_HORS_PERIMETRE | 1 |
| MANQUE | 1 |

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
| Messagerie | 3 | 3 | 100.0 % |
| Performance | 2 | 2 | 100.0 % |
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
| Messagerie |  |  |  |  |  |  |  | 3 |  |  |  |  |  |
| Performance |  |  |  |  |  |  |  |  | 2 |  |  |  |  |
| Reseau |  |  |  |  |  |  |  |  |  | 4 |  |  |  |
| Securite |  |  |  |  |  |  |  |  |  |  | 5 |  |  |
| Telephonie |  |  |  |  |  |  |  |  |  |  |  | 3 |  |
| Web / Intranet |  |  |  |  |  |  |  |  |  |  |  |  | 3 |

## Erreurs

| Id | Texte | Attendu | Obtenu | Verdict |
|---|---|---|---|---|
| T-032 | mon ordi est mort | RESOLUTION_AUTO / Materiel, Performance | ESCALADE / Inconnu | MANQUE |
| T-048 | comment changer ma photo sur l intranet | ESCALADE / Inconnu | RESOLUTION_AUTO / Web / Intranet | FAUSSE_HORS_PERIMETRE |

## Decisions incertaines (a revoir)

- T-006 « outlook plante au demarrage » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- T-010 « tout rame quand j ouvre plusieurs fenetres » -> RESOLUTION_AUTO / Performance (score 1.0, CORRECT)
- T-017 « mon casque n est pas detecte en visio » -> RESOLUTION_AUTO / Materiel (score 1.0, CORRECT)
- T-018 « teams ne veut pas partager mon ecran » -> RESOLUTION_AUTO / Materiel (score 1.0, CORRECT)
- T-032 « mon ordi est mort » -> ESCALADE / Inconnu (score 0.0, MANQUE)
- T-034 « un mail bizarre me demande mes identifiants » -> ESCALADE / Securite (score 1.0, CORRECT)
- T-035 « on m a vole mon ordinateur portable dans le train » -> ESCALADE / Securite (score 1.0, CORRECT)
- T-039 « j ai efface un dossier partage par erreur » -> ESCALADE / Donnees (score 2.0, CORRECT)
- T-040 « fichier client corrompu impossible a ouvrir » -> ESCALADE / Donnees (score 1.0, CORRECT)
- T-042 « le serveur de fichiers est indisponible » -> ESCALADE / Infrastructure (score 2.0, CORRECT)
- T-043 « ou se trouve la machine a cafe » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- T-044 « je veux poser mes conges la semaine prochaine » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- T-045 « le badge de la porte ne fonctionne plus » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- T-046 « quelle est la date de la prochaine reunion d equipe » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- T-047 « ma chaise de bureau est cassee » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- T-049 « il fait trop chaud dans l open space » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- T-050 « besoin d une formation sur excel » -> ESCALADE / Inconnu (score 0.0, CORRECT)
