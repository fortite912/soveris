"""
Parametres calibrables du moteur (charges depuis soveris/parametres.json).

  seuil_confiance   score pondere minimal pour oser une resolution automatique (N1)
  seuil_revue       score STRICTEMENT inferieur => decision "incertaine" (file a revoir) ;
                    s'ajoute aux cas Inconnu et aux egalites entre categories
  tolerance_pluriel accepte un suffixe pluriel (s, x) apres un mot-cle
  poids_partage     un mot-cle present dans plusieurs articles pese 1/nb_articles
  poids_multimot    multiplicateur applique aux mots-cles composes (plusieurs mots)
  marge_n2          un article N2 l'emporte s'il est a moins de `marge_n2` point(s)
                    du meilleur N1 (0 = seulement a egalite stricte)

Ce fichier est le SEUL que la boucle d'auto-amelioration a le droit de modifier
(voir soveris/auto_amelioration.py). Chaque valeur est bornee par PLAGES.
"""
import json
import os

CHEMIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parametres.json")

# Bornes admissibles (garde-fou de la calibration automatique)
PLAGES = {
    "seuil_confiance": (0.5, 3.0),
    "seuil_revue": (0.5, 3.0),
    "tolerance_pluriel": (False, True),
    "poids_partage": (False, True),
    "poids_multimot": (1.0, 3.0),
    "marge_n2": (0.0, 2.0),
}

DEFAUTS = {
    "seuil_confiance": 1.0,
    "seuil_revue": 1.0,
    "tolerance_pluriel": False,
    "poids_partage": False,
    "poids_multimot": 1.0,
    "marge_n2": 0.0,
}


def valider(parametres):
    """Leve ValueError si un parametre sort de sa plage ou est inconnu."""
    for cle, valeur in parametres.items():
        if cle not in PLAGES:
            raise ValueError(f"parametre inconnu : {cle}")
        bas, haut = PLAGES[cle]
        if isinstance(bas, bool):
            if not isinstance(valeur, bool):
                raise ValueError(f"{cle} doit etre booleen")
        elif not (bas <= float(valeur) <= haut):
            raise ValueError(f"{cle}={valeur} hors plage [{bas}, {haut}]")
    return parametres


def charger(chemin=CHEMIN):
    with open(chemin, encoding="utf-8") as f:
        p = dict(DEFAUTS)
        p.update(json.load(f))
    return valider(p)


def ecrire(parametres, chemin=CHEMIN):
    valider(parametres)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(parametres, f, ensure_ascii=False, indent=1)
        f.write("\n")


PARAMETRES = charger()
