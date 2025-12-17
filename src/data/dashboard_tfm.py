import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de página
st.set_page_config(
    page_title="BilingualMind Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🧠 BilingualMind - Proyecto TFM")
st.markdown("**Dashboard interactivo para análisis de PISA, ESS y Neurociencia**")
st.markdown("---")

# Métricas principales en 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Accuracy PISA",
        value="78.2%",
        delta="+2.3%",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Recall Macro",
        value="0.75",
        delta="-0.02",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="F1-Score",
        value="0.76",
        delta="+0.01"
    )

with col4:
    st.metric(
        label="MAE ESS",
        value="0.23",
        delta="-0.05",
        delta_color="inverse"
    )

st.markdown("---")

# Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Análisis PISA",
    "🌍 European Social Survey",
    "🧠 Neurociencia",
    "⚙️ Configuración"
])

# Pestaña 1: PISA
with tab1:
    st.header("Resultados del Modelo PISA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Matriz de Confusión")
        # Matriz de confusión simulada
        confusion_matrix = np.array([
            [120, 15, 8, 5],
            [10, 95, 12, 7],
            [8, 10, 105, 9],
            [5, 8, 10, 115]
        ])
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto'],
                   yticklabels=['Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto'])
        plt.xlabel('Predicción')
        plt.ylabel('Real')
        plt.title('Matriz de Confusión - Modelo PISA')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Métricas por Clase")
        metrics_data = {
            'Clase': ['Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto'],
            'Precision': [0.82, 0.78, 0.81, 0.85],
            'Recall': [0.81, 0.76, 0.79, 0.84],
            'F1-Score': [0.815, 0.77, 0.80, 0.845]
        }
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)
        
        st.subheader("Comparativa de Modelos")
        models_data = {
            'Modelo': ['Random Forest', 'SVM', 'XGBoost', 'Red Neuronal'],
            'Accuracy': [0.782, 0.765, 0.791, 0.775],
            'F1-Score': [0.76, 0.74, 0.77, 0.75]
        }
        st.bar_chart(pd.DataFrame(models_data).set_index('Modelo'))

# Pestaña 2: ESS
with tab2:
    st.header("European Social Survey - Bienestar Social")
    
    # Datos simulados para ESS
    ess_data = pd.DataFrame({
        'País': ['España', 'Francia', 'Alemania', 'Italia', 'Reino Unido', 
                'Suecia', 'Noruega', 'Dinamarca', 'Países Bajos', 'Bélgica'],
        'Bienestar': [6.8, 6.9, 7.2, 6.5, 7.0, 7.5, 7.6, 7.8, 7.4, 7.1],
        'Confianza Social': [5.2, 5.5, 6.0, 4.8, 5.8, 6.5, 6.8, 7.0, 6.2, 5.6],
        'Educación': [7.0, 7.2, 7.5, 6.8, 7.3, 7.8, 7.9, 8.0, 7.6, 7.2]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mapa de Calor de Correlaciones")
        corr_matrix = ess_data.select_dtypes(include=[np.number]).corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=.5, cbar_kws={"shrink": .8})
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top 5 Países por Bienestar")
        top_countries = ess_data.nlargest(5, 'Bienestar')
        fig = px.bar(top_countries, x='País', y='Bienestar',
                    color='Bienestar', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

# Pestaña 3: Neurociencia
with tab3:
    st.header("Análisis de Neuroimagen")
    
    st.subheader("Activación Cerebral - Bilingües vs Monolingües")
    
    # Crear datos simulados de activación cerebral
    np.random.seed(42)
    brain_data = np.random.randn(10, 10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Corte Axial")
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(brain_data, cmap='hot', interpolation='nearest')
        plt.colorbar(im, ax=ax, label='Nivel de Activación')
        ax.set_title('Activación - Área Broca')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Comparativa Grupos")
        groups_data = pd.DataFrame({
            'Grupo': ['Bilingües', 'Monolingües'],
            'Activación Prefrontal': [2.8, 1.9],
            'Activación Temporal': [2.4, 1.7],
            'Conectividad': [3.1, 2.2]
        })
        st.dataframe(groups_data, use_container_width=True)
        
        # Gráfico de comparación
        fig, ax = plt.subplots(figsize=(6, 4))
        x = np.arange(len(groups_data['Grupo']))
        width = 0.25
        ax.bar(x - width, groups_data['Activación Prefrontal'], width, label='Prefrontal')
        ax.bar(x, groups_data['Activación Temporal'], width, label='Temporal')
        ax.bar(x + width, groups_data['Conectividad'], width, label='Conectividad')
        ax.set_xticks(x)
        ax.set_xticklabels(groups_data['Grupo'])
        ax.legend()
        ax.set_ylabel('Nivel de Activación')
        st.pyplot(fig)

# Pestaña 4: Configuración
with tab4:
    st.header("Configuración del Modelo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parámetros del Modelo")
        
        # Sliders para parámetros
        threshold = st.slider(
            "Umbral de Clasificación",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Ajusta el umbral para la clasificación"
        )
        
        n_estimators = st.slider(
            "Número de Estimadores (Random Forest)",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
        
        max_depth = st.select_slider(
            "Profundidad Máxima",
            options=[5, 10, 15, 20, 25, 30, 'Sin límite'],
            value=20
        )
    
    with col2:
        st.subheader("Selección de Modelo")
        
        model_type = st.selectbox(
            "Algoritmo",
            ["Random Forest", "Gradient Boosting", "SVM", "Red Neuronal", "Ensemble"]
        )
        
        feature_selection = st.multiselect(
            "Selección de Características",
            ["Datos PISA", "Datos ESS", "Neuroimagen", "Demográficos", "Socioeconómicos"],
            default=["Datos PISA", "Datos ESS"]
        )
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔄 Reentrenar Modelo", type="primary"):
                st.success("Modelo reentrenado exitosamente!")
        
        with col_btn2:
            if st.button("💾 Guardar Configuración"):
                st.info("Configuración guardada")
        
        with col_btn3:
            if st.button("📊 Generar Reporte"):
                st.warning("Generando reporte...")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración Global")
    
    st.subheader("Datos")
    data_source = st.radio(
        "Fuente de Datos",
        ["PISA 2022", "ESS Round 10", "Dataset Personalizado"]
    )
    
    st.subheader("Visualización")
    theme = st.selectbox(
        "Tema",
        ["Claro", "Oscuro", "Automático"]
    )
    
    chart_style = st.selectbox(
        "Estilo de Gráficos",
        ["Plotly", "Matplotlib", "Seaborn"]
    )
    
    st.subheader("Exportación")
    if st.button("📥 Exportar Dashboard"):
        st.sidebar.success("Exportación iniciada")
    
    st.markdown("---")
    st.markdown("### 📊 Métricas del Proyecto")
    st.metric("Completado", "85%")
    st.progress(0.85)
    
    st.markdown("---")
    st.caption("TFM Máster Data Science")
    st.caption("Estudiante: Gema")
    st.caption("Versión: 1.0")

# Footer
st.markdown("---")
st.caption("© 2024 BilingualMind - Proyecto de Investigación en Ciencia de Datos")
