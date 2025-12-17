# ==============================================================================
# src/features/build_features.py
# Carga el archivo intermedio, aplica ingeniería y guarda los sets listos 
# para ML en data/03_processed/.
# ==============================================================================

import pandas as pd
import yaml
import logging
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_params():
    """Carga los parámetros de configuración (Ruta y Codificación corregida)."""
    try:
        # RUTA CORREGIDA: 'config/params.yaml'
        # CODIFICACIÓN CORREGIDA: encoding='utf-8' para evitar el error 'charmap'
        with open('config/params.yaml', 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error al cargar params.yaml: {e}")
        return None

def load_intermediate_data(path):
    """Carga el dataset limpio y fusionado desde data/02_intermediate/."""
    if not os.path.exists(path):
        logging.error(f"Archivo intermedio NO ENCONTRADO en: {path}. ¿Ejecutaste make_dataset.py?")
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        logging.info(f"Datos intermedios cargados. Tamaño: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Fallo al leer los datos intermedios: {e}")
        return pd.DataFrame()

def apply_transformations(df, params):
    """Realiza la Ingeniería de Características, escalado y codificación."""
    
    logging.info("Aplicando Feature Engineering y Preprocesamiento...")
    
    # ⚠️ RECREA AQUÍ TU CÓDIGO DE INGENIERÍA DE CARACTERÍSTICAS
    
    # --- Preparación para Transformación ---
    target = params.get('model_params', {}).get('target_variable')
    preprocessing = params.get('preprocessing', {})
    
    if target not in df.columns:
        logging.error(f"Variable objetivo '{target}' no encontrada en los datos.")
        return None, None

    y = df[target]
    X = df.drop(columns=[target], errors='ignore')
    
    numerical_features = preprocessing.get('numerical_features', [])
    categorical_features = preprocessing.get('categorical_features', [])
    
    # --- Pipeline de Preprocesamiento ---
    preprocessor = ColumnTransformer(
        transformers=[
            # Escalado de características numéricas
            ('num', StandardScaler(), [col for col in numerical_features if col in X.columns]),
            # Codificación de características categóricas
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), [col for col in categorical_features if col in X.columns])
        ],
        remainder='drop' 
    )
    
    X_processed = preprocessor.fit_transform(X)
    # Obtener los nombres de las columnas después de la codificación OneHot
    feature_names = preprocessor.get_feature_names_out()
    X_processed_df = pd.DataFrame(X_processed, columns=feature_names)
    
    return X_processed_df, y

def split_and_save_data(X, y, params):
    """Divide los datos en entrenamiento y prueba y los guarda en data/03_processed/."""
    
    preprocessing = params.get('preprocessing', {})
    paths = params.get('paths', {})
    
    # División de datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=preprocessing.get('test_size', 0.2), 
        random_state=preprocessing.get('random_seed', 42), 
        # stratify=y 
    )

    processed_path = paths.get('processed_data')
    os.makedirs(processed_path, exist_ok=True)
    
    # Guardar sets de datos
    X_train.to_csv(processed_path + 'X_train.csv', index=False)
    y_train.to_frame('target').to_csv(processed_path + 'y_train.csv', index=False)
    X_test.to_csv(processed_path + 'X_test.csv', index=False)
    y_test.to_frame('target').to_csv(processed_path + 'y_test.csv', index=False)
    
    logging.info(f"Sets guardados. Train X: {X_train.shape}, Test X: {X_test.shape}")


if __name__ == "__main__":
    params = load_params()
    if params:
        intermediate_path = params.get('paths', {}).get('intermediate_merged')
        data_df = load_intermediate_data(intermediate_path)
        
        if not data_df.empty:
            X_processed, y = apply_transformations(data_df, params)
            if X_processed is not None:
                split_and_save_data(X_processed, y, params)
                logging.info("Proceso build_features.py completado.")