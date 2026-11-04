# Evaluation — jeu `synthetique`

_Genere le 2026-11-04T13:17:55_

| Indicateur | Valeur |
|---|---|
| Cas | 204 |
| Decisions correctes | 204 (100.0 %) |
| Erreurs critiques (fausse resolution) | 0 |
| Escalades critiques mal orientees | 0 |
| Decisions incertaines | 150 |
| Latence mediane / p95 / max (ms) | 0.316 / 0.505 / 2.443 |

## Verdicts

| Verdict | Nombre |
|---|---|
| CORRECT | 204 |

## Precision par classe attendue

| Classe | Cas | Corrects | Precision |
|---|---|---|---|
| Collaboration | 12 | 12 | 100.0 % |
| Compte / Acces | 18 | 18 | 100.0 % |
| Donnees | 12 | 12 | 100.0 % |
| Inconnu | 24 | 24 | 100.0 % |
| Infrastructure | 12 | 12 | 100.0 % |
| Logiciel | 12 | 12 | 100.0 % |
| Materiel | 24 | 24 | 100.0 % |
| Messagerie | 12 | 12 | 100.0 % |
| Performance | 12 | 12 | 100.0 % |
| Reseau | 18 | 18 | 100.0 % |
| Securite | 24 | 24 | 100.0 % |
| Telephonie | 12 | 12 | 100.0 % |
| Web / Intranet | 12 | 12 | 100.0 % |

## Matrice de confusion (attendu en ligne, predit en colonne)

| attendu \ predit | Collaboration | Compte / Acces | Donnees | Inconnu | Infrastructure | Logiciel | Materiel | Messagerie | Performance | Reseau | Securite | Telephonie | Web / Intranet |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Collaboration | 12 |  |  |  |  |  |  |  |  |  |  |  |  |
| Compte / Acces |  | 18 |  |  |  |  |  |  |  |  |  |  |  |
| Donnees |  |  | 12 |  |  |  |  |  |  |  |  |  |  |
| Inconnu |  |  |  | 24 |  |  |  |  |  |  |  |  |  |
| Infrastructure |  |  |  |  | 12 |  |  |  |  |  |  |  |  |
| Logiciel |  |  |  |  |  | 12 |  |  |  |  |  |  |  |
| Materiel |  |  |  |  |  |  | 24 |  |  |  |  |  |  |
| Messagerie |  |  |  |  |  |  |  | 12 |  |  |  |  |  |
| Performance |  |  |  |  |  |  |  |  | 12 |  |  |  |  |
| Reseau |  |  |  |  |  |  |  |  |  | 18 |  |  |  |
| Securite |  |  |  |  |  |  |  |  |  |  | 24 |  |  |
| Telephonie |  |  |  |  |  |  |  |  |  |  |  | 12 |  |
| Web / Intranet |  |  |  |  |  |  |  |  |  |  |  |  | 12 |

## Decisions incertaines (a revoir)

- S-001 « svp le wifi ne marche plus merci » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-002 « bonjour, le wifi ne marche plus » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-003 « le wifi ne marche plus !!! » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-004 « depuis ce matin le wifi ne marche plus c est bloquant » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-005 « depuis ce matin le wifi ne marche plus !!! » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-006 « depuis ce matin le wifi ne marche plus » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-007 « bonjour, plus d internet !!! » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-008 « urgent : plus d internet merci » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-009 « plus d internet pouvez vous m aider » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-010 « urgent : plus d internet !!! » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-011 « re-bonjour, plus d internet pouvez vous m aider » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-012 « plus d internet merci » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-013 « svp le vpn ne se connecte pas au 2e etage » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-014 « hello le vpn ne se connecte pas pouvez vous m aider » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-015 « le vpn ne se connecte pas au 2e etage » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-016 « le vpn ne se connecte pas !!! » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-017 « le vpn ne se connecte pas merci » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-018 « bonjour, le vpn ne se connecte pas pouvez vous m aider » -> RESOLUTION_AUTO / Reseau (score 1, CORRECT)
- S-025 « urgent : mon compte est bloque c est bloquant » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- S-026 « svp mon compte est bloque pouvez vous m aider » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- S-027 « urgent : mon compte est bloque au 2e etage » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- S-028 « re-bonjour, mon compte est bloque pouvez vous m aider » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- S-029 « hello mon compte est bloque merci » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- S-030 « depuis ce matin mon compte est bloque » -> RESOLUTION_AUTO / Compte / Acces (score 1, CORRECT)
- S-037 « hello outlook ne s ouvre plus » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-038 « depuis ce matin outlook ne s ouvre plus c est bloquant » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-039 « bonjour, outlook ne s ouvre plus au 2e etage » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-040 « bonjour, outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-041 « urgent : outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-042 « outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-043 « je ne recois plus mes mails merci » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-044 « hello je ne recois plus mes mails c est bloquant » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-045 « je ne recois plus mes mails pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-046 « hello je ne recois plus mes mails !!! » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-047 « urgent : je ne recois plus mes mails c est bloquant » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-048 « svp je ne recois plus mes mails c est bloquant » -> RESOLUTION_AUTO / Messagerie (score 1, CORRECT)
- S-049 « depuis ce matin l imprimante ne fonctionne pas au 2e etage » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-050 « l imprimante ne fonctionne pas au 2e etage » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-051 « urgent : l imprimante ne fonctionne pas depuis hier » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-052 « re-bonjour, l imprimante ne fonctionne pas !!! » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-053 « re-bonjour, l imprimante ne fonctionne pas pouvez vous m aider » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-054 « bonjour, l imprimante ne fonctionne pas » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-061 « hello mon ecran reste noir au 2e etage » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-062 « svp mon ecran reste noir !!! » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-063 « bonjour, mon ecran reste noir merci » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-064 « urgent : mon ecran reste noir c est bloquant » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-065 « mon ecran reste noir depuis hier » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-066 « mon ecran reste noir au 2e etage » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-067 « urgent : ma souris ne marche plus » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-068 « depuis ce matin ma souris ne marche plus » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-069 « depuis ce matin ma souris ne marche plus depuis hier » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-070 « ma souris ne marche plus merci » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-071 « urgent : ma souris ne marche plus merci » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-072 « ma souris ne marche plus pouvez vous m aider » -> RESOLUTION_AUTO / Materiel (score 1, CORRECT)
- S-073 « hello mon ordinateur est lent c est bloquant » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-074 « depuis ce matin mon ordinateur est lent c est bloquant » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-075 « re-bonjour, mon ordinateur est lent !!! » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-076 « svp mon ordinateur est lent merci » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-077 « hello mon ordinateur est lent au 2e etage » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-078 « bonjour, mon ordinateur est lent c est bloquant » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-079 « hello le poste rame au 2e etage » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-080 « hello le poste rame !!! » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-081 « bonjour, le poste rame pouvez vous m aider » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-082 « urgent : le poste rame » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-083 « depuis ce matin le poste rame c est bloquant » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-084 « urgent : le poste rame !!! » -> RESOLUTION_AUTO / Performance (score 1, CORRECT)
- S-097 « svp teams ne marche pas merci » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- S-098 « urgent : teams ne marche pas au 2e etage » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- S-099 « svp teams ne marche pas » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- S-100 « depuis ce matin teams ne marche pas » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- S-101 « urgent : teams ne marche pas !!! » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- S-102 « depuis ce matin teams ne marche pas pouvez vous m aider » -> RESOLUTION_AUTO / Collaboration (score 1, CORRECT)
- S-109 « l intranet ne s affiche pas depuis hier » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-110 « bonjour, l intranet ne s affiche pas pouvez vous m aider » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-111 « svp l intranet ne s affiche pas !!! » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-112 « urgent : l intranet ne s affiche pas c est bloquant » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-113 « depuis ce matin l intranet ne s affiche pas pouvez vous m aider » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-114 « urgent : l intranet ne s affiche pas merci » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-115 « svp chrome ne charge pas les pages pouvez vous m aider » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-116 « re-bonjour, chrome ne charge pas les pages c est bloquant » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-117 « hello chrome ne charge pas les pages depuis hier » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-118 « urgent : chrome ne charge pas les pages pouvez vous m aider » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-119 « re-bonjour, chrome ne charge pas les pages !!! » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-120 « bonjour, chrome ne charge pas les pages au 2e etage » -> RESOLUTION_AUTO / Web / Intranet (score 1, CORRECT)
- S-121 « depuis ce matin mon telephone ne recoit plus d appels au 2e etage » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-122 « bonjour, mon telephone ne recoit plus d appels !!! » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-123 « depuis ce matin mon telephone ne recoit plus d appels !!! » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-124 « svp mon telephone ne recoit plus d appels » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-125 « re-bonjour, mon telephone ne recoit plus d appels pouvez vous m aider » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-126 « urgent : mon telephone ne recoit plus d appels pouvez vous m aider » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-127 « urgent : le softphone est muet merci » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-128 « svp le softphone est muet au 2e etage » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-129 « hello le softphone est muet pouvez vous m aider » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-130 « urgent : le softphone est muet pouvez vous m aider » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-131 « hello le softphone est muet depuis hier » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-132 « hello le softphone est muet au 2e etage » -> RESOLUTION_AUTO / Telephonie (score 1, CORRECT)
- S-133 « depuis ce matin j ai recu un mail de phishing » -> ESCALADE / Securite (score 1, CORRECT)
- S-134 « bonjour, j ai recu un mail de phishing !!! » -> ESCALADE / Securite (score 1, CORRECT)
- S-135 « re-bonjour, j ai recu un mail de phishing depuis hier » -> ESCALADE / Securite (score 1, CORRECT)
- S-136 « re-bonjour, j ai recu un mail de phishing c est bloquant » -> ESCALADE / Securite (score 1, CORRECT)
- S-137 « j ai recu un mail de phishing merci » -> ESCALADE / Securite (score 1, CORRECT)
- S-138 « j ai recu un mail de phishing c est bloquant » -> ESCALADE / Securite (score 1, CORRECT)
- S-139 « bonjour, un virus a ete detecte » -> ESCALADE / Securite (score 1, CORRECT)
- S-140 « bonjour, un virus a ete detecte au 2e etage » -> ESCALADE / Securite (score 1, CORRECT)
- S-141 « svp un virus a ete detecte merci » -> ESCALADE / Securite (score 1, CORRECT)
- S-142 « bonjour, un virus a ete detecte c est bloquant » -> ESCALADE / Securite (score 1, CORRECT)
- S-143 « urgent : un virus a ete detecte !!! » -> ESCALADE / Securite (score 1, CORRECT)
- S-144 « hello un virus a ete detecte pouvez vous m aider » -> ESCALADE / Securite (score 1, CORRECT)
- S-145 « svp mon compte a ete pirate c est bloquant » -> ESCALADE / Securite (score 1, CORRECT)
- S-146 « mon compte a ete pirate depuis hier » -> ESCALADE / Securite (score 1, CORRECT)
- S-147 « hello mon compte a ete pirate c est bloquant » -> ESCALADE / Securite (score 1, CORRECT)
- S-148 « urgent : mon compte a ete pirate depuis hier » -> ESCALADE / Securite (score 1, CORRECT)
- S-149 « urgent : mon compte a ete pirate pouvez vous m aider » -> ESCALADE / Securite (score 1, CORRECT)
- S-150 « re-bonjour, mon compte a ete pirate !!! » -> ESCALADE / Securite (score 1, CORRECT)
- S-151 « re-bonjour, on m a vole mon portable merci » -> ESCALADE / Securite (score 1, CORRECT)
- S-152 « depuis ce matin on m a vole mon portable au 2e etage » -> ESCALADE / Securite (score 1, CORRECT)
- S-153 « svp on m a vole mon portable » -> ESCALADE / Securite (score 1, CORRECT)
- S-154 « on m a vole mon portable » -> ESCALADE / Securite (score 1, CORRECT)
- S-155 « urgent : on m a vole mon portable !!! » -> ESCALADE / Securite (score 1, CORRECT)
- S-156 « bonjour, on m a vole mon portable » -> ESCALADE / Securite (score 1, CORRECT)
- S-175 « svp le fichier est corrompu merci » -> ESCALADE / Donnees (score 1, CORRECT)
- S-176 « re-bonjour, le fichier est corrompu depuis hier » -> ESCALADE / Donnees (score 1, CORRECT)
- S-177 « svp le fichier est corrompu c est bloquant » -> ESCALADE / Donnees (score 1, CORRECT)
- S-178 « bonjour, le fichier est corrompu merci » -> ESCALADE / Donnees (score 1, CORRECT)
- S-179 « bonjour, le fichier est corrompu au 2e etage » -> ESCALADE / Donnees (score 1, CORRECT)
- S-180 « hello le fichier est corrompu au 2e etage » -> ESCALADE / Donnees (score 1, CORRECT)
- S-181 « urgent : ou est la machine a cafe pouvez vous m aider » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-182 « bonjour, ou est la machine a cafe c est bloquant » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-183 « re-bonjour, ou est la machine a cafe pouvez vous m aider » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-184 « re-bonjour, ou est la machine a cafe merci » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-185 « ou est la machine a cafe » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-186 « svp ou est la machine a cafe c est bloquant » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-187 « depuis ce matin je veux poser des conges pouvez vous m aider » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-188 « re-bonjour, je veux poser des conges c est bloquant » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-189 « je veux poser des conges !!! » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-190 « bonjour, je veux poser des conges » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-191 « hello je veux poser des conges au 2e etage » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-192 « depuis ce matin je veux poser des conges merci » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-193 « depuis ce matin ma chaise est cassee !!! » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-194 « ma chaise est cassee c est bloquant » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-195 « urgent : ma chaise est cassee pouvez vous m aider » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-196 « svp ma chaise est cassee !!! » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-197 « ma chaise est cassee merci » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-198 « urgent : ma chaise est cassee au 2e etage » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-199 « urgent : besoin d une formation depuis hier » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-200 « re-bonjour, besoin d une formation c est bloquant » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-201 « besoin d une formation depuis hier » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-202 « re-bonjour, besoin d une formation pouvez vous m aider » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-203 « bonjour, besoin d une formation !!! » -> ESCALADE / Inconnu (score 0, CORRECT)
- S-204 « urgent : besoin d une formation au 2e etage » -> ESCALADE / Inconnu (score 0, CORRECT)
