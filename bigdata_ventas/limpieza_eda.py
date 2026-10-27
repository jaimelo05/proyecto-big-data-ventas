
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum as spark_sum,
    when,
    trim
)

# =====================================================
# 1. CREAR SESION DE SPARK
# =====================================================

spark = (
    SparkSession.builder
    .appName("Limpieza_EDA_Ventas")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# =====================================================
# 2. CARGAR LOS DATOS
# =====================================================

df = spark.read.csv(
    "ventas.csv",
    header=True,
    inferSchema=True
)

print("\n=== ESQUEMA DE LOS DATOS ===")
df.printSchema()

print("\n=== CANTIDAD DE REGISTROS ORIGINALES ===")
print("Total de registros:", df.count())

# =====================================================
# 3. CONTAR VALORES NULOS POR COLUMNA
# =====================================================

print("\n=== VALORES VACIOS POR COLUMNA ===")

df.select([
    spark_sum(
        when(
            col(c).isNull() |
            (trim(col(c).cast("string")) == ""),
            1
        ).otherwise(0)
    ).alias(c)
    for c in df.columns
]).show()

# =====================================================
# 4. IDENTIFICAR REGISTROS DUPLICADOS
# =====================================================

print("\n=== REGISTROS DUPLICADOS ===")

total_original = df.count()
total_sin_duplicados = df.dropDuplicates().count()

print("Registros duplicados:", total_original - total_sin_duplicados)

# =====================================================
# 5. LIMPIAR LOS DATOS
# Eliminar duplicados y filas incompletas
# =====================================================

df_limpio = df.dropDuplicates()

# Convertir las cadenas vacías en valores nulos
for c in df.columns:
    df_limpio = df_limpio.withColumn(
        c,
        when(
            trim(col(c).cast("string")) == "",
            None
        ).otherwise(col(c))
    )

df_limpio = df_limpio.dropna(
    subset=[
        "id_venta",
        "fecha",
        "producto",
        "categoria",
        "ciudad",
        "cantidad",
        "precio"
    ]
)

# =====================================================
# 6. VALIDAR CANTIDAD Y PRECIO
# =====================================================

df_limpio = df_limpio.filter(
    (col("cantidad") > 0) &
    (col("precio") > 0)
)

print("\n=== REGISTROS DESPUES DE LA LIMPIEZA ===")
print("Total de registros limpios:", df_limpio.count())

# =====================================================
# 7. CALCULAR INGRESOS POR VENTA
# =====================================================

df_limpio = df_limpio.withColumn(
    "ingresos",
    col("cantidad") * col("precio")
)

print("\n=== DATOS LIMPIOS ===")
df_limpio.show(truncate=False)

# =====================================================
# 8. ANALISIS EXPLORATORIO DE DATOS (EDA)
# =====================================================

print("\n=== ESTADISTICAS DESCRIPTIVAS ===")
df_limpio.describe(
    ["cantidad", "precio", "ingresos"]
).show()

# =====================================================
# 9. INGRESOS POR PRODUCTO
# =====================================================

print("\n=== INGRESOS POR PRODUCTO ===")

df_limpio.groupBy("producto").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# =====================================================
# 10. INGRESOS POR CIUDAD
# =====================================================

print("\n=== INGRESOS POR CIUDAD ===")

df_limpio.groupBy("ciudad").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# =====================================================
# 11. INGRESOS POR CATEGORIA
# =====================================================

print("\n=== INGRESOS POR CATEGORIA ===")

df_limpio.groupBy("categoria").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# =====================================================
# 12. GUARDAR LOS DATOS LIMPIOS
# =====================================================

df_limpio.write.mode("overwrite").option(
    "header", True
).csv("ventas_limpias")

print("\nProceso de limpieza y analisis finalizado.")
print("Los datos limpios se guardaron en la carpeta ventas_limpias.")

# =====================================================
# 13. CERRAR SPARK
# =====================================================

spark.stop()
