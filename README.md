# Análisis de Vendedores y Asesoría con GenAI - Mercado Libre

Este repositorio contiene una solución técnica para el análisis exploratorio de datos (EDA) de vendedores de Mercado Libre y una propuesta de sistema de recomendación basado en IA Generativa.

## 📋 Descripción del Proyecto
El objetivo es identificar patrones de comportamiento en vendedores de e-commerce y utilizar esos insights para generar recomendaciones personalizadas que maximicen sus ventas.

### Componentes Principales:
1.  **EDA Profundo:** Análisis estadístico (Mann-Whitney, Chi-Square) sobre reputación, precios y logística.
2.  **Segmentación:** Clustering de vendedores para identificar perfiles (Amateurs vs. Profesionales).
3.  **GenAI Advisor:** Módulo conceptual que utiliza LLMs para traducir métricas en consejos de negocio accionables.

## Insights Clave
* **Reputación y Precio:** Se validó estadísticamente que los vendedores `Green_Gold` pueden mantener precios significativamente más altos sin perder competitividad.
* **Logística:** Existe una dependencia crítica entre el uso de logística *Fulfillment* y la alta reputación.
* **Psicología de Precios:** El 60% de los top sellers utilizan *Charm Pricing* (precios terminados en .99 o .90).

## Tecnologías Utilizadas
* **Python 3.10+**
* **Pandas & NumPy:** Manipulación de datos.
* **Seaborn & Matplotlib:** Visualización.
* **SciPy:** Pruebas de hipótesis estadísticas.
* **OpenAI API (Simulado):** Generación de texto para recomendaciones.

## Cómo ejecutar este proyecto

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/LauraMerchanO/meli-seller-analysis.git](https://github.com/TU_USUARIO/meli-seller-analysis.git)
