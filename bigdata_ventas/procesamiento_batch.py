from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

# =====================================================
# 1. CREAR SESION DE SPARK
# =====================================================

spark = (
    SparkSession.builder
    .appName("ProcesamientoBatchVentas")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# =====================================================
# 2. CARGAR LOS DATOS LIMPIOS
# =====================================================

df = spark.read.csv(
    "ventas_limpias",
    header=True,
    inferSchema=True
)

print("\n=== DATOS LIMPIOS ===")
df.show(truncate=False)

print("\n=== TOTAL DE REGISTROS ANALIZADOS ===")
print("Total de registros:", df.count())

# =====================================================
# 3. INGRESOS POR PRODUCTO
# =====================================================

print("\n=== INGRESOS POR PRODUCTO ===")

df.groupBy("producto").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# =====================================================
# 4. INGRESOS POR CIUDAD
# =====================================================

print("\n=== INGRESOS POR CIUDAD ===")

df.groupBy("ciudad").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# =====================================================
# 5. INGRESOS POR CATEGORIA
# =====================================================

print("\n=== INGRESOS POR CATEGORIA ===")

df.groupBy("categoria").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# =====================================================
# 6. GUARDAR LOS RESULTADOS
# =====================================================

df.groupBy("producto").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).write.mode("overwrite").option(
    "header", True
).csv("resultados_productos")

df.groupBy("ciudad").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).write.mode("overwrite").option(
    "header", True
).csv("resultados_ciudades")

df.groupBy("categoria").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).write.mode("overwrite").option(
    "header", True
).csv("resultados_categorias")

print("\nProcesamiento batch finalizado correctamente.")
print("Los resultados se guardaron en sus respectivas carpetas.")

# =====================================================
# 7. CERRAR SPARK
# =====================================================

spark.stop()
