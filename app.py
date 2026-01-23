import streamlit as st

from app.info_proyecto import mostrar_info_proyecto
from app.datos_gral import mostrar_datos_gral
from app.carreras_sel import mostrar_carreras_sel
from app.dashboard_proceso import mostrar_procesados
from streamlit_option_menu import option_menu


# --- Configuración general ---
st.set_page_config(
    page_title="Proyecto de Tesis Maestría en Ciencia de Datos",
    page_icon="📊",
    layout="wide"
)

with st.sidebar:
    seccion=option_menu(
        menu_title="",
        options=["Información del Proyecto", "Visión General", "Análisis por Carreras","Exploración de Tópicos"],
        icons=["info-circle", "bar-chart", "stack of books", "save instagram"])     #"bar-chart"  graph-up-arrow  funnel

if seccion == "Información del Proyecto":
    mostrar_info_proyecto()

elif seccion == "Visión General":
    mostrar_datos_gral() 
    
elif seccion == "Análisis por Carreras":
    mostrar_carreras_sel()
    
elif seccion == "Exploración de Tópicos":
    mostrar_procesados()   
