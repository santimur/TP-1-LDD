'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Generar bibliotecas populares.
'''


import pandas as pd
from pathlib import Path

# Ruta al archivo original
ruta_csv = Path("ruta/TablasOriginales/bibliotecas-populares.csv")

# Lectura del CSV original
bibliotecas = pd.read_csv(ruta_csv)

# Limpieza de columnas innecesarias
bibliotecas.drop(columns=[
    "tipo_latitud_longitud", 
    "telefono", 
    "web", 
    "domicilio", 
    "observacion", 
    "latitud", 
    "longitud", 
    "subcategoria", 
    "fuente", 
    "anio_actualizacion", 
    "cod_tel", 
    "piso", 
    "cp", 
    "informacion_adicional"
], inplace=True)

# Selección de columnas clave
biblioteca_2 = bibliotecas[[
    "nro_conabip",
    "nombre",
    "id_departamento",
    "departamento",
    "provincia",
    "mail",
    "fecha_fundacion"
]].copy()

# Procesamiento del email
biblioteca_2["mail"] = biblioteca_2["mail"].str.split('@').str[1]
biblioteca_2["mail"] = biblioteca_2["mail"].str.split('.').str[0]

# Procesamiento de la fecha
biblioteca_2["fecha_fundacion"] = pd.to_datetime(biblioteca_2["fecha_fundacion"], errors='coerce')
biblioteca_2["año_fundacion"] = biblioteca_2["fecha_fundacion"].dt.year
biblioteca_2.drop(columns=["fecha_fundacion"], inplace=True)

# Renombrar columnas
biblioteca_2.columns = [
    "id_biblioteca", 
    "nombre_biblioteca",
    "id_depto",
    "nombre_departamento",
    "nombre_provincia",
    "dominio_email",
    "año_fundacion"
]

# Filtrado según el modelo relacional
columnas_MR = ["id_biblioteca", "nombre_biblioteca", "id_depto", "año_fundacion", "dominio_email"]
biblioteca_clean = biblioteca_2[columnas_MR]

# Ruta de salida
ruta_salida = Path("ruta/TablasModelo/bibliotecas_populares_limpio.csv")

# Guardar CSV limpio
biblioteca_clean.to_csv(ruta_salida, index=False)
print("Archivo guardado como:", ruta_salida)
