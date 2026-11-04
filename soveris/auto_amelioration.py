"""
============================================================
 Soveris - Auto-amelioration controlee (recalibrage des parametres)
============================================================

Mecanisme retenu (voir docs/AUTO_AMELIORATION.md) : recherche exhaustive,
deterministe et bornee des PARAMETRES du moteur (soveris/parametres.json)
sur les donnees de DEV, puis application seulement si TOUS les garde-fous
passent. La base de connaissances et le code ne sont jamais modifies
automatiquement.

Objectif sur dev (ordre lexicographique) :
  1. moins d'erreurs critiques (fausses resolutions)
  2. plus de decisions correctes
  3. moins d'escalades critiques mal orientees
Le seuil de revue est choisi a part : couvrir le plus d'erreurs de dev avec
le moins de cas signales.

Garde-fous avant application :
  G1  amelioration STRICTE de l'objectif sur dev
  G2  aucune regression sur le jeu GELE (corrects, erreurs critiques)
  G3  aucune regression sur les synthetiques
  G4  parametres dans leurs plages (parametres.valider)
  G5  suites de tests vertes avec les nouveaux parametres (dont test reseau)
  G6  entree au journal (docs/JOURNAL_AMELIORATIONS.md) + baseline refigee
  Le changement tient dans un fichier : reversible par `git revert`.

Usage : python -m soveris calibrer [--appliquer] [--commit]
Codes de sortie : 0 rien a changer ou applique ; 1 garde-fou en echec ; 2 erreur.
============================================================
"""

import itertools
import json
import os
import shutil
import subprocess
import sys
import time

from . import evaluation, parametres

RACINE = evaluation.RACINE
CHEMIN_JOURNAL = os.path.join(RACINE, "docs", "JOURNAL_AMELIORATIONS.md")

GRILLE = {
    "tolerance_pluriel": [False, True],
    "poids_partage": [False, True],
    "poids_multimot": [1.0, 1.5, 2.0],
    "marge_n2": [0.0, 0.5, 1.0, 1.5],
    "seuil_confiance": [0.5, 1.0, 1.5],
}
GRILLE_REVUE = [0.5, 1.0, 1.5, 2.0]


def objectif(rapport):
    """Tuple a MAXIMISER (lexicographique)."""
    return (-rapport["erreurs_critiques"], rapport["corrects"], -rapport["critiques_mal_orientees"])


def _lignes(jeu, p):
    return [evaluation.evaluer_cas(c, p) for c in evaluation.charger_jeu(jeu)]


def choisir_seuil_revue(p, lignes_dev):
    """
    Pour chaque seuil candidat : combien d'erreurs de dev sont signalees
    "incertaines" (couverture) et combien de cas sont signales au total (cout).
    On prend la couverture maximale, puis le cout minimal, puis le seuil courant
    s'il est a egalite (stabilite), sinon le plus bas.
    """
    erreurs = [l for l in lignes_dev if l["verdict"] != "CORRECT"]
    meilleur = None
    for seuil in GRILLE_REVUE:
        def incertain(l):
            return l["categorie"] == "Inconnu" or l["score"] < seuil or l["ambigu"]
        couverture = sum(1 for l in erreurs if incertain(l))
        cout = sum(1 for l in lignes_dev if incertain(l))
        cle = (couverture, -cout, seuil == p.get("seuil_revue"), -seuil)
        if meilleur is None or cle > meilleur[0]:
            meilleur = (cle, seuil, couverture, cout)
    _, seuil, couverture, cout = meilleur
    return seuil, {"couverture_erreurs": f"{couverture}/{len(erreurs)}", "cas_signales": f"{cout}/{len(lignes_dev)}"}


def explorer(courant):
    """Parcourt la grille sur dev ; renvoie (meilleurs parametres, rapport dev, nb essais)."""
    cles = list(GRILLE)
    # La configuration courante est evaluee en premier : a objectif EGAL elle
    # est toujours conservee (stabilite : pas de changement sans gain strict).
    meilleur_p = dict(courant)
    meilleur_r = evaluation.construire_rapport("dev", _lignes("dev", courant))
    meilleur_obj = objectif(meilleur_r)
    essais = 1
    for valeurs in itertools.product(*(GRILLE[k] for k in cles)):
        p = dict(courant)
        p.update(dict(zip(cles, valeurs)))
        if p == courant:
            continue
        try:
            parametres.valider(p)
        except ValueError:
            continue
        essais += 1
        r = evaluation.construire_rapport("dev", _lignes("dev", p))
        obj = objectif(r)
        # Gain strict requis ; a gain egal, le candidat qui change le MOINS de
        # parametres par rapport au courant est prefere (changement minimal).
        nb_chg = sum(1 for k in p if p[k] != courant.get(k))
        if obj > meilleur_obj or (obj == meilleur_obj and meilleur_p != courant
                                  and nb_chg < sum(1 for k in meilleur_p if meilleur_p[k] != courant.get(k))):
            meilleur_p, meilleur_r, meilleur_obj = p, r, obj
    return meilleur_p, meilleur_r, essais


def lancer_tests():
    for commande in ([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                     [sys.executable, "tests.py"]):
        proc = subprocess.run(commande, cwd=RACINE, capture_output=True, text=True)
        if proc.returncode != 0:
            return False, (proc.stdout + proc.stderr)[-1500:]
    return True, ""


def entree_journal(avant, apres, p_avant, p_apres):
    diff = {k: (p_avant[k], p_apres[k]) for k in p_apres if p_avant.get(k) != p_apres[k]}
    lignes = [
        "",
        f"### Calibration automatique du {time.strftime('%Y-%m-%d %H:%M')}",
        "",
        "Commit : celui qui introduit cette entrée (`git log -1 -- docs/JOURNAL_AMELIORATIONS.md`) ; "
        "réversible par `git revert`. Détail dans `reports/calibration.json`.",
        "",
        "| Paramètre | Avant | Après |", "|---|---|---|",
    ] + [f"| `{k}` | {a} | {b} |" for k, (a, b) in diff.items()] + [
        "",
        "| Jeu | Avant | Après |", "|---|---|---|",
    ] + [f"| {jeu} | {avant[jeu]['corrects']}/{avant[jeu]['total']}, {avant[jeu]['erreurs_critiques']} crit. "
         f"| {apres[jeu]['corrects']}/{apres[jeu]['total']}, {apres[jeu]['erreurs_critiques']} crit. |"
         for jeu in ("dev", "test", "synthetique")] + [""]
    with open(CHEMIN_JOURNAL, "a", encoding="utf-8") as f:
        f.write("\n".join(lignes))


def executer(appliquer=False, commit=False, silencieux=False):
    def dire(*a):
        if not silencieux:
            print(*a)
    try:
        courant = parametres.charger()
        rapports_avant = {jeu: evaluation.resume(evaluation.evaluer_jeu(jeu, courant)) for jeu in evaluation.FICHIERS_JEUX}
        obj_avant = objectif(evaluation.evaluer_jeu("dev", courant))

        candidat, r_dev, essais = explorer(courant)
        lignes_dev = _lignes("dev", candidat)
        candidat["seuil_revue"], info_revue = choisir_seuil_revue(candidat, lignes_dev)
        obj_apres = objectif(r_dev)

        rapport = {
            "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "essais": essais,
            "parametres_courants": courant,
            "parametres_candidats": candidat,
            "objectif_avant": obj_avant,
            "objectif_apres": obj_apres,
            "seuil_revue": info_revue,
            "garde_fous": {},
            "applique": False,
        }
        gf = rapport["garde_fous"]

        changement = {k for k in candidat if candidat[k] != courant.get(k)}
        gf["G1_amelioration_dev"] = obj_apres > obj_avant
        if not changement:
            rapport["verdict"] = "aucun changement : les parametres courants sont deja optimaux sur dev"
            dire(rapport["verdict"])
            _ecrire(rapport)
            return 0
        if not gf["G1_amelioration_dev"]:
            # Seul le seuil de revue change (sans effet sur les decisions) : on
            # l'accepte si les autres garde-fous passent, mais sans pretendre a un gain.
            if changement - {"seuil_revue"}:
                rapport["verdict"] = "rejet : aucun gain strict sur dev"
                dire(rapport["verdict"])
                _ecrire(rapport)
                return 0

        r_test = evaluation.resume(evaluation.evaluer_jeu("test", candidat))
        r_syn = evaluation.resume(evaluation.evaluer_jeu("synthetique", candidat))
        gf["G2_jeu_gele_sans_regression"] = (r_test["corrects"] >= rapports_avant["test"]["corrects"]
                                             and r_test["erreurs_critiques"] <= rapports_avant["test"]["erreurs_critiques"])
        gf["G3_synthetiques_sans_regression"] = (r_syn["corrects"] >= rapports_avant["synthetique"]["corrects"]
                                                 and r_syn["erreurs_critiques"] <= rapports_avant["synthetique"]["erreurs_critiques"])
        try:
            parametres.valider(candidat)
            gf["G4_plages"] = True
        except ValueError as exc:
            gf["G4_plages"] = False
            rapport["erreur_plages"] = str(exc)
        rapports_apres = {"dev": evaluation.resume(r_dev), "test": r_test, "synthetique": r_syn}
        rapport["avant"], rapport["apres"] = rapports_avant, rapports_apres

        if not all(gf.values()):
            rapport["verdict"] = "rejet : garde-fou en echec " + str({k: v for k, v in gf.items() if not v})
            dire(rapport["verdict"])
            _ecrire(rapport)
            return 1

        dire(f"Proposition ({essais} essais) : " + ", ".join(f"{k}: {courant.get(k)} -> {candidat[k]}" for k in sorted(changement)))
        dire(f"  dev  {rapports_avant['dev']['corrects']}/{rapports_avant['dev']['total']} -> {rapports_apres['dev']['corrects']}/{rapports_apres['dev']['total']}"
             f"  (crit. {rapports_avant['dev']['erreurs_critiques']} -> {rapports_apres['dev']['erreurs_critiques']})")
        dire(f"  gele {rapports_avant['test']['corrects']}/{rapports_avant['test']['total']} -> {r_test['corrects']}/{r_test['total']}"
             f"  (crit. {rapports_avant['test']['erreurs_critiques']} -> {r_test['erreurs_critiques']})")
        if not appliquer:
            rapport["verdict"] = "proposition (non appliquee : relancer avec --appliquer)"
            _ecrire(rapport)
            return 0

        # --- Application reversible : sauvegarde, ecriture, tests, journal ---
        sauvegarde = parametres.CHEMIN + ".bak"
        shutil.copyfile(parametres.CHEMIN, sauvegarde)
        parametres.ecrire(candidat)
        ok, sortie = lancer_tests()
        gf["G5_tests_verts"] = ok
        if not ok:
            shutil.move(sauvegarde, parametres.CHEMIN)
            rapport["verdict"] = "rejet : tests en echec avec les nouveaux parametres (restaures)"
            rapport["sortie_tests"] = sortie
            dire(rapport["verdict"])
            _ecrire(rapport)
            return 1
        os.remove(sauvegarde)
        # Baseline refigee dans un sous-processus (le module charge les parametres a l'import)
        subprocess.run([sys.executable, "-m", "soveris", "evaluer", "--figer-baseline"], cwd=RACINE,
                       capture_output=True, text=True, check=True)
        entree_journal(rapports_avant, rapports_apres, courant, candidat)
        gf["G6_journal"] = True
        hash_commit = None
        if commit:
            subprocess.run(["git", "add", parametres.CHEMIN, CHEMIN_JOURNAL,
                            os.path.join(RACINE, "reports", "baseline.json")], cwd=RACINE, check=True)
            message = ("Calibration automatique des parametres (dev "
                       f"{rapports_avant['dev']['corrects']}->{rapports_apres['dev']['corrects']}/{rapports_apres['dev']['total']}, "
                       f"gele {rapports_avant['test']['corrects']}->{r_test['corrects']}/{r_test['total']})")
            subprocess.run(["git", "commit", "-q", "-m", message], cwd=RACINE, check=True)
            hash_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RACINE,
                                         capture_output=True, text=True, check=True).stdout.strip()
        rapport["applique"] = True
        rapport["commit"] = hash_commit
        rapport["verdict"] = "applique" + (f" (commit {hash_commit}, reversible par git revert)" if hash_commit else "")
        dire(rapport["verdict"])
        _ecrire(rapport)
        return 0
    except Exception as exc:
        if not silencieux:
            print(f"ERREUR de la calibration : {exc!r}", file=sys.stderr)
        return 2


def _ecrire(rapport):
    os.makedirs(evaluation.DOSSIER_RAPPORTS, exist_ok=True)
    with open(os.path.join(evaluation.DOSSIER_RAPPORTS, "calibration.json"), "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=1, default=str)
