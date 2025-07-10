import csv
import folium
from folium.plugins import MarkerCluster


def read_data(file_path):
    """
    - Fonction qui prend en paramètre le chemin relatif du fichier CSV
    - Lit les données du fichier CSV et extrait les informations 
    des sites archéologiques
    - Retourne un dictionnaire où chaque clé est un identifiant unique et la 
    valeur est un dictionnaire contenant : Identifiant du site, 
    Coordonnées GPS (latitude, longitude), Adresse, Code postal, Commune, 
    Nature et date de l'opération archéologique
    - Convertit la latitude et la longitude en float
    - Supprime les lignes incomplètes 
    - Retourne le dictionnaire contenant les données valides 
    """

    sites = {}  
    
    with open(file_path, encoding="utf-8", mode="r") as f:
        reader = csv.DictReader(f, delimiter=";") 
        reader.fieldnames = [name.lstrip("\ufeff") for name in reader.fieldnames]

        for site in reader:
            try:
            
                sites[site['Identifiant']] = {
                   "identifiant": site['Identifiant'],
                   "lat": float(site['latitude']),  
                   "lon": float(site['longitude']),  
                   "Adresse": site['Adresse'],
                   "Code postal": site['Code postal'],
                   "Commune": site['Commune'],
                   "Nature de l'opération": site["Nature de l'opération"],
                   "Date de l'opération": site["Date de l'opération"]
               }
            except (ValueError, KeyError) as e:  
               print(f"Erreur {e} pour {site}")

    return sites  

def create_map(data):
    """
    - Fonction qui prend en paramètre les informations à la sortie 
    de la fonction read_data
    - Centre la carte sur Paris.
    - Création des clusters pour regrouper les sites archéologiques 
    par proximité. 
    - Création du popup avec des informations sur chaque site archéologique
    - Ajout d'une échelle
    """

    center_lat, center_lon = 48.8566, 2.3522
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True)
    marker_cluster = MarkerCluster().add_to(my_map)

    for site in data.values():
        popup_content = f"""
        <b>Identifiant:</b> {site['identifiant']}<br>
        <b>Adresse:</b> {site['Adresse']} ({site['Commune']})<br>
        <b>Date de l'opération:</b> {site["Date de l'opération"]}<br>
        <b>Nature de l'opération:</b> {site["Nature de l'opération"]}
        """
        
        folium.Marker(
            [site["lat"], site["lon"]],
            popup=folium.Popup(popup_content, max_width=300), 
            tooltip=site["Adresse"],  
            icon=folium.Icon(color="pink", icon="circle")  
        ).add_to(marker_cluster)
        my_map.options["control_scale"] = True
      
    return my_map  

def main():
    """
    Fonction principale qui :
    - Charge les données depuis le fichier CSV.
    - Affiche le nombre de sites valides et d'arrondissements détectés.
    - Génère la carte et l'enregistre sous forme de fichier HTML.
    """

    file_path = "datas/referentiel_archeologique_de_paris.csv"
    data = read_data(file_path)
    
    print(f"Données valides chargées : {len(data)} sites archéologiques")
    print(f"Nombre d'arrondissements détectés : {len(set(site['Code postal'][-2:] for site in data.values() if site['Code postal'].startswith('75')))}")

    map_object = create_map(data)
    map_object.save("sites_archéo.html") 

    print("Carte générée : 'sites_archéo.html'")

main()