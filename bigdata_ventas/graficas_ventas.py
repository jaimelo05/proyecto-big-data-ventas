import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import csv
import glob
import os

def leer_resultados(carpeta):
    archivos = glob.glob(os.path.join(carpeta, "part-*.csv"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron resultados en {carpeta}"
        )

    with open(archivos[0], "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)

    return filas

os.makedirs("graficos", exist_ok=True)

# Gráfico de ingresos por producto
productos = leer_resultados("resultados_productos")
productos.sort(
    key=lambda fila: float(fila["ingresos_totales"]),
    reverse=True
)

plt.figure(figsize=(8, 5))
plt.bar(
    [fila["producto"] for fila in productos],
    [float(fila["ingresos_totales"]) for fila in productos]
)
plt.title("Ingresos por producto")
plt.xlabel("Producto")
plt.ylabel("Ingresos (COP)")
plt.tight_layout()
plt.savefig("graficos/ingresos_productos.png")
plt.close()

# Gráfico de ingresos por ciudad
ciudades = leer_resultados("resultados_ciudades")
ciudades.sort(
    key=lambda fila: float(fila["ingresos_totales"]),
    reverse=True
)

plt.figure(figsize=(8, 5))
plt.bar(
    [fila["ciudad"] for fila in ciudades],
    [float(fila["ingresos_totales"]) for fila in ciudades]
)
plt.title("Ingresos por ciudad")
plt.xlabel("Ciudad")
plt.ylabel("Ingresos (COP)")
plt.tight_layout()
plt.savefig("graficos/ingresos_ciudades.png")
plt.close()

# Gráfico de ingresos por categoría
categorias = leer_resultados("resultados_categorias")
categorias.sort(
    key=lambda fila: float(fila["ingresos_totales"]),
    reverse=True
)

plt.figure(figsize=(8, 5))
plt.bar(
    [fila["categoria"] for fila in categorias],
    [float(fila["ingresos_totales"]) for fila in categorias]
)
plt.title("Ingresos por categoría")
plt.xlabel("Categoría")
plt.ylabel("Ingresos (COP)")
plt.tight_layout()
plt.savefig("graficos/ingresos_categorias.png")
plt.close()

print("Graficos creados correctamente en la carpeta graficos.")
