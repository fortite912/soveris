"""
============================================================
 Soveris - Evaluation reproductible
============================================================

Rejoue un jeu de donnees etiquete et produit un rapport (JSON + Markdown) :
precision globale et par classe, matrice de confusion, erreurs critiques,
decisions a faible confiance, latence.

Jeux disponibles (dossier data/) :
  - "test"        : jeu GELE (data/test_gele.json) - verification seulement
  - "dev"         : jeu de developpement (data/dev.json) - iteration
  - "synthetique" : cas generes (data/synthetiques.json) - robustesse
  - "tous"        : concatenation des trois (a titre indicatif)

Verdicts par cas :
  CORRECT                decision conforme (et categorie acceptee si auto)
  MANQUE                 escalade alors qu'une resolution etait attendue
                         (erreur CONSERVATRICE : sans danger)
  MAL_CATEGORISE         resolu automatiquement, mauvaise categorie
  FAUSSE_DANGEREUSE      resolu alors qu'une escalade critique etait attendue
  FAUSSE_HORS_PERIMETRE  resolu alors que la demande sort du perimetre

Les deux derniers verdicts sont les ERREURS CRITIQUES. Une escalade
critique orientee vers la mauvaise categorie (ex. securite -> Inconnu)
n'est pas une erreur de decision, mais elle est listee a part
("critiques_mal_orientees") car elle ralentit la prise en charge.

Aucune librairie externe. Aucun acces reseau.
============================================================
"""

import json
import os
import statistics
import time

from . import analyser, est_incertain

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_DONNEES = os.path.join(RACINE, "data")
DOSSIER_RAPPORTS = os.path.join(RACINE, "reports")

FICHIERS_JEUX = {
    "test": "test_gele.json",
    "dev": "dev.json",
    "synthetique": "synthetiques.json",
}

VERDICTS_CRITIQUES = ("FAUSSE_DANGEREUSE", "FAUSSE_HORS_PERIMETRE")


def charger_jeu(nom):
    """Charge un jeu etiquete. 'tous' concatene les trois jeux."""
    if nom == "tous":
        cas = []
        for n in FICHIERS_JEUX:
            cas.extend(charger_jeu(n))
        return cas
    if nom not in FICHIERS_JEUX:
        raise ValueError(f"Jeu inconnu : {nom} (attendu : {', '.join(FICHIERS_JEUX)}, tous)")
    chemin = os.path.join(DOSSIER_DONNEES, FICHIERS_JEUX[nom])
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)["cas"]


def verdict(cas, resultat):
    """Classe le resultat de l'agent face a l'etiquette attendue."""
    attendu = cas["attendu"]
    if attendu == "RESOLUTION_AUTO":
        if resultat["decision"] != "RESOLUTION_AUTO":
            return "MANQUE"
        return "CORRECT" if resultat["categorie"] in cas["categories"] else "MAL_CATEGORISE"
    # ESCALADE attendue
    if resultat["decision"] == "ESCALADE":
        return "CORRECT"
    return "FAUSSE_DANGEREUSE" if cas["critique"] else "FAUSSE_HORS_PERIMETRE"


def evaluer_cas(cas):
    """Analyse un cas et renvoie la ligne detaillee du rapport."""
    r = analyser(cas["texte"])
    v = verdict(cas, r)
    return {
        "id": cas.get("id"),
        "texte": cas["texte"],
        "source": cas.get("source"),
        "attendu": cas["attendu"],
        "categories_attendues": cas["categories"],
        "critique": cas["critique"],
        "decision": r["decision"],
        "categorie": r["categorie"],
        "score": r["score"],
        "confiance": r["confiance"],
        "mots_reconnus": r["mots_reconnus"],
        "ambigu": r.get("ambigu", False),
        "incertain": est_incertain(r),
        "verdict": v,
        "categorie_correcte": r["categorie"] in cas["categories"],
        "temps_ms": r["temps_ms"],
    }


def evaluer_jeu(nom):
    """Evalue un jeu complet et renvoie le rapport structure."""
    cas = charger_jeu(nom)
    depart = time.perf_counter()
    lignes = [evaluer_cas(c) for c in cas]
    duree_totale_ms = (time.perf_counter() - depart) * 1000
    return construire_rapport(nom, lignes, duree_totale_ms)


def construire_rapport(nom, lignes, duree_totale_ms=None):
    total = len(lignes)
    corrects = sum(1 for l in lignes if l["verdict"] == "CORRECT")
    verdicts = {}
    for l in lignes:
        verdicts[l["verdict"]] = verdicts.get(l["verdict"], 0) + 1

    # Precision par classe attendue (classe = premiere categorie acceptee)
    par_classe = {}
    for l in lignes:
        cle = l["categories_attendues"][0]
        p = par_classe.setdefault(cle, {"total": 0, "corrects": 0, "erreurs": []})
        p["total"] += 1
        if l["verdict"] == "CORRECT":
            p["corrects"] += 1
        else:
            p["erreurs"].append({"id": l["id"], "texte": l["texte"], "verdict": l["verdict"],
                                 "obtenu": f"{l['decision']} / {l['categorie']}"})
    for p in par_classe.values():
        p["precision"] = round(p["corrects"] / p["total"] * 100, 1)

    # Matrice de confusion : categorie attendue -> categorie predite
    matrice = {}
    for l in lignes:
        attendue = l["categories_attendues"][0]
        matrice.setdefault(attendue, {})
        matrice[attendue][l["categorie"]] = matrice[attendue].get(l["categorie"], 0) + 1

    critiques = [l for l in lignes if l["verdict"] in VERDICTS_CRITIQUES]
    critiques_mal_orientees = [
        l for l in lignes
        if l["critique"] and l["decision"] == "ESCALADE" and not l["categorie_correcte"]
    ]
    incertains = [l for l in lignes if l["incertain"]]
    temps = [l["temps_ms"] for l in lignes]

    return {
        "jeu": nom,
        "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": total,
        "corrects": corrects,
        "precision": round(corrects / total * 100, 1) if total else 0.0,
        "verdicts": verdicts,
        "erreurs_critiques": len(critiques),
        "critiques_mal_orientees": len(critiques_mal_orientees),
        "incertains": len(incertains),
        "latence_ms": {
            "mediane": round(statistics.median(temps), 3) if temps else 0,
            "p95": round(sorted(temps)[max(0, int(len(temps) * 0.95) - 1)], 3) if temps else 0,
            "max": round(max(temps), 3) if temps else 0,
            "total_jeu": round(duree_totale_ms, 1) if duree_totale_ms is not None else None,
        },
        "par_classe": par_classe,
        "matrice_confusion": matrice,
        "details_critiques": critiques,
        "details_critiques_mal_orientees": critiques_mal_orientees,
        "details_incertains": [{"id": l["id"], "texte": l["texte"], "obtenu": f"{l['decision']} / {l['categorie']}",
                                "score": l["score"], "verdict": l["verdict"]} for l in incertains],
        "erreurs": [l for l in lignes if l["verdict"] != "CORRECT"],
    }


def rendre_markdown(rapport):
    r = rapport
    lignes = [
        f"# Evaluation — jeu `{r['jeu']}`",
        "",
        f"_Genere le {r['horodatage']}_",
        "",
        "| Indicateur | Valeur |",
        "|---|---|",
        f"| Cas | {r['total']} |",
        f"| Decisions correctes | {r['corrects']} ({r['precision']} %) |",
        f"| Erreurs critiques (fausse resolution) | {r['erreurs_critiques']} |",
        f"| Escalades critiques mal orientees | {r['critiques_mal_orientees']} |",
        f"| Decisions incertaines | {r['incertains']} |",
        f"| Latence mediane / p95 / max (ms) | {r['latence_ms']['mediane']} / {r['latence_ms']['p95']} / {r['latence_ms']['max']} |",
        "",
        "## Verdicts",
        "",
        "| Verdict | Nombre |",
        "|---|---|",
    ]
    for v, n in sorted(r["verdicts"].items()):
        lignes.append(f"| {v} | {n} |")
    lignes += ["", "## Precision par classe attendue", "", "| Classe | Cas | Corrects | Precision |", "|---|---|---|---|"]
    for cle, p in sorted(r["par_classe"].items()):
        lignes.append(f"| {cle} | {p['total']} | {p['corrects']} | {p['precision']} % |")
    colonnes = sorted({c for ligne in r["matrice_confusion"].values() for c in ligne})
    lignes += ["", "## Matrice de confusion (attendu en ligne, predit en colonne)", "",
               "| attendu \\ predit | " + " | ".join(colonnes) + " |",
               "|---|" + "---|" * len(colonnes)]
    for attendue in sorted(r["matrice_confusion"]):
        ligne = r["matrice_confusion"][attendue]
        lignes.append(f"| {attendue} | " + " | ".join(str(ligne.get(c, "")) for c in colonnes) + " |")
    if r["erreurs"]:
        lignes += ["", "## Erreurs", "", "| Id | Texte | Attendu | Obtenu | Verdict |", "|---|---|---|---|---|"]
        for e in r["erreurs"]:
            lignes.append(f"| {e['id']} | {e['texte']} | {e['attendu']} / {', '.join(e['categories_attendues'])} "
                          f"| {e['decision']} / {e['categorie']} | {e['verdict']} |")
    if r["details_critiques_mal_orientees"]:
        lignes += ["", "## Escalades critiques mal orientees", ""]
        for e in r["details_critiques_mal_orientees"]:
            lignes.append(f"- {e['id']} « {e['texte']} » : attendu {', '.join(e['categories_attendues'])}, obtenu {e['categorie']}")
    if r["details_incertains"]:
        lignes += ["", "## Decisions incertaines (a revoir)", ""]
        for e in r["details_incertains"]:
            lignes.append(f"- {e['id']} « {e['texte']} » -> {e['obtenu']} (score {e['score']}, {e['verdict']})")
    return "\n".join(lignes) + "\n"


def ecrire_rapports(rapport, dossier=DOSSIER_RAPPORTS, prefixe="evaluation"):
    os.makedirs(dossier, exist_ok=True)
    base = os.path.join(dossier, f"{prefixe}_{rapport['jeu']}")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=1)
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(rendre_markdown(rapport))
    return base + ".json", base + ".md"


def resume(rapport):
    """Resume compact (pour baseline.json et diagnostic)."""
    return {
        "total": rapport["total"],
        "corrects": rapport["corrects"],
        "precision": rapport["precision"],
        "erreurs_critiques": rapport["erreurs_critiques"],
        "critiques_mal_orientees": rapport["critiques_mal_orientees"],
        "incertains": rapport["incertains"],
        "par_classe": {k: v["precision"] for k, v in rapport["par_classe"].items()},
        "latence_p95_ms": rapport["latence_ms"]["p95"],
    }


def ecrire_baseline(chemin=None, commit=None):
    """Evalue les trois jeux et fige la reference reports/baseline.json."""
    chemin = chemin or os.path.join(DOSSIER_RAPPORTS, "baseline.json")
    baseline = {
        "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "commit": commit,
        "jeux": {nom: resume(evaluer_jeu(nom)) for nom in FICHIERS_JEUX},
    }
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(baseline, f, ensure_ascii=False, indent=1)
    return baseline
