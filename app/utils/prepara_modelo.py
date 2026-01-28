# generar_umap_y_topics.ipynb / .py
# Requisitos: bertopic>=0.17.3, umap-learn, pandas, safetensors (si usaste safetensors)
# Ejecutar en el mismo entorno donde guardaste el modelo.
# Ajusta `MODEL_FOLDER`, `TOPIC_DOCS_CSV` y `TOPIC_FREQ_CSV` si es necesario.

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
#from tqdm.auto import tqdm

import os

#Ejecutar solo si no existen las carpetas con los archivos

def prueba(nbre_dir_modelo, carrera):
    # path de carpetas de modelos
    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path_modelos = os.path.join(path , 'modelos')  #muestra C:\Users\accar\Notebooks\ProyectoTesisMCD\modelos
    print(path_modelos)
    path_datos = os.path.join(path , 'datos')   #muestra C:\Users\accar\Notebooks\ProyectoTesisMCD\datos
    print(path_datos)
    
    MODEL_FOLDER = os.path.join(path_modelos , nbre_dir_modelo ) #"../modelos/model_Licenciatura_en_Psicología"  # <- carpeta del modelo
    print(MODEL_FOLDER)
    
    TOPIC_DOCS_CSV = path_datos+"/topic_docs.csv"
    TOPIC_FREQ_CSV = path_datos+"/topic_freq.csv"
    
    OUT_CSV = path_datos+"/topics_enriquecidos.csv"

    print(OUT_CSV) 
    print('1 topic freq: '+TOPIC_FREQ_CSV)
    print('1 topic docs: ' +TOPIC_DOCS_CSV)

    if Path(TOPIC_FREQ_CSV).exists():
        print('topic freq: '+TOPIC_FREQ_CSV)
        df_freq = pd.read_csv(TOPIC_FREQ_CSV, encoding='latin1', sep=';')
        # Intentamos unir por columna Topic/Topic_id
        for cand in ("Topic", "topic", "topic_id"):
            if cand in df_freq.columns:
                df_freq = df_freq.rename(columns={cand: "Topic"})
                break
        df_freq["Topic"] = df_freq["Topic"].astype(int)
        topics_enriquecidos = topics_enriquecidos.merge(df_freq, on="Topic", how="left", suffixes=("", "_freq"))
        print("Se unió topic_freq.csv.")
    if Path(TOPIC_DOCS_CSV).exists():
        print('2 topic docs: ' +TOPIC_DOCS_CSV)
        df_docs = pd.read_csv(TOPIC_DOCS_CSV, encoding='latin1', sep=';')
        # No unimos todos los docs (sería gran tamaño), guardamos aparte el merge completo si querés
        merged_docs_path = "/mnt/data/topic_docs_enriquecidos.csv"
        df_docs.to_csv(merged_docs_path, index=False)
        print("Se copió topic_docs.csv a", merged_docs_path)

def prepara_modelo(nbre_dir_modelo, carrera):
    from bertopic import BERTopic
    from umap import UMAP
    
    # path de carpetas de modelos
    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path_modelos = os.path.join(path , 'modelos')  #muestra C:\Users\accar\Notebooks\ProyectoTesisMCD\modelos
    print(path_modelos)
    path_datos = os.path.join(path , 'datos')   #muestra C:\Users\accar\Notebooks\ProyectoTesisMCD\datos
    print(path_datos)
    
        
    # Por si el archivo de embeddings está en formato safetensors
    HAS_SAFETENSORS = True
    try:
        from safetensors.numpy import load_file as safetensors_load_numpy
    except Exception:
        HAS_SAFETENSORS = False
    

    MODEL_FOLDER = os.path.join(path_modelos , nbre_dir_modelo ) #"../modelos/model_Licenciatura_en_Psicología"  # <- carpeta del modelo
    print(MODEL_FOLDER)
    
    TOPIC_DOCS_CSV = path_datos+"/topic_docs.csv"
    TOPIC_FREQ_CSV = path_datos+"/topic_freq.csv"
    
    OUT_CSV = path_datos+"/topics_enriquecidos.csv"

    print(OUT_CSV)  #muestra C:\Users\accar\Notebooks\ProyectoTesisMCD\datos/topics_enriquecidos.csv
    
    # # ---------------------------
    # # Carga del modelo BERTopic
    # # ---------------------------
    print("Cargando modelo BERTopic desde:", MODEL_FOLDER)
    topic_model = None
    if not Path(MODEL_FOLDER).exists():
         raise FileNotFoundError(f"No encontré la carpeta del modelo en {MODEL_FOLDER}")
    
    try:
        # BERTopic.load admite rutas a la carpeta del modelo guardado
        topic_model = BERTopic.load(MODEL_FOLDER)
        print("Modelo cargado vía BERTopic.load() correctamente.")
    except Exception as e:
        print("No se pudo cargar el modelo con BERTopic.load(). Intentaremos reconstruir partes desde archivos (fallback).")
        print("Error:", e)
        # no hacemos raise aquí; intentaremos cargar embeddings y topics.json manualmente
    
     
    # ---------------------------
    # Obtener info de tópicos
    # ---------------------------
    # Preferimos usar get_topic_info() (nueva API)
    topic_info_df = None
    try:
        topic_info_df = topic_model.get_topic_info()
        # get_topic_info puede devolver un DataFrame; normalizamos columnas
        # Asegurarnos que las columnas incluyan: Topic, Count, Name, Representation (o Words)
        topic_info_df = topic_info_df.rename(columns=lambda c: c.strip())
        print("Se obtuvo topic_info desde el modelo.")
    except Exception as e:
        print("No se pudo obtener topic_info desde el modelo:", e)
        # Intentamos leer topics.json si existe
        topics_json_path = Path(MODEL_FOLDER) / "topics.json"
        if topics_json_path.exists():
            with open(topics_json_path, "r", encoding="utf-8") as f:
                topics_json = json.load(f)
            # topics.json suele ser dict topic_id -> list of [word, score]
            rows = []
            for k, v in topics_json.items():
                try:
                    topic_id = int(k)
                except:
                    topic_id = k
                words = ", ".join([t[0] for t in v]) if isinstance(v, list) else str(v)
                rows.append({"Topic": topic_id, "Words": words, "Count": None})
            topic_info_df = pd.DataFrame(rows)
            print("Se construyó topic_info desde topics.json.")
        else:
            raise RuntimeError("No encontré topic_info ni topics.json para reconstruirlo.")
    
    # Aseguramos que exista columna 'Topic' como int
    if "Topic" not in topic_info_df.columns:
        # algunos métodos devuelven 'topic' o 'Topic' diferente, intentamos inferir
        for cand in ("topic", "topic_id", "Topic"):
            if cand in topic_info_df.columns:
                topic_info_df = topic_info_df.rename(columns={cand: "Topic"})
                break
    
    # ---------------------------
    # Obtener embeddings de tópicos
    # ---------------------------
    topic_embeddings = None
    embedding_sources_tried = []
    
    # 1) Intentar obtener desde el objeto topic_model (atributos habituales)
    if topic_model is not None:
        for attr in ("topic_embeddings_", "topic_embeddings", "topic_vectors_", "topic_vectors"):
            embedding_sources_tried.append(f"obj.{attr}")
            if hasattr(topic_model, attr):
                topic_embeddings = getattr(topic_model, attr)
                print(f"Encontré embeddings en topic_model.{attr}")
                break
    
    # 2) Intentar cargar archivo topic_embeddings.safetensors
    emb_file_candidates = [
        Path(MODEL_FOLDER) / "topic_embeddings.safetensors",
        Path(MODEL_FOLDER) / "topic_embeddings.npy",
        Path(MODEL_FOLDER) / "topic_embeddings.npy.npy",
        Path(MODEL_FOLDER) / "topic_embeddings"
    ]
    if topic_embeddings is None:
        for p in emb_file_candidates:
            if p.exists():
                if p.suffix == ".safetensors":
                    if not HAS_SAFETENSORS:
                        raise ImportError("El archivo topic_embeddings.safetensors existe pero no está instalado 'safetensors'. Instalalo con `pip install safetensors`.")
                    print("Cargando embeddings desde", p)
                    # safetensors numpy loader devuelve dict {tensor_name: array}
                    # normalmente hay un único tensor; extraemos el primer valor.
                    emb_dict = safetensors_load_numpy(str(p))
                    if isinstance(emb_dict, dict):
                        # tomar primer tensor
                        first_key = list(emb_dict.keys())[0]
                        topic_embeddings = emb_dict[first_key]
                    else:
                        topic_embeddings = emb_dict
                    break
                else:
                    print("Cargando embeddings desde", p)
                    try:
                        topic_embeddings = np.load(str(p))
                        break
                    except Exception as e:
                        print("Error cargando npy:", e)
    
    # 3) Si aún no hay embeddings, intentar construir a partir de ctfidf y vectorizer
    if topic_embeddings is None:
        ctfidf_candidates = [
            Path(MODEL_FOLDER) / "ctfidf.safetensors",
            Path(MODEL_FOLDER) / "c_tf_idf.npy",
            Path(MODEL_FOLDER) / "ctfidf.npy",
            Path(MODEL_FOLDER) / "c_tf_idf.npy"
        ]
        for p in ctfidf_candidates:
            if p.exists():
                print("Intentando usar c-TF-IDF desde", p)
                if p.suffix == ".safetensors":
                    if not HAS_SAFETENSORS:
                        raise ImportError("El archivo ctfidf.safetensors existe pero no está instalado 'safetensors'. Instalalo con `pip install safetensors`.")
                    ctfidf_dict = safetensors_load_numpy(str(p))
                    # Puede estar en una key
                    arr = list(ctfidf_dict.values())[0]
                    topic_embeddings = arr
                    break
                else:
                    try:
                        topic_embeddings = np.load(str(p))
                        break
                    except Exception as e:
                        print("Error cargando ctfidf npy:", e)
    
    if topic_embeddings is None:
        raise RuntimeError(f"No pude encontrar embeddings de tópicos. Intenté: {embedding_sources_tried} y buscar archivos en {MODEL_FOLDER}. Asegurate que topic_embeddings.safetensors o el atributo exista.")
    
    topic_embeddings = np.asarray(topic_embeddings)
    print("topic_embeddings shape:", topic_embeddings.shape)
    
    # ---------------------------
    # Alineamiento: qué tópicos tenemos y en qué orden
    # ---------------------------
    # topic_info_df puede tener Topic ordenado de varias formas; necesitamos alinear embeddings con topic IDs.
    # Si el modelo tiene attribute topic_model.topic_mapping (o similar), podríamos usarlo.
    topic_ids = None
    if hasattr(topic_model, "topic_mapper_"):
        # versiones pueden diferir
        try:
            topic_ids = topic_model.topic_mapper_.mapping.keys()
        except Exception:
            topic_ids = None
    
    # Método robusto: asumimos que embeddings están ordenados por índice 0..n-1 y que topic_info_df tiene la misma cantidad (o
    # topic -1 reserved for -1 topic). Comprobamos longitudes:
    n_emb = topic_embeddings.shape[0]
    n_info = topic_info_df.shape[0]
    
    print(f"N embeddings: {n_emb}, N registros topic_info: {n_info}")
    
    # Si coincide, asignamos índice incremental
    if n_emb == n_info:
        # Añadimos coordenadas por posición
        topic_info_df = topic_info_df.reset_index(drop=True)
        index_to_topicid = topic_info_df["Topic"].tolist()
        print("Cantidad de embeddings coincide con cantidad de filas topic_info. Procedemos alineación por orden.")
    else:
        # Si no coincide, intentamos inferir topic ids: buscar columna 'Topic' y ordenarlos
        print("Las dimensiones no coinciden: intentaremos alinear por 'Topic' si los ids son 0..n-1 o similar.")
        # si topic IDs van de 0..(n_emb-1) entonces ok
        possible_ids = sorted([int(t) for t in topic_info_df["Topic"].unique() if pd.notna(t)])
        if len(possible_ids) == n_emb and possible_ids == list(range(min(possible_ids), min(possible_ids)+n_emb)):
            index_to_topicid = possible_ids
            print("Alineamiento inferido: topic ids corresponden a índices de embeddings.")
        else:
            # fallback: usamos las primeras n_emb topics
            index_to_topicid = topic_info_df["Topic"].iloc[:n_emb].tolist()
            print("Alineamiento por fallback: asigné las primeras filas de topic_info a las embeddings (revisar si esto es correcto).")
    
    # Reordenamos embeddings para formar una matriz en el mismo orden que index_to_topicid
    # Si index_to_topicid es lista de topic ids en el mismo orden que embeddings, lo mantenemos.
    # Creamos un DataFrame auxiliar
    emb_df = pd.DataFrame(topic_embeddings)
    emb_df["embedding_index"] = emb_df.index
    emb_df["Topic"] = index_to_topicid[:emb_df.shape[0]]
    
    # ---------------------------
    # Calcular UMAP 2D sobre embeddings de tópicos
    # ---------------------------
    print("Calculando UMAP 2D sobre embeddings de tópicos...")
    umap = UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.0)
    coords = umap.fit_transform(topic_embeddings)
    print("UMAP generado. Shape:", coords.shape)
    
    # Añadimos coordenadas al emb_df (siempre recortamos a la longitud de coords)
    emb_df["x"] = coords[:, 0]
    emb_df["y"] = coords[:, 1]
    
    # ---------------------------
    # Construir topics_enriquecidos DataFrame
    # ---------------------------
    # Primero normalizamos topic_info_df para tener columnas clave
    df_info = topic_info_df.copy()
    if "Words" not in df_info.columns:
        # Muchas versiones usan 'Representation' o 'Name' o 'Representation' con tokens
        for cand in ("Representation", "Representations", "Name", "Representation"):
            if cand in df_info.columns:
                df_info = df_info.rename(columns={cand: "Words"})
                break
    
    # Asegurarnos Count
    if "Count" not in df_info.columns:
        # topic_info puede usar 'Count' o 'Count' lowercase
        for cand in ("count", "Counts"):
            if cand in df_info.columns:
                df_info = df_info.rename(columns={cand: "Count"})
                break
    
    # Unimos df_info con emb_df por Topic
    df_info['Topic'] = df_info['Topic'].astype(int)
    emb_df['Topic'] = emb_df['Topic'].astype(int)
    df_merged = pd.merge(df_info, emb_df[["Topic", "x", "y", "embedding_index"]], on="Topic", how="left")
    
    # Añadimos top palabras formateadas: si no existe 'Words', buscamos en topics.json
    if "Words" not in df_merged.columns or df_merged["Words"].isnull().all():
        # intentar topics.json si no lo habíamos usado antes
        topics_json_path = Path(MODEL_FOLDER) / "topics.json"
        if topics_json_path.exists():
            with open(topics_json_path, "r", encoding="utf-8") as f:
                topics_json = json.load(f)
            words_col = []
            for tid in df_merged["Topic"].tolist():
                try:
                    items = topics_json.get(str(int(tid)), topics_json.get(str(tid), []))
                    words = ", ".join([w for w,sc in items]) if isinstance(items, list) else str(items)
                except Exception:
                    words = ""
                words_col.append(words)
            df_merged["Words"] = words_col
        else:
            df_merged["Words"] = df_merged.get("Words", "")
    
    # Orden final por frecuencia si existe Count
    if "Count" in df_merged.columns and df_merged["Count"].notna().any():
        df_merged = df_merged.sort_values(by="Count", ascending=False)
    
    # Columnas útiles finales
    cols_keep = ["Topic", "Words", "Count", "x", "y", "embedding_index"]
    existing_cols_keep = [c for c in cols_keep if c in df_merged.columns]
    topics_enriquecidos = df_merged[existing_cols_keep].reset_index(drop=True)

    #agregar carrera
    topics_enriquecidos['carrera'] = carrera

    # Guardamos CSV
    topics_enriquecidos.to_csv(OUT_CSV, index=False, encoding='latin1', sep=';')
    print(f"archivo guardado: {OUT_CSV}")
    print("Resumen de topics_enriquecidos:")
    print(topics_enriquecidos.head(20))
    
    # ---------------------------
    # Opcional: enriquecer con topic_freq.csv y topic_docs.csv si existen
    # ---------------------------
    print('1 topic freq: '+TOPIC_FREQ_CSV)
    print('1 topic docs: ' +TOPIC_DOCS_CSV)
    try:
        if Path(TOPIC_FREQ_CSV).exists():
            print('topic freq: '+TOPIC_FREQ_CSV)
            df_freq = pd.read_csv(TOPIC_FREQ_CSV)
            # Intentamos unir por columna Topic/Topic_id
            for cand in ("Topic", "topic", "topic_id"):
                if cand in df_freq.columns:
                    df_freq = df_freq.rename(columns={cand: "Topic"})
                    break
            df_freq["Topic"] = df_freq["Topic"].astype(int)
            topics_enriquecidos = topics_enriquecidos.merge(df_freq, on="Topic", how="left", suffixes=("", "_freq"))
            print("Se unió topic_freq.csv.")
        if Path(TOPIC_DOCS_CSV).exists():
            print('2 topic docs: ' +TOPIC_DOCS_CSV)
            df_docs = pd.read_csv(TOPIC_DOCS_CSV)
            # No unimos todos los docs (sería gran tamaño), guardamos aparte el merge completo si querés
            merged_docs_path = "/mnt/data/topic_docs_enriquecidos.csv"
            df_docs.to_csv(merged_docs_path, index=False)
            print("Se copió topic_docs.csv a", merged_docs_path)
    except Exception as e:
        print("Advertencia al unir CSVs adicionales:", e)
        
    print("Ok")


