import folium.raster_layers
from ipyleaflet import Map, Marker, TileLayer
from ipywidgets import HTML, Layout
from shiny.express import ui,render
from shinywidgets import render_widget
import pandas as pd
import plotly.express as px
import folium 
from folium.plugins import MarkerCluster
from folium import raster_layers

DATA_PATH = "./datas/referentiel_archeologique_de_paris.csv"
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
        zoom_start=12, 
        control_scale=True,
    )
    folium.TileLayer(
        tiles="https://tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=ee88aacf61b2452ead6be5356cc070ac",
        attr="Maps © Thunderforest, Data © OpenStreetMap",
        name="Thunderforest Transport Dark",
        control=True
    ).add_to(my_map)

    marker_cluster = MarkerCluster().add_to(my_map)

    for _, row in df_points.iterrows():
        popup_content = f"""
        <b>Adresse:</b> {row['Adresse']} ({row['Commune']})<br>
        <b>Date de l'opération:</b> {row["Date de l'opération"]}<br>
        <b>Nature de l'opération:</b> {row["Nature de l'opération"]}
        """
        
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300), 
            icon=folium.Icon(color="pink", icon="circle")  
        ).add_to(marker_cluster)
        my_map.options["control_scale"] = True

# 3️⃣ Couche WMS BRGM — Cavités souterraines
    folium.raster_layers.WmsTileLayer(
        url="https://geoservices.brgm.fr/risques",
        name="Cavités souterraines",
        layers="CAVITE_LOCALISEE",
        fmt="image/png",
        transparent=True,
        attr="© BRGM – Cavités",
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
