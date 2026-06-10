"""
============================================================
 Soveris - Persistance SQLite et metriques
============================================================

Chaque ticket traite est enregistre dans une base SQLite.
A partir de ces donnees, on calcule les metriques qui interessent
une Direction des Systemes d'Information (le R.O.I.) :

  - taux de resolution automatique (= % de tickets traites SANS humain)
  - volume par categorie
  - nombre de tickets escalades
  - tickets NON RECONNUS (pistes d'enrichissement de la base)
  - temps moyen de traitement par ticket (millisecondes)

sqlite3 fait partie de Python standard : aucune installation requise.
============================================================
"""

import os
import sqlite3
from datetime import datetime

# Chemin ABSOLU, construit a partir de l'emplacement de ce fichier :
# la base est toujours creee a cote du code, peu importe le dossier
# depuis lequel on lance la demonstration. (Robustesse "jour J".)
NOM_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "soveris.db")


def connexion():
    """Ouvre une connexion vers la base SQLite (creee si absente)."""
    return sqlite3.connect(NOM_BASE)


def init_base():
    """
    Cree la table 'tickets' si elle n'existe pas encore.
    Une seule table suffit pour ce POC : on reste simple et lisible.
    """
    with connexion() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                horodatage    TEXT,
                texte         TEXT,
                categorie     TEXT,
                niveau        TEXT,
                decision      TEXT,
                score         INTEGER,
                article_id    TEXT,
                temps_ms      REAL
            )
            """
        )


def enregistrer(resultat):
    """
    Enregistre en base le resultat renvoye par l'agent (soveris.analyser).
    'resultat' est le dictionnaire produit par la fonction analyser().
    """
    with connexion() as conn:
        conn.execute(
            """
            INSERT INTO tickets
                (horodatage, texte, categorie, niveau, decision, score, article_id, temps_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                resultat["texte"],
                resultat["categorie"],
                resultat["niveau"],
                resultat["decision"],
                resultat["score"],
                resultat["article_id"],
                resultat.get("temps_ms"),
            ),
        )


def calculer_metriques():
    """
    Calcule les indicateurs cles a partir de tous les tickets enregistres.
    Renvoie un dictionnaire pret a etre affiche.
    """
    with connexion() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]

        # Nombre de tickets resolus automatiquement (sans intervention humaine)
        resolus = conn.execute(
            "SELECT COUNT(*) FROM tickets WHERE decision = 'RESOLUTION_AUTO'"
        ).fetchone()[0]

        escalades = total - resolus

        # Tickets non reconnus par la base : chaque occurrence est une piste
        # d'enrichissement de la base de connaissances (boucle d'amelioration).
        non_reconnus = conn.execute(
            "SELECT COUNT(*) FROM tickets WHERE categorie = 'Inconnu'"
        ).fetchone()[0]

        # Temps moyen de traitement (ms) - preuve du cout de calcul plancher.
        temps_moyen = conn.execute(
            "SELECT AVG(temps_ms) FROM tickets WHERE temps_ms IS NOT NULL"
        ).fetchone()[0]

        # Volume par categorie (GROUP BY : meme technique que dans mon bot)
        par_categorie = conn.execute(
            """
            SELECT categorie, COUNT(*)
            FROM tickets
            GROUP BY categorie
            ORDER BY COUNT(*) DESC
            """
        ).fetchall()

    taux_auto = (resolus / total * 100) if total > 0 else 0

    return {
        "total": total,
        "resolus_auto": resolus,
        "escalades": escalades,
        "non_reconnus": non_reconnus,
        "taux_resolution_auto": round(taux_auto, 1),
        "temps_moyen_ms": round(temps_moyen, 3) if temps_moyen is not None else 0,
        "par_categorie": par_categorie,
    }


def reinitialiser():
    """Vide la table (utile pour relancer une demonstration propre)."""
    with connexion() as conn:
        conn.execute("DROP TABLE IF EXISTS tickets")
    init_base()


# Permet de tester ce fichier seul : python database.py
if __name__ == "__main__":
    init_base()
    print(f"Base '{NOM_BASE}' initialisee.")
    print("Metriques actuelles :", calculer_metriques())
