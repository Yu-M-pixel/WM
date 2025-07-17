# Gros titre H1

## Un peut moins gros H2

### Salut H3

#### Coucou H4

##### Test Bold

1 - C'est quoi ton projet

2 - Comment l'installer

2.1 Cloner le répertoire git
2.2 Créer un environnement virtuel (python3 -m venv .venv)
2.3 Activer l'environnement (source .venv/bin/activate)
2.4 Installer les dépendances (pip install -r requirements.txt)

3 - Lancer le projet 
Une fois le projet installé, pour le lancer  :

```bash
shiny run --launch-browser app.py
```
# Patrimoine & Prévention : Cartographie des sites archéologiques et des risques à Paris

> **Projet universitaire - Master 2 Télédétection & Géomatique appliquées à l’environnement**  
> Université Paris 1 Panthéon-Sorbonne / Université Paris Cité  
> Module : **WebMapping**


##  Présentation

Ce projet propose une **application web interactive** croisant :

- Les **données archéologiques de Paris** (Référentiel archéologique)
- Les **données de risques naturels** (mouvements de terrain, inondations, anciennes carrières)

L’objectif est de **valoriser le patrimoine enfoui** tout en **évaluant sa vulnérabilité** face aux aléas géologiques (inondations, mouvement de terrain, carrières souterrains, etc.). Le tout est présenté via une **carte dynamique et un histogramme**.

## Structure du projet

```
projet/
│
├── app.py                  # Application principale (Shiny Python)
├── styles.css              # Feuille de style personnalisée
├── requirements.txt        # Dépendances Python
├── README.md               # Documentation GitHub
│
├── datas/
│   ├── referentiel_archeologique_de_paris.csv
│   └── carrieres/
│       └── plub_carriere.shp
│       └── ... (autres fichiers shapefile nécessaires)
│
├── logo/
│   ├── brgm.png
│   ├── data_gouv.png
│   └── paris_data.png
│
└── .venv/ (non versionné)
```

---

## Installation et lancement

### Prérequis

- Python ≥ 3.9
- Environnement virtuel recommandé
- Connexion Internet (pour charger les tuiles WMS)

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-utilisateur/projet-patrimoine.git
cd projet-patrimoine

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate        

# Sur Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
shiny run --reload app.py
```

Puis ouvrir [http://localhost:8000](http://localhost:8000) dans votre navigateur.

---

##  Fonctionnalités principales

- Carte interactive centrée sur Paris  
- Affichage des sites archéologiques (avec clustering)  
- Popups informatifs sur les fouilles  
- Couches WMS (inondations, mouvements de terrain)  
- Intégration shapefile des carrières  
- Histogramme des sites par arrondissement  




## Dépendances (`requirements.txt`)

> Voir fichier complet [`requirements.txt`](requirements.txt)

Extraits :
```
shiny==1.4.0
folium==0.19.6
ipyleaflet==0.19.2
geopandas==...
plotly==...
...
```

---

## Contexte académique

Ce projet est réalisé dans le cadre du **Master 2 Télédétection & Géomatique appliquées à l’environnement**,  
par l'**Université Paris 1 Panthéon-Sorbonne / Université Paris Cité**,  
dans le cadre du module **WebMapping** (année universitaire 2024–2025).

---

## 📄 Licence et utilisation

- Projet à visée **pédagogique uniquement**
- Les données utilisées sont toutes **publiques et libres d’accès** via [data.gouv.fr](https://data.gouv.fr)

---

## Contact

**Auteur** : Movchan Yuliia  
Email : movchan.yuliia@etu.univ-paris1.fr  

## Données et sources 

1. Référentiel archéologique de Paris (https://www.data.gouv.fr/api/1/datasets/r/fb42db24-7fe5-4ebd-85ad-d9d153243979); 
2. Carrières souterraines (https://www.data.gouv.fr/fr/datasets/r/8569d081-c63e-4f63-aa4e-a8eccf70264e); 
3. Risques naturels (https://mapsref.brgm.fr/wxs/georisques/risques); 
4. Mouvements de terrain (https://geoservices.brgm.fr/risques);


---