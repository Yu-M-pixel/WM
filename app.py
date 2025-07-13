import folium
import folium.raster_layers
from ipyleaflet import Map, Marker, TileLayer
from ipywidgets import HTML, Layout
from shiny.express import ui,render
from shinywidgets import render_widget
import pandas as pd
import plotly.express as px
import folium 
from folium.plugins import MarkerCluster
from folium import FeatureGroup
import geopandas as gpd
from folium import GeoJson

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "datas", "referentiel_archeologique_de_paris.csv")
CARRIERES_PATH = os.path.join(BASE_DIR, "datas", "carrieres", "plub_carriere.shp")
print("Chemin du shapefile :", CARRIERES_PATH)
print("Existe ?", os.path.exists(CARRIERES_PATH))



ui.include_css("./styles.css")

ui.h2("Sites archéologiques à Paris", class_="custom")

ui.HTML("[TODO]")

@render.ui
def create_map():
    """
    - Fonction qui prend en paramètre les informations à la sortie 
    de la fonction read_data
    - Centre la carte sur Paris.
    - Création des clusters pour regrouper les sites archéologiques 
    par proximité. 
    - Création du popup avec des informations sur chaque site archéologique
    - Ajout d'une échelle
    """
    df_points = pd.read_csv(DATA_PATH, sep=';')

    center_lat, center_lon = 48.8566, 2.3522
    my_map = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=11, 
        control_scale=True,
        tiles= None,
    )

    folium.TileLayer(
        tiles="https://tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=ee88aacf61b2452ead6be5356cc070ac",
        attr="Maps © Thunderforest",
        name="Thunderforest Transport Dark",
        control=True
    ).add_to(my_map)

    folium.TileLayer(
        tiles="https://tile.thunderforest.com/atlas/{z}/{x}/{y}.png?apikey=ee88aacf61b2452ead6be5356cc070ac",
        attr="Maps © Atlas",
        name="Atlas",
        control=True
    ).add_to(my_map)

    sites_layer = FeatureGroup(name="Sites archéologiques")
    marker_cluster = MarkerCluster().add_to(sites_layer)
    sites_layer.add_to(my_map)

    for _, row in df_points.iterrows():
        popup_content = f"""
        <b>Adresse:</b> {row['Adresse']} ({row['Commune']})<br>
        <b>Date de l'opération:</b> {row["Date de l'opération"]}<br>
        <b>Nature de l'opération:</b> {row["Nature de l'opération"]}<br>
        <b>Antiquité:</b> {row["Antiquité"]}<br>
        <b>Protohistoire:</b> {row["Protohistoire"]}<br>
        <b>Moyen-Age:</b> {row["Moyen-Age"]}<br>
        <b>Temps modernes:</b> {row["Temps modernes"]}<br>
        <b>Epoque contemporaine:</b> {row["Epoque contemporaine"]}

        
"""
        
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300), 
            icon=folium.Icon(color="pink", icon="circle")  
        ).add_to(marker_cluster)
        my_map.options["control_scale"] = True

# 6️⃣ Couche WMS BRGM — Enveloppe inondation (cours d'eau/submersion)
    folium.raster_layers.WmsTileLayer(
        url="https://mapsref.brgm.fr/wxs/georisques/risques",
        name="Enveloppe inondation (EAIP)",
        layers="MASQ_EAIP",
        fmt="image/png",
        transparent=True,
        attr="© BRGM – Enveloppe inondation",
        overlay=True,
        control=True
    ).add_to(my_map)

# 4️⃣ Couche WMS BRGM — Mouvements de terrain
    folium.raster_layers.WmsTileLayer(
        url="https://geoservices.brgm.fr/risques",
        name="Mouvements de terrain",
        layers="MVT_LOCALISE",
        fmt="image/png",
        transparent=True,
        attr="© BRGM – Mouvements de terrain",
        overlay=True,
        control=True
    ).add_to(my_map)
#   Anciennes carrières

    try:
        # Charger le shapefile avec GeoPandas
        gdf_carrieres= gpd.read_file(CARRIERES_PATH)
        print("Nombre de polygones chargés :", len(gdf_carrieres))
        print("CRS :", gdf_carrieres.crs)
        print(gdf_carrieres.head())

        # Reprojeter vers WGS84 si besoin (souvent les shapefiles sont en Lambert 93)
        if gdf_carrieres.crs is None:
            gdf_carrieres.set_crs(epsg=2154, inplace=True)  # Souvent Lambert 93
        gdf_carrieres = gdf_carrieres.to_crs(epsg=4326)

        # Ajouter à la carte Folium
        folium.GeoJson(
            data=gdf_carrieres,
            name="Anciennes carrières",
            tooltip=folium.GeoJsonTooltip(fields=list(gdf_carrieres.columns[:3])),
            style_function=lambda x: {
                'color': 'orange',
                'weight': 2,
                'fillOpacity': 0.3,
            }
        ).add_to(my_map)


    except Exception as e:
        print("Erreur lors du chargement du shapefile : ", e)

    folium.LayerControl().add_to(my_map)

    return my_map  

ui.HTML("[TODO]")   

ui.HTML("<br/><br/>")

ui.h2("Quantité de sites archéologiques par code postal", style_="text-align: center;")

ui.HTML("[TODO]")   

@render_widget
def histogram():
    df_points = pd.read_csv(DATA_PATH, sep=';')
    data_count = df_points["Code postal"].value_counts().reset_index()
    data_count.columns = ["Code postal", "Nombre de sites"]

    # Trie croissant par code postal
    data_count = data_count.sort_values("Code postal")
    data_count["Code postal"] = data_count["Code postal"].astype(str)

    fig = px.bar(
        data_count,
        x="Code postal",
        y="Nombre de sites",
        hover_data={"Nombre de sites": True, "Code postal": False},  # Affiche uniquement la valeur
        labels={"Code postal": "Code postal", "Nombre de sites": "Nombre de sites"},
        text="Nombre de sites"
    )

    fig.update_traces(textposition='outside')

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=data_count["Code postal"],
            categoryorder='array',
            categoryarray=data_count["Code postal"]
        ),
        yaxis=dict(
            tickformat='d',
            showticklabels=False,  # Masque les labels de l'axe Y
            showgrid=False,        # Supprime la grille horizontale
            zeroline=False,        # Supprime la ligne horizontale à 0
        ),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )



    return fig
