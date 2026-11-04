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

# Le jeu est GELE dans data/test_gele.json (protege par empreinte).
# JEU_VALIDATION conserve l'ancien format (tuple) pour compatibilite.
import json
import os

_CHEMIN_JEU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "test_gele.json")

with open(_CHEMIN_JEU, encoding="utf-8") as _f:
    JEU_VALIDATION = [
        (c["texte"], c["attendu"], tuple(c["categories"]), c["critique"])
        for c in json.load(_f)["cas"]
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
