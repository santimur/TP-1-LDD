'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Métricas GQM.
'''

import pandas as pd

# Cargar el archivo CSV
df = pd.read_excel("ruta/TablasOriginales/establecimientos_educativos.xlsx" , header=12)


# Filtrar filas con email no vacío
df_validos = df[~df["Mail"].isna()]
N_total = len(df_validos)

# Definir separadores sospechosos de múltiples mails
separadores = r"[;,/\-]"

# Crear máscara booleana: True si el campo contiene alguno de los separadores
multi_mask = df_validos["Mail"].astype(str).str.contains(separadores)

# Contar cuántos casos hay con múltiples correos
N_multi = multi_mask.sum()
P_multi = (N_multi / N_total) * 100

# Mostrar resultados
print(f"Registros con email no nulo: {N_total}")
print(f"Registros con múltiples direcciones detectadas: {N_multi}")
print(f"Porcentaje con múltiples mails: {P_multi:.2f}%")