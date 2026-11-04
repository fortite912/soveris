# Evaluation — jeu `synthetique`

_Genere le 2026-11-04T13:32:13_

| Indicateur | Valeur |
|---|---|
| Cas | 204 |
| Decisions correctes | 204 (100.0 %) |
| Erreurs critiques (fausse resolution) | 0 |
| Escalades critiques mal orientees | 0 |
| Decisions incertaines | 48 |
| Latence mediane / p95 / max (ms) | 0.706 / 1.003 / 1.073 |

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

- S-037 « hello outlook ne s ouvre plus » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- S-038 « depuis ce matin outlook ne s ouvre plus c est bloquant » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- S-039 « bonjour, outlook ne s ouvre plus au 2e etage » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- S-040 « bonjour, outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- S-041 « urgent : outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- S-042 « outlook ne s ouvre plus pouvez vous m aider » -> RESOLUTION_AUTO / Messagerie (score 1.0, CORRECT)
- S-133 « depuis ce matin j ai recu un mail de phishing » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-134 « bonjour, j ai recu un mail de phishing !!! » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-135 « re-bonjour, j ai recu un mail de phishing depuis hier » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-136 « re-bonjour, j ai recu un mail de phishing c est bloquant » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-137 « j ai recu un mail de phishing merci » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-138 « j ai recu un mail de phishing c est bloquant » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-151 « re-bonjour, on m a vole mon portable merci » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-152 « depuis ce matin on m a vole mon portable au 2e etage » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-153 « svp on m a vole mon portable » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-154 « on m a vole mon portable » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-155 « urgent : on m a vole mon portable !!! » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-156 « bonjour, on m a vole mon portable » -> ESCALADE / Securite (score 1.0, CORRECT)
- S-175 « svp le fichier est corrompu merci » -> ESCALADE / Donnees (score 1.0, CORRECT)
- S-176 « re-bonjour, le fichier est corrompu depuis hier » -> ESCALADE / Donnees (score 1.0, CORRECT)
- S-177 « svp le fichier est corrompu c est bloquant » -> ESCALADE / Donnees (score 1.0, CORRECT)
- S-178 « bonjour, le fichier est corrompu merci » -> ESCALADE / Donnees (score 1.0, CORRECT)
- S-179 « bonjour, le fichier est corrompu au 2e etage » -> ESCALADE / Donnees (score 1.0, CORRECT)
- S-180 « hello le fichier est corrompu au 2e etage » -> ESCALADE / Donnees (score 1.0, CORRECT)
- S-181 « urgent : ou est la machine a cafe pouvez vous m aider » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-182 « bonjour, ou est la machine a cafe c est bloquant » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-183 « re-bonjour, ou est la machine a cafe pouvez vous m aider » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-184 « re-bonjour, ou est la machine a cafe merci » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-185 « ou est la machine a cafe » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-186 « svp ou est la machine a cafe c est bloquant » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-187 « depuis ce matin je veux poser des conges pouvez vous m aider » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-188 « re-bonjour, je veux poser des conges c est bloquant » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-189 « je veux poser des conges !!! » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-190 « bonjour, je veux poser des conges » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-191 « hello je veux poser des conges au 2e etage » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-192 « depuis ce matin je veux poser des conges merci » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-193 « depuis ce matin ma chaise est cassee !!! » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-194 « ma chaise est cassee c est bloquant » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-195 « urgent : ma chaise est cassee pouvez vous m aider » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-196 « svp ma chaise est cassee !!! » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-197 « ma chaise est cassee merci » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-198 « urgent : ma chaise est cassee au 2e etage » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-199 « urgent : besoin d une formation depuis hier » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-200 « re-bonjour, besoin d une formation c est bloquant » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-201 « besoin d une formation depuis hier » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-202 « re-bonjour, besoin d une formation pouvez vous m aider » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-203 « bonjour, besoin d une formation !!! » -> ESCALADE / Inconnu (score 0.0, CORRECT)
- S-204 « urgent : besoin d une formation au 2e etage » -> ESCALADE / Inconnu (score 0.0, CORRECT)
