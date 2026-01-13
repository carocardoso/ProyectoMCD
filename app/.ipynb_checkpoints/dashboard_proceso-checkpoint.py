import streamlit as st
import pandas as pd
import plotly.express as px
import os
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import zipfile
from pathlib import Path

# -----------------------------------------------------------
# Cargar archivos
# -----------------------------------------------------------
def cargar_datos():
    #path = os.getcwd()
    #path_datos = os.path.join(path, "datos")

    base_path = Path(__file__).resolve().parent.parent
    #ruta = base_path / "datos" / "datos_seleccionados.csv"
#    df = pd.read_csv(ruta, encoding="latin1", sep=";")

    # TOPIC_DOCS_CSV = os.path.join(path_datos, "topic_docs.csv")
    # TOPIC_FREQ_CSV = os.path.join(path_datos, "topic_freq.csv")
    # DOCS_CSV = os.path.join(path_datos, "datos_carr_sel_prepro.csv")

    TOPIC_DOCS_CSV = base_path / "datos" / "topic_docs.csv"
    TOPIC_FREQ_CSV = base_path / "datos" / "topic_freq.csv"
    DOCS_CSV = base_path / "datos" / "datos_carr_sel_prepro.csv"

    df_tfreq = pd.read_csv(TOPIC_FREQ_CSV, encoding="latin1", sep=";") #, on_bad_lines="warn")
    df_tdocs = pd.read_csv(TOPIC_DOCS_CSV, encoding="latin1", sep=";") #, on_bad_lines="warn")
    df_docs = pd.read_csv(DOCS_CSV, encoding="latin1", sep=";")

    # nombres de columnas homogéneos
    df_tfreq.columns = df_tfreq.columns.str.lower()
    df_tdocs.columns = df_tdocs.columns.str.lower()
    df_docs.columns = df_docs.columns.str.lower()

    return df_tdocs, df_tfreq, df_docs


# -----------------------------------------------------------
# Cargar modelo BERTopic
# -----------------------------------------------------------
def cargar_modelo(carrera):
   # path = os.getcwd()
   # path_modelos = os.path.join(path, "modelos")
    base_path = Path(__file__).resolve().parent.parent
  #  ruta = base_path / "datos" / "datos_seleccionados.csv"

    carrera_modelo = "model_"+carrera.replace(" ", "_")
    #carrera_modelo = "model_Licenciatura_en_Psicología"   # Línea que vos usaste para pruebas

    model_path = base_path / "modelos" / carrera_modelo  #os.path.join(path_modelos, carrera_modelo)
    print("MODELO:", model_path)

    carrera_zip = carrera_modelo + ".zip" 
    zip_path =  base_path / "modelos" / carrera_zip  # os.path.join(path_modelos, carrera_modelo + ".zip")

    
    # Verificar si la carpeta del modelo existe
    if not os.path.exists(model_path):
        print(f"La carpeta del modelo no existe: {model_path}")
        
        # Verificar si existe el ZIP para descomprimirlo
        if os.path.exists(zip_path):
            print(f"Descomprimiendo modelo desde: {zip_path} ...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(path_modelos)
            print("Descompresión completa.")
        else:
            raise FileNotFoundError(
                f"No se encontró la carpeta del modelo ni el archivo ZIP: {zip_path}"
            )

    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    modelo = BERTopic.load(model_path, embedding_model)
    return modelo


# -----------------------------------------------------------
# Dashboard
# -----------------------------------------------------------
def mostrar_procesados():

    st.set_page_config(
        page_title="Análisis de Tópicos por Carrera",
        layout="wide"
    )

    st.title("📘 Tópicos por Carrera")
    st.markdown("Exploración interactiva de tópicos generados con **BERTopic**.")

    topicdocs, topicfreq, docs = cargar_datos()

    # ------------------------------
    # FILTROS SIDEBAR
    # ------------------------------
    st.sidebar.header("🔍 Filtros")

    carreras = sorted(docs["carrera"].dropna().unique())
    carrera_sel = st.sidebar.selectbox("Carrera", carreras)

    # ------------------------------
    # FILTRO POR CARRERA
    # ------------------------------
    tdocs_filtrado = topicdocs[ (topicdocs["carrera"] == carrera_sel) ] #&   (topicdocs["topic"] != -1)]
    print(topicfreq.columns)
    tfreq_filtrado = topicfreq[(topicfreq["carrera"] == carrera_sel) ] #& (topicfreq["topic"] != -1) ]

    docs_filtrado = docs[docs["carrera"] == carrera_sel]   # 🔥 Este es el correcto

    # ------------------------------
    # Frecuencia de tópicos
    # ------------------------------
    st.subheader(f"📊 Frecuencia de Tópicos - {carrera_sel}")

    fig_bar = px.bar(
        tfreq_filtrado,
        x="topic",
        y="count",
        color="count",
        title=f"Tópicos más frecuentes en {carrera_sel}"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ------------------------------
    # Cargar modelo
    # ------------------------------
    modelo = cargar_modelo(carrera_sel)

    # ------------------------------
    # Info de tópicos
    # ------------------------------
    st.header("📌 Exploración de tópicos de la carrera")

    freq_lista = modelo.get_topic_info()
    freq_lista = freq_lista[["Topic", "Count", "Representation"]]

    st.dataframe(
        freq_lista,
        column_config={
            "Topic": st.column_config.TextColumn(
            "Tópico"
        ),
            "Count": st.column_config.TextColumn(
            "Cant. Docs.",
            max_chars=15
        ),
            
        },
        hide_index=True,
    )

    all_topics = modelo.get_topics()

    fig1 = modelo.visualize_barchart(
        top_n_topics=len(all_topics),
        n_words=5
    )
    st.plotly_chart(fig1, use_container_width=True)

    if (len(all_topics) - 1) > 2:
        st.write("Distribución entre tópicos")
        fig2 = modelo.visualize_topics()
        st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------------------------------
    # 🔥 Evolución de tópicos en el tiempo
    #   (CORREGIDO — usa df_docs filtrado, no topicdocs)
    # ----------------------------------------------------
    st.header("📈 Evolución de tópicos por año")

    docs_list = docs_filtrado["texto_limpio"].tolist()
    timestamps = docs_filtrado["anio"].tolist()

    print("Docs:", len(docs_list))
    print("Timestamps:", len(timestamps))

    # -----------------------------------------
    # DEBUG PROFUNDO – NECESARIO
    # -----------------------------------------
    print("\n===== DEBUG TOPICS_OVER_TIME =====")
    print("docs_filtrado.shape:", docs_filtrado.shape)
    
    docs_list = docs_filtrado["texto_limpio"].tolist()
    timestamps = docs_filtrado["anio"].tolist()
    
    print("Len docs_list:", len(docs_list))
    print("Len timestamps:", len(timestamps))
    
    # Los topics EXACTOS que BERTopic asignó a estos documentos
    pred_topics, _ = modelo.transform(docs_list)
    print("Len pred_topics:", len(pred_topics))
    
    # Cantidad de topics asignados como -1
    print("Cantidad de -1:", sum([t == -1 for t in pred_topics]))

    # -----------------------------------------
    # DEBUG 2 – VER LOS TOPICS QUE CREA EL MODELO
    # -----------------------------------------
    pred_topics, _ = modelo.transform(docs_list)
    
    print("Len pred_topics:", len(pred_topics))
    print("Muestras de topics:", pred_topics[:20])
    
    # Contar cuántos -1 hay
    cant_menos1 = sum([t == -1 for t in pred_topics])
    print("Cantidad de topics = -1:", cant_menos1)
    topics= tdocs_filtrado["topic"]
    print("len(docs):", len(docs_list))
    print("len(topics):", len(topics))
    print("len(timestamps):", len(timestamps))

    # Ahora SÍ tienen el mismo tamaño y coinciden con el modelo
    topics_over_time = modelo.topics_over_time(
        docs_list,
        timestamps,
        nr_bins=20
    )

    fig4 = modelo.visualize_topics_over_time(
        topics_over_time,
        top_n_topics=10
    )
    st.plotly_chart(fig4, use_container_width=True)
