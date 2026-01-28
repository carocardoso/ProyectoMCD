# contiene funciones básicas o repetitivas en diferentes scripts
ROJO = "\033[31m"
VERDE = "\033[32m"
CYAN = "\033[96m"
RESET = "\033[0m" # Restablece el color

NEGRITA = "\033[1m"
NORMAL = "\033[0m"

def mostrar_titulo(texto):  #formato para títulos de resultados


    print(ROJO +"="* (len(texto) + 4))
    print(ROJO+NEGRITA+f"🔶 {texto}"+NORMAL)
    print(ROJO+"="*(len(texto) + 4)+RESET)


    