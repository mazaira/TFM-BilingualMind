
># TFM-BilingualMind: Modelización Predictiva del Impacto del Bilingüismo en el Desarrollo Cognitivo y las Proyecciones Laborales con Técnicas de Machine Learning

**Autor:** [Gema Dominguez Polo] 
**Tutor:** [Juan Manuel Moreno Lamparero] 
**Máster:** Máster Data Science and business analytics - IMF 
**Fecha:** [Diciembre, 2025]

---

##Resumen Ejecutivo
Este TFM, titulado "BilingualMind", aplica la Ciencia de Datos para cuantificar el impacto real del bilingüismo en el rendimiento académico y el bienestar social, aislando su efecto del principal factor enmascarador: el Estatus Socioeconómico y Cultural (ESCS).

El estudio integra tres fuentes de datos de gran escala (PISA, ESS y el dataset de Neuroimagen OpenNeuro ds001796) siguiendo la metodología CRISP-DM.

 Metodología y Modelos
Fuentes: Datos de rendimiento (PISA), bienestar/laboral (ESS) y activación cerebral (Tarea Flanker de Neuroimagen).

Técnicas: Se combinaron modelos estadísticos (OLS) con Machine Learning basado en árboles (XGBoost) y clasificadores avanzados (SVM, Random Forest).

Rendimiento: El modelo SVM demostró ser el más efectivo para la clasificación, alcanzando un 71.3% de accuracy y un AUC-ROC de 0.781.

 Resultados Clave e Interpretación (SHAP)
El valor central del proyecto reside en la interpretabilidad mediante valores SHAP, que descompuso la contribución predictiva de cada variable:

Factor ESCS: El ESCS mostró una importancia predictiva 2.25 veces superior al bilingüismo (0.45 vs. 0.20), confirmando su rol dominante en los resultados sociales y académicos.

Punto Óptimo: Los análisis identificaron un "punto óptimo" donde el bilingüismo maximiza su impacto positivo en contextos de ESCS medio (+0.171).

Ventaja Neural: En contraste con los resultados académicos, el análisis de Neuroimagen (GLM) reveló una ventaja cognitiva intrínseca en bilingües, manifestada como una activación más eficiente en las regiones de control ejecutivo durante la Tarea Flanker.

 Conclusión
Se concluye que el bilingüismo implica una ventaja sutil y robusta a nivel neural, pero su manifestación en resultados académicos y laborales queda mayormente eclipsada por la ventaja contextual masiva que aporta el Estatus Socioeconómico. Estos resultados validan el uso de ML interpretable como herramienta clave para informar y refinar las políticas educativas.

Palabras clave: Bilingüismo, ESCS, Machine Learning, XGBoost, SHAP, Función Ejecutiva, Neuroimagen, PISA, Modelización Predictiva.



## 🏗️ Arquitectura del Proyecto

```mermaid
graph TB
    A[Datasets Públicos<br>PISA/ESS/openeuro] --> B[data/01_raw/];
    B --> C[Preprocesamiento<br>src/data/];
    C --> D[Extracción de<br>Características<br>src/features/];
    D --> E[Modelado ML<br>src/models/];
    E --> F{Evaluación};
    F --> G[Resultados<br>reports/];
    F --> H[Dashboard<br>src/dashboard/];
    
    I[Configuración<br>config/params.yaml] --> C;
    I --> E;
    
    J[Análisis Exploratorio<br>notebooks/] --> D;
