import pandas as pd

def procesar_datos(df):
    # Ejemplo: agregar columna longitud del título
    df["longitud_titulo"] = df["titulo"].str.len()
    return df
