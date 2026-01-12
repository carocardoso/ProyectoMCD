import streamlit as st
#import os
import pandas as pd
import numpy as np
import streamlit_shadcn_ui as ui
import plotly.express as px
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
sns.set()
from wordcloud import WordCloud


def cargar_datos():
   # directorio_actual = os.getcwd()
    base_path = Path(__file__).resolve().parent.parent
    ruta = base_path / "datos" / "datos_carr_sel_prepro.csv"
    df = pd.read_csv(ruta, encoding="latin1", sep=";")
    
   # df = pd.read_csv("datos\\datos_carr_sel_prepro.csv", encoding='latin1', sep=";")
    return df

def mostrar_carreras_sel():
    st.title("📊 Datos de las carreras seleccionadas")
    st.markdown("""    Se presenta información de los TFG seleccionados para el modelado de tópicos.    """)

    df = cargar_datos()

    # ------------------------------
    # FILTROS SIDEBAR
    # ------------------------------
    st.sidebar.header("🔍 Filtros")

    df_carreras = sorted(df["carrera"].dropna().unique())
    df_carreras = np.insert(df_carreras, 0, 'Todas')
    carrera = st.sidebar.selectbox("Carrera", df_carreras)


    # # Selección de carrera
    # # --------------------
    # # agregar "Todas" a la selección de las carreras
    # df_carreras = df["carrera"].unique()    
    # df_carreras = np.insert(df["carrera"].unique(), 0, 'Todas')
    
    #st.sidebar.title("Opciones de análisis")
    
  #  df_info_carr = df
    # cols = st.columns(2)
    # with cols[0]:
    #     carrera = st.selectbox("Seleccionar carrera:", df_carreras)
    # # with cols[1]:

    df_info_carr = df
    if carrera!='Todas':        
        df_info_carr = df[df["carrera"] == carrera]

    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader(f"🎓 Análisis de la carrera:")
        st.subheader(f" {carrera}")
    with cols2[1]:
        st.subheader(f" 🧮 Total TFG: {len(df_info_carr)}")

    # Gráfico de barras: cantidad de TFG por años
    #-------------------------------------------
    fig_anio = px.bar(df_info_carr.groupby("anio")["titulo"].count(),
                      title="TFG por año en la carrera seleccionada")
    st.plotly_chart(fig_anio, use_container_width=True)

    # Lista de TFG
    # ----------------
        # Lista de TFG seleccionados
    #----------------------------
    
    df_lista = df_info_carr[['anio','titulo','descargas','vistas','url']].sort_values(by='anio', ascending=False)
    
    st.data_editor(
    df_lista,
        column_config={
            "url": st.column_config.LinkColumn(
                "Ver TFG", display_text="🔗",
            ),
        },
        hide_index=True,
    )
    
    # df_lista = df_info_carr[['anio','titulo','resumen','descargas','vistas']]
    # st.dataframe(df_lista, width='stretch')
    
    # Crear nube de palabras
    # -------------------------
    st.subheader("Nube de palabras")
    texto = " ".join(df_info_carr["texto_tok"])

    nube = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        max_words=100,
        collocations=False
    ).generate(texto)
    st.image(nube.to_array(), use_container_width=False, width=500)

    
#     # Lista de TFG seleccionados
#     #----------------------------
    
#     df_lista = df_info_carr[['anio','titulo','descargas','vistas','url']]
    
#     st.data_editor(
#     df_lista,
#     column_config={
#         "url": st.column_config.LinkColumn(
#             "Ver TFG", display_text="🔗",
#         ),
#     },
#     hide_index=True,
# )
   