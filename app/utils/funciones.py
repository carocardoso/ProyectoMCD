# contiene funciones básicas o repetitivas en diferentes scripts
ROJO = "\033[31m"
VERDE = "\033[32m"
CYAN = "\033[96m"
RESET = "\033[0m" # Restablece el color

NEGRITA = "\033[1m"
NORMAL = "\033[0m"

# Definir colores para gráficos
colores = ['#2E86AB', '#A23B72', '#F18F01']

def mostrar_titulo(texto):  #formato para títulos de resultados


    print(ROJO +"="* (len(texto) + 4))
    print(ROJO+NEGRITA+f"🔶 {texto}"+NORMAL)
    print(ROJO+"="*(len(texto) + 4)+RESET)


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

    