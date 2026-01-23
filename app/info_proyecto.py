import streamlit as st

def mostrar_info_proyecto():
    st.title("Tendencias temáticas en Trabajos Finales de Graduación")
    st.markdown("""
    Esta aplicación muestra el desarrollo del proyecto de análisis de trabajos finales de carreras de grado de una institución de educación superior argentina, aplicando técnicas de modelado de tópicos.
    Este proyecto forma parte de la tesis de Maestría en Ciencia de Datos Aplicada a la Inteligencia de Negocios.
    """)

    st.markdown("""
    ## ℹ️ Modelado de tópicos
        Es una técnica de aprendizaje automático no supervisado utilizada para descubrir estructuras temáticas ocultas en grandes volúmenes de documentos. 
        Identifica grupos de palabras que aparecen juntas frecuentemente para representar temas latentes, sin necesidad de etiquetas previas
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
    ## 📁 Organización de este sitio
    Esta aplicación está organizada en 4 secciones:
    1. Información del proecto: presenta brevemente el objetivo de la aplicación y la organización de la misma.
    2. Visión general: se muestra el volumen de producción académica estudiantil de la Universidad y publicado entre los años 2015 y 2024.
    3. Análisis por carrera: se focaliza en el análisis estadístico de tres carreras.
    4. Exploración de tópicos: se presenta los resultados del modelado temático con BERTopic aplicado a las tres carreras seleccionadas.
    """)
    # 2. Dashboard del dataset de las tres carreras seleccionadas
    # 3. Dashboard de resultados del modelado temático
    # 4. Información técnica y metodológica del proyecto
    # """)
    