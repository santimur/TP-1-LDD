'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Generar bibliotecas populares.
'''

import pandas as pd

# Ruta al archivo
ruta_archivo = "ruta/scripts/TablasOriginales/establecimientos_educativos.xlsx"

# Cargar datos a partir de la fila 14 (index 13), sin encabezados
df = pd.read_excel(ruta_archivo, header=None, skiprows=13)

# Seleccionar columnas por posición: 
# - Columna 4 → ID depto
# - Columna 5 → nombre depto
# - Columna 5 → nombre localidad
# - Columna 2 → nombre provincia
df_departamentos = df[[4, 3, 0]].dropna().drop_duplicates().copy()

# Renombrar columnas
df_departamentos.columns = ['id_depto', 'nombre_depto', 'provincia']

# Asegurar que el ID quede como string con ceros (ej: 02007)
df_departamentos['id_depto'] = df_departamentos['id_depto'].astype(str).str.zfill(5)

# Guardar CSV
df_departamentos.to_csv("ruta/TablasModelo/departamentosNUEVO.csv", index=False)


print("Archivo 'departamentosNUEVO.csv' generado correctamente con ID numérico.")