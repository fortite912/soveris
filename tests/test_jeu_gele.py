"""
Le jeu de test GELE ne doit jamais etre modifie pour ameliorer un score.
Ce test compare l'empreinte SHA-256 du fichier a la valeur figee ici.
Toute modification (ajout, suppression, correction d'etiquette) le fait
echouer : il faut alors une decision explicite et documentee, pas un
ajustement discret.
"""
import hashlib
import json
import os
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEMIN = os.path.join(RACINE, "data", "test_gele.json")

# Empreinte du contenu CANONIQUE des cas (independante de la mise en forme).
EMPREINTE_ATTENDUE = "cbc5ff91a2a50fd38670c0e1f82bd2e4fafa520bb75d559b444655006463d877"
NOMBRE_CAS = 50


def empreinte_canonique(chemin=CHEMIN):
    with open(chemin, encoding="utf-8") as f:
        cas = json.load(f)["cas"]
    canonique = json.dumps(cas, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonique.encode("utf-8")).hexdigest(), len(cas)


class TestJeuGele(unittest.TestCase):
    def test_empreinte_inchangee(self):
        empreinte, n = empreinte_canonique()
        self.assertEqual(n, NOMBRE_CAS, "le nombre de cas du jeu gele a change")
        self.assertEqual(empreinte, EMPREINTE_ATTENDUE,
                         "data/test_gele.json a ete modifie : interdit sans decision documentee")

    def test_dev_et_synthetiques_disjoints_du_gele(self):
        with open(CHEMIN, encoding="utf-8") as f:
            geles = {c["texte"] for c in json.load(f)["cas"]}
        for nom in ("dev.json", "synthetiques.json"):
            with open(os.path.join(RACINE, "data", nom), encoding="utf-8") as f:
                cas = json.load(f)["cas"]
            self.assertTrue(all(c["source"] != "test_gele" for c in cas), nom)
            doublons = [c["texte"] for c in cas if c["texte"] in geles]
            self.assertEqual(doublons, [], f"{nom} contient des cas du jeu gele")

    def test_synthetiques_marques_generes(self):
        with open(os.path.join(RACINE, "data", "synthetiques.json"), encoding="utf-8") as f:
            cas = json.load(f)["cas"]
        self.assertTrue(cas and all(c["source"] == "generes" for c in cas))


if __name__ == "__main__":
    unittest.main()
