import zipfile
import os

def descomprimir_zip(archivo_zip):

    nbre = archivo_zip.split('.')
    # Directorio donde se extraerán los archivos
    directorio_extraccion ="../modelos/"+nbre[0]
    #directorio_extraccion = 'ruta/a/tu/carpeta'
    
    # Abre el archivo ZIP en modo de lectura
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        # Extrae todos los archivos al directorio especificado
        zip_ref.extractall(directorio_extraccion)
    
    print(f"Archivos extraídos de '{nombre_archivo_zip}' en '{directorio_extraccion}'")


