"""
============================================================
 Soveris - Interface web locale de demonstration
============================================================

Une interface web pour presenter l'agent a un public non technique
(mentors, responsables IT, jury) : on tape un incident, l'agent
repond, et le tableau de bord se met a jour en direct.

Fidele au positionnement du projet :
  - 100 % Python standard (http.server) : AUCUNE dependance externe.
  - Serveur lie a 127.0.0.1 uniquement : rien n'est expose au reseau,
    aucune donnee ne quitte la machine (souverainete).
  - Le moteur (paquet soveris/) et la persistance (database.py) sont
    strictement inchanges : l'interface n'est qu'une vitrine.

Lancement :
  python web.py            -> demarre sur http://127.0.0.1:8000
  python web.py 8080       -> port personnalise
  option --sans-navigateur -> ne pas ouvrir le navigateur automatiquement
============================================================
"""

import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import soveris
import database

PORT_DEFAUT = 8000

# ------------------------------------------------------------------
#  La page (HTML + CSS + JS embarques : un seul fichier, zero build)
# ------------------------------------------------------------------
PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Soveris — démonstration</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: linear-gradient(160deg, #061a30 0%, #04101f 100%);
    color: #e8eef5; min-height: 100vh; padding: 32px 16px;
  }
  .conteneur { max-width: 880px; margin: 0 auto; }

  header { display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }
  .logo {
    width: 44px; height: 44px; border: 2px solid #38bdd4; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 22px; color: #38bdd4;
  }
  h1 { font-size: 26px; letter-spacing: 4px; font-weight: 600; }
  .slogan { color: #8fa6bd; margin: 4px 0 26px 58px; font-size: 14px; }

  .saisie { display: flex; gap: 10px; }
  input[type=text] {
    flex: 1; padding: 13px 16px; font-size: 15px; border-radius: 9px;
    border: 1px solid #1c3a5f; background: #0b2440; color: #e8eef5; outline: none;
  }
  input[type=text]:focus { border-color: #38bdd4; }
  button {
    padding: 13px 22px; font-size: 15px; font-weight: 600; border: none;
    border-radius: 9px; background: #2ea7c9; color: #04101f; cursor: pointer;
  }
  button:hover { background: #38bdd4; }

  .exemples { margin: 14px 0 26px; display: flex; flex-wrap: wrap; gap: 8px; }
  .puce {
    font-size: 12.5px; padding: 6px 12px; border-radius: 999px; cursor: pointer;
    border: 1px solid #1c3a5f; background: transparent; color: #8fa6bd;
  }
  .puce:hover { border-color: #38bdd4; color: #e8eef5; background: #0b2440; }

  .carte {
    background: #0b2440; border: 1px solid #1c3a5f; border-radius: 12px;
    padding: 20px 22px; margin-bottom: 22px; display: none;
  }
  .badge {
    display: inline-block; padding: 5px 14px; border-radius: 7px;
    font-size: 13px; font-weight: 700; letter-spacing: 1px;
  }
  .badge.auto { background: #143d2a; color: #4ade80; border: 1px solid #2f9e63; }
  .badge.escalade { background: #40191c; color: #f87171; border: 1px solid #d64545; }
  .texte-ticket { color: #8fa6bd; font-size: 13.5px; margin: 12px 0 10px; }
  .meta { display: flex; flex-wrap: wrap; gap: 18px; margin: 10px 0; font-size: 14px; }
  .meta b { color: #38bdd4; font-weight: 600; }
  .mots { margin: 10px 0 4px; display: flex; flex-wrap: wrap; gap: 6px; }
  .mot { font-size: 12px; padding: 4px 10px; border-radius: 999px;
         background: #10345c; color: #7dd3e8; }
  .solution {
    margin-top: 14px; padding: 14px 16px; border-left: 3px solid #38bdd4;
    background: #081b33; border-radius: 0 8px 8px 0;
    white-space: pre-line; font-size: 14px; color: #cfdcea;
  }
  .solution .titre-sol { color: #8fa6bd; font-size: 12px; letter-spacing: 1px;
    text-transform: uppercase; display: block; margin-bottom: 8px; }

  .metriques { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .tuile {
    background: #0b2440; border: 1px solid #1c3a5f; border-radius: 10px;
    padding: 14px 10px; text-align: center;
  }
  .tuile .valeur { font-size: 22px; font-weight: 700; color: #e8eef5; }
  .tuile .etiquette { font-size: 11.5px; color: #8fa6bd; margin-top: 3px; }
  .barre { grid-column: 1 / -1; background: #0b2440; border: 1px solid #1c3a5f;
    border-radius: 10px; padding: 12px 16px; }
  .barre .fond { background: #081b33; border-radius: 999px; height: 10px; margin-top: 8px; }
  .barre .plein { background: linear-gradient(90deg, #2ea7c9, #4ade80);
    height: 10px; border-radius: 999px; width: 0%; transition: width .4s; }
  .barre .legende { font-size: 12px; color: #8fa6bd; }

  footer { margin-top: 30px; text-align: center; color: #56708c; font-size: 12px; }
</style>
</head>
<body>
<div class="conteneur">
  <header>
    <div class="logo">S</div>
    <h1>SOVERIS</h1>
  </header>
  <div class="slogan">Agent de triage du support IT niveau 1 · 100 % local · zéro dépendance</div>

  <div class="saisie">
    <input type="text" id="texte" placeholder="Décrivez un incident… (ex : je n'arrive plus à me connecter au wifi)" autofocus>
    <button onclick="envoyer()">Analyser</button>
  </div>

  <div class="exemples" id="exemples"></div>

  <div class="carte" id="resultat"></div>

  <div class="metriques" id="metriques">
    <div class="tuile"><div class="valeur" id="m-total">0</div><div class="etiquette">tickets traités</div></div>
    <div class="tuile"><div class="valeur" id="m-auto">0</div><div class="etiquette">résolus automatiquement</div></div>
    <div class="tuile"><div class="valeur" id="m-esc">0</div><div class="etiquette">escalades vers un humain</div></div>
    <div class="tuile"><div class="valeur" id="m-temps">—</div><div class="etiquette">temps moyen / ticket</div></div>
    <div class="barre">
      <span class="legende">Taux de résolution automatique : <b id="m-taux">0 %</b></span>
      <div class="fond"><div class="plein" id="m-barre"></div></div>
    </div>
  </div>

  <footer>Traitement souverain : ce serveur n'écoute que sur 127.0.0.1 — aucune donnée ne quitte cette machine.</footer>
</div>

<script>
  var EXEMPLES = [
    "je n'arrive plus à me connecter au wifi",
    "j'ai oublié mon mot de passe",
    "ma webcam ne marche plus sur Teams",
    "j'ai reçu un mail de phishing",
    "le serveur de production est down",
    "où est la machine à café ?"
  ];

  var zone = document.getElementById("exemples");
  EXEMPLES.forEach(function (t) {
    var b = document.createElement("button");
    b.className = "puce"; b.textContent = t;
    b.onclick = function () {
      document.getElementById("texte").value = t;
      envoyer();
    };
    zone.appendChild(b);
  });

  document.getElementById("texte").addEventListener("keydown", function (e) {
    if (e.key === "Enter") envoyer();
  });

  function envoyer() {
    var texte = document.getElementById("texte").value.trim();
    if (!texte) return;
    fetch("/api/analyser", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texte: texte })
    }).then(function (r) { return r.json(); })
      .then(function (d) { afficher(texte, d); majMetriques(); });
  }

  function afficher(texte, d) {
    var carte = document.getElementById("resultat");
    carte.innerHTML = "";
    carte.style.display = "block";

    var badge = document.createElement("span");
    var auto = d.decision === "RESOLUTION_AUTO";
    badge.className = "badge " + (auto ? "auto" : "escalade");
    badge.textContent = auto ? "RÉSOLU AUTOMATIQUEMENT" : "ESCALADE VERS UN INGÉNIEUR";
    carte.appendChild(badge);

    var t = document.createElement("div");
    t.className = "texte-ticket"; t.textContent = "« " + texte + " »";
    carte.appendChild(t);

    var meta = document.createElement("div");
    meta.className = "meta";
    meta.innerHTML =
      "<span>Catégorie : <b></b></span><span>Niveau : <b></b></span>" +
      "<span>Confiance : <b></b></span><span>Traité en <b></b></span>";
    var b = meta.querySelectorAll("b");
    b[0].textContent = d.categorie;
    b[1].textContent = d.niveau;
    b[2].textContent = d.confiance;
    b[3].textContent = d.temps_ms + " ms";
    carte.appendChild(meta);

    if (d.mots_reconnus && d.mots_reconnus.length) {
      var mots = document.createElement("div");
      mots.className = "mots";
      d.mots_reconnus.forEach(function (m) {
        var s = document.createElement("span");
        s.className = "mot"; s.textContent = m;
        mots.appendChild(s);
      });
      carte.appendChild(mots);
    }

    var motif = document.createElement("div");
    motif.className = "texte-ticket"; motif.textContent = d.motif;
    carte.appendChild(motif);

    if (d.solution) {
      var sol = document.createElement("div");
      sol.className = "solution";
      var titre = document.createElement("span");
      titre.className = "titre-sol";
      titre.textContent = auto ? "Réponse envoyée à l'utilisateur"
                               : "Contexte transmis à l'ingénieur";
      sol.appendChild(titre);
      sol.appendChild(document.createTextNode(d.solution));
      carte.appendChild(sol);
    }
  }

  function majMetriques() {
    fetch("/api/metriques").then(function (r) { return r.json(); })
      .then(function (m) {
        document.getElementById("m-total").textContent = m.total;
        document.getElementById("m-auto").textContent = m.resolus_auto;
        document.getElementById("m-esc").textContent = m.escalades;
        document.getElementById("m-temps").textContent =
          m.total ? m.temps_moyen_ms + " ms" : "—";
        document.getElementById("m-taux").textContent = m.taux_resolution_auto + " %";
        document.getElementById("m-barre").style.width = m.taux_resolution_auto + "%";
      });
  }

  majMetriques();
</script>
</body>
</html>
"""


class Poignee(BaseHTTPRequestHandler):
    """Sert la page et les deux points d'API (analyser, metriques)."""

    def _envoyer(self, code, contenu, type_contenu="application/json; charset=utf-8"):
        donnees = contenu.encode("utf-8") if isinstance(contenu, str) else contenu
        self.send_response(code)
        self.send_header("Content-Type", type_contenu)
        self.send_header("Content-Length", str(len(donnees)))
        self.end_headers()
        self.wfile.write(donnees)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._envoyer(200, PAGE, "text/html; charset=utf-8")
        elif self.path == "/api/metriques":
            self._envoyer(200, json.dumps(database.calculer_metriques(), ensure_ascii=False))
        else:
            self._envoyer(404, json.dumps({"erreur": "introuvable"}))

    def do_POST(self):
        if self.path != "/api/analyser":
            self._envoyer(404, json.dumps({"erreur": "introuvable"}))
            return
        try:
            longueur = int(self.headers.get("Content-Length", 0))
            corps = json.loads(self.rfile.read(longueur).decode("utf-8"))
            texte = (corps.get("texte") or "").strip()
        except Exception:
            self._envoyer(400, json.dumps({"erreur": "requete invalide"}))
            return
        if not texte:
            self._envoyer(400, json.dumps({"erreur": "texte vide"}))
            return
        resultat = soveris.traiter(texte)
        database.enregistrer(resultat)
        self._envoyer(200, json.dumps(resultat, ensure_ascii=False))

    def log_message(self, format, *args):
        # Journal minimal : on ne pollue pas la console pendant une demo.
        pass


if __name__ == "__main__":
    arguments = [a for a in sys.argv[1:] if not a.startswith("--")]
    port = int(arguments[0]) if arguments else PORT_DEFAUT

    # Base propre a chaque demonstration (comme demo.py).
    database.reinitialiser()

    serveur = ThreadingHTTPServer(("127.0.0.1", port), Poignee)
    adresse = f"http://127.0.0.1:{port}"
    print("=" * 56)
    print("  SOVERIS - interface web de demonstration")
    print(f"  En ecoute sur {adresse}  (127.0.0.1 uniquement)")
    print("  Arret : Ctrl+C")
    print("=" * 56)

    if "--sans-navigateur" not in sys.argv:
        webbrowser.open(adresse)

    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\nArret du serveur.")
        serveur.server_close()
