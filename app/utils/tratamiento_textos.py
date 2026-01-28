# -*- coding: utf-8 -*-

####
### USAR TPU

# import threading
# import subprocess
# import time
# import requests
import os
from collections import Counter
#from nltk import word_tokenize
from nltk.tokenize import word_tokenize

#!pip install PyPDF2 langchain_core langchain_ollama

    
# si el resumen tiene pocas palabras generar un resumen más extenso    
def extraer_pal_resumen(df, pdf_path):

    for i in range(len(df)):
        reg=df.loc[i]
        tokens = word_tokenize(reg['resumen'])  #separa el texto en tokens
        cant_palabras = len([w for w in tokens if w.isalnum()])   #cuenta la cantidade palabras (sin símbolos)
        print(str(cant_palabras)+" "+str(reg['id']))
        if cant_palabras<100:
            print(str(cant_palabras)+" "+str(reg['id']))
            #extraer un resumen de pdf y reemplazar
            filename = str(reg['pdf'])
            name = filename.split("/")[-1]
            pdf_file_path = os.path.join(pdf_path, str(filename))
            
            if pdf_file_path.lower().endswith('.pdf'):
                print(f"Resumiendo {name}...")
                summary_text = name   #####    esto VA: summarize_pdf_with_ollama(pdf_file_path)
                df.iloc[i]['resumen'] = summary_text  
    return df


