"""Journal local (sans donnees personnelles), file a revoir, integration des corrections, diagnostic."""
import json
import os
import tempfile
import unittest
from unittest import mock

import soveris
from soveris import journal, diagnostic, evaluation


class TestJournal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.p_dec = mock.patch.object(journal, "CHEMIN_DECISIONS", os.path.join(d, "decisions.jsonl"))
        self.p_rev = mock.patch.object(journal, "CHEMIN_A_REVOIR", os.path.join(d, "a_revoir.jsonl"))
        self.p_dir = mock.patch.object(journal, "DOSSIER_JOURNAL", d)
        self.p_dev = mock.patch.object(journal, "CHEMIN_DEV", os.path.join(d, "dev.json"))
        for p in (self.p_dec, self.p_rev, self.p_dir, self.p_dev):
            p.start()
        with open(journal.CHEMIN_DEV, "w", encoding="utf-8") as f:
            json.dump({"description": "test", "cas": []}, f)

    def tearDown(self):
        for p in (self.p_dec, self.p_rev, self.p_dir, self.p_dev):
            p.stop()
        self.tmp.cleanup()

    def test_pseudonymisation(self):
        t = journal.pseudonymiser("Jean DUPONT jean.dupont@ex.fr tel 06 12 34 56 78 badge 123456 http://x.y/z")
        for interdit in ("DUPONT", "@", "06 12", "123456", "http"):
            self.assertNotIn(interdit, t)

    def test_decisions_sans_texte(self):
        r = soveris.traiter("Mon mot de passe pour jean.dupont@ex.fr est refuse")
        self.assertEqual(r["decision"], "RESOLUTION_AUTO")
        with open(journal.CHEMIN_DECISIONS, encoding="utf-8") as f:
            contenu = f.read()
        self.assertNotIn("jean.dupont", contenu)
        self.assertNotIn("texte", json.loads(contenu.splitlines()[0]))

    def test_file_a_revoir_et_integration(self):
        soveris.traiter("xyzzy totalement inconnu")  # Inconnu -> incertain
        etat = journal.etat_file_revue()
        self.assertEqual(etat["en_attente"], 1)
        # un humain corrige
        cas = journal._lire(journal.CHEMIN_A_REVOIR)
        cas[0]["correction"] = {"attendu": "ESCALADE", "categories": ["Inconnu"], "critique": False}
        with open(journal.CHEMIN_A_REVOIR, "w", encoding="utf-8") as f:
            f.write(json.dumps(cas[0]) + "\n")
        self.assertEqual(journal.integrer_revues(), 1)
        self.assertEqual(journal.integrer_revues(), 0)  # idempotent
        with open(journal.CHEMIN_DEV, encoding="utf-8") as f:
            dev = json.load(f)
        self.assertEqual(dev["cas"][0]["source"], "revue")
        self.assertEqual(dev["cas"][0]["attendu"], "ESCALADE")


class TestDiagnostic(unittest.TestCase):
    def test_comparaison_detecte_regression(self):
        rapports = {"test": evaluation.evaluer_jeu("test")}
        ref = {"jeux": {"test": evaluation.resume(rapports["test"])}}
        self.assertEqual(diagnostic.comparer(rapports, ref), [])
        pire = json.loads(json.dumps(ref))
        pire["jeux"]["test"]["precision"] += 10
        pire["jeux"]["test"]["erreurs_critiques"] = -1
        ecarts = diagnostic.comparer(rapports, pire)
        self.assertEqual({e["indicateur"] for e in ecarts}, {"precision", "erreurs_critiques"})
        self.assertTrue(all(e["priorite"] == diagnostic.P1 for e in ecarts))

    def test_code_sortie_sans_regression(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = os.path.join(d, "baseline.json")
            evaluation.ecrire_baseline(chemin)
            self.assertEqual(diagnostic.executer(baseline=chemin, lancer_tests=False, ecrire=False, silencieux=True), 0)

    def test_code_sortie_avec_regression(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = os.path.join(d, "baseline.json")
            b = evaluation.ecrire_baseline(chemin)
            b["jeux"]["test"]["precision"] = 100.0
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(b, f)
            self.assertEqual(diagnostic.executer(baseline=chemin, lancer_tests=False, ecrire=False, silencieux=True), 1)


if __name__ == "__main__":
    unittest.main()
