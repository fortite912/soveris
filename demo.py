"""
============================================================
 Soveris - Demonstration (a lancer devant le jury)
============================================================

Deux modes :

  python demo.py            -> joue une serie de tickets d'exemple
                               puis affiche le tableau de bord (metriques).

  python demo.py --interactif  -> vous tapez vos propres tickets a la main
                                  (impressionnant en live : le jury propose
                                   une panne, vous la tapez, l'agent repond).

Affichage : couleurs ANSI natives (aucune librairie externe).
  - Les couleurs s'activent uniquement dans un vrai terminal.
  - Pour les desactiver : definir la variable d'environnement NO_COLOR.

Aucune librairie externe. Lancement immediat.
============================================================
"""

import os
import sys
import time

import soveris
import database

# ------------------------------------------------------------------
#  Couleurs ANSI (Python standard uniquement)
# ------------------------------------------------------------------

def _couleurs_actives():
    """
    Active les couleurs seulement si :
      - on est dans un vrai terminal (pas une redirection de fichier),
      - et l'utilisateur n'a pas demande NO_COLOR (standard reconnu).
    Sous Windows, os.system("") active le support des sequences ANSI.
    """
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    os.system("")  # active le mode VT (couleurs) dans la console Windows
    return True


# Sortie en UTF-8 pour les accents et caracteres graphiques.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

COULEURS = _couleurs_actives()

def c(texte, code):
    """Entoure le texte d'un code couleur ANSI (si les couleurs sont actives)."""
    return f"\033[{code}m{texte}\033[0m" if COULEURS else texte

VERT, ROUGE, JAUNE, CYAN, GRIS, GRAS = "92", "91", "93", "96", "90", "1"

LARGEUR = 64

# Quelques tickets realistes pour la demonstration automatique.
TICKETS_DEMO = [
    "Bonjour, je n'arrive plus a me connecter au wifi depuis ce matin",
    "J'ai oublie mon mot de passe, mon compte est verrouille",
    "Outlook ne s'ouvre plus, je ne recois plus mes mails",
    "L'imprimante du 2e etage fait un bourrage papier",
    "Mon ordinateur est tres lent et rame en permanence",
    "Je n'arrive pas a me connecter au VPN en teletravail",
    "Je n'ai plus acces au dossier partage du service",
    "J'ai recu un mail suspect de phishing, j'ai clique sur le lien",
    "Le serveur de production est down, personne ne peut travailler",
    "Est-ce qu'il va faire beau demain ?",
]


def banniere():
    """Affiche l'en-tete de la demonstration."""
    from connaissances import BASE_CONNAISSANCES
    nb = len(BASE_CONNAISSANCES)
    ligne = "─" * (LARGEUR - 2)
    # IMPORTANT : on calcule la largeur (ljust) AVANT de coloriser,
    # car les codes couleur ANSI sont invisibles mais comptent dans len().
    titre = "  SOVERIS · Agent de triage du support IT N1".ljust(LARGEUR - 2)
    sous = f"  100 % Python standard · 0 dependance · {nb} cas couverts".ljust(LARGEUR - 2)
    print(c(f"┌{ligne}┐", GRIS))
    print(c("│", GRIS) + c(titre, GRAS) + c("│", GRIS))
    print(c("│", GRIS) + c(sous, GRIS) + c("│", GRIS))
    print(c(f"└{ligne}┘", GRIS))


def afficher_resultat(numero, resultat):
    """Affiche proprement le traitement d'un ticket."""
    print(c("─" * LARGEUR, GRIS))
    print(f"{c('Ticket #' + str(numero), GRAS)} : {resultat['texte']}")

    if resultat["decision"] == "RESOLUTION_AUTO":
        etiquette = c(" RESOLU AUTO ", "1;30;42")     # noir sur vert
    else:
        etiquette = c("  ESCALADE   ", "1;97;41")     # blanc sur rouge

    confiance = resultat.get("confiance", "-")
    couleur_conf = VERT if resultat["score"] >= 2 else (JAUNE if resultat["score"] == 1 else ROUGE)
    print(
        f"  {etiquette}  "
        f"Categorie : {c(resultat['categorie'], GRAS)} ({resultat['niveau']})   "
        f"Confiance : {c(confiance, couleur_conf)}   "
        + c(f"{resultat['temps_ms']} ms", GRIS)
    )
    print(f"  Motif        : {resultat['motif']}")
    if resultat["mots_reconnus"]:
        print(f"  Mots reconnus: {c(', '.join(resultat['mots_reconnus']), CYAN)}")

    if resultat["decision"] == "RESOLUTION_AUTO":
        print("  Reponse envoyee a l'utilisateur :")
        for ligne in resultat["solution"].split("\n"):
            print(c(f"      {ligne}", GRIS))
    elif resultat["solution"]:
        print("  Contexte transmis a l'ingenieur :")
        for ligne in resultat["solution"].split("\n"):
            print(c(f"      {ligne}", GRIS))


def barre_progression(pourcentage, largeur=30):
    """Petite barre de progression textuelle pour le tableau de bord."""
    plein = round(pourcentage / 100 * largeur)
    return c("█" * plein, VERT) + c("░" * (largeur - plein), GRIS)


def afficher_tableau_de_bord():
    """Affiche les metriques (le R.O.I.) apres traitement."""
    m = database.calculer_metriques()
    print("\n" + c("═" * LARGEUR, GRIS))
    print(c(" TABLEAU DE BORD  -  indicateurs de pilotage (R.O.I.)", GRAS))
    print(c("═" * LARGEUR, GRIS))
    print(f"  Tickets traites            : {c(str(m['total']), GRAS)}")
    print(f"  Resolus automatiquement    : {c(str(m['resolus_auto']), VERT)}")
    print(f"  Escalades vers un humain   : {c(str(m['escalades']), JAUNE)}"
          + c(f"   (dont non reconnus : {m['non_reconnus']})", GRIS))
    print(f"  Taux de resolution auto    : {barre_progression(m['taux_resolution_auto'])} "
          + c(f"{m['taux_resolution_auto']} %", GRAS))
    print(f"  Temps moyen de traitement  : {c(str(m['temps_moyen_ms']) + ' ms / ticket', CYAN)}")
    print("\n  Volume par categorie :")
    for categorie, nombre in m["par_categorie"]:
        print(f"      {categorie:<18} : {nombre}")
    print(c("═" * LARGEUR, GRIS))
    if m["resolus_auto"] > 0:
        minutes = m["resolus_auto"] * 10
        print(f"  Lecture : {c(str(m['resolus_auto']), VERT)} sollicitations traitees sans mobiliser")
        print(f"  un ingenieur, soit ≈ {c(str(minutes) + ' min', GRAS)} de temps N1 preserve "
              + c("(hypothese 10 min/ticket)", GRIS))
    if m["non_reconnus"] > 0:
        print(c(f"  Boucle d'amelioration : {m['non_reconnus']} ticket(s) non reconnu(s) = "
                "piste(s) d'enrichissement de la base.", GRIS))
    print(c("═" * LARGEUR, GRIS))


def mode_automatique():
    """Joue tous les tickets de demonstration."""
    banniere()
    print(c(f"\n### DEMONSTRATION AUTOMATIQUE - {len(TICKETS_DEMO)} tickets representatifs ###\n", GRAS))
    for i, texte in enumerate(TICKETS_DEMO, start=1):
        resultat = soveris.traiter(texte)
        database.enregistrer(resultat)
        afficher_resultat(i, resultat)
        # Courte pause pour rendre la demonstration lisible en direct
        # (uniquement dans un vrai terminal, jamais dans les tests).
        if sys.stdout.isatty():
            time.sleep(0.35)
    afficher_tableau_de_bord()


def mode_interactif():
    """Permet de taper ses propres tickets (pour une demo live)."""
    banniere()
    print(c("\n### MODE INTERACTIF - decrivez un incident, ou 'q' pour terminer ###\n", GRAS))
    numero = 1
    while True:
        try:
            texte = input(c("Decrivez l'incident > ", CYAN)).strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C / Ctrl+Z : on termine proprement avec le tableau de bord.
            print()
            break
        if texte.lower() in ("quit", "q", "exit"):
            break
        if not texte:
            # Entree a vide (fausse manipulation) : on redemande,
            # on ne quitte pas la demonstration.
            continue
        resultat = soveris.traiter(texte)
        database.enregistrer(resultat)
        afficher_resultat(numero, resultat)
        numero += 1
    afficher_tableau_de_bord()


if __name__ == "__main__":
    # On repart d'une base propre a chaque demonstration.
    database.reinitialiser()

    if "--interactif" in sys.argv or "-i" in sys.argv:
        mode_interactif()
    else:
        mode_automatique()
