import folium
import folium.raster_layers
from shiny.express import ui,render
from shinywidgets import render_widget
import pandas as pd
import plotly.express as px
from folium.plugins import MarkerCluster
from folium import FeatureGroup
import geopandas as gpd

#Chemins 

DATA_PATH = ("./datas/referentiel_archeologique_de_paris.csv")
CARRIERES_PATH = ("./datas/carrieres/plub_carriere.shp")

#Importation du fichier des styles
ui.include_css("./styles.css")

#Titre
ui.HTML("""
<h2 class="custom";>
  <br>Patrimoine & Prévention:<br>
  Cartographie des sites archéologiques et des risques à Paris
</h2>
""")

#Logos
ui.HTML("""
<div class="logo-bar">
  <img src="logo/data_gouv.png" class="logo" alt="Logo 1">
  <img src="logo/brgm.png" class="logo" alt="Logo 2">
  <img src="logo/paris_data.png" class="logo" alt="Logo 3">
</div>
""")

#Texte
ui.HTML("""
<div style="font-family: 'Monserrat', sans-serif; font-size: 16px; line-height: 1.6;">
  <p style="text-align: justify;">
    Le <strong>Référentiel archéologique de Paris</strong> est le fruit du projet <em>R&CAP</em>, mené en collaboration avec l'<a href="https://www.inrap.fr/" target="_blank">Inrap</a>, la <a href="https://www.culture.gouv.fr/Regions/Drac-Ile-de-France" target="_blank">Drac Île-de-France</a>, et le <a href="https://www.archeo.ens.fr/" target="_blank">CNRS (UMR 7041 ArScAn)</a>. Il recense les découvertes archéologiques réalisées à Paris, de l’époque moderne aux interventions préventives les plus récentes. Les archives de <strong>Théodore Vacquer</strong>, de la <em>Commission du Vieux Paris</em>, ainsi que des cartes archéologiques établies par Michel Fleury (1971) et Didier Busson (1998), constituent des sources majeures de cette base de données.
  </p>

  <p style="text-align: justify;">
    Ce référentiel, accessible au public et aux chercheurs, est enrichi régulièrement dans une démarche de valorisation du patrimoine parisien. Pour en savoir plus, consultez la <a href="https://www.paris.fr/pages/journees-de-l-archeologie-paris-et-ses-mysteres-enfouis-16479" target="_blank">page dédiée sur Paris.fr</a>.
  </p>

  <p style="text-align: justify;">
    Cette carte interactive propose une approche originale en <strong>croisant les données archéologiques</strong> du territoire parisien avec des <strong>données de risques naturels</strong> : mouvements de terrain, inondations et anciennes carrières. Ce croisement permet de mieux comprendre l'évolution historique de Paris, tout en sensibilisant aux enjeux de conservation du patrimoine face aux aléas géologiques. Les données sur les risques proviennent du Bureau de recherches géologiques et minières (BRGM).   
  </p>
</div>
""")

#Fonction de création de carte 
"""
    - Fonction qui prend en paramètre les informations à la sortie 
    de la fonction read_data
    - Centre la carte sur Paris.
    - Création des clusters pour regrouper les sites archéologiques 
    par proximité. 
    - Création du popup avec des informations sur chaque site archéologique
    - Ajout d'une échelle
    """

@render.ui
def create_map():
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

# Importation du couche WMS BRGM — Enveloppe inondation 
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

# Importation du couche WMS BRGM — Mouvements de terrain
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

#   Importation du shapefile d'anciennes carrières 
    try:
        gdf_carrieres= gpd.read_file(CARRIERES_PATH)
        
        if gdf_carrieres.crs is None:
            gdf_carrieres.set_crs(epsg=2154, inplace=True)  # Souvent Lambert 93
        gdf_carrieres = gdf_carrieres.to_crs(epsg=4326)

        folium.GeoJson(
            data=gdf_carrieres,
            name="Anciennes carrières",
            tooltip=folium.GeoJsonTooltip(fields=list(gdf_carrieres.columns[:3])),
            style_function=lambda x: {
                'color': 'yellow',
                'weight': 2,
                'fillOpacity': 0.3,
            }
        ).add_to(my_map)

    except Exception as e:
        print("Erreur shapefile :", e)

    folium.LayerControl().add_to(my_map)
        
    return ui.HTML(f"""
<div class="map-container" style="height: 400px; width: 80%; margin: 20px auto;">
    {my_map._repr_html_()}
</div>
""")

#Texte 

ui.HTML(""" 
<div style="font-family: 'Monserrat', sans-serif; font-size: 16px; line-height: 1.6;">
  <p style="text-align: justify;">
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    Le patrimoine archéologique, précieux témoin de notre passé, est particulièrement vulnérable face aux <strong>risques naturels</strong> qui affectent le sous-sol parisien. Parmi les menaces identifiées, les <strong>inondations potentielles</strong> liées à la Seine et les <strong>carrières souterraines non stabilisées</strong> peuvent entraîner des dommages irréversibles sur les vestiges enfouis. L’eau peut altérer les matériaux anciens ou retarder les fouilles, tandis que les effondrements liés aux cavités peuvent rendre certains sites totalement inaccessibles ou irrécupérables.
  </p>

  <p style="text-align: justify;">
    Cette carte interactive vise à croiser les <strong>données archéologiques</strong> avec les <strong>zones à risques naturels</strong>, afin d’identifier les secteurs les plus exposés. Le graphique ci-dessous met en évidence une concentration notable de sites archéologiques dans le <strong>5<sup>e</sup> arrondissement</strong>, un secteur riche en vestiges gallo-romains. Or, cette zone est <strong>partiellement incluse dans l’enveloppe potentielle d’inondation</strong>, ce qui renforce la nécessité d'une approche préventive dans la gestion du patrimoine.
  </p>

  <p style="text-align: justify;">
    Croiser ces couches d'information permet ainsi de mieux anticiper les interventions, protéger les sites sensibles et guider les politiques d’aménagement du territoire en tenant compte de l’histoire enfouie sous nos pieds.
  </p>
</div>
""")   

ui.HTML("<br/><br/>")


ui.HTML("""
    <h2 class="custom">
Nombre de sites archéologiques par arrondissement   
    </h2>
    """)

#Création d'histogramme

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
        text="Nombre de sites",
        color_discrete_sequence=["#d072a4"]
        
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

# Boutons vers le téléchargement des sources 

ui.HTML("""
<div style="font-family: 'Monserrat', sans-serif; font-size: 16px; line-height: 1.6;">
  <p><strong>Sources de données :</strong></p>
  <p>
    <strong>Flux WMS :</strong><br>
    <a href="https://mapsref.brgm.fr/wxs/georisques/risques" target="_blank" class="btn-link">Enveloppe inondation</a>
    <a href="https://geoservices.brgm.fr/risques" target="_blank" class="btn-link">Mouvements de terrain</a>
  </p>
  <p>
    <strong>Anciennes carrières (.shp) :</strong><br>
    <a href="https://www.data.gouv.fr/fr/datasets/r/8569d081-c63e-4f63-aa4e-a8eccf70264e" target="_blank" class="btn-link">Télécharger le shapefile</a>
  </p>
  <p>
    <strong>Référentiel archéologique de Paris (.csv) :</strong><br>
    <a href="https://www.data.gouv.fr/api/1/datasets/r/fb42db24-7fe5-4ebd-85ad-d9d153243979" target="_blank" class="btn-link">Télécharger le fichier CSV</a>
  </p>
</div>
""")

