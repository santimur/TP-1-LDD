'''
Laboratorio de Datos - TP 1
Integrantes:
Barrios Bruno
Mur Santiago
Operti Bruno
               
Consultas SQL.
'''


import pandas as pd
import duckdb
from pathlib import Path

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Rutas

base_path = Path("ruta/TablasModelo")

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Carga de datasets normalizados

BP = pd.read_csv(base_path / "bibliotecas_populares_limpio.csv")
EE = pd.read_csv(base_path / "establecimientos_educativos_limpia.csv")
dept = pd.read_csv(base_path / "departamentosNUEVO.csv")
niveles_estab = pd.read_csv(base_path / "niveles_establecimientos_comunes_3FN.csv")
niveles = pd.read_csv(base_path / "niveles.csv")
nivel_educ_dept = pd.read_csv(base_path / "nivel_educativo_por_departamento_3fn.csv")

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Consulta i: Comparar cantidad de establecimientos vs población por nivel educativo
#- Usaremos la tabla niveles_establecimientos_comunes_3FN.csv para contar la cantidad de establecimientos de modalidad común por nivel y departamento.
#- Usaremos la tabla nivel_educativo_por_departamento_3fn.csv para la población por nivel y departamento.
#- Usaremos la tabla departamentosNUEVO.csv para obtener provincia y nombre de departamento.
#- Usaremos la tabla niveles.csv para identificar los id de nivel correspondientes a jardín, primaria y secundaria.



consulta_i = duckdb.query("""
    WITH
    conteo_ee AS (
        SELECT
            EE.id_depto,
            dept.provincia,
            dept.nombre_depto AS departamento,
            ne.id_nivel,
            COUNT(DISTINCT ne.id_establecimiento) AS cantidad
        FROM niveles_estab AS ne
        INNER JOIN EE ON EE.id_establecimiento = ne.id_establecimiento
        INNER JOIN dept ON dept.id_depto = EE.id_depto
        WHERE ne.id_nivel IN ('jardin_infante', 'primario', 'secundario')
        GROUP BY EE.id_depto, dept.provincia, dept.nombre_depto, ne.id_nivel
    ),
    poblacion AS (
        SELECT
            ned.id_depto,
            ned.id_nivel,
            SUM(ned.cantidad) AS poblacion
        FROM nivel_educ_dept AS ned
        WHERE ned.id_nivel IN ('jardin_infante', 'primaria', 'secundaria')
        GROUP BY ned.id_depto, ned.id_nivel
    ),
    tabla AS (
        SELECT
            d.provincia,
            d.nombre_depto AS departamento,
            COALESCE(jardines.cantidad, 0) AS jardines,
            COALESCE(pjardin.poblacion, 0) AS poblacion_jardin,
            COALESCE(primarias.cantidad, 0) AS primarias,
            COALESCE(pprimaria.poblacion, 0) AS poblacion_primaria,
            COALESCE(secundarias.cantidad, 0) AS secundarios,
            COALESCE(psecundaria.poblacion, 0) AS poblacion_secundaria
        FROM dept d
        LEFT JOIN (SELECT * FROM conteo_ee WHERE id_nivel = 'jardin_infante') AS jardines
            ON d.id_depto = jardines.id_depto
        LEFT JOIN (SELECT * FROM conteo_ee WHERE id_nivel = 'primario') AS primarias
            ON d.id_depto = primarias.id_depto
        LEFT JOIN (SELECT * FROM conteo_ee WHERE id_nivel = 'secundario') AS secundarias
            ON d.id_depto = secundarias.id_depto
        LEFT JOIN (SELECT * FROM poblacion WHERE id_nivel = 'jardin_infante') AS pjardin
            ON d.id_depto = pjardin.id_depto
        LEFT JOIN (SELECT * FROM poblacion WHERE id_nivel = 'primaria') AS pprimaria
            ON d.id_depto = pprimaria.id_depto
        LEFT JOIN (SELECT * FROM poblacion WHERE id_nivel = 'secundaria') AS psecundaria
            ON d.id_depto = psecundaria.id_depto
    )
    SELECT
        provincia,
        departamento,
        jardines,
        poblacion_jardin,
        primarias,
        poblacion_primaria,
        secundarios,
        poblacion_secundaria
    FROM tabla
    ORDER BY provincia, primarias DESC
""").df()

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Consulta ii: Bibliotecas populares fundadas desde 1950 por departamento

consulta_ii = duckdb.query("""
    SELECT
        dept.provincia,
        dept.nombre_depto AS departamento,
        COUNT(*) AS cantidad_BP_fundadas_desde_1950
    FROM BP
    INNER JOIN dept ON dept.id_depto = BP.id_depto
    WHERE BP.año_fundacion >= 1950
    GROUP BY dept.provincia, dept.nombre_depto
    ORDER BY dept.provincia, cantidad_BP_fundadas_desde_1950 DESC
""").df()

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Consulta iii: Cantidad de EE, BP y población total por departamento

consulta_iii = duckdb.query("""
    WITH
    ee_por_depto AS (
        SELECT id_depto, COUNT(DISTINCT id_establecimiento) AS cantEE
        FROM EE
        GROUP BY id_depto
    ),
    bp_por_depto AS (
        SELECT id_depto, COUNT(DISTINCT id_biblioteca) AS cantBP
        FROM BP
        GROUP BY id_depto
    ),
    poblacion_por_depto AS (
        SELECT id_depto, SUM(cantidad) AS poblacion_total
        FROM nivel_educ_dept
        GROUP BY id_depto
    )
    SELECT
        d.provincia,
        d.nombre_depto AS departamento,
        COALESCE(ee.cantEE, 0) AS cantEE,
        COALESCE(bp.cantBP, 0) AS cantBP,
        COALESCE(pob.poblacion_total, 0) AS poblacion_total
    FROM dept d
    LEFT JOIN ee_por_depto ee ON d.id_depto = ee.id_depto
    LEFT JOIN bp_por_depto bp ON d.id_depto = bp.id_depto
    LEFT JOIN poblacion_por_depto pob ON d.id_depto = pob.id_depto
    ORDER BY d.provincia, d.nombre_depto
""").df()

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Consulta iv: Dominio de email más frecuente por departamento

consulta_iv = duckdb.query("""
    WITH tabla_temporal AS (
        SELECT
            dept.provincia,
            dept.nombre_depto AS departamento,
            BP.dominio_email AS mail
        FROM BP
        INNER JOIN dept ON dept.id_depto = BP.id_depto
        WHERE BP.dominio_email IS NOT NULL
    ),
    tabla_temp_conteo AS (
        SELECT
            provincia,
            departamento,
            mail,
            COUNT(*) AS cantidad
        FROM tabla_temporal
        GROUP BY provincia, departamento, mail
    ),
    tabla_maxima AS (
        SELECT
            provincia,
            departamento,
            mail,
            cantidad,
            ROW_NUMBER() OVER (PARTITION BY provincia, departamento ORDER BY cantidad DESC) AS rn
        FROM tabla_temp_conteo
    )
    SELECT
        provincia AS Provincia,
        departamento AS Departamento,
        mail AS Dominio_mas_frecuente
    FROM tabla_maxima
    WHERE rn = 1
    ORDER BY Provincia, Departamento
""").df()

# ----------------------------------------------------------------------------------------------------------------------------------- #
# Guardado de resultados

consulta_i.to_csv(base_path / "consulta_i.csv", index=False)
consulta_ii.to_csv(base_path / "consulta_ii.csv", index=False)
consulta_iii.to_csv(base_path / "consulta_iii.csv", index=False)
consulta_iv.to_csv(base_path / "consulta_iv.csv", index=False)

print("Todas las consultas fueron ejecutadas y guardadas correctamente.")
