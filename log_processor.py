import re
import sqlite3 as sql
import pandas as pd

def analyser_fichier(chemin_fichier):
    with open(chemin_fichier, "r") as f:
        lines = f.readlines()

    motif = r'(\S+) - - \[(.*?)\] "(\S+) (\S+) HTTP/1.1" (\d+) (\d+)'
    data = []

    for line in lines:
        resultat = re.match(motif, line)
        if resultat:
            entree = {
                "ip" : resultat.group(1),
                "date" : resultat.group(2),
                "methode" : resultat.group(3),
                "url" : resultat.group(4),
                "code" : resultat.group(5),
                "taille" : resultat.group(6)
            }
            data.append(entree)

    df = pd.DataFrame(data)

    urls_sensibles = ["/admin", "/.env"]  
    df_sensibles = df[df["url"].isin(urls_sensibles)]
    ips_url_sensibles = df_sensibles["ip"].unique()

    compte_ip = df["ip"].value_counts()
    ips_frequentes = compte_ip[compte_ip > 40]
    liste_ips_frequentes = ips_frequentes.index.tolist()     

    codes_erreur = ["400", "401", "403", "404", "500"]
    df_codeErreur = df[df["code"].isin(codes_erreur)]
    ips_codeErreur = df_codeErreur["ip"].unique()

    ips_suspectes = set(ips_url_sensibles) | set(ips_codeErreur) | set(liste_ips_frequentes)

    df["suspect"] = df["ip"].isin(ips_suspectes)

    cnx = sql.connect("logs.db")
    df.to_sql("logs", cnx, if_exists="replace", index=False)
    cnx.close()

    return len(df)