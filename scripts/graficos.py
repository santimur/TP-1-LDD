'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Generar gráficos de relación de tablas.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# CARGA DE DATOS
# -----------------------------
carpeta_modelo = 'ruta/carpeta_TablasModelo'       # Cargar ruta correspondiente a la ubicacion de la carpeta TablasModelo (finalizando con /)
carpeta_consultas = 'ruta/carpeta_consultasSQL'    # Cargar ruta correspondiente a la ubicacion de la carpeta consultasSQL (finalizando con /)
df_biblios = pd.read_csv(carpeta_modelo + "bibliotecas_populares_limpio.csv")
df_deptos = pd.read_csv(carpeta_modelo + "departamentosNUEVO.csv")
df_ee = pd.read_csv(carpeta_modelo + "establecimientos_educativos_limpia.csv")
df_niveles_por_dpto = pd.read_csv(carpeta_modelo + "nivel_educativo_por_departamento_3fn.csv")
df_niveles_ee = pd.read_csv(carpeta_modelo + "niveles_establecimientos_comunes_3FN.csv")
df_consulta_i = pd.read_csv(carpeta_consultas + "consulta_i.csv")
# -----------------------------
# i) Cantidad de BP por provincia (ordenado de forma decreciente)
# -----------------------------

# Join BP con departamentos para obtener provincia
df_bp_prov = df_biblios.merge(df_deptos, on="id_depto")
bp_por_provincia = df_bp_prov.groupby("provincia").size().sort_values(ascending=False)

# Grafico
plt.figure()
bp_por_provincia.plot(kind="bar")
plt.title("Cantidad de Bibliotecas Populares por Provincia")
plt.ylabel("Cantidad de BP")
plt.xlabel("Provincia")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("bp_por_provincia.png")
plt.show()

# -----------------------------
# ii) Cantidad de EE por depto vs población (por nivel y grupo etario)
# -----------------------------

# Creación del gráfico en un solo scatter plot
fig, ax = plt.subplots(figsize=(12, 7))

# Agrego un scatter plot por cada nivel educativo (con color diferente)
ax.scatter(df_consulta_i['poblacion_jardin'], df_consulta_i['jardines'], color='orange', label='Jardín (0-5 años)', alpha=0.7)
ax.scatter(df_consulta_i['poblacion_primaria'], df_consulta_i['primarias'], color='blue', label='Primaria (6-12 años)', alpha=0.7)
ax.scatter(df_consulta_i['poblacion_secundaria'], df_consulta_i['secundarios'], color='green', label='Secundaria (13-17 años)', alpha=0.7)

# Títulos y etiquetas
ax.set_title('Cantidad de EE vs Población por Nivel Educativo y Grupo Etario')
ax.set_xlabel('Población por Nivel Educativo')
ax.set_ylabel('Cantidad de Establecimientos Educativos')

# Leyenda y estética
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("EE_vs_depto_y_poblacion.png")
plt.show()


# -----------------------------
# iii) Boxplot por provincia de cantidad de EE por depto
# -----------------------------

# Agrupar EE por depto
ee_por_dpto = df_ee.groupby("id_depto").size().reset_index(name="cant_ee")

# Merge con departamentos
ee_con_prov = ee_por_dpto.merge(df_deptos, on="id_depto")

# Ordenar provincias por mediana
orden_provincias = ee_con_prov.groupby("provincia")["cant_ee"].median().sort_values().index

# Grafico
plt.figure(figsize=(14, 6))
sns.boxplot(
    data=ee_con_prov,
    x="provincia",
    y="cant_ee",
    order=orden_provincias,
    palette="pastel"
)
plt.xticks(rotation=45, ha="right")
plt.title("Distribución de EE en cada Provincia")
plt.ylabel("Cantidad de EE")
plt.xlabel("Provincia")
plt.tight_layout()
plt.savefig("boxplot_ee_por_provincia.png")
plt.show()

# -----------------------------
# iv) Relación BP y EE cada mil habitantes por departamento
# -----------------------------

# Sumamos la población por depto como suma total de alumnos
poblacion_depto = df_niveles_por_dpto.groupby("id_depto")["cantidad"].sum().reset_index(name="poblacion")

# BP por depto
bp_por_dpto = df_biblios.groupby("id_depto").size().reset_index(name="cant_bp")

# EE por depto
ee_por_dpto = df_ee.groupby("id_depto").size().reset_index(name="cant_ee")

# Merge
df_rel = poblacion_depto.merge(bp_por_dpto, on="id_depto", how="left")\
                        .merge(ee_por_dpto, on="id_depto", how="left")\
                        .fillna(0)

# Calculamos datos por mil habitantes
df_rel["bp_x_mil"] = df_rel["cant_bp"] * 1000 / df_rel["poblacion"]
df_rel["ee_x_mil"] = df_rel["cant_ee"] * 1000 / df_rel["poblacion"]

# Grafico
plt.figure()
sns.scatterplot(
    data=df_rel,
    x="bp_x_mil",
    y="ee_x_mil"
)
plt.title("Relación entre BP y EE cada mil habitantes por Departamento")
plt.xlabel("BP cada mil habitantes")
plt.ylabel("EE cada mil habitantes")
plt.tight_layout()
plt.savefig("bp_vs_ee_por_mil_hab.png")
plt.show()