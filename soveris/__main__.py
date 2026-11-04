"""
Point d'entree en ligne de commande : python -m soveris <commande>

  evaluer   [--jeu dev|test|synthetique|tous]   evaluation reproductible (JSON + Markdown)
  diagnose  [--baseline reports/baseline.json]   auto-diagnostic (code de sortie CI)
  calibrer  [--appliquer]                        auto-amelioration controlee
  integrer-revues                                verse les cas corriges de la file "a revoir" dans dev
  demo                                           quelques exemples
"""
import argparse
import sys


def main(argv=None):
    parseur = argparse.ArgumentParser(prog="python -m soveris", description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = parseur.add_subparsers(dest="commande")

    p_eval = sous.add_parser("evaluer", help="evaluation reproductible")
    p_eval.add_argument("--jeu", default="dev", choices=["dev", "test", "synthetique", "tous"])
    p_eval.add_argument("--sans-ecriture", action="store_true", help="n'ecrit pas de rapport")
    p_eval.add_argument("--figer-baseline", action="store_true",
                        help="evalue les trois jeux et ecrit reports/baseline.json")

    p_diag = sous.add_parser("diagnose", help="auto-diagnostic complet")
    p_diag.add_argument("--baseline", default=None)
    p_diag.add_argument("--sans-tests", action="store_true", help="n'execute pas les suites de tests")

    p_cal = sous.add_parser("calibrer", help="auto-amelioration controlee")
    p_cal.add_argument("--appliquer", action="store_true", help="ecrit les parametres retenus")

    sous.add_parser("integrer-revues", help="integre les corrections de la file a revoir dans dev")
    sous.add_parser("demo", help="exemples")

    args = parseur.parse_args(argv)

    if args.commande == "evaluer":
        from . import evaluation
        if args.figer_baseline:
            import subprocess
            try:
                commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                                        text=True, check=True).stdout.strip()
            except Exception:
                commit = None
            b = evaluation.ecrire_baseline(commit=commit)
            for nom, r in b["jeux"].items():
                print(f"baseline {nom:12}: {r['corrects']}/{r['total']} ({r['precision']} %), "
                      f"critiques {r['erreurs_critiques']}")
            return 0
        rapport = evaluation.evaluer_jeu(args.jeu)
        if not args.sans_ecriture:
            js, md = evaluation.ecrire_rapports(rapport)
            print(f"Rapports : {js}\n          {md}")
        print(f"Jeu {args.jeu} : {rapport['corrects']}/{rapport['total']} corrects "
              f"({rapport['precision']} %), erreurs critiques : {rapport['erreurs_critiques']}, "
              f"incertains : {rapport['incertains']}")
        return 0

    if args.commande == "diagnose":
        from . import diagnostic
        return diagnostic.executer(baseline=args.baseline, lancer_tests=not args.sans_tests)

    if args.commande == "calibrer":
        from . import auto_amelioration
        return auto_amelioration.executer(appliquer=args.appliquer)

    if args.commande == "integrer-revues":
        from . import journal
        n = journal.integrer_revues()
        print(f"{n} cas corrige(s) integre(s) dans data/dev.json")
        return 0

    if args.commande == "demo":
        from . import analyser
        for texte in ["Je n'arrive plus a me connecter au wifi",
                      "J'ai supprime un mail important", "Ou est la cantine ?"]:
            r = analyser(texte)
            print(f"{texte!r} -> {r['decision']} / {r['categorie']} (score {r['score']})")
        return 0

    parseur.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
