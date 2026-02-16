## 🥐 Análisis de Ventas de Panadería

Proyecto de análisis de datos enfocado en procesar y explorar ventas históricas de una panadería utilizando Python y pandas.
Este dataset fue descargado de Kaggle para poder desarrollar dicho proyecto.

Se aplican técnicas de limpieza, transformación y análisis exploratorio de datos (EDA) para convertir información cruda en métricas útiles para la toma de decisiones.

El propósito principal es identificar patrones de comportamiento, productos más vendidos, días con mayor facturación y detectar valores atípicos en las ventas.

---

## 🎯 Objetivos del proyecto

- Leer datos desde un archivo CSV
- Inspeccionar estructura y tipos de datos
- Detectar y tratar valores nulos
- Normalizar formatos de fecha y columnas numéricas
- Calcular estadísticas descriptivas
- Analizar ventas por día, producto y lugar
- Detectar valores atípicos (outliers)
- Generar un reporte automático con los resultados

---

## 📁 Estructura del proyecto
```
ANÁLISIS DE DATOS/
│
├── Bakery Sales.csv        # Dataset original de ventas
├── proyecto_1.py            # Script principal de análisis
├── resumen_ventas.txt       # Reporte generado automáticamente
└── README.md                # Documentación del proyecto
```

---
## 🛠️ Tecnologías utilizadas

- Python 3
- pandas
- Análisis Exploratorio de Datos (EDA)
- Estadística descriptiva
- Manejo de archivos

---

## ⚙️ Requisitos e instalación

1. Tener Python 3.7 o superior instalado.
2. Instalar la librería pandas:
   ```bash
   pip install pandas
   ```

## 🚀 Cómo ejecutar el script
1. Clona este repositorio o descarga los archivos en una misma carpeta.
2. Abre una terminal en esa carpeta.
3. Ejecuta el script: `python proyecto_1.py`
4. Al finalizar, se generará el archivo `resumen_ventas.txt` con todos los resultados.

## 📊 Resultados principales (ejemplo)

Al ejecutar el script obtendrás:

- **Día con más ventas:** Viernes
- **Producto más vendido:** (depende de los datos, por ejemplo "croissant")
- **Lugar con mayores ventas:** (ej. "Unknown" o alguna localidad)
- **Outliers detectados:** X registros con montos inusualmente altos o bajos.

Puedes consultar el archivo `resumen_ventas.txt` para ver todos los detalles.

## 📈 Ejemplo de salida en consola
```
==================================================
 Cargando el DATASET
==================================================
 Dimensiones: 2100 filas, 28 columnas
```

## 📝 Notas adicionales
Los outliers detectados pueden ser errores de carga o pedidos excepcionales. Se recomienda revisarlos manualmente.

El script está comentado paso a paso para facilitar su comprensión y modificación.

## 📬 Contacto y contribuciones
Si tienes dudas, sugerencias o deseas contribuir, no dudes en abrir un issue o enviar un pull request.