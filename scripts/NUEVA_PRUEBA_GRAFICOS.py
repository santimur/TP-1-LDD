# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 18:26:58 2025

@author: santi
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# -----------------------------
# CARGA DE DATOS
# -----------------------------
carpeta = 'C:/Users/santi/Documents/GitHub/TP-1-LDD/TablasModelo/'  # o ruta absoluta si preferís

df_biblios = pd.read_csv(carpeta + "bibliotecas_populares_limpio.csv")
df_deptos = pd.read_csv(carpeta + "departamentosNUEVO.csv")
df_ee = pd.read_csv(carpeta + "establecimientos_educativos_limpia.csv")
df_niveles_por_dpto = pd.read_csv(carpeta + "nivel_educativo_por_departamento_3fn.csv")
df_niveles_ee = pd.read_csv(carpeta + "niveles_establecimientos_comunes_3FN.csv")

# -----------------------------
# i) Cantidad de BP por provincia (ordenado descendente)
# -----------------------------
# Join BP con departamentos para obtener provincia
df_bp_prov = df_biblios.merge(df_deptos, on="id_depto")
bp_por_provincia = df_bp_prov.groupby("provincia").size().sort_values(ascending=False)

# Plot
plt.figure()
bp_por_provincia.plot(kind="bar", color="skyblue")
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
# Se agrupa por id_depto y nivel
df_niveles_por_dpto["grupo_etario"] = df_niveles_por_dpto["id_nivel"].map({
    "jardin_maternal": "Inicial",
    "jardin_infante": "Inicial",
    "primaria": "Niñez",
    "secundaria": "Adolescencia",
    "terciario": "Adultos"
})

# Sumar por depto, nivel y grupo
df_agg = df_niveles_por_dpto.merge(df_deptos, on="id_depto")

# Plot
plt.figure()
sns.scatterplot(
    data=df_agg,
    x="cantidad",
    y="id_depto",
    hue="grupo_etario",
    style="id_nivel",
    palette="tab10"
)
plt.title("Cantidad de EE por Departamento según Nivel Educativo")
plt.xlabel("Cantidad de EE")
plt.ylabel("ID Departamento")
plt.legend(title="Grupo Etario / Nivel")
plt.tight_layout()
plt.savefig("ee_por_depto_vs_poblacion.png")
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

# Plot
plt.figure(figsize=(14, 6))
sns.boxplot(
    data=ee_con_prov,
    x="provincia",
    y="cant_ee",
    order=orden_provincias,
    palette="pastel"
)
plt.xticks(rotation=45, ha="right")
plt.title("Distribución de EE por Departamento en cada Provincia")
plt.ylabel("Cantidad de EE")
plt.xlabel("Provincia")
plt.tight_layout()
plt.savefig("boxplot_ee_por_provincia.png")
plt.show()

# -----------------------------
# iv) Relación BP y EE cada mil habitantes por departamento
# -----------------------------
# Supuesto: la tabla de población está reflejada indirectamente en `nivel_educativo_por_departamento_3fn.csv`
# Por lo tanto, sumamos la población por depto como suma total de alumnos
poblacion_depto = df_niveles_por_dpto.groupby("id_depto")["cantidad"].sum().reset_index(name="poblacion")

# BP por depto
bp_por_dpto = df_biblios.groupby("id_depto").size().reset_index(name="cant_bp")

# EE por depto
ee_por_dpto = df_ee.groupby("id_depto").size().reset_index(name="cant_ee")

# Unir todo
df_rel = poblacion_depto.merge(bp_por_dpto, on="id_depto", how="left")\
                        .merge(ee_por_dpto, on="id_depto", how="left")\
                        .fillna(0)

# Calcular tasas por mil habitantes
df_rel["bp_x_mil"] = df_rel["cant_bp"] * 1000 / df_rel["poblacion"]
df_rel["ee_x_mil"] = df_rel["cant_ee"] * 1000 / df_rel["poblacion"]

# Plot
plt.figure()
sns.scatterplot(
    data=df_rel,
    x="bp_x_mil",
    y="ee_x_mil"
)
plt.title("Relación entre BP y EE cada mil habitantes por Departamento")
plt.xlabel("BP cada mil hab.")
plt.ylabel("EE cada mil hab.")
plt.tight_layout()
plt.savefig("bp_vs_ee_por_mil.png")
plt.show()