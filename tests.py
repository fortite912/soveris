"""
============================================================
 Soveris - Tests automatises
============================================================

Verifie le comportement attendu de l'agent : c'est le filet de
securite qui garantit qu'une modification (nouvel article, nouveau
mot-cle) ne casse pas une decision existante.

Lancement :  python tests.py
Resultat  :  liste des verifications, et "TOUS LES TESTS PASSENT"
             si le comportement de l'agent est conforme.

Aucune librairie externe : assertions en Python standard.
============================================================
"""

import soveris
import database
from connaissances import BASE_CONNAISSANCES

RESULTATS = []


def verifier(nom, condition, detail=""):
    """Enregistre le resultat d'une verification."""
    RESULTATS.append((nom, bool(condition), detail))


# ------------------------------------------------------------------
# 1. Cas nominaux : incidents courants -> resolution automatique (N1)
# ------------------------------------------------------------------
r = soveris.analyser("Je n'arrive plus a me connecter au wifi")
verifier("Wifi -> resolution automatique", r["decision"] == "RESOLUTION_AUTO", r["decision"])
verifier("Wifi -> categorie Reseau", r["categorie"] == "Reseau", r["categorie"])

r = soveris.analyser("J'ai oublie mon mot de passe, compte verrouille")
verifier("Mot de passe -> resolution automatique", r["decision"] == "RESOLUTION_AUTO", r["decision"])
verifier("Mot de passe -> categorie Compte / Acces", r["categorie"] == "Compte / Acces", r["categorie"])

r = soveris.analyser("Ma webcam ne marche plus sur Teams")
verifier("Peripherique/visio -> resolu (nouveaux articles)", r["decision"] == "RESOLUTION_AUTO", r["categorie"])

# ------------------------------------------------------------------
# 2. Cas sensibles : securite / infrastructure -> escalade N2
# ------------------------------------------------------------------
r = soveris.analyser("J'ai recu un mail de phishing tres suspect")
verifier("Phishing -> ESCALADE", r["decision"] == "ESCALADE", r["decision"])
verifier("Phishing -> categorie Securite (N2)", r["categorie"] == "Securite" and r["niveau"] == "N2",
         f"{r['categorie']}/{r['niveau']}")

r = soveris.analyser("Le serveur de production est down pour tout le monde")
verifier("Serveur down -> ESCALADE Infrastructure", r["decision"] == "ESCALADE"
         and r["categorie"] == "Infrastructure", r["categorie"])

# ------------------------------------------------------------------
# 3. Prudence : inconnu et egalite de score
# ------------------------------------------------------------------
r = soveris.analyser("Ou est la cantine ?")
verifier("Hors perimetre -> ESCALADE (jamais deviner)", r["decision"] == "ESCALADE"
         and r["categorie"] == "Inconnu", r["categorie"])

# "supprime" (N2 Donnees) et "mail" (N1 Messagerie) font 1 point chacun :
# a egalite, l'agent doit choisir la PRUDENCE (escalade N2).
r = soveris.analyser("J'ai supprime un mail important")
verifier("Egalite N1/N2 -> la prudence l'emporte (N2)", r["niveau"] == "N2", f"{r['categorie']}/{r['niveau']}")

# ------------------------------------------------------------------
# 4. Robustesse du matching (frontiere de mot)
# ------------------------------------------------------------------
r = soveris.analyser("Quel est le motif de votre visite ?")
verifier("'motif' ne declenche pas le mot-cle 'mot'", "mot" not in r["mots_reconnus"], str(r["mots_reconnus"]))

r = soveris.analyser("J'AI OUBLIE MON MOT DE PASSE !!!")
verifier("Majuscules/ponctuation sans effet", r["decision"] == "RESOLUTION_AUTO", r["decision"])

r = soveris.analyser("Je n'arrive pas a me connecter au reseau")
verifier("Accents normalises (reseau/réseau)", soveris.normaliser("réseau") == "reseau")

# ------------------------------------------------------------------
# 5. Performance et persistance
# ------------------------------------------------------------------
r = soveris.analyser("Mon ordinateur est lent")
verifier("Traitement < 50 ms (deterministe, sans GPU)", r["temps_ms"] < 50, f"{r['temps_ms']} ms")

database.reinitialiser()
database.enregistrer(r)
m = database.calculer_metriques()
verifier("Persistance SQLite (1 ticket enregistre)", m["total"] == 1, str(m["total"]))
verifier("Integrite de la base de connaissances",
         all({"id", "categorie", "niveau", "mots_cles", "solution"} <= set(a) for a in BASE_CONNAISSANCES)
         and all(a["niveau"] in ("N1", "N2") for a in BASE_CONNAISSANCES),
         f"{len(BASE_CONNAISSANCES)} articles")

# ------------------------------------------------------------------
# 6. Verrou du jeu de demonstration (le "70 %" presente au jury)
# ------------------------------------------------------------------
# Si un ajout dans la base de connaissances change le comportement
# sur les 10 tickets de reference, ce test echoue : le chiffre
# annonce au jury est ainsi protege contre toute regression.
from demo import TICKETS_DEMO

resultats_demo = [soveris.analyser(t) for t in TICKETS_DEMO]
nb_auto = sum(1 for r in resultats_demo if r["decision"] == "RESOLUTION_AUTO")
verifier("Jeu de demonstration verrouille : 7/10 resolus (70 %)", nb_auto == 7, f"{nb_auto}/10")

# ------------------------------------------------------------------
# 7. Verrou du banc de validation (50 tickets independants)
# ------------------------------------------------------------------
# Le banc mesure l'exactitude des decisions ET les fausses resolutions
# (l'agent qui repond a tort). Etat de reference : 46/50 corrects,
# zero fausse resolution dangereuse. Toute regression fait echouer.
import validation

b = validation.evaluer()
verifier("Validation 50 tickets : 46/50 decisions correctes (92 %)",
         b["corrects"] == 46, f"{b['corrects']}/50")
verifier("Validation : ZERO fausse resolution dangereuse",
         len(b["fausses_dangereuses"]) == 0, str(len(b["fausses_dangereuses"])))

# ------------------------------------------------------------------
# Bilan
# ------------------------------------------------------------------
if __name__ == "__main__":
    echecs = 0
    for nom, ok, detail in RESULTATS:
        statut = "OK " if ok else "ECHEC"
        complement = f"   [{detail}]" if (detail and not ok) else ""
        print(f"  [{statut}] {nom}{complement}")
        if not ok:
            echecs += 1
    print("-" * 56)
    total = len(RESULTATS)
    if echecs == 0:
        print(f"  TOUS LES TESTS PASSENT ({total}/{total})")
    else:
        print(f"  {echecs} echec(s) sur {total} tests")
        raise SystemExit(1)
