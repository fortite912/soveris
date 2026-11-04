"""
============================================================
 Soveris - Auto-diagnostic
============================================================

Une seule commande : python -m soveris diagnose

  1. lance les suites de tests (tests/ via unittest, et tests.py historique) ;
  2. evalue les trois jeux (test gele, dev, synthetiques) ;
  3. compare a reports/baseline.json (regressions de precision, d'erreurs
     critiques, par classe) ;
  4. releve les decisions a faible confiance et l'etat de la file "a revoir" ;
  5. ecrit reports/diagnostic.json + .md avec des constats PRIORISES.

Code de sortie (utilisable en CI) :
  0  aucun probleme bloquant
  1  tests en echec OU regression contre la baseline
  2  erreur d'execution du diagnostic

Aucun acces reseau. Les tests sont lances en sous-processus Python local.
============================================================
"""

import json
import os
import subprocess
import sys
import time

from . import evaluation

RACINE = evaluation.RACINE
CHEMIN_BASELINE = os.path.join(evaluation.DOSSIER_RAPPORTS, "baseline.json")

# Priorites des constats
P1, P2, P3, P4 = "P1-bloquant", "P2-regression", "P3-qualite", "P4-information"


def lancer_suites():
    """Execute les deux suites de tests et renvoie leur statut."""
    suites = {
        "unittest (tests/)": [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        "tests.py (historique)": [sys.executable, "tests.py"],
    }
    resultats = {}
    for nom, commande in suites.items():
        depart = time.perf_counter()
        proc = subprocess.run(commande, cwd=RACINE, capture_output=True, text=True)
        sortie = (proc.stdout + proc.stderr).strip().splitlines()
        resultats[nom] = {
            "ok": proc.returncode == 0,
            "code": proc.returncode,
            "duree_s": round(time.perf_counter() - depart, 2),
            "dernieres_lignes": sortie[-6:],
        }
    return resultats


def charger_baseline(chemin=None):
    chemin = chemin or CHEMIN_BASELINE
    if not os.path.exists(chemin):
        return None
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def comparer(rapports, baseline):
    """Compare les resumes courants a la baseline ; renvoie la liste des ecarts."""
    ecarts = []
    if not baseline:
        return ecarts
    for nom, rapport in rapports.items():
        ref = baseline.get("jeux", {}).get(nom)
        if not ref:
            continue
        cour = evaluation.resume(rapport)
        if cour["erreurs_critiques"] > ref["erreurs_critiques"]:
            ecarts.append({"priorite": P1, "jeu": nom, "indicateur": "erreurs_critiques",
                           "avant": ref["erreurs_critiques"], "apres": cour["erreurs_critiques"],
                           "message": f"[{nom}] erreurs critiques en hausse : {ref['erreurs_critiques']} -> {cour['erreurs_critiques']}"})
        if cour["precision"] < ref["precision"]:
            ecarts.append({"priorite": P2 if nom != "test" else P1, "jeu": nom, "indicateur": "precision",
                           "avant": ref["precision"], "apres": cour["precision"],
                           "message": f"[{nom}] precision en baisse : {ref['precision']} % -> {cour['precision']} %"})
        for classe, prec_ref in ref.get("par_classe", {}).items():
            prec = cour["par_classe"].get(classe)
            if prec is not None and prec < prec_ref:
                ecarts.append({"priorite": P3, "jeu": nom, "indicateur": f"classe:{classe}",
                               "avant": prec_ref, "apres": prec,
                               "message": f"[{nom}] classe {classe} : {prec_ref} % -> {prec} %"})
        if cour["critiques_mal_orientees"] > ref["critiques_mal_orientees"]:
            ecarts.append({"priorite": P3, "jeu": nom, "indicateur": "critiques_mal_orientees",
                           "avant": ref["critiques_mal_orientees"], "apres": cour["critiques_mal_orientees"],
                           "message": f"[{nom}] escalades critiques mal orientees : {ref['critiques_mal_orientees']} -> {cour['critiques_mal_orientees']}"})
        if cour["total"] != ref["total"] and nom == "test":
            ecarts.append({"priorite": P1, "jeu": nom, "indicateur": "total",
                           "avant": ref["total"], "apres": cour["total"],
                           "message": f"[test] le nombre de cas du jeu gele a change : {ref['total']} -> {cour['total']}"})
    return ecarts


def construire_constats(tests, rapports, ecarts, file_revue):
    constats = []
    for nom, t in (tests or {}).items():
        if not t["ok"]:
            constats.append({"priorite": P1, "message": f"Suite de tests en echec : {nom} (code {t['code']})",
                             "detail": t["dernieres_lignes"]})
    constats.extend({"priorite": e["priorite"], "message": e["message"], "detail": e} for e in ecarts)
    for nom, r in rapports.items():
        if r["erreurs_critiques"]:
            constats.append({"priorite": P3, "message": f"[{nom}] {r['erreurs_critiques']} erreur(s) critique(s) presente(s)",
                             "detail": [f"{c['id']} « {c['texte']} » -> {c['decision']} / {c['categorie']}" for c in r["details_critiques"]]})
        if r["critiques_mal_orientees"]:
            constats.append({"priorite": P4, "message": f"[{nom}] {r['critiques_mal_orientees']} escalade(s) critique(s) mal orientee(s)",
                             "detail": [f"{c['id']} « {c['texte']} » -> {c['categorie']}" for c in r["details_critiques_mal_orientees"]]})
        if r["incertains"]:
            constats.append({"priorite": P4, "message": f"[{nom}] {r['incertains']}/{r['total']} decision(s) a faible confiance",
                             "detail": [f"{c['id']} « {c['texte']} » -> {c['obtenu']}" for c in r["details_incertains"][:10]]})
    if file_revue:
        constats.append({"priorite": P4, "message": f"File « a revoir » : {file_revue['en_attente']} cas en attente, "
                                                    f"{file_revue['corriges']} corrige(s) non integre(s)",
                         "detail": file_revue})
    ordre = {P1: 0, P2: 1, P3: 2, P4: 3}
    constats.sort(key=lambda c: ordre[c["priorite"]])
    return constats


def rendre_markdown(diag):
    l = [f"# Auto-diagnostic Soveris", "", f"_Genere le {diag['horodatage']}_ — verdict : **{diag['verdict']}** (code {diag['code_sortie']})", ""]
    if diag["tests"]:
        l += ["## Tests", "", "| Suite | Statut | Duree |", "|---|---|---|"]
        for nom, t in diag["tests"].items():
            l.append(f"| {nom} | {'OK' if t['ok'] else 'ECHEC'} | {t['duree_s']} s |")
        l.append("")
    l += ["## Evaluation", "", "| Jeu | Cas | Precision | Erreurs critiques | Mal orientees | Incertains | Baseline precision |", "|---|---|---|---|---|---|---|"]
    for nom, r in diag["evaluation"].items():
        ref = (diag.get("baseline") or {}).get("jeux", {}).get(nom, {})
        l.append(f"| {nom} | {r['total']} | {r['precision']} % | {r['erreurs_critiques']} | {r['critiques_mal_orientees']} | {r['incertains']} | {ref.get('precision', '—')} % |")
    l += ["", "## Constats priorises", ""]
    if not diag["constats"]:
        l.append("Aucun constat.")
    for c in diag["constats"]:
        l.append(f"- **{c['priorite']}** — {c['message']}")
        detail = c.get("detail")
        if isinstance(detail, list):
            for d in detail[:10]:
                l.append(f"  - {d}")
    return "\n".join(l) + "\n"


def executer(baseline=None, lancer_tests=True, ecrire=True, silencieux=False):
    """Point d'entree. Renvoie le code de sortie."""
    try:
        tests = lancer_suites() if lancer_tests else {}
        rapports = {nom: evaluation.evaluer_jeu(nom) for nom in evaluation.FICHIERS_JEUX}
        ref = charger_baseline(baseline)
        ecarts = comparer(rapports, ref)
        try:
            from . import journal
            file_revue = journal.etat_file_revue()
        except Exception:
            file_revue = None
        constats = construire_constats(tests, rapports, ecarts, file_revue)
        bloquant = any(c["priorite"] in (P1, P2) for c in constats)
        code = 1 if bloquant else 0
        diag = {
            "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "verdict": "REGRESSION OU ECHEC" if bloquant else "OK",
            "code_sortie": code,
            "baseline": ref,
            "tests": tests,
            "evaluation": {nom: evaluation.resume(r) for nom, r in rapports.items()},
            "ecarts": ecarts,
            "constats": constats,
        }
        if ecrire:
            os.makedirs(evaluation.DOSSIER_RAPPORTS, exist_ok=True)
            with open(os.path.join(evaluation.DOSSIER_RAPPORTS, "diagnostic.json"), "w", encoding="utf-8") as f:
                json.dump(diag, f, ensure_ascii=False, indent=1)
            with open(os.path.join(evaluation.DOSSIER_RAPPORTS, "diagnostic.md"), "w", encoding="utf-8") as f:
                f.write(rendre_markdown(diag))
            for nom, r in rapports.items():
                evaluation.ecrire_rapports(r)
        if not silencieux:
            print(rendre_markdown(diag))
        return code
    except Exception as exc:  # erreur du diagnostic lui-meme
        if not silencieux:
            print(f"ERREUR du diagnostic : {exc!r}", file=sys.stderr)
        return 2
