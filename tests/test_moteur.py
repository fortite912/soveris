"""Tests unitaires du moteur et de l'evaluation (comportements, pas de cas de jeux de test)."""
import unittest

import soveris
from soveris import evaluation


class TestMoteur(unittest.TestCase):
    def test_normalisation(self):
        self.assertEqual(soveris.normaliser("Réseau TÉLÉPHONE"), "reseau telephone")

    def test_resultat_structure(self):
        r = soveris.analyser("mon imprimante fait un bourrage papier")
        for cle in ("texte", "score", "mots_reconnus", "confiance", "ambigu", "temps_ms",
                    "categorie", "niveau", "decision", "motif", "solution", "article_id"):
            self.assertIn(cle, r)
        self.assertEqual(r["decision"], "RESOLUTION_AUTO")

    def test_inconnu_est_incertain_et_escalade(self):
        r = soveris.analyser("xyzzy plugh")
        self.assertEqual(r["decision"], "ESCALADE")
        self.assertEqual(r["categorie"], "Inconnu")
        self.assertTrue(soveris.est_incertain(r))

    def test_n2_prime_sur_n1_a_egalite(self):
        r = soveris.analyser("J'ai supprime un mail important")
        self.assertEqual(r["niveau"], "N2")
        self.assertTrue(r["ambigu"])

    def test_texte_vide(self):
        r = soveris.analyser("")
        self.assertEqual(r["decision"], "ESCALADE")

    def test_determinisme(self):
        a = soveris.analyser("le vpn ne marche pas")
        b = soveris.analyser("le vpn ne marche pas")
        self.assertEqual((a["decision"], a["categorie"], a["score"]), (b["decision"], b["categorie"], b["score"]))


class TestEvaluation(unittest.TestCase):
    def test_verdicts(self):
        cas_auto = {"attendu": "RESOLUTION_AUTO", "categories": ["Reseau"], "critique": False}
        cas_crit = {"attendu": "ESCALADE", "categories": ["Securite"], "critique": True}
        cas_hors = {"attendu": "ESCALADE", "categories": ["Inconnu"], "critique": False}
        auto_reseau = {"decision": "RESOLUTION_AUTO", "categorie": "Reseau"}
        auto_autre = {"decision": "RESOLUTION_AUTO", "categorie": "Messagerie"}
        escalade = {"decision": "ESCALADE", "categorie": "Inconnu"}
        self.assertEqual(evaluation.verdict(cas_auto, auto_reseau), "CORRECT")
        self.assertEqual(evaluation.verdict(cas_auto, auto_autre), "MAL_CATEGORISE")
        self.assertEqual(evaluation.verdict(cas_auto, escalade), "MANQUE")
        self.assertEqual(evaluation.verdict(cas_crit, auto_autre), "FAUSSE_DANGEREUSE")
        self.assertEqual(evaluation.verdict(cas_hors, auto_autre), "FAUSSE_HORS_PERIMETRE")
        self.assertEqual(evaluation.verdict(cas_crit, escalade), "CORRECT")

    def test_rapport_complet(self):
        r = evaluation.evaluer_jeu("dev")
        self.assertEqual(r["total"], len(evaluation.charger_jeu("dev")))
        self.assertIn("matrice_confusion", r)
        self.assertIn("par_classe", r)
        md = evaluation.rendre_markdown(r)
        self.assertIn("Matrice de confusion", md)

    def test_jeu_inconnu(self):
        with self.assertRaises(ValueError):
            evaluation.charger_jeu("inexistant")


if __name__ == "__main__":
    unittest.main()
