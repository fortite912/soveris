"""
============================================================
 Soveris - Coeur de l'agent de triage de support IT
============================================================

C'est ici que la "decision" est prise. L'agent fait 3 choses :

  1. CLASSIFIER   le ticket  (quelle categorie ? quel niveau ?)
  2. CHERCHER     une solution dans la base de connaissances
  3. DECIDER      : resolution automatique OU escalade vers un humain

Le moteur de scoring par mots-cles est le meme principe que celui
utilise dans mon premier POC (scoring d'offres d'emploi) : on compte
combien de mots-cles d'un article apparaissent dans la demande de
l'utilisateur, et l'article qui obtient le meilleur score gagne.

Ameliorations v2 :
  - correspondance par FRONTIERE DE MOT (regex \\b) : "mot" ne
    matche plus "motif", "down" ne matche plus "download".
  - en cas d'EGALITE de score entre un article N1 et un article N2,
    l'agent privilegie la PRUDENCE : il escalade (N2 gagne).
  - niveau de CONFIANCE affiche (selon le nombre de mots reconnus).
  - TEMPS DE TRAITEMENT mesure pour chaque ticket (en millisecondes).

Aucune librairie externe : tout est en Python standard.
============================================================
"""

import re
import time
import unicodedata
from collections import Counter

from connaissances import BASE_CONNAISSANCES
from .parametres import PARAMETRES

# Seuil de confiance : score pondere minimum pour que l'agent ose proposer
# une solution automatique. En dessous, par prudence, on escalade.
# (Alias historique ; la valeur vivante est PARAMETRES["seuil_confiance"].)
SEUIL_CONFIANCE = PARAMETRES["seuil_confiance"]


def normaliser(texte):
    """
    Met le texte en minuscules et retire les accents.
    Exemple : "Mon ordinateur est TRES lent !" -> "mon ordinateur est tres lent !"

    On normalise pour que "telephone", "Telephone" et "telephone"
    soient traites de la meme facon (bug classique des accents).
    """
    texte = texte.lower()
    # Decompose les caracteres accentues puis retire les accents
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    # Apostrophes et traits d'union deviennent des espaces : "partage d'ecran",
    # "partage d ecran" et "wi-fi" / "wi fi" sont alors identiques.
    texte = re.sub(r"[\u2019'`\-]+", " ", texte)
    return re.sub(r"\s+", " ", texte).strip()


# Nombre d'articles dans lesquels chaque mot-cle (normalise) apparait.
# Un mot partage par plusieurs articles ("acces", "connexion", "serveur")
# est moins discriminant qu'un mot propre a un seul article.
_FREQUENCE_MOTS = Counter(
    normaliser(mot) for article in BASE_CONNAISSANCES for mot in set(article["mots_cles"])
)


def poids_mot(mot_cle, parametres=None):
    """Poids d'un mot-cle selon les parametres (1.0 par defaut, comportement historique)."""
    p = parametres or PARAMETRES
    poids = 1.0
    if p["poids_partage"]:
        poids /= _FREQUENCE_MOTS.get(normaliser(mot_cle), 1)
    if " " in mot_cle.strip():
        poids *= p["poids_multimot"]
    return poids


def motif_mot(mot_cle, parametres=None):
    """Expression reguliere d'un mot-cle (frontiere de mot, pluriel optionnel)."""
    p = parametres or PARAMETRES
    suffixe = r"(?:s|x)?" if p["tolerance_pluriel"] else ""
    return r"\b" + re.escape(normaliser(mot_cle)) + suffixe + r"\b"


def scorer_article(texte_ticket, article, parametres=None):
    """
    Calcule le score d'un article face a la demande de l'utilisateur.
    Le score = somme des poids des mots-cles de l'article presents dans
    le ticket (tous les poids valent 1 avec les parametres historiques).

    La recherche se fait par FRONTIERE DE MOT (\\b en regex) :
    le mot-cle "mot" est reconnu dans "mot de passe" mais PAS dans
    "motif" ou "remote". Cela elimine les faux positifs du simple
    "in" (recherche de sous-chaine).

    Renvoie aussi la liste des mots-cles trouves (utile pour expliquer
    la decision a l'oral : "l'agent a reconnu les mots wifi et connexion").
    """
    texte_normalise = normaliser(texte_ticket)
    mots_trouves = []
    score = 0.0
    occupes = []  # portions du texte deja comptees : un meme mot du ticket
    #              ne peut pas valoir deux fois ("mail" et "mails" sur "mails")
    for mot_cle in article["mots_cles"]:
        for m in re.finditer(motif_mot(mot_cle, parametres), texte_normalise):
            if any(m.start() < fin and m.end() > debut for debut, fin in occupes):
                continue
            occupes.append((m.start(), m.end()))
            mots_trouves.append(mot_cle)
            score += poids_mot(mot_cle, parametres)
            break
    return round(score, 3), mots_trouves


def niveau_confiance(score):
    """
    Traduit le score brut en niveau de confiance lisible.
    Sert uniquement a l'affichage et au reporting : la DECISION,
    elle, reste regie par SEUIL_CONFIANCE et le niveau N1/N2.
    """
    if score >= 2.5:
        return "TRES HAUTE"
    if score >= 1.5:
        return "HAUTE"
    if score > 0:
        return "MOYENNE"
    return "NULLE"


def analyser(texte_ticket, parametres=None):
    """
    Fonction principale de l'agent.
    Prend un ticket en langage naturel et renvoie un resultat structure.

    Etapes :
      1. On score TOUS les articles de la base.
      2. On garde le meilleur. En cas d'egalite N1/N2, le N2 gagne :
         a score egal, l'agent prefere escalader que repondre a tort.
      3. On decide : resolution auto, escalade, ou demande non reconnue.

    Renvoie un dictionnaire avec toute la "tracabilite" de la decision,
    y compris le temps de traitement en millisecondes.
    """
    p = parametres or PARAMETRES
    depart = time.perf_counter()

    # --- Etape 1 : scorer tous les articles, meilleur N1 et meilleur N2 a part ---
    meilleurs = {"N1": (0.0, None, []), "N2": (0.0, None, [])}  # score, article, mots
    candidats = []  # (score, categorie) de tous les articles reconnus

    for article in BASE_CONNAISSANCES:
        score, mots = scorer_article(texte_ticket, article, p)
        if score == 0:
            continue
        candidats.append((score, article["categorie"]))
        if score > meilleurs[article["niveau"]][0]:
            meilleurs[article["niveau"]] = (score, article, mots)

    # --- Etape 2 : arbitrage N1 / N2 ---
    # La prudence l'emporte : le N2 gagne a egalite, et meme s'il est a moins
    # de `marge_n2` point(s) du meilleur N1 (0 = egalite stricte seulement).
    score_n1, article_n1, mots_n1 = meilleurs["N1"]
    score_n2, article_n2, mots_n2 = meilleurs["N2"]
    if article_n2 is not None and score_n2 >= score_n1 - p["marge_n2"]:
        meilleur_score, meilleur_article, meilleurs_mots = score_n2, article_n2, mots_n2
    else:
        meilleur_score, meilleur_article, meilleurs_mots = score_n1, article_n1, mots_n1

    # Ambiguite : un autre article d'une AUTRE categorie fait le meme score.
    ambigu = any(
        s == meilleur_score and meilleur_article is not None and cat != meilleur_article["categorie"]
        for s, cat in candidats
    )

    temps_ms = (time.perf_counter() - depart) * 1000

    base = {
        "texte": texte_ticket,
        "score": meilleur_score,
        "mots_reconnus": meilleurs_mots,
        "confiance": niveau_confiance(meilleur_score),
        "ambigu": ambigu,
        "temps_ms": round(temps_ms, 3),
    }

    # --- Etape 3 : decision ---
    # Cas A : aucun mot-cle reconnu -> on ne devine pas, on escalade.
    if meilleur_article is None or meilleur_score == 0:
        return {
            **base,
            "categorie": "Inconnu",
            "niveau": "N2",
            "decision": "ESCALADE",
            "motif": "Aucun mot-cle reconnu : qualification humaine requise.",
            "solution": None,
            "article_id": None,
        }

    # Cas B : l'incident est de niveau N2 -> escalade avec contexte.
    if meilleur_article["niveau"] == "N2":
        return {
            **base,
            "categorie": meilleur_article["categorie"],
            "niveau": "N2",
            "decision": "ESCALADE",
            "motif": "Incident sensible : escalade vers un ingenieur N2.",
            "solution": meilleur_article["solution"],  # contexte pour l'ingenieur
            "article_id": meilleur_article["id"],
        }

    # Cas C : niveau N1 mais confiance trop faible -> escalade par prudence.
    if meilleur_score < p["seuil_confiance"]:
        return {
            **base,
            "categorie": meilleur_article["categorie"],
            "niveau": "N1",
            "decision": "ESCALADE",
            "motif": "Confiance insuffisante pour une reponse automatique.",
            "solution": None,
            "article_id": meilleur_article["id"],
        }

    # Cas D : N1 + confiance suffisante -> RESOLUTION AUTOMATIQUE.
    return {
        **base,
        "categorie": meilleur_article["categorie"],
        "niveau": "N1",
        "decision": "RESOLUTION_AUTO",
        "motif": "Incident courant resolu automatiquement par l'agent.",
        "solution": meilleur_article["solution"],
        "article_id": meilleur_article["id"],
    }


def est_incertain(resultat):
    """
    Une decision est "incertaine" (a revoir par un humain) si :
      - aucun mot-cle n'a ete reconnu (categorie Inconnu), ou
      - le score est strictement inferieur a PARAMETRES["seuil_revue"], ou
      - deux articles de categories differentes sont a egalite (ambigu).
    Sert au journal (file "a revoir") et au diagnostic ; ne change pas la decision.
    """
    return (
        resultat["categorie"] == "Inconnu"
        or resultat["score"] < PARAMETRES["seuil_revue"]
        or resultat.get("ambigu", False)
    )


def traiter(texte_ticket):
    """
    Analyse ET journalise (usage "production" : demo, web).
    analyser() reste pure pour l'evaluation ; traiter() ajoute le journal local
    des decisions (sans donnee personnelle) et la file "a revoir".
    """
    from . import journal  # import local : le journal n'est charge qu'en usage reel
    resultat = analyser(texte_ticket)
    try:
        journal.consigner(resultat, est_incertain(resultat))
    except OSError:
        pass  # le journal ne doit jamais faire echouer le traitement
    return resultat


# Permet de tester ce module seul : python -m soveris demo
if __name__ == "__main__":
    exemples = [
        "Je n'arrive plus a me connecter au wifi",
        "J'ai oublie mon mot de passe et mon compte est bloque",
        "Mon poste affiche un message suspect de rancongiciel",
        "J'ai supprime un mail important",       # egalite N1/N2 -> prudence
        "Ou est la cantine ?",
    ]
    for texte in exemples:
        r = analyser(texte)
        print(f"\nTicket   : {texte}")
        print(f"  -> Categorie : {r['categorie']} ({r['niveau']})")
        print(f"  -> Decision  : {r['decision']}  [{r['motif']}]")
        print(f"  -> Confiance : {r['confiance']}  ({r['score']} mot(s) : {r['mots_reconnus']})")
        print(f"  -> Traite en : {r['temps_ms']} ms")
