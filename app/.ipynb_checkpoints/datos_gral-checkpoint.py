import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import plotly.express as px
from pathlib import Path
import os

def cargar_datos():
    base_path = Path(__file__).resolve().parent.parent
    ruta = base_path / "datos" / "datos_seleccionados.csv"
    print("RUTA: ")
    print(ruta)
    df = pd.read_csv(ruta, encoding="latin1", sep=";")
    return df
    
def mostrar_datos_gral():
    df = cargar_datos()
    
    st.title("📊 Datos del proyecto")
    st.markdown("""    Se presenta información general de los TFG recopilados    """)
    
    st.subheader("📌 Resumen General del Repositorio")
    
    cols = st.columns(4)
    with cols[0]:
        ui.metric_card(title="Total TFG", content=len(df), key="card1")
    with cols[1]:
        ui.metric_card(title="Total Carreras", content=df["carrera"].nunique(),  key="card2")
    with cols[2]:
        ui.metric_card(title="Total Facultades", content= df['facultad'].nunique(), key="card3")
    with cols[3]:
        ui.metric_card(title="Años analizados", content= f"{df['anio'].min()} - {df['anio'].max()}", key="card4")

    st.subheader("⭐ Ranking por Facultades")
    
    fig_fac = px.bar(df.groupby("facultad")["titulo"].count())
    fig_fac.update_layout(title="Distribución de TFG por Facultad")
    st.plotly_chart(fig_fac, width='stretch') #use_container_width=True)

    fig_anio = px.bar(df.groupby("anio")["titulo"].count())
    fig_anio.update_layout(title="Distribución de TFG por Años")
    st.plotly_chart(fig_anio, width='stretch')  # use_container_width=True)


    st.subheader("⭐ Ranking por Carreras")
    
    df_ranking = df["carrera"].value_counts().reset_index()
    df_ranking.columns = ["carrera", "cantidad"]
    fig_carr = px.bar(df_ranking,
        x="carrera",
        y="cantidad",
        title="Ranking de Carreras",
    )
    st.plotly_chart(fig_carr, config={"responsive": True} )

    st.dataframe(df_ranking, width='stretch')
    
