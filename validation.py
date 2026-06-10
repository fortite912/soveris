"""
============================================================
 Soveris - Banc de validation independant
============================================================

POURQUOI CE FICHIER EXISTE
Le jeu de demonstration (demo.py, 10 tickets) sert a MONTRER l'agent.
Il ne suffit pas a MESURER l'agent : ses tickets et la base de
connaissances ont le meme auteur (biais de circularite).

Ce banc applique une methode plus stricte :
  - 50 tickets rediges du point de vue d'un utilisateur reel
    (formulations vagues, fautes de frappe, cas pieges, demandes
    hors perimetre), SANS regarder les mots-cles de la base ;
  - chaque ticket est etiquete avec le comportement ATTENDU ;
  - on mesure non seulement les resolutions, mais surtout les
    FAUSSES RESOLUTIONS (l'agent repond a tort) - la metrique
    de confiance qui compte pour une DSI.

Classification des resultats :
  CORRECT      decision conforme a l'attendu (et bonne categorie si auto)
  MANQUE       l'agent escalade un ticket qu'on esperait resoluble
               (erreur CONSERVATRICE : un humain prend le relais, sans danger)
  MAL_CATEGORISE  resolu automatiquement mais mauvaise categorie
  FAUSSE_DANGEREUSE  resolu automatiquement alors qu'une escalade
               critique etait attendue (securite, donnees, infrastructure)
  FAUSSE_HORS_PERIMETRE  resolu automatiquement alors que la demande
               sort du perimetre du support technique

Lancement :  python validation.py
============================================================
"""

import soveris

# Chaque entree : (texte utilisateur, decision attendue,
#                  categories acceptees si resolution, escalade critique ?)
JEU_VALIDATION = [
    # ---- Incidents courants : resolution automatique attendue (32) ----
    ("le wifi coupe sans arret dans la salle de reunion", "RESOLUTION_AUTO", ("Reseau",), False),
    ("impossible de me connecter a internet ce matin", "RESOLUTION_AUTO", ("Reseau",), False),
    ("mon mot de passe ne marche plus", "RESOLUTION_AUTO", ("Compte / Acces",), False),
    ("compte bloque apres plusieurs essais", "RESOLUTION_AUTO", ("Compte / Acces",), False),
    ("je ne recois plus mes emails depuis hier", "RESOLUTION_AUTO", ("Messagerie",), False),
    ("outlook plante au demarrage", "RESOLUTION_AUTO", ("Messagerie", "Logiciel"), False),
    ("l imprimante affiche plus de toner", "RESOLUTION_AUTO", ("Materiel",), False),
    ("bourrage papier au troisieme etage", "RESOLUTION_AUTO", ("Materiel",), False),
    ("mon pc est super lent depuis la mise a jour", "RESOLUTION_AUTO", ("Performance",), False),
    ("tout rame quand j ouvre plusieurs fenetres", "RESOLUTION_AUTO", ("Performance",), False),
    ("le vpn refuse de se connecter depuis chez moi", "RESOLUTION_AUTO", ("Reseau",), False),
    ("acces refuse au lecteur reseau commun", "RESOLUTION_AUTO", ("Compte / Acces", "Reseau"), False),
    ("je n ai plus acces au dossier du service compta", "RESOLUTION_AUTO", ("Compte / Acces",), False),
    ("ma souris ne repond plus", "RESOLUTION_AUTO", ("Materiel",), False),
    ("ecran noir au demarrage du poste", "RESOLUTION_AUTO", ("Materiel",), False),
    ("le clavier tape des caracteres bizarres", "RESOLUTION_AUTO", ("Materiel",), False),
    ("mon casque n est pas detecte en visio", "RESOLUTION_AUTO", ("Materiel", "Collaboration"), False),
    ("teams ne veut pas partager mon ecran", "RESOLUTION_AUTO", ("Collaboration", "Materiel"), False),
    ("le micro ne marche pas pendant les reunions zoom", "RESOLUTION_AUTO", ("Collaboration",), False),
    ("impossible d ouvrir l application de compta", "RESOLUTION_AUTO", ("Logiciel",), False),
    ("le logiciel de paie affiche une erreur au lancement", "RESOLUTION_AUTO", ("Logiciel",), False),
    ("je dois installer un programme mais ca echoue", "RESOLUTION_AUTO", ("Logiciel",), False),
    ("chrome ne charge aucune page", "RESOLUTION_AUTO", ("Web / Intranet",), False),
    ("l intranet est inaccessible depuis mon poste", "RESOLUTION_AUTO", ("Web / Intranet",), False),
    ("le site de l entreprise ne s affiche pas", "RESOLUTION_AUTO", ("Web / Intranet",), False),
    ("mon telephone pro ne recoit plus d appels", "RESOLUTION_AUTO", ("Telephonie",), False),
    ("la carte sim n est pas reconnue", "RESOLUTION_AUTO", ("Telephonie",), False),
    ("le portable de service ne s allume plus", "RESOLUTION_AUTO", ("Telephonie", "Materiel"), False),
    ("je n arrive pas a me connecter o wifi", "RESOLUTION_AUTO", ("Reseau",), False),
    ("ma boite est pleine je ne peux plus recevoir de courrier", "RESOLUTION_AUTO", ("Messagerie",), False),
    ("session windows verrouillee impossible de rentrer", "RESOLUTION_AUTO", ("Compte / Acces",), False),
    ("mon ordi est mort", "RESOLUTION_AUTO", ("Materiel", "Performance"), False),

    # ---- Cas sensibles : escalade attendue, erreur = DANGEREUSE (10) ----
    ("je crois que j ai un virus sur mon poste", "ESCALADE", ("Securite",), True),
    ("un mail bizarre me demande mes identifiants", "ESCALADE", ("Securite",), True),
    ("on m a vole mon ordinateur portable dans le train", "ESCALADE", ("Securite",), True),
    ("ransomware detecte par l antivirus", "ESCALADE", ("Securite",), True),
    ("plus personne n arrive a se connecter au serveur", "ESCALADE", ("Infrastructure",), True),
    ("la prod est tombee tout le monde est bloque", "ESCALADE", ("Infrastructure",), True),
    ("j ai efface un dossier partage par erreur", "ESCALADE", ("Donnees",), True),
    ("fichier client corrompu impossible a ouvrir", "ESCALADE", ("Donnees",), True),
    ("je pense que mon compte a ete pirate", "ESCALADE", ("Securite",), True),
    ("le serveur de fichiers est indisponible", "ESCALADE", ("Infrastructure",), True),

    # ---- Hors perimetre : escalade attendue (qualification humaine) (8) ----
    ("ou se trouve la machine a cafe", "ESCALADE", ("Inconnu",), False),
    ("je veux poser mes conges la semaine prochaine", "ESCALADE", ("Inconnu",), False),
    ("le badge de la porte ne fonctionne plus", "ESCALADE", ("Inconnu",), False),
    ("quelle est la date de la prochaine reunion d equipe", "ESCALADE", ("Inconnu",), False),
    ("ma chaise de bureau est cassee", "ESCALADE", ("Inconnu",), False),
    ("comment changer ma photo sur l intranet", "ESCALADE", ("Inconnu",), False),
    ("il fait trop chaud dans l open space", "ESCALADE", ("Inconnu",), False),
    ("besoin d une formation sur excel", "ESCALADE", ("Inconnu",), False),
]


def evaluer():
    """
    Rejoue les 50 tickets et classe chaque resultat.
    Renvoie un dictionnaire de metriques (utilise aussi par tests.py).
    """
    bilan = {
        "total": len(JEU_VALIDATION),
        "corrects": 0,
        "manques": [],                # escalades conservatrices (sans danger)
        "mal_categorises": [],        # resolu, mais mauvaise categorie
        "fausses_dangereuses": [],    # resolu alors qu'escalade critique attendue
        "fausses_hors_perimetre": [], # resolu alors que hors perimetre
    }

    for texte, attendu, categories_ok, critique in JEU_VALIDATION:
        r = soveris.analyser(texte)
        obtenu = (texte, f"{r['decision']} / {r['categorie']}")

        if attendu == "RESOLUTION_AUTO":
            if r["decision"] == "RESOLUTION_AUTO":
                if r["categorie"] in categories_ok:
                    bilan["corrects"] += 1
                else:
                    bilan["mal_categorises"].append(obtenu)
            else:
                bilan["manques"].append(obtenu)
        else:  # ESCALADE attendue
            if r["decision"] == "ESCALADE":
                bilan["corrects"] += 1
            elif critique:
                bilan["fausses_dangereuses"].append(obtenu)
            else:
                bilan["fausses_hors_perimetre"].append(obtenu)

    bilan["exactitude"] = round(bilan["corrects"] / bilan["total"] * 100, 1)
    return bilan


def _afficher_liste(titre, liste):
    if liste:
        print(f"\n  {titre} ({len(liste)}) :")
        for texte, obtenu in liste:
            print(f"    - \"{texte}\"")
            print(f"      -> {obtenu}")


if __name__ == "__main__":
    b = evaluer()
    print("=" * 64)
    print(" BANC DE VALIDATION  -  50 tickets independants")
    print("=" * 64)
    print(f"  Decisions correctes        : {b['corrects']} / {b['total']}  ({b['exactitude']} %)")
    print(f"  Escalades conservatrices   : {len(b['manques'])}  (sans danger : un humain reprend)")
    print(f"  Resolutions mal categorisees : {len(b['mal_categorises'])}")
    print(f"  FAUSSES RESOLUTIONS dangereuses    : {len(b['fausses_dangereuses'])}")
    print(f"  Fausses resolutions hors perimetre : {len(b['fausses_hors_perimetre'])}")
    _afficher_liste("Escalades conservatrices", b["manques"])
    _afficher_liste("Mal categorisees", b["mal_categorises"])
    _afficher_liste("FAUSSES RESOLUTIONS DANGEREUSES", b["fausses_dangereuses"])
    _afficher_liste("Fausses resolutions hors perimetre", b["fausses_hors_perimetre"])
    print("=" * 64)
