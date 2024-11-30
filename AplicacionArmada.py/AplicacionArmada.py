import streamlit as st 
import pandas as pd
import plotly.express as px
from PIL import Image
import folium
from streamlit_folium import st_folium

# Configuración de la página
img = Image.open("ArmadaChile.png")
st.set_page_config(page_title="Armada de Chile", page_icon=img, layout="wide", initial_sidebar_state="collapsed")

# Título de la página
st.title("Armada de Chile")    
with st.container():
    image_url = "https://www.armada.cl/armada/site/artic/20220609/imag/foto_0000003020220609101856/BAE.jpg"
    st.markdown(
        f"""
        <style>
        .header {{
            background-image: url('{image_url}');
            background-size: 105%;
            background-position: center;
            height: 250px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<p class="header"></p>', unsafe_allow_html=True)

# Opciones del sidebar
st.sidebar.title("Opciones")
pagina = st.sidebar.selectbox("Selecciona una opción", ["Postulantes y seleccionados", "División de tropas", "Mapa reparticiones navales"])
if pagina == "Postulantes y seleccionados":
    df = pd.read_csv("C:/Users/David/Desktop/Proyecto/PostulantesMarina_NAVAL.csv")
    df_avg = df.groupby("Año")["POSTULANTES"].mean().reset_index()
    fig2 = px.bar(df_avg, x="Año", y="POSTULANTES", title="Promedio de postulantes por Año Escuela Naval", color="Año")
    st.plotly_chart(fig2)

    df_esgram = pd.read_csv("C:/Users/David/Desktop/Proyecto/PostulantesMarina_ESGRAM.csv")       
    df_esgram['Año'] = df_esgram['Subcategoría'].str[:4]
    df_avg = df_esgram.groupby("Año")["POSTULANTES"].mean().reset_index()
    fig2 = px.bar(df_avg, x="Año", y="POSTULANTES", title="Promedio de Postulantes por Año Escuela de Grumetes", color="Año")
    st.plotly_chart(fig2)

# Sección de División de Tropas
elif pagina == "División de tropas":  # Aquí debería ser `elif` ya que sigue al `if` anterior
    df_tropa = pd.read_csv("C:/Users/David/Desktop/Proyecto/tropa_limpio.csv")
    df_ingreso_mujeres = pd.read_csv("C:/Users/David/Desktop/Proyecto/ingresoMujeresEscuelasMatrices2_limpio.csv")

    df_tropa_sum = df_tropa.groupby("Año")["Planificado"].sum().reset_index()
    df_ingreso_mujeres_sum = df_ingreso_mujeres[["Año_2010", "Año_2011", "Año_2012"]].sum().reset_index(name='Total Mujeres')

    df_combined = pd.DataFrame({
        "Categoría": ["Mujeres", "Tropa"],
        "Cantidad": [df_ingreso_mujeres_sum["Total Mujeres"].sum(), df_tropa_sum["Planificado"].sum()]
    })

    fig = px.pie(df_combined, names="Categoría", values="Cantidad", title="Porcentaje de Mujeres vs. Tropa Profesional")
    st.plotly_chart(fig)

# Sección de Mapa de Reparticiones Navales
elif pagina == "Mapa reparticiones navales": 
     st.subheader("Mapa de Reparticiones Navales") 
     if pagina == "Mapa reparticiones navales":
       
        data = pd.DataFrame({
        "ciudad": ["Arica", "Iquique", "Antofagasta", "Caldera", "Coquimbo", 
                   "Valparaíso", "Talcahuano", "San Antonio", "Valdivia", 
                   "Punta Arenas", "Puerto Montt", "Puerto Aysén", "Chaitén"],
        "latitud": [-18.4783, -20.2307, -23.6509, -27.0675, -29.9533, 
                    -33.0472, -36.724, -33.5938, -39.8142, 
                    -53.1625, -41.4693, -45.4032, -42.918],
        "longitud": [-70.3126, -70.1357, -70.3975, -70.8176, -71.3380, 
                     -71.6127, -73.1168, -71.6210, -73.2459, 
                     -70.9078, -72.9424, -72.6915, -72.7086]
    })

    # Crear el mapa centrado en Chile
        mapa = folium.Map(location=[-35.6751, -71.543], zoom_start=5)

    # Agregar marcadores al mapa
        for _, row in data.iterrows():
            folium.Marker(
            location=[row["latitud"], row["longitud"]],
            popup=row["ciudad"]
        ).add_to(mapa)

    
     st_folium(mapa, width=700, height=500)