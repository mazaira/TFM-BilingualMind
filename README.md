

#  TFM-BilingualMind:Modelización Predictiva del Impacto del Bilingüismo en el Desarrollo Cognitivo y las Proyecciones Laborales con Técnicas de Machine Learning

**Autor:** [Gema Dominguez Polo]  
**Tutor:** [Juan Manuel Moreno Lamparero]  
**Máster:** Máster Data Science and business analytics - IMF  
**Fecha:** [Diciembre, 2025]

## 📋 Resumen Ejecutivo
Este Trabajo Fin de Máster (TFM) implementa un pipeline completo de análisis de datos de neuroimagen para investigar diferencias cerebrales entre individuos monolingües y bilingües. Combina técnicas de procesamiento de imágenes médicas (NIfTI), extracción de características, modelado con Machine Learning y visualización interactiva.

## 🎯 Objetivos
- **Objetivo General:** Desarrollar un sistema de análisis que identifique patrones en neuroimagen asociados al bilingüismo.
- **Objetivos Específicos:**
  1. Implementar un pipeline reproducible de preprocesamiento de imágenes MRI.
  2. Extraer características volumétricas y morfométricas de regiones cerebrales.
  3. Evaluar modelos de clasificación para distinguir entre grupos.
  4. Desplegar un dashboard interactivo para visualización de resultados.
  5. Documentar todo el proceso para garantizar reproducibilidad.

## 🏗️ Arquitectura del Proyecto

```mermaid
graph TB
    A[Datasets Públicos<br>OASIS/ADNI] --> B[data/01_raw/];
    B --> C[Preprocesamiento<br>src/data/];
    C --> D[Extracción de<br>Características];
    D --> E[Modelado ML<br>src/models/];
    E --> F{Evaluación};
    F --> G[Resultados<br>reports/];
    F --> H[Dashboard<br>src/dashboard/];
    
    I[Configuración<br>config/params.yaml] --> C;
    I --> E;
    
    J[Análisis Exploratorio<br>notebooks/] --> D;