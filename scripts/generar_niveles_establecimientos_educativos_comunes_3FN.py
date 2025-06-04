'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Generar niveles de EE comunes en 3FN.
'''

import pandas as pd

# Leer archivo original
ruta_archivo = "ruta/TablasOriginales/establecimientos_educativos.xlsx"
df = pd.read_excel(ruta_archivo, header=12)
df.columns = df.columns.str.strip()

# Renombrar columnas relevantes
df = df.rename(columns={
    "Cueanexo": "id_establecimiento",
    "Código de departamento": "id_depto",
    "Común": "modalidad_comun",
    "Nivel inicial - Jardín maternal": "jardin_maternal",
    "Nivel inicial - Jardín de infantes": "jardin_infante",
    "Primario": "primario",
    "Secundario": "secundario",
    "Secundario - INET": "secundario_inet",
    "SNU": "snu",
    "SNU - INET": "snu_inet",
    "SNU - Cursos": "snu_cursos"
})

# Filtrar solo establecimientos de modalidad común
df_comun = df[df["modalidad_comun"] == 1].copy()

# Lista de niveles a transformar
niveles = [
    "jardin_maternal",
    "jardin_infante",
    "primario",
    "secundario",
    "secundario_inet",
    "snu",
    "snu_inet",
    "snu_cursos"
]

# Seleccionar columnas necesarias
df_niveles = df_comun[["id_establecimiento"] + niveles].copy()

# Transformar a formato largo (long format)
df_long = df_niveles.melt(id_vars="id_establecimiento", 
                          value_vars=niveles,
                          var_name="id_nivel", 
                          value_name="tiene")

# Filtrar solo filas donde tiene == 1
df_long = df_long[df_long["tiene"] == 1].copy()
df_long.drop(columns="tiene", inplace=True)

# Guardar archivo
ruta_salida = "ruta/TablasModelo/niveles_establecimientos_comunes_3FN.csv"
df_long.to_csv(ruta_salida, index=False)

print("Archivo generado:", ruta_salida)

