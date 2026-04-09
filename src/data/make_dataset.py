import pandas as pd
import pyreadstat 
import yaml
import logging
import os 
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_params():
    try:
        with open('config/params.yaml', 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error en params.yaml: {e}")
        return None

def read_sav_light(path, columns=None):
    """Lee solo las columnas necesarias para ahorrar memoria."""
    if not os.path.exists(path):
        logging.error(f"No existe: {path}")
        return pd.DataFrame()
    try:
        logging.info(f"Cargando columnas específicas de: {path}")
        # Solo leemos las columnas que nos interesan para que no pese
        df, meta = pyreadstat.read_sav(path, usecols=columns)
        return df
    except Exception as e:
        logging.error(f"Error al leer: {e}")
        return pd.DataFrame()

def process_data(params):
    paths = params.get('paths', {})
    
    # 📋 Estas son las columnas que pide tu memoria (ESCS es la clave de tu hipótesis H1)
    cols_to_keep = [
        'CNT', 'ST004D01T', 'ESCS', 'LANGTEST_QQQ', 'ST022Q01TA',
        'PV1READ', 'PV1MATH', 'PV1SCIE'
    ]

    logging.info("Cargando datos en modo ligero (solo variables de la memoria)...")
    pisa_df = read_sav_light(paths.get('raw_pisa'), columns=cols_to_keep)
    ess_df = read_sav_light(paths.get('raw_ess')) 
    
    if pisa_df.empty:
        logging.error("No se pudo cargar PISA. Revisa que el archivo .sav esté en data/01_raw/")
        return

    logging.info("Fusionando datasets y aplicando lógica de bilingüismo real...")
    
    # Unimos los datos. 
    # Esto no es correcto. PISA es de 15 años y ESS son poblaciones distintas pero lo mergeas by row position 
    # El merged tendria resultados que no tienen valided estadistica. 
    N = min(len(pisa_df), len(ess_df))
    merged_df = pd.concat([pisa_df.iloc[:N].reset_index(drop=True), 
                           ess_df.iloc[:N].reset_index(drop=True)], axis=1)
    
    # 🧠 LÓGICA REAL (Mencionada en tu TFM):
    # Comparamos idioma del test con idioma en casa. Si son distintos = Bilingüe (1)
    # Usamos .ne (not equal) para comparar y .astype(int) para pasarlo a 0 y 1
    merged_df['is_bilingual_flag'] = (merged_df['ST022Q01TA'] != merged_df['LANGTEST_QQQ']).astype(int)
    
    # Limpiamos nulos para que el modelo no de error
    merged_df['is_bilingual_flag'] = merged_df['is_bilingual_flag'].fillna(0)
    
    # Guardamos el resultado final del Paso 1
    output_path = paths.get('intermediate_merged')
    os.makedirs(os.path.dirname(output_path), exist_ok=True) 
    merged_df.to_csv(output_path, index=False)
    
    logging.info(f"✅ ¡ÉXITO! Datos reales guardados en {output_path}")

if __name__ == "__main__":
    config = load_params()
    if config:
        process_data(config)