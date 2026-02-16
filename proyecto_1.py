import pandas as pd

# 1.- Lectura del data set 
print("\n" + "=" * 50)
print(" Cargando el DATASET")
print("=" * 50)

df=pd.read_csv("Bakery Sales.csv")
print(f" Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")

# 2.- Inspección básica  de datos 
print("\n" + "=" * 50)
print("Inspección básica de datos")
print("=" * 50)

print("\n--- Primeras filas del dataset ---")
print(df.dtypes)
print(df.head (6))
print("\n--- Valores nulos por columna ---")
print(df.isnull().sum())
print("\n--- Valores únicos por columna")
print(df.nunique())

# 3.- Limpieza de datos
print("\n" + "=" *50)
print("Limpieza de datos")
print("=" *50)

#3.1 Convertir "datetime"
df["datetime"]=pd.to_datetime(df["datetime"],errors="coerce")
print("\n Columna 'datetime' normalizada a un solo formato fecha ")

#3.2 Identificar columnas de productos (todo lo que no sea metadato)
meta_cols=["datetime","day of week","total","place"]
productos=[col for col in df.columns if col not in meta_cols]
print(f"Columnas de productos detectadas ({len(productos)}):")
print(productos)

#3.3 Convertir columnas de productos a númerico
for col in productos:
    df[col]=pd.to_numeric(df[col],errors ="coerce")

# 3.4 Rellenar "NaN" en productos con 0 (no se vendió esa unidad)
df[productos]=df[productos].fillna(0)

#3.5 Rellenar NaN en "place" con "Unknow"
df["place"]=df["place"].fillna("Unknown")

#3.6 Aegurar que "total" sea númerico
df["total"]=pd.to_numeric(df["total"], errors="coerce")

#3.7 Eliminar filas completamente vacías (las que están al final del archivo)
df.dropna(how="all", inplace=True)
print("\n --- Resumen después de limpieza ---")
print(f"Filas restantes:{len(df)}")
print(f"Valores nulos por columna:\n{df.isnull().sum()}")

# 4.- Estadísticas descriptivas 
print("\n" + "=" * 50)
print("--- Estadísticas descriptivas ---")
print("=" * 50)

print("\n --- Resumen estadístico rápido --- ")
print(df.describe())

#4.1 Ventas por día de la semana 
print("\n --- Ventas totales por día de la semana ---")
ventas_dia=df.groupby("day of week")["total"].agg(["sum","mean","count"])
ventas_dia=ventas_dia.sort_values("sum",ascending=False)
print(ventas_dia)

#4.2 Top 10 productos más vendidos 
print("\n --- Top 10 productos más vendidos ---")
top_productos=df[productos].sum().sort_values(ascending=False).head(11)
print(top_productos)

#4.3 Top 10 lugares con mayores ventas 
print("\n --- Top 10 lugares con mayores ventas ---")
top_lugares=df.groupby("place")["total"].sum().sort_values(ascending=False).head(11)
print(top_lugares)

# Detección de outliers en "total"
print("\n" + "=" * 50)
print(" --- Detección de outliers en 'total' --- ")
print("=" * 50)

Q1 = df["total"].quantile(0.25)
Q3 = df["total"].quantile(0.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR

outliers = df[(df["total"] < lim_inf) | (df["total"] > lim_sup)]
print(f" Número de outliers detectados: {len(outliers)}")
if len(outliers) > 0:
    print("\n Algunos ejemplos de outliers:")
    print(outliers[["datetime", "day of week", "total", "place"]].head(10))

# Resumen de archivo en texto

print("\n" + "=" * 50)
print("--- Resumen de ventas---")
print("=" * 50)

with open("resumen_ventas.txt", "w", encoding="utf-8") as f:
    f.write("RESUMEN DEL ANÁLISIS DE VENTAS\n")
    f.write("=" * 40 + "\n\n")
    f.write("1. Estadísticas descriptivas:\n")
    f.write(df.describe().to_string())
    f.write("\n\n2. Ventas por día de la semana:\n")
    f.write(ventas_dia.to_string())
    f.write("\n\n3. Top 10 productos más vendidos:\n")
    f.write(top_productos.to_string())
    f.write("\n\n4. Top 10 lugares con mayores ventas:\n")
    f.write(top_lugares.to_string())
    f.write(f"\n\n5. Número de outliers en 'total': {len(outliers)}")

print("\n Resumen guardado correctamente.")


