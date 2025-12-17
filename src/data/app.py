import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
import warnings

# =============================================
# CONFIGURACIÓN Y INICIALIZACIÓN
# =============================================

# Configuración de página (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="BilingualMind - TFM Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Silenciar advertencias
warnings.filterwarnings('ignore')

# =============================================
# FUNCIONES DE BASE DE DATOS
# =============================================

def inicializar_base_datos():
    """Inicializa la base de datos con datos de ejemplo para el TFM"""
    try:
        # Crear directorio para base de datos
        os.makedirs("database", exist_ok=True)
        db_path = "database/bilingualmind.db"
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tabla PISA con estructura mejorada
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pisa_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CNT TEXT,
                PV1READ REAL,
                ESCS REAL,
                BILINGUAL INTEGER,
                REGION TEXT,
                GENDER INTEGER,
                AGE INTEGER,
                WEIGHT REAL
            )
        ''')
        
        # Tabla ESS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ess_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT,
                gndr INTEGER,
                eduyrs REAL,
                hinctnta REAL,
                bilingual INTEGER,
                age INTEGER,
                region TEXT
            )
        ''')
        
        # Verificar si necesitamos insertar datos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM pisa_data")
        count_pisa = cursor.fetchone()[0]
        
        if count_pisa == 0:
            # Datos de ejemplo realistas para TFM
            datos_pisa = [
                # Albania (bilingües)
                ('ALB', 247.571, -1.1112, 1, 'Sur Europa', 1, 15, 1.0),
                ('ALB', 258.472, -0.8507, 1, 'Sur Europa', 2, 16, 0.9),
                ('ALB', 284.670, -0.3867, 1, 'Sur Europa', 1, 15, 1.1),
                
                # España (mix)
                ('ESP', 485.320, 0.2432, 0, 'Sur Europa', 1, 16, 1.0),
                ('ESP', 492.150, 0.5765, 1, 'Sur Europa', 2, 15, 0.8),
                ('ESP', 476.890, -0.1234, 0, 'Sur Europa', 1, 16, 1.2),
                
                # Francia (bilingües)
                ('FRA', 492.150, 0.8765, 1, 'Oeste Europa', 2, 15, 1.0),
                ('FRA', 501.230, 1.2345, 1, 'Oeste Europa', 1, 16, 0.9),
                ('FRA', 488.760, 0.6543, 1, 'Oeste Europa', 2, 15, 1.1),
                
                # Alemania
                ('DEU', 498.760, 1.0345, 1, 'Oeste Europa', 1, 16, 1.0),
                ('DEU', 512.340, 1.4567, 1, 'Oeste Europa', 2, 15, 0.8),
                ('DEU', 503.210, 1.1234, 0, 'Oeste Europa', 1, 16, 1.1),
                
                # Finlandia (alto rendimiento)
                ('FIN', 523.450, 1.5678, 1, 'Norte Europa', 1, 15, 1.0),
                ('FIN', 534.120, 1.7890, 1, 'Norte Europa', 2, 16, 0.9),
            ]
            
            cursor.executemany('''
                INSERT INTO pisa_data (CNT, PV1READ, ESCS, BILINGUAL, REGION, GENDER, AGE, WEIGHT)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', datos_pisa)
        
        # Datos ESS
        cursor.execute("SELECT COUNT(*) FROM ess_data")
        count_ess = cursor.fetchone()[0]
        
        if count_ess == 0:
            datos_ess = [
                ('ES', 1, 12.5, 5, 1, 25, 'Sur'),
                ('ES', 2, 14.2, 6, 1, 30, 'Sur'),
                ('FR', 1, 13.8, 7, 1, 28, 'Oeste'),
                ('FR', 2, 15.1, 8, 1, 35, 'Oeste'),
                ('DE', 1, 14.5, 7, 0, 32, 'Oeste'),
                ('DE', 2, 13.2, 6, 0, 29, 'Oeste'),
                ('UK', 1, 13.9, 7, 1, 31, 'Norte'),
                ('UK', 2, 12.8, 5, 1, 27, 'Norte'),
            ]
            
            cursor.executemany('''
                INSERT INTO ess_data (country, gndr, eduyrs, hinctnta, bilingual, age, region)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', datos_ess)
        
        conn.commit()
        conn.close()
        return db_path
        
    except Exception as e:
        st.error(f"❌ Error inicializando base de datos: {e}")
        return None

@st.cache_data(ttl=3600)
def cargar_datos():
    """Carga datos desde SQLite"""
    try:
        db_path = inicializar_base_datos()
        if not db_path:
            return pd.DataFrame(), pd.DataFrame(), ""
            
        conn = sqlite3.connect(db_path)
        
        # Cargar datos
        df_pisa = pd.read_sql("SELECT * FROM pisa_data", conn)
        df_ess = pd.read_sql("SELECT * FROM ess_data", conn)
        
        conn.close()
        
        return df_pisa, df_ess, db_path
        
    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")
        return pd.DataFrame(), pd.DataFrame(), ""

# =============================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================

def crear_grafico_principal(df_pisa):
    """Crea el gráfico principal de análisis"""
    if df_pisa.empty:
        st.warning("📊 No hay datos disponibles para mostrar el gráfico")
        return None
        
    # Crear copia para no modificar el original
    df = df_pisa.copy()
    df['Grupo_Linguistico'] = df['BILINGUAL'].map({1: 'Bilingüe', 0: 'Monolingüe'})
    
    fig = px.scatter(
        df, 
        x='ESCS', 
        y='PV1READ', 
        color='Grupo_Linguistico',
        title="📚 Rendimiento en Lectura vs Estatus Socioeconómico - Análisis PISA",
        labels={
            'ESCS': 'Índice Socioeconómico y Cultural (ESCS)',
            'PV1READ': 'Puntuación en Comprensión Lectora', 
            'Grupo_Linguistico': 'Estatus Lingüístico'
        },
        color_discrete_map={'Bilingüe': '#2ECC71', 'Monolingüe': '#E74C3C'},
        hover_data=['CNT', 'REGION', 'GENDER']
    )
    
    fig.update_layout(
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(size=12)
    )
    
    return fig

def crear_metricas_principales(df_pisa, df_ess):
    """Crea las métricas principales del dashboard"""
    if not df_pisa.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_estudiantes = len(df_pisa)
            st.metric("👥 Total Estudiantes", f"{total_estudiantes:,}")
        
        with col2:
            bilingues = df_pisa['BILINGUAL'].sum()
            porcentaje_bilingues = (bilingues / total_estudiantes) * 100
            st.metric("🌍 Estudiantes Bilingües", f"{bilingues:,}", f"{porcentaje_bilingues:.1f}%")
        
        with col3:
            promedio_lectura = df_pisa['PV1READ'].mean()
            st.metric("📖 Puntuación Promedio Lectura", f"{promedio_lectura:.1f}")
        
        with col4:
            paises = df_pisa['CNT'].nunique()
            st.metric("🇺🇳 Países Representados", paises)

def crear_analisis_comparativo(df_pisa):
    """Análisis comparativo entre grupos"""
    if df_pisa.empty:
        st.warning("No hay datos para análisis comparativo")
        return
        
    st.subheader("📊 Análisis Comparativo por Grupo Lingüístico")
    
    # Estadísticas por grupo
    stats = df_pisa.groupby('BILINGUAL').agg({
        'PV1READ': ['mean', 'std', 'count'],
        'ESCS': ['mean', 'std']
    }).round(2)
    
    # Renombrar para mejor visualización
    stats.columns = ['Lectura_Promedio', 'Lectura_Desv', 'N', 'ESCS_Promedio', 'ESCS_Desv']
    stats.index = ['Monolingüe', 'Bilingüe']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Estadísticas Descriptivas:**")
        st.dataframe(stats, use_container_width=True)
    
    with col2:
        # Diferencia en puntuación
        if len(df_pisa[df_pisa['BILINGUAL'] == 1]) > 0 and len(df_pisa[df_pisa['BILINGUAL'] == 0]) > 0:
            prom_bilingue = df_pisa[df_pisa['BILINGUAL'] == 1]['PV1READ'].mean()
            prom_monolingue = df_pisa[df_pisa['BILINGUAL'] == 0]['PV1READ'].mean()
            diferencia = prom_bilingue - prom_monolingue
            diferencia_porcentaje = (diferencia / prom_monolingue) * 100 if prom_monolingue != 0 else 0
            
            st.metric(
                "🎯 Diferencia en Puntuación", 
                f"{diferencia:+.1f} puntos",
                delta=f"{diferencia_porcentaje:+.1f}%",
                delta_color="normal"
            )
            
            # Análisis de ESCS
            escs_bilingue = df_pisa[df_pisa['BILINGUAL'] == 1]['ESCS'].mean()
            escs_monolingue = df_pisa[df_pisa['BILINGUAL'] == 0]['ESCS'].mean()
            
            st.metric(
                "🏠 Diferencia en ESCS",
                f"{(escs_bilingue - escs_monolingue):+.2f}",
                help="Diferencia en índice socioeconómico promedio"
            )
        else:
            st.warning("No hay suficientes datos para comparación")

# =============================================
# SECCIONES PRINCIPALES
# =============================================

def seccion_analisis_principal(df_pisa, df_ess):
    """Sección principal de análisis"""
    st.header("📈 Análisis Principal - BilingualMind")
    
    if df_pisa.empty:
        st.error("🚫 No hay datos PISA disponibles para análisis")
        return
    
    # Métricas principales
    crear_metricas_principales(df_pisa, df_ess)
    
    st.markdown("---")
    
    # Gráfico principal
    fig = crear_grafico_principal(df_pisa)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis comparativo
    crear_analisis_comparativo(df_pisa)

def seccion_evidencias_tfm():
    """Sección de evidencias para el TFM"""
    st.header("🎓 Evidencias Científicas - TFM BilingualMind")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Fundamentación Teórica")
        st.markdown("""
        ### Hipótesis Principal
        El bilingüismo ejerce un efecto moderador positivo en la relación 
        entre estatus socioeconómico y rendimiento académico.
        
        ### Variables de Estudio
        - **Variable Dependiente**: PV1READ (Comprensión Lectora PISA)
        - **Variable Independiente**: ESCS (Índice Socioeconómico)
        - **Variable Moderadora**: BILINGUAL (Estatus Bilingüe)
        - **Variables de Control**: Género, Edad, Región, País
        """)
    
    with col2:
        st.subheader("📋 Metodología")
        st.markdown("""
        ### Diseño de Investigación
        1. **Fuente de Datos**: OECD PISA 2018 + ESS
        2. **Muestra**: Estudiantes de 15 años
        3. **Análisis**: Modelos de regresión con interacción
        4. **Control**: Variables sociodemográficas
        
        ### Métodos Estadísticos
        - Análisis descriptivo comparativo
        - Modelos de regresión lineal
        - Análisis de interacción
        - Visualización avanzada
        """)
    
    st.markdown("---")
    
    st.subheader("🎯 Contribución Esperada")
    st.info("""
    Este estudio busca evidenciar empíricamente el **efecto protector del bilingüismo** 
    frente a desventajas socioeconómicas, proporcionando insights para políticas 
    educativas basadas en datos.
    """)

def seccion_gestion_datos(df_pisa, df_ess, db_path):
    """Sección de gestión y exploración de datos"""
    st.header("📁 Gestión y Exploración de Datos")
    
    if db_path:
        st.info(f"**Ubicación de base de datos:** `{db_path}`")
    else:
        st.error("No se pudo acceder a la base de datos")
        return
    
    tab1, tab2, tab3 = st.tabs(["📊 Datos PISA", "🌍 Datos ESS", "🔍 SQL Explorer"])
    
    with tab1:
        st.subheader("Dataset PISA")
        if not df_pisa.empty:
            st.write(f"**Registros:** {len(df_pisa):,} | **Variables:** {len(df_pisa.columns)}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Primeras filas:**")
                st.dataframe(df_pisa.head(10), use_container_width=True)
            with col2:
                st.write("**Resumen estadístico:**")
                st.dataframe(df_pisa.describe(), use_container_width=True)
        else:
            st.warning("No hay datos PISA disponibles")
    
    with tab2:
        st.subheader("Dataset ESS")
        if not df_ess.empty:
            st.write(f"**Registros:** {len(df_ess):,} | **Variables:** {len(df_ess.columns)}")
            st.dataframe(df_ess.head(10), use_container_width=True)
        else:
            st.warning("No hay datos ESS disponibles")
    
    with tab3:
        st.subheader("Explorador SQL")
        st.info("Ejecuta consultas SQL personalizadas en la base de datos")
        
        query = st.text_area(
            "Consulta SQL:",
            value="SELECT CNT, BILINGUAL, AVG(PV1READ) as Promedio_Lectura FROM pisa_data GROUP BY CNT, BILINGUAL",
            height=100
        )
        
        if st.button("Ejecutar Consulta"):
            try:
                conn = sqlite3.connect(db_path)
                resultado = pd.read_sql(query, conn)
                conn.close()
                
                st.write("**Resultado:**")
                st.dataframe(resultado, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error en la consulta: {e}")

# =============================================
# APLICACIÓN PRINCIPAL
# =============================================

def main():
    """Función principal de la aplicación"""
    
    # Header principal
    st.title("🎓 BilingualMind - TFM Master Data Science")
    st.markdown("""
    **Análisis del impacto del bilingüismo en el rendimiento académico y su interacción 
    con factores socioeconómicos utilizando datos PISA y ESS**
    """)
    st.markdown("---")
    
    # Cargar datos con spinner
    with st.spinner("🔄 Cargando datos y realizando análisis..."):
        df_pisa, df_ess, db_path = cargar_datos()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navegación")
    seccion = st.sidebar.radio(
        "Selecciona una sección:",
        ["📈 Análisis Principal", "🎓 Evidencias TFM", "📁 Gestión de Datos"]
    )
    
    # Mostrar sección seleccionada
    if seccion == "📈 Análisis Principal":
        seccion_analisis_principal(df_pisa, df_ess)
    
    elif seccion == "🎓 Evidencias TFM":
        seccion_evidencias_tfm()
    
    elif seccion == "📁 Gestión de Datos":
        seccion_gestion_datos(df_pisa, df_ess, db_path)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        <b>BilingualMind</b> - TFM Master Data Science | 
        Análisis de datos PISA & ESS | 
        Desarrollado para investigación educativa
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================
# EJECUCIÓN
# =============================================

if __name__ == "__main__":
    # Ejecutar aplicación (sin configuraciones obsoletas)
    main()