"""
Le moteur est 100 % local : AUCUN appel reseau a l'execution.

Deux verrous complementaires :
  1. statique  : les modules du moteur n'importent aucune bibliotheque reseau ;
  2. dynamique : toute tentative d'ouvrir une socket pendant l'analyse,
                 l'evaluation ou le diagnostic leve une exception.
"""
import os
import re
import socket
import unittest
from unittest import mock

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES_MOTEUR = [
    os.path.join(RACINE, "connaissances.py"),
    os.path.join(RACINE, "database.py"),
] + [os.path.join(RACINE, "soveris", f) for f in os.listdir(os.path.join(RACINE, "soveris")) if f.endswith(".py")]

IMPORTS_INTERDITS = re.compile(
    r"^\s*(import|from)\s+(urllib|http\.client|http\s*$|socket|ssl|requests|httpx|aiohttp|ftplib|smtplib|xmlrpc|telnetlib)\b",
    re.MULTILINE,
)


def _interdire(*args, **kwargs):
    raise AssertionError("Appel reseau detecte : le moteur doit rester 100 % local")


class TestAucunReseau(unittest.TestCase):
    def test_aucun_import_reseau_dans_le_moteur(self):
        for chemin in MODULES_MOTEUR:
            with open(chemin, encoding="utf-8") as f:
                source = f.read()
            self.assertIsNone(IMPORTS_INTERDITS.search(source),
                              f"{os.path.basename(chemin)} importe une bibliotheque reseau")

    def test_aucune_socket_pendant_analyse_evaluation_diagnostic(self):
        import soveris
        from soveris import evaluation, diagnostic

        with mock.patch.object(socket, "socket", side_effect=_interdire), \
             mock.patch.object(socket, "create_connection", side_effect=_interdire), \
             mock.patch.object(socket, "getaddrinfo", side_effect=_interdire):
            for nom in ("test", "dev", "synthetique"):
                for cas in evaluation.charger_jeu(nom):
                    soveris.analyser(cas["texte"])
            rapport = evaluation.evaluer_jeu("dev")
            self.assertGreater(rapport["total"], 0)
            # Diagnostic complet sans sous-processus de tests (ils sont deja en cours)
            code = diagnostic.executer(lancer_tests=False, ecrire=False, silencieux=True)
            self.assertIn(code, (0, 1, 2))


if __name__ == "__main__":
    unittest.main()
