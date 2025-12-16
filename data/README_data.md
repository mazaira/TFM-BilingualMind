# 📂 Fuente y Descripción de los Datos - Proyecto BilingualMind

## 1. 🗺️ Origen de los Datos
*   **Conjunto de datos principal:** [REEMPLAZA: Nombre del dataset, ej: "ADNI", "HCP", "OASIS"]
*   **DOI / Enlace de referencia:** [REEMPLAZA: https://doi.org/xxxxxxx o https://portal.conjunto-datos.org]
*   **Tipo de datos:** [REEMPLAZA: ej: Imágenes de Resonancia Magnética (MRI) estructural T1, datos de comportamiento cognitivo]
*   **Cita obligatoria (si la hay):** [REEMPLAZA: Cita en formato APA que pide el proveedor de datos]

## 2. 📥 Procedimiento de Acceso y Descarga

1.  Registro y solicitud de acceso en el portal: **[REEMPLAZA: Nombre del portal, ej: "LONI Image & Data Archive"]**.
2.  Aceptación del **Acuerdo de Uso de Datos** (Data Use Agreement).
3.  Descarga mediante la herramienta: **[REEMPLAZA: ej: "Download Manager del portal", "Comandos `aws s3 sync`"]**.
4.  Se descargaron los datos correspondientes a: **[REEMPLAZA: ej: "50 sujetos del grupo 'Control' y 50 del grupo 'Bilingüe tardío'"]**.

## 3. 📁 Estructura Interna de `data/01_raw/`

## 4. 🔄 Flujo de Procesamiento
1.  **Datos Originales:** Se almacenan en `01_raw/`. *NO se modifican nunca*.
2.  **Procesamiento Intermedio:** Los resultados de pasos intermedios (ej., imágenes normalizadas, máscaras) se guardan en `02_interim/`.
3.  **Datos Finales:** Los datos listos para el análisis/modelado (ej., tablas de características extraídas) se guardan en `03_processed/`.

## 5. ⚠️ Notas Importantes
*   **Los archivos de `01_raw/` son MUY PESADOS (GBs).** Por eso **NO** se suben a GitHub. Este archivo (`README_data.md`) sirve para que cualquier persona pueda replicar la descarga.
*   El código para procesar estos datos está en la carpeta `src/data/`.

