'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Generar Población (nivel educativo por departamento) en 3FN.
'''


import pandas as pd

# Cargar niveles (desde niveles.csv)
niveles_dict = {
    "jardin_maternal": [0, 1, 2, 3],
    "jardin_infante": [4, 5],
    "primaria": list(range(6, 13)),
    "secundaria": list(range(13, 19)),
    "terciario": list(range(19, 51))
}

# Leer archivo original
ruta_excel = "ruta/TablasOriginales/Poblacion_por_Edad_por_Departamento.xlsx"
df_raw = pd.read_excel(ruta_excel, skiprows=12, header=None)

# Eliminar filas vacías
df = df_raw.dropna(how='all').reset_index(drop=True)

# Lista para almacenar resultados
resultados = []

i = 0
while i < len(df):
    fila = df.iloc[i]
    
    if isinstance(fila[1], str) and "AREA #" in fila[1]:
        id_depto = int(fila[1].split("AREA #")[-1].strip())
        nombre_departamento = fila[2]

        i += 1
        while i < len(df) and not (df.iloc[i][1] == "Edad"):
            i += 1
        i += 1
        
        # Inicializar acumulador por nivel
        niveles_contadores = {nivel: 0 for nivel in niveles_dict}
        poblacion_total = 0
        
        while i < len(df):
            edad = df.iloc[i][1]
            casos = df.iloc[i][2]
            
            if isinstance(edad, str) and edad.strip().lower() == "total":
                poblacion_total = casos
                i += 1
                break
            
            if pd.api.types.is_number(edad):
                edad = int(edad)
                for nivel, edades in niveles_dict.items():
                    if edad in edades:
                        niveles_contadores[nivel] += casos
            i += 1

        # Guardar datos por nivel
        for nivel, cantidad in niveles_contadores.items():
            resultados.append({
                "id_depto": id_depto,
                "id_nivel": nivel,
                "cantidad": cantidad
            })
        # También podés agregar la población total si querés como fila extra (opcional)

    else:
        i += 1

# Crear DataFrame final
df_resultado = pd.DataFrame(resultados)

# Agrupar comunas de CABA
df_resultado.loc[df_resultado['id_depto'].astype(str).str.startswith("20"), 'id_depto'] = 2000
df_agrupado = df_resultado.groupby(["id_depto", "id_nivel"], as_index=False)["cantidad"].sum()

# Exportar CSV final normalizado
ruta_salida = "ruta/TablasModelo/nivel_educativo_por_departamento_3fn.csv"
df_agrupado.to_csv(ruta_salida, index=False)
print("Archivo en formato 3FN generado:", ruta_salida)
