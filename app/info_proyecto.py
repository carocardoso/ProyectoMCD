import streamlit as st

def mostrar_info_proyecto():
    st.title("ℹ️ Información del Proyecto")
    st.markdown("""
    Esta aplicación muestra el desarrollo del proyecto de análisis de trabajos finales de carreras de grado de una Universidad Argentina, aplicando técnicas      de modelado de tópicos.
    Este proyecto forma parte de la tesis de maestría y tiene como propósito analizar tendencias en los trabajos finales de algunas carreras universitarias.
    << completar>>
    """)
    
    # ## 🎯 Objetivo del Trabajo
    # Analizar tendencias en los trabajos finales de tres carreras universitarias.

    # ## 🛠️ Herramientas utilizadas
    # - **Python**
    # - **Pandas**
    # - **Streamlit**
    # - **Jupyter Notebooks**
    # - **Plotly**
    # - **Procesamiento de Lenguaje Natural**
    
    st.markdown("""
    ## 📁 Organización del Proyecto
    La interfaz de este sitio está organizada de la siguiente manera:
    1. Dashboard del dataset principal
    2. Dashboard del dataset de las tres carreras seleccionadas
    3. Dashboard de resultados del modelado temático
    4. Información técnica y metodológica del proyecto
    """)
    