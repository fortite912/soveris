"""
============================================================
 Soveris - Base de connaissances (Knowledge Base)
============================================================

C'est le "cerveau metier" de l'agent Soveris : la liste des incidents
de support IT que l'agent sait reconnaitre et resoudre.

Chaque article contient :
  - id          : identifiant unique
  - categorie   : famille de l'incident (Reseau, Compte, Materiel...)
  - niveau      : "N1" = resoluble automatiquement
                  "N2" = doit etre escalade a un ingenieur
  - mots_cles   : les mots qui declenchent cet article
  - solution    : la reponse renvoyee a l'utilisateur

Pour ajouter un nouveau cas de support, il suffit d'ajouter
un dictionnaire dans la liste BASE_CONNAISSANCES. C'est volontaire :
la base est declarative, lisible et modifiable sans toucher au code
de l'agent — un expert metier peut l'enrichir sans etre developpeur.
============================================================
"""

BASE_CONNAISSANCES = [
    {
        "id": "KB-001",
        "categorie": "Reseau",
        "niveau": "N1",
        "mots_cles": ["wifi", "connexion", "internet", "reseau", "connecter", "deconnecte", "wi-fi", "ethernet", "cable"],
        "solution": (
            "1. Desactivez puis reactivez le Wi-Fi de votre poste.\n"
            "2. Verifiez que vous etes connecte au reseau d'entreprise (et non a un reseau invite).\n"
            "3. Oubliez le reseau puis reconnectez-vous avec vos identifiants.\n"
            "Si le probleme persiste apres ces etapes, le ticket sera escalade."
        ),
    },
    {
        "id": "KB-002",
        "categorie": "Compte / Acces",
        "niveau": "N1",
        "mots_cles": ["mot de passe", "mdp", "password", "oublie", "verrouille", "bloque", "connexion", "identifiant", "session"],
        "solution": (
            "1. Rendez-vous sur le portail de reinitialisation : https://reset.entreprise.local\n"
            "2. Cliquez sur 'Mot de passe oublie' et suivez la procedure par e-mail.\n"
            "3. Le compte se deverrouille automatiquement apres 15 minutes en cas de blocage."
        ),
    },
    {
        "id": "KB-003",
        "categorie": "Messagerie",
        "niveau": "N1",
        "mots_cles": ["mail", "email", "outlook", "messagerie", "boite", "mails", "courriel", "courrier", "piece jointe"],
        "solution": (
            "1. Fermez completement Outlook puis rouvrez-le.\n"
            "2. Verifiez votre connexion reseau (voir aussi incident Wi-Fi).\n"
            "3. Mode sans echec : touche Windows + R, tapez 'outlook /safe'.\n"
            "4. Si la boite est pleine, archivez les anciens messages."
        ),
    },
    {
        "id": "KB-004",
        "categorie": "Materiel",
        "niveau": "N1",
        "mots_cles": ["imprimante", "imprimer", "impression", "papier", "bourrage", "cartouche", "toner", "scanner", "encre"],
        "solution": (
            "1. Verifiez que l'imprimante est allumee et connectee au reseau.\n"
            "2. Annulez les impressions en attente dans la file d'impression.\n"
            "3. Verifiez le bac a papier et le niveau d'encre/toner.\n"
            "4. Eteignez/rallumez l'imprimante (cycle d'alimentation)."
        ),
    },
    {
        "id": "KB-005",
        "categorie": "Performance",
        "niveau": "N1",
        "mots_cles": ["lent", "lenteur", "rame", "freeze", "fige", "lente", "ralenti", "performance"],
        "solution": (
            "1. Redemarrez votre poste (la cause n.1 des lenteurs).\n"
            "2. Fermez les applications inutiles et les onglets de navigateur.\n"
            "3. Verifiez l'espace disque disponible (doit rester > 10 %).\n"
            "4. Lancez une analyse antivirus rapide."
        ),
    },
    {
        "id": "KB-006",
        "categorie": "Logiciel",
        "niveau": "N1",
        "mots_cles": ["logiciel", "application", "appli", "programme", "demarre", "ouvre", "plante", "erreur", "installer"],
        "solution": (
            "1. Fermez completement l'application puis relancez-la.\n"
            "2. Redemarrez le poste si l'application reste bloquee.\n"
            "3. Verifiez les mises a jour en attente.\n"
            "4. Notez le message d'erreur exact avant toute escalade."
        ),
    },
    {
        "id": "KB-007",
        "categorie": "Reseau",
        "niveau": "N1",
        "mots_cles": ["vpn", "tunnel", "acces distant", "client vpn"],
        "solution": (
            "1. Verifiez d'abord votre connexion internet (hors VPN).\n"
            "2. Fermez puis relancez le client VPN.\n"
            "3. Reconnectez-vous avec vos identifiants d'entreprise.\n"
            "4. Changez de point d'acces si plusieurs sont proposes."
        ),
    },
    {
        "id": "KB-008",
        "categorie": "Compte / Acces",
        "niveau": "N1",
        "mots_cles": ["partage", "dossier", "lecteur", "fichier", "acces", "droits", "serveur", "lecteur reseau"],
        "solution": (
            "1. Verifiez que vous etes connecte au reseau d'entreprise ou au VPN.\n"
            "2. Reconnectez le lecteur reseau (clic droit > Reconnecter).\n"
            "3. Si l'acces est refuse, une demande de droits sera transmise."
        ),
    },
    {
        "id": "KB-009",
        "categorie": "Materiel",
        "niveau": "N1",
        "mots_cles": ["souris", "clavier", "ecran", "moniteur", "casque", "webcam", "peripherique", "usb", "branche"],
        "solution": (
            "1. Verifiez le branchement du peripherique (debranchez/rebranchez).\n"
            "2. Essayez un autre port USB, ou un autre poste pour isoler la panne.\n"
            "3. Pour un peripherique sans fil : verifiez piles/batterie et dongle.\n"
            "4. Si l'ecran reste noir : verifiez le cable video et la source d'affichage."
        ),
    },
    {
        "id": "KB-010",
        "categorie": "Collaboration",
        "niveau": "N1",
        "mots_cles": ["teams", "zoom", "visio", "visioconference", "micro", "camera", "reunion en ligne", "partage d'ecran"],
        "solution": (
            "1. Verifiez que le bon micro / la bonne camera sont selectionnes dans l'application.\n"
            "2. Fermez les autres applications utilisant la camera.\n"
            "3. Quittez et rejoignez a nouveau la reunion.\n"
            "4. En dernier recours, utilisez la version navigateur de l'outil."
        ),
    },
    {
        "id": "KB-011",
        "categorie": "Web / Intranet",
        "niveau": "N1",
        "mots_cles": ["navigateur", "chrome", "edge", "firefox", "site", "page web", "intranet", "cookies"],
        "solution": (
            "1. Actualisez la page (Ctrl + F5 pour forcer le rechargement).\n"
            "2. Videz le cache et les cookies du navigateur.\n"
            "3. Essayez en navigation privee, puis avec un autre navigateur.\n"
            "4. Si seul l'intranet est inaccessible, verifiez votre connexion VPN."
        ),
    },
    {
        "id": "KB-012",
        "categorie": "Telephonie",
        "niveau": "N1",
        "mots_cles": ["telephone", "mobile", "smartphone", "sim", "appel", "portable", "softphone"],
        "solution": (
            "1. Redemarrez le telephone.\n"
            "2. Verifiez le mode avion et le volume de la sonnerie.\n"
            "3. Pour un softphone : verifiez le casque et l'etat de la connexion reseau.\n"
            "4. Si la ligne reste muette, le ticket sera transmis a la telephonie."
        ),
    },
    # --- Cas qui DOIVENT etre escalades a un ingenieur (N2) ---
    {
        "id": "KB-101",
        "categorie": "Securite",
        "niveau": "N2",
        "mots_cles": ["virus", "ransomware", "piratage", "hacke", "phishing", "hameconnage", "suspect", "rancongiciel", "arnaque",
                      "vole", "volee", "pirate", "piratee", "demande mes identifiants", "cheval de troie", "malware",
                      "faux site", "chiffre", "usurpation", "compromis"],
        "solution": (
            "INCIDENT DE SECURITE - escalade prioritaire vers l'equipe securite.\n"
            "Consigne immediate a l'utilisateur : deconnectez le poste du reseau "
            "et ne saisissez aucun identifiant."
        ),
    },
    {
        "id": "KB-102",
        "categorie": "Infrastructure",
        "niveau": "N2",
        "mots_cles": ["serveur", "panne", "production", "prod", "down", "indisponible", "coupure", "tout le monde",
                      "plus personne", "personne ne peut", "tout le service", "toute l equipe", "generale"],
        "solution": (
            "PANNE D'INFRASTRUCTURE potentielle - escalade vers l'equipe systeme/reseau.\n"
            "Contexte a verifier : nombre d'utilisateurs impactes, perimetre, criticite."
        ),
    },
    {
        "id": "KB-103",
        "categorie": "Donnees",
        "niveau": "N2",
        "mots_cles": ["supprime", "perdu", "efface", "corrompu", "illisible", "disparu", "recuperer", "restauration", "sauvegarde", "par erreur"],
        "solution": (
            "PERTE DE DONNEES potentielle - escalade vers l'equipe systeme.\n"
            "Consigne immediate : ne plus ecrire sur le poste/le lecteur concerne.\n"
            "Contexte a verifier : emplacement des fichiers, date de derniere sauvegarde."
        ),
    },
]


def categories_connues():
    """Renvoie la liste des categories presentes dans la base (sans doublon)."""
    return sorted({article["categorie"] for article in BASE_CONNAISSANCES})


# Permet de tester ce fichier seul : python connaissances.py
if __name__ == "__main__":
    print(f"Base de connaissances : {len(BASE_CONNAISSANCES)} articles")
    for cat in categories_connues():
        nb = sum(1 for a in BASE_CONNAISSANCES if a["categorie"] == cat)
        print(f"  - {cat} : {nb} article(s)")
