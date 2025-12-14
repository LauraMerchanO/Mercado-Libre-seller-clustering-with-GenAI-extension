# Análisis de vendedores en Mercado Libre

Este proyecto realiza un análisis exploratorio y una segmentación de vendedores de Mercado Libre utilizando técnicas de Machine Learning (Clustering). El objetivo es identificar patrones de comportamiento, estrategias de venta (volumen vs. margen) y perfiles logísticos.

## Descripción del caso

El script procesa un dataset de publicaciones de Mercado Libre para:
1. **Limpieza de Datos:** Detección de outliers, manejo de nulos y estandarización.
2. **Feature Engineering:** Creación de métricas clave como precios promedio, variabilidad y stock.
3. **Análisis Exploratorio (EDA):** Distribución de precios, reputación y tipos de logística.
4. **Clustering:** Segmentación de vendedores utilizando K-Means y PCA para reducir dimensionalidad.

## Estructura del repositorio

- `AnalisisExploratorio.py`: Script principal con todo el flujo de procesamiento y modelado.
- `requirements.txt`: Lista de dependencias necesarias.
- `README.md`: Documentación del proyecto.
- `df_challenge_meli - df_challenge_meli.csv`: Dataset del caso práctico.

## Instalación y uso

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/LauraMerchanO/meli-seller-analysis.git](https://github.com/TU_USUARIO/meli-seller-analysis.git)
Instalar las dependencias:

Bash
pip install -r requirements.txt
Ejecución: El dataset necesario ya se encuentra en el repositorio. Simplemente ejecuta el script:

Bash
python analisis.py
Tecnologías
Python 3

Pandas & NumPy: Manipulación de datos.

Scikit-learn: Preprocesamiento, PCA y K-Means.

Seaborn & Matplotlib: Visualización estática.

Plotly: Visualización interactiva.


### Pasos finales de Git

Asegúrate de que los archivos `requirements.txt`, `.gitignore` y `README.md` (con la versión actualizada) estén en tu directorio, y luego usa los siguientes comandos:

```bash
# 1. Asegúrate de que tu analisis.ipynb/py esté listo
# 2. Crea los nuevos archivos
# 3. Agrega todos los archivos al staging area (incluyendo el dataset si no lo habías hecho)
git add .

# 4. Haz el commit
git commit -m "feat: Inicialización de repositorio con análisis de vendedores y configuración de entorno"

# 5. Sube los cambios
git push origin <rama_principal>
