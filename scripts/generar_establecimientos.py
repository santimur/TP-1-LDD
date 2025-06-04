'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Generar tabla de establecimientos educativos.
'''

import pandas as pd

# Ruta al archivo original
ruta_archivo = "ruta/TablasOriginales/establecimientos_educativos.xlsx"

# Leer el archivo usando la fila 12 (índice 11) como encabezado
df = pd.read_excel(ruta_archivo, header=12)

# Limpiar nombres de columnas de espacios (por si acaso)
df.columns = df.columns.str.strip()

# Renombrar columnas
df = df.rename(columns={
    "Cueanexo": "id_establecimiento",
    "Nombre": "nombre_establecimiento",
    "Código de departamento": "id_depto",
    "Ámbito": "ambito",
    "Común": "modalidad_comun",
    "Especial": "modalidad_especial",
    "Adultos": "modalidad_adultos"
})

# Seleccionar columnas deseadas
columnas_finales = [
    "id_establecimiento",
    "nombre_establecimiento",
    "id_depto",
    "ambito",
    "modalidad_comun",
    "modalidad_especial",
    "modalidad_adultos"
]

df = df[columnas_finales]

# Eliminar duplicados
df = df.drop_duplicates()

# Exportar a CSV limpio
ruta_salida = "ruta/TablasModelo/establecimientos_educativos_limpia.csv"
df.to_csv(ruta_salida, index=False)

print("Archivo generado con las columnas seleccionadas:", ruta_salida)
