"""
Generateur de cas SYNTHETIQUES (deterministe, graine fixe).

Produit data/synthetiques.json en combinant des prefixes, des noyaux de
demande etiquetes et des suffixes. Les cas sont marques "source": "generes"
et sont EXCLUS du jeu gele. Ils servent a detecter des fragilites
(variantes de formulation), pas a mesurer la precision reelle.

Lancement : python scripts/generer_synthetiques.py
"""
import json
import os
import random

A, E = "RESOLUTION_AUTO", "ESCALADE"

# (noyau, decision attendue, categories acceptees, critique)
NOYAUX = [
    ("le wifi ne marche plus", A, ["Reseau"], False),
    ("plus d internet", A, ["Reseau"], False),
    ("le vpn ne se connecte pas", A, ["Reseau"], False),
    ("mon mot de passe est refuse", A, ["Compte / Acces"], False),
    ("mon compte est bloque", A, ["Compte / Acces"], False),
    ("je n ai plus acces au dossier partage", A, ["Compte / Acces"], False),
    ("outlook ne s ouvre plus", A, ["Messagerie", "Logiciel"], False),
    ("je ne recois plus mes mails", A, ["Messagerie"], False),
    ("l imprimante ne fonctionne pas", A, ["Materiel"], False),
    ("bourrage papier", A, ["Materiel"], False),
    ("mon ecran reste noir", A, ["Materiel"], False),
    ("ma souris ne marche plus", A, ["Materiel"], False),
    ("mon ordinateur est lent", A, ["Performance"], False),
    ("le poste rame", A, ["Performance"], False),
    ("le logiciel plante", A, ["Logiciel"], False),
    ("l application affiche une erreur", A, ["Logiciel"], False),
    ("teams ne marche pas", A, ["Collaboration"], False),
    ("mon micro ne fonctionne pas en visio", A, ["Collaboration"], False),
    ("l intranet ne s affiche pas", A, ["Web / Intranet"], False),
    ("chrome ne charge pas les pages", A, ["Web / Intranet"], False),
    ("mon telephone ne recoit plus d appels", A, ["Telephonie"], False),
    ("le softphone est muet", A, ["Telephonie"], False),
    ("j ai recu un mail de phishing", E, ["Securite"], True),
    ("un virus a ete detecte", E, ["Securite"], True),
    ("mon compte a ete pirate", E, ["Securite"], True),
    ("on m a vole mon portable", E, ["Securite"], True),
    ("le serveur est down pour tout le monde", E, ["Infrastructure"], True),
    ("plus personne n a acces a la production", E, ["Infrastructure"], True),
    ("j ai supprime des fichiers par erreur", E, ["Donnees"], True),
    ("le fichier est corrompu", E, ["Donnees"], True),
    ("ou est la machine a cafe", E, ["Inconnu"], False),
    ("je veux poser des conges", E, ["Inconnu"], False),
    ("ma chaise est cassee", E, ["Inconnu"], False),
    ("besoin d une formation", E, ["Inconnu"], False),
]
PREFIXES = ["", "bonjour, ", "urgent : ", "depuis ce matin ", "re-bonjour, ", "hello ", "svp "]
SUFFIXES = ["", " merci", " depuis hier", " c est bloquant", " pouvez vous m aider", " !!!", " au 2e etage"]


def generer(graine=42, par_noyau=6):
    alea = random.Random(graine)
    cas = []
    for noyau, attendu, categories, critique in NOYAUX:
        combos = {(p, s) for p in PREFIXES for s in SUFFIXES}
        for prefixe, suffixe in alea.sample(sorted(combos), par_noyau):
            texte = f"{prefixe}{noyau}{suffixe}".strip()
            cas.append({"texte": texte, "attendu": attendu, "categories": categories,
                        "critique": critique, "source": "generes"})
    for i, c in enumerate(cas, 1):
        c["id"] = f"S-{i:03d}"
        # ordre des cles stable
        cas[i - 1] = {k: c[k] for k in ("id", "texte", "attendu", "categories", "critique", "source")}
    return cas


if __name__ == "__main__":
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, "data", "synthetiques.json")
    cas = generer()
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump({"description": "Cas SYNTHETIQUES generes par scripts/generer_synthetiques.py "
                                  "(graine 42). Marques 'generes', exclus du jeu gele.",
                   "cas": cas}, f, ensure_ascii=False, indent=1)
    print(f"{len(cas)} cas ecrits dans {chemin}")
