"""
============================================================
 Soveris - Journal local des decisions et file "a revoir"
============================================================

Le moteur journalise chaque decision prise en production (via traiter())
dans journal/decisions.jsonl, SANS donnee personnelle : seul un condense
SHA-256 tronque du texte est conserve, avec la categorie, la decision,
le score et la latence.

Les decisions INCERTAINES (voir soveris.est_incertain) sont en plus rangees
dans journal/a_revoir.jsonl avec un texte PSEUDONYMISE (e-mails, telephones,
suites de chiffres, URL masques) pour qu'un humain puisse les relire et
indiquer la bonne reponse. Un cas corrige a la forme :

  {"texte": "...", "obtenu": {...}, "correction": {"attendu": "ESCALADE",
   "categories": ["Securite"], "critique": true}}

`python -m soveris integrer-revues` verse les cas corriges dans data/dev.json
(source "revue"), ce qui alimente la boucle d'auto-amelioration.

Le dossier journal/ est ignore par git. Tout est local.
============================================================
"""

import hashlib
import json
import os
import re
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_JOURNAL = os.path.join(RACINE, "journal")
CHEMIN_DECISIONS = os.path.join(DOSSIER_JOURNAL, "decisions.jsonl")
CHEMIN_A_REVOIR = os.path.join(DOSSIER_JOURNAL, "a_revoir.jsonl")
CHEMIN_DEV = os.path.join(RACINE, "data", "dev.json")

_MOTIFS_PSEUDO = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "<email>"),
    (re.compile(r"https?://\S+|www\.\S+"), "<url>"),
    (re.compile(r"(?:\+?\d[\s.-]?){9,}"), "<telephone>"),
    (re.compile(r"\b\d{4,}\b"), "<nombre>"),
    (re.compile(r"\b[A-Z][a-z]+ [A-Z][A-Z-]+\b"), "<nom>"),  # "Jean DUPONT"
]


def pseudonymiser(texte):
    """Masque les motifs les plus courants de donnees personnelles."""
    for motif, remplacement in _MOTIFS_PSEUDO:
        texte = motif.sub(remplacement, texte)
    return texte


def empreinte(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:16]


def _ajouter(chemin, enregistrement):
    os.makedirs(DOSSIER_JOURNAL, exist_ok=True)
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(json.dumps(enregistrement, ensure_ascii=False) + "\n")


def _lire(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def consigner(resultat, incertain):
    """Journalise une decision ; range le cas dans la file si incertain."""
    base = {
        "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "empreinte": empreinte(resultat["texte"]),
        "categorie": resultat["categorie"],
        "niveau": resultat["niveau"],
        "decision": resultat["decision"],
        "score": resultat["score"],
        "confiance": resultat["confiance"],
        "ambigu": resultat.get("ambigu", False),
        "incertain": incertain,
        "temps_ms": resultat["temps_ms"],
    }
    _ajouter(CHEMIN_DECISIONS, base)
    if incertain:
        _ajouter(CHEMIN_A_REVOIR, {
            "horodatage": base["horodatage"],
            "empreinte": base["empreinte"],
            "texte": pseudonymiser(resultat["texte"]),
            "obtenu": {"decision": resultat["decision"], "categorie": resultat["categorie"],
                       "score": resultat["score"], "mots_reconnus": resultat["mots_reconnus"]},
            "correction": None,
        })


def etat_file_revue():
    cas = _lire(CHEMIN_A_REVOIR)
    corriges = [c for c in cas if c.get("correction")]
    return {"total": len(cas), "en_attente": len(cas) - len(corriges), "corriges": len(corriges)}


def integrer_revues():
    """
    Verse les cas corriges (et non encore integres) dans data/dev.json.
    Les cas restent dans la file, marques "integre": true.
    Renvoie le nombre de cas integres.
    """
    cas = _lire(CHEMIN_A_REVOIR)
    with open(CHEMIN_DEV, encoding="utf-8") as f:
        dev = json.load(f)
    existants = {c["texte"] for c in dev["cas"]}
    n = 0
    for c in cas:
        corr = c.get("correction")
        if not corr or c.get("integre") or c["texte"] in existants:
            continue
        if corr.get("attendu") not in ("RESOLUTION_AUTO", "ESCALADE") or not corr.get("categories"):
            continue
        n += 1
        dev["cas"].append({
            "id": f"R-{len(dev['cas']) + 1:03d}",
            "texte": c["texte"],
            "attendu": corr["attendu"],
            "categories": list(corr["categories"]),
            "critique": bool(corr.get("critique", False)),
            "source": "revue",
        })
        c["integre"] = True
        existants.add(c["texte"])
    if n:
        with open(CHEMIN_DEV, "w", encoding="utf-8") as f:
            json.dump(dev, f, ensure_ascii=False, indent=1)
        with open(CHEMIN_A_REVOIR, "w", encoding="utf-8") as f:
            for c in cas:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return n
