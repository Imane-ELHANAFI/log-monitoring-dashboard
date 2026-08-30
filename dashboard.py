from flask import Flask , render_template , redirect ,request 
from log_processor import analyser_fichier
import pandas as pd
import sqlite3 as sql
import os

app = Flask(__name__)

@app.route("/")
def acceuil():
    return render_template("home.html")

@app.route("/add-log")
def add_log():
    return render_template("add_log.html")

@app.route("/upload", methods=["POST"])
def upload():
    fichier = request.files["monFichier"]
    chemin = os.path.join("uploads", fichier.filename)
    os.makedirs("uploads", exist_ok=True)
    fichier.save(chemin)
    analyser_fichier(chemin)
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    cnx = sql.connect("logs.db")
    df = pd.read_sql("SELECT * FROM logs", cnx)
    cnx.close()

    ip_recherchee = request.args.get("ip")
    suspect_seulement = request.args.get("suspect")

    if ip_recherchee:
        df = df[df["ip"] == ip_recherchee]

    if suspect_seulement == "oui":
        df = df[df["suspect"] == 1]

    logs = df.to_dict(orient="records")

    stats_codes = df["code"].value_counts().to_dict()

    nombre_suspects = int(df["suspect"].sum())

    recommandations = []

    if (df["url"].isin(["/admin", "/.env"])).any():
        recommandations.append({
            "titre": "Restreindre l'accès aux pages sensibles",
            "texte": "Des tentatives d'accès à des pages comme /admin ou /.env ont été détectées. Limitez l'accès à ces pages par IP autorisée, et ne publiez jamais de fichiers de configuration (.env) sur un serveur accessible publiquement."
        })

    if (df["ip"].value_counts() > 40).any():
        recommandations.append({
            "titre": "Mettre en place une limitation du nombre de requêtes",
            "texte": "Certaines IPs ont envoyé un nombre anormalement élevé de requêtes. Il est recommandé de mettre en place un système de limitation (rate limiting) pour ralentir ou bloquer les IPs trop actives."
        })

    codes_erreur_int = [400, 401, 403, 404, 500]
    if df["code"].astype(int).isin(codes_erreur_int).sum() > 5:
        recommandations.append({
            "titre": "Bloquer automatiquement les IPs générant trop d'erreurs",
            "texte": "Un nombre élevé de codes d'erreur (401, 403, 404, 500) a été observé. La mise en place d'un blocage automatique temporaire après plusieurs échecs consécutifs (type fail2ban) est recommandée."
        })

    if nombre_suspects == 0:
        recommandations.append({
            "titre": "Aucune activité suspecte détectée",
            "texte": "Aucun comportement suspect n'a été identifié dans ce fichier de logs selon les critères actuels. Continuez à surveiller régulièrement vos journaux serveur."
        })

    return render_template("dashboard.html", nombre_lignes=len(df), logs=logs, stats_codes=stats_codes, nombre_suspects=nombre_suspects, recommandations=recommandations)


if __name__ == "__main__" :
    app.run(debug=True)
