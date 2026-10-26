from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

# Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("AnalisisVentas") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Leer los datos de ventas
ventas = spark.read.csv(
    "ventas.csv",
    header=True,
    inferSchema=True
)

# Calcular los ingresos por venta
ventas = ventas.withColumn(
    "ingresos",
    col("cantidad") * col("precio")
)

print("\n=== DATOS DE VENTAS ===")
ventas.show(truncate=False)

# Calcular los ingresos totales
print("\n=== INGRESOS TOTALES ===")
ventas.select(
    spark_sum("ingresos").alias("ingresos_totales")
).show()

# Ventas por producto
print("\n=== INGRESOS POR PRODUCTO ===")
ventas.groupBy("producto").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# Ventas por ciudad
print("\n=== INGRESOS POR CIUDAD ===")
ventas.groupBy("ciudad").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# Ventas por categoría
print("\n=== INGRESOS POR CATEGORIA ===")
ventas.groupBy("categoria").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# Guardar los resultados
ventas.groupBy("producto").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).write.mode("overwrite").option(
    "header", True
).csv("resultados_productos")

ventas.groupBy("ciudad").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).write.mode("overwrite").option(
    "header", True
).csv("resultados_ciudades")

ventas.groupBy("categoria").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).write.mode("overwrite").option(
    "header", True
).csv("resultados_categorias")

print("\nAnalisis finalizado. Resultados guardados correctamente.")

spark.stop()
