from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, count

spark = SparkSession.builder \
    .appName("Limpieza_EDA_Ventas") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Cargar los datos
df = spark.read.csv(
    "ventas.csv",
    header=True,
    inferSchema=True
)

print("\n=== ESQUEMA DE LOS DATOS ===")
df.printSchema()

print("\n=== CANTIDAD DE REGISTROS ORIGINALES ===")
print(df.count())

print("\n=== VALORES VACIOS POR COLUMNA ===")
df.select([
    count(col(c)).alias(c) for c in df.columns
]).show()

print("\n=== REGISTROS DUPLICADOS ===")
print("Duplicados:", df.count() - df.dropDuplicates().count())

# Limpiar datos: eliminar filas duplicadas y registros incompletos
df_limpio = df.dropDuplicates().dropna(
    subset=[
        "id_venta", "fecha", "producto",
        "categoria", "ciudad", "cantidad", "precio"
    ]
)

# Conservar registros con cantidad y precio válidos
df_limpio = df_limpio.filter(
    (col("cantidad") > 0) & (col("precio") > 0)
)

# Transformación: calcular ingresos por venta
df_limpio = df_limpio.withColumn(
    "ingresos", col("cantidad") * col("precio")
)

print("\n=== DATOS LIMPIOS ===")
df_limpio.show(truncate=False)

print("\n=== RESUMEN ESTADISTICO ===")
df_limpio.select(
    "cantidad", "precio", "ingresos"
).describe().show()

print("\n=== INGRESOS POR PRODUCTO ===")
df_limpio.groupBy("producto").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

print("\n=== INGRESOS POR CIUDAD ===")
df_limpio.groupBy("ciudad").agg(
    spark_sum("ingresos").alias("ingresos_totales")
).orderBy(
    col("ingresos_totales").desc()
).show()

# Guardar datos limpios
df_limpio.write.mode("overwrite").option(
    "header", True
).csv("ventas_limpias")

print("\nLimpieza y analisis exploratorio finalizados.")

spark.stop()
