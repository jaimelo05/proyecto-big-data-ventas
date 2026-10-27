# proyecto-big-data-ventas
Proyecto Big Data: Análisis de Ventas con Apache Spark

1. Descripción del proyecto
Este proyecto tiene como objetivo aplicar técnicas de Big Data para procesar y analizar información de ventas de una empresa. Se utiliza Apache Spark con Python (PySpark) para limpiar los datos, realizar análisis exploratorios, calcular ingresos y comparar resultados por producto, ciudad y categoría.
El proyecto trabaja con un archivo CSV de ventas y desarrolla un proceso de procesamiento por lotes (Batch Processing).

2. Objetivos

Objetivo general

Implementar un proceso de procesamiento de datos de ventas mediante Apache Spark que permita limpiar, organizar y analizar la información para obtener resultados útiles para la toma de decisiones.

Objetivos específicos

- Identificar y tratar valores vacíos y registros duplicados.
- Limpiar los datos y calcular los ingresos de las ventas.
- Analizar los ingresos por producto, ciudad y categoría.
- Guardar los resultados obtenidos y generar gráficas para facilitar su interpretación.

3. Tecnologías utilizadas

- Python.
- Apache Spark.
- PySpark.
- Matplotlib para la generación de gráficas.
- Archivos CSV para almacenar los datos.

4. Estructura del proyecto

- "ventas.csv": archivo con los datos originales de las ventas.
- "limpieza_eda.py": realiza la limpieza de los datos y el análisis exploratorio.
- "procesamiento_batch.py": procesa los datos limpios y calcula los ingresos por producto, ciudad y categoría.
- "graficas_ventas.py": genera las gráficas de los resultados.
- "ventas_limpias/": carpeta donde se guardan los datos después de la limpieza.
- "resultados_productos/": resultados agrupados por producto.
- "resultados_ciudades/": resultados agrupados por ciudad.
- "resultados_categorias/": resultados agrupados por categoría.
- "graficos/": carpeta destinada a las gráficas generadas.

Las carpetas de resultados se crean al ejecutar los programas correspondientes.

5. Requisitos previos

Para ejecutar el proyecto se necesita:

- Tener Python instalado.
- Tener Java instalado y configurado para la versión de Apache Spark utilizada.
- Tener PySpark instalado.
- Contar con Matplotlib para generar las gráficas.

Instalación de las dependencias de Python:

pip install pyspark matplotlib

6. Pasos para ejecutar el proyecto

Los siguientes comandos deben ejecutarse desde la terminal, dentro de la carpeta principal del proyecto y en el orden indicado.

Paso 1. Limpiar y explorar los datos

python3 limpieza_eda.py

Este programa carga "ventas.csv", identifica valores vacíos y duplicados, elimina registros incompletos o con cantidades y precios no válidos, calcula los ingresos y guarda los datos limpios en "ventas_limpias/".

Paso 2. Realizar el procesamiento Batch

python3 procesamiento_batch.py

Este programa utiliza los datos de "ventas_limpias/" y calcula los ingresos totales por producto, ciudad y categoría. Los resultados se guardan en sus respectivas carpetas.

Paso 3. Generar las gráficas

python3 graficas_ventas.py

Este programa genera representaciones gráficas que permiten comparar los ingresos y facilitar la interpretación de los resultados, según las rutas configuradas en el script.

Importante: primero se debe ejecutar el proceso de limpieza y después el procesamiento Batch, porque el segundo depende de los datos generados por el primero.

7. Resultados esperados

Al ejecutar los programas se obtiene:

- Un conjunto de datos depurados.
- Estadísticas descriptivas de las ventas.
- Comparaciones de ingresos por producto, ciudad y categoría.
- Archivos con los resultados agrupados.
- Gráficas que permiten interpretar los resultados de manera visual.

8. Conclusión

El proyecto permite aplicar conceptos de Big Data mediante el procesamiento por lotes con Apache Spark. La limpieza de los datos contribuye a mejorar su calidad, mientras que el análisis de los ingresos facilita la identificación de los productos, las ciudades y las categorías con mayor participación en las ventas. Además, la organización de los scripts y los resultados permite documentar y reproducir el proceso de análisis.
