# Log Monitoring Dashboard

Application web permettant d'analyser des logs de serveur et de détecter des activités suspectes, avec visualisation des données sous forme de tableau de bord.

Ce projet a été développé dans le cadre d'un stage, avec pour objectif de découvrir concrètement le fonctionnement d'un projet web tout en abordant des notions de cybersécurité et d'analyse de données.

## Fonctionnalités

- **Upload de fichiers de logs** (format Apache/Nginx "combined") directement depuis le navigateur
- **Extraction automatique** des informations clés : adresse IP, date, méthode HTTP, URL, code de réponse, taille
- **Détection de comportements suspects**, basée sur 3 critères combinés :
  - Nombre de requêtes anormalement élevé pour une même IP
  - Accès à des URLs sensibles (`/admin`, `/.env`, etc.)
  - Nombre élevé de codes d'erreur (400, 401, 403, 404, 500)
- **Tableau de bord visuel** avec statistiques et graphiques (Chart.js)
- **Filtres et recherche** dans les logs (par IP, par statut suspect)
- **Recommandations de sécurité** générées automatiquement à partir des résultats de l'analyse
- Générateur de fichiers de logs de test, pour développer et tester l'application sans avoir besoin d'un vrai serveur

## Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python | Traitement et logique de détection |
| Flask | Serveur web / backend |
| Pandas | Analyse et manipulation des données |
| SQLite | Stockage des données analysées |
| HTML / CSS / JavaScript | Interface utilisateur |
| Chart.js | Visualisation graphique des statistiques |
| Jinja2 | Génération dynamique des pages HTML |

## Structure du projet

```
log-monitoring-dashboard/
├── templates/              # Pages HTML (Jinja2)
│   ├── home.html
│   ├── add_log.html
│   └── dashboard.html
├── static/                  # Fichiers statiques
│   ├── style.css
│   └── graphique.js
├── uploads/                  # Fichiers de logs uploadés (créé automatiquement)
├── dashboard.py             # Application Flask (routes)
├── log_processor.py         # Logique d'extraction, de détection et de stockage
├── generate_log.py          # Générateur de fichiers de logs de test
├── logs.db                  # Base de données SQLite (créée automatiquement)
├── requirements.txt         # Dépendances Python
└── README.md
```

## Installation

### Prérequis
- Python 3.10 ou supérieur
- Git

### Étapes

1. Cloner le dépôt :
```bash
git clone https://github.com/Imane-ELHANAFI/log-monitoring-dashboard.git
cd log-monitoring-dashboard
```

2. Créer et activer un environnement virtuel :
```bash
python -m venv env
```

Sur Windows (PowerShell) :
```bash
.\env\Scripts\Activate.ps1
```

Sur Mac/Linux :
```bash
source env/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### 1. (Optionnel) Générer un fichier de logs de test

Si vous n'avez pas de fichier de logs réel sous la main, générez-en un avec le script fourni :
```bash
python generate_log.py
```

Cela crée un fichier `access.log` contenant du trafic normal et des comportements suspects simulés.

### 2. Lancer l'application

```bash
python dashboard.py
```

### 3. Ouvrir l'application dans le navigateur

Rendez-vous sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 4. Analyser un fichier de logs

- Depuis la page d'accueil, cliquez sur **"Ajouter un fichier de log"**
- Sélectionnez votre fichier (`.log` ou `.txt`, format Apache/Nginx "combined")
- Cliquez sur **"Analyser le fichier"**
- Vous êtes redirigé automatiquement vers le tableau de bord, avec les statistiques, le graphique et les recommandations correspondant à votre fichier

## Règles de détection des comportements suspects

Une IP est considérée comme suspecte si elle correspond à **au moins une** des règles suivantes :

| Règle | Critère |
|---|---|
| Volume de requêtes | Plus de 40 requêtes envoyées par la même IP |
| URLs sensibles | Au moins un accès à une URL comme `/admin` ou `/.env` |
| Codes d'erreur | Présence de codes d'erreur (400, 401, 403, 404, 500) associés à l'IP |

Ces seuils sont définis dans `log_processor.py` et peuvent être ajustés selon le contexte d'utilisation.

## Limites actuelles et pistes d'amélioration

- Les seuils de détection sont fixes et pourraient être rendus configurables depuis l'interface
- Le format de log accepté est actuellement limité au format Apache/Nginx "combined"
- La détection pourrait être enrichie avec d'autres critères (fréquence temporelle des requêtes, géolocalisation des IPs, détection de motifs d'injection dans les URLs, etc.)
- Les noms de fichiers uploadés ne sont pas encore sécurisés (à améliorer avec `secure_filename` de Werkzeug avant tout déploiement en production)

## Auteur

Projet réalisé par Imane ELHANAFI dans le cadre d'un stage.
