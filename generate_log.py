import random
import os 
from datetime import datetime, timedelta 

IPS_NORMALES = [f"192.168.1.{i}" for i in range(2, 40)]
IPS_SUSPECTES = ["203.0.113.5", "198.51.100.23"]

HTTP_METHODES = ["GET", "POST", "PUT", "DELETE"]

URLS_NORMALES = ["/accueil", "/contact", "/apropos", "/produits", "/blog", "/panier"]
URLS_SENSIBLES = ["/admin", "/.env"]

CODES_NORMAUX = [200, 201]
CODES_ERREUR = [400, 401, 403, 404, 500]

def generer_ligne(suspect=False) :
    if suspect : 
        ip = random.choice(IPS_SUSPECTES)
        http = random.choice(HTTP_METHODES)
        url = random.choice(URLS_SENSIBLES)
        code = random.choice(CODES_ERREUR)
        taille = random.randint(200,5000)
        temps_maintenant = datetime.now()
        text = temps_maintenant.strftime("%d/%b/%Y:%H:%M:%S")
        ligne = ip+" - - ["+text+" +0000] \""+http+" "+url +" HTTP/1.1\" " +str(code)+" "+str(taille)    
    else : 
        ip = random.choice(IPS_NORMALES)
        http = random.choice(HTTP_METHODES)
        url = random.choice(URLS_NORMALES)
        code = random.choice(CODES_NORMAUX)
        taille = random.randint(200,5000)
        temps_maintenant = datetime.now()
        text = temps_maintenant.strftime("%d/%b/%Y:%H:%M:%S")
        ligne = ip+" - - ["+text+" +0000] \""+http+" "+url +" HTTP/1.1\" "+str(code)+" "+str(taille)

    return ligne

lignes = []
for i in range(100):
    est_suspect = random.random() < 0.1
    ligne = generer_ligne(suspect=est_suspect)
    lignes.append(ligne)  



with open("access.log", "w") as f :
    f.write("\n".join(lignes))

