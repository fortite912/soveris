"""La calibration automatique : stabilite, gain reel, garde-fous (sans ecrire de fichier)."""
import unittest
from unittest import mock

from soveris import auto_amelioration, evaluation, parametres


class TestCalibration(unittest.TestCase):
    def test_grille_dans_les_plages(self):
        for cle, valeurs in auto_amelioration.GRILLE.items():
            for v in valeurs:
                parametres.valider({cle: v})

    def test_stabilite_a_objectif_egal(self):
        courant = parametres.charger()
        candidat, _, essais = auto_amelioration.explorer(courant)
        self.assertGreater(essais, 1)
        # Sans gain strict, la configuration courante est conservee telle quelle.
        obj_courant = auto_amelioration.objectif(evaluation.evaluer_jeu("dev", courant))
        obj_candidat = auto_amelioration.objectif(evaluation.evaluer_jeu("dev", candidat))
        if obj_candidat == obj_courant:
            self.assertEqual(candidat, courant)

    def test_retrouve_un_gain_depuis_les_defauts_historiques(self):
        historiques = dict(parametres.DEFAUTS)
        candidat, r_dev, _ = auto_amelioration.explorer(historiques)
        avant = evaluation.evaluer_jeu("dev", historiques)
        self.assertGreater(auto_amelioration.objectif(r_dev), auto_amelioration.objectif(avant))
        # Le gain trouve sur dev ne doit pas degrader le jeu gele (garde-fou G2)
        gele_avant = evaluation.evaluer_jeu("test", historiques)
        gele_apres = evaluation.evaluer_jeu("test", candidat)
        self.assertGreaterEqual(gele_apres["corrects"], gele_avant["corrects"])
        self.assertLessEqual(gele_apres["erreurs_critiques"], gele_avant["erreurs_critiques"])

    def test_mode_proposition_n_ecrit_pas_les_parametres(self):
        avant = parametres.charger()
        with mock.patch.object(auto_amelioration, "_ecrire"):
            code = auto_amelioration.executer(appliquer=False, silencieux=True)
        self.assertIn(code, (0, 1))
        self.assertEqual(parametres.charger(), avant)


if __name__ == "__main__":
    unittest.main()
