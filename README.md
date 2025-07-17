# Patrimoine & Prévention : Cartographie des sites archéologiques et des risques à Paris

Ce projet est réalisé dans le cadre du **Master 2 Télédétection & Géomatique appliquées à l’environnement**,  
par l'**Université Paris 1 Panthéon-Sorbonne / Université Paris Cité**,  
dans le cadre du module **WebMapping** (année universitaire 2024–2025).

##  Présentation

Ce projet propose une **application web interactive** croisant :

- Les **données archéologiques de Paris** (Référentiel archéologique)
- Les **données de risques naturels** (mouvements de terrain, inondations, anciennes carrières)

L’objectif est de **valoriser le patrimoine enfoui** tout en **évaluant sa vulnérabilité** face aux aléas géologiques (inondations, mouvement de terrain, carrières souterrains, etc.). Le tout est présenté via une **carte dynamique et un histogramme**.

## Structure du projet

```
projet/WM
│
├── app.py                 # Fichier d'entrée  
├── styles.css             
├── requirements.txt        
├── README.md               
│
├── datas/
│   ├── referentiel_archeologique_de_paris.csv      #Fichier d'exemple
│   └── carrieres/
│       └── plub_carriere.shp       #Fichier d'exemple
│       └── ... (autres fichiers shapefile nécessaires)
│
```

---

## Installation et lancement

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Yu-M-pixel/WM.git
cd WM

# 2. Créer et activer un environnement virtuel

## Sur Linux/Mac
python3 -m venv .venv
source .venv/bin/activate        

## Sur Windows : 
python3.exe -m venv .venv
.venv\Scripts\activate.bat

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


## Auteur

Movchan Yuliia  
[Yuliia.movchan@etu.univ-paris1.fr](mailto://Yuliia.movchan@etu.univ-paris1.fr)

## Données et sources 

1. Référentiel archéologique de Paris (https://www.data.gouv.fr/api/1/datasets/r/fb42db24-7fe5-4ebd-85ad-d9d153243979); 
2. Carrières souterraines (https://www.data.gouv.fr/fr/datasets/r/8569d081-c63e-4f63-aa4e-a8eccf70264e); 
3. Risques naturels (https://mapsref.brgm.fr/wxs/georisques/risques); 
4. Mouvements de terrain (https://geoservices.brgm.fr/risques);
5. https://github.com/Romb38
6. https://shiny.posit.co/py/
7. https://openai.com/index/chatgpt/


---