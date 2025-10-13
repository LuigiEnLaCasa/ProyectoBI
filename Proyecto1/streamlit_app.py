"""
ODS Classifier - Aplicación Web Interactiva
Sección 3: Desarrollo de aplicación web para clasificación de textos ODS

Esta aplicación permite:
1. Clasificar textos según los 17 Objetivos de Desarrollo Sostenible (ODS)
2. Ver probabilidades de predicción 
3. Re-entrenar el modelo con nuevos ejemplos
4. Gestionar modelos y archivos
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict
import time

# Configuración de la página
st.set_page_config(
    page_title="ODS Classifier",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL base de la API (ajustar según necesidad)
API_BASE_URL = "http://127.0.0.1:8000"

# Mapeo de ODS (Objetivos de Desarrollo Sostenible)
# NOTA: Este modelo específico fue entrenado solo con 3 categorías ODS
ODS_MAPPING = {
    1: "Fin de la Pobreza",
    3: "Salud y Bienestar", 
    4: "Educación de Calidad"
}

# Mapeo completo para referencia (comentado porque el modelo actual no los predice)
"""
Proyecto 1 - Etapa 2
- Alejandro Hoyos
- Andrés Julián Bolivar
- Luis Alberto Pinilla
"""

def check_api_health():
    """Verifica si la API está disponible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_models():
    """Obtiene la lista de modelos disponibles"""
    try:
        # Agregar timestamp para evitar cache
        import time
        response = requests.get(f"{API_BASE_URL}/files/models?t={int(time.time())}", timeout=10)
        if response.status_code == 200:
            models = response.json().get("modelos", [])
            return sorted(models, reverse=True)  # Ordenar por fecha (más recientes primero)
        return []
    except Exception as e:
        st.error(f"Error obteniendo modelos: {e}")
        return []

def predict_text(texts: List[str], model_path: str = None):
    """Realiza predicción sobre textos"""
    try:
        payload = {"textos": texts}
        if model_path:
            payload["modelo_path"] = model_path
            
        response = requests.post(f"{API_BASE_URL}/predict/", json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def retrain_model(texts: List[str], labels: List[int], base_model: str = None, dataset_info: dict = None):
    """Re-entrena el modelo con nuevos ejemplos"""
    try:
        # Usar información del dataset si se proporciona, sino usar valores por defecto
        if dataset_info:
            base_file = dataset_info.get("file", "data/train/Datos_etapa1.xlsx")
            text_col = dataset_info.get("text_col", "textos")
            label_col = dataset_info.get("label_col", "labels")
        else:
            # Mantener compatibilidad hacia atrás
            base_file = "data/train/Datos_etapa1.xlsx"
            text_col = "textos"
            label_col = "labels"
        
        payload = {
            "base_file_path": base_file,
            "text_col": text_col,
            "label_col": label_col, 
            "textos": texts,
            "labels": labels
        }

        response = requests.post(f"{API_BASE_URL}/retrain/json", json=payload, timeout=600)  # 10 minutos

        if response.status_code == 200:
            return True, response.json()
        else:
            error_detail = response.json().get('detail', 'Error desconocido') if response.content else f"HTTP {response.status_code}"
            return False, error_detail
            
    except requests.exceptions.Timeout:
        return False, "Tiempo de espera agotado. El dataset es grande (2,424 ejemplos base). El re-entrenamiento puede tardar hasta 10 minutos. Por favor, inténtalo de nuevo."
    except requests.exceptions.ConnectionError:
        return False, "Error de conexión con la API. Verifica que esté ejecutándose."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def upload_file(file_content, filename):
    """Sube archivo a la API"""
    try:
        files = {"file": (filename, file_content, "text/csv")}
        response = requests.post(f"{API_BASE_URL}/files/upload", files=files, timeout=20)
        return response.status_code == 200
    except:
        return False

def evaluate_model(model_name: str, test_file: str = "test_evaluation.csv", text_col: str = "texto", label_col: str = "categoria_esperada"):
    """Evalúa un modelo usando un archivo de test"""
    try:
        payload = {
            "model_name": model_name,
            "test_file_name": test_file,
            "text_col": text_col,
            "label_col": label_col
        }
        
        # Aumentar timeout para datasets grandes
        timeout = 120 if "DatosAumentadosTest" in test_file else 60 if "etapa" in test_file else 30
            
        response = requests.post(f"{API_BASE_URL}/evaluate/from-file", json=payload, timeout=timeout)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            error_detail = response.json().get('detail', 'Error desconocido') if response.content else f"HTTP {response.status_code}"
            return False, error_detail
    except Exception as e:
        return False, str(e)

# Interfaz principal
def main():
    # Header principal
    st.title("Clasificador ODS - Objetivos de Desarrollo Sostenible")
    
    # Status de conexión API (compacto en sidebar)
    if not check_api_health():
        st.error("⚠️ **API no disponible**. Asegúrate de que esté ejecutándose en `http://127.0.0.1:8000`")
        st.code("uvicorn api.app:app --reload")
        st.stop()
    
    # Configuración del sidebar organizada
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Estado de API
        st.success("🟢 API Conectada")
        
        # Selección de modelo
        modelos_disponibles = get_available_models()
        
        if modelos_disponibles:
            selected_model = st.selectbox(
                "Modelo a utilizar:",
                ["Último modelo"] + modelos_disponibles
            )
            model_path = None if selected_model == "Último modelo" else selected_model
            
            # Info del modelo seleccionado
            st.caption(f"Modelos disponibles: {len(modelos_disponibles)}")
        else:
            st.warning("No hay modelos entrenados disponibles")
            model_path = None
    
    # Pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Predicción", "🔄 Re-entrenamiento", "📊 Análisis", "⚙️ Gestión"])
    
    # TAB 1: PREDICCIÓN
    with tab1:
        st.header("🔍 Clasificación de Textos")
        
        # Layout principal mejorado
        col_input, col_info = st.columns([3, 1])
        
        with col_input:
            # Método de entrada
            input_method = st.radio("Método de entrada:", ["Texto individual", "Múltiples textos", "Archivo CSV"])
            
            texts_to_predict = []
            
            if input_method == "Texto individual":
                text_input = st.text_area(
                    "Ingresa el texto a clasificar:",
                    placeholder="Ejemplo: La educación primaria gratuita es fundamental para el desarrollo...",
                    height=150
                )
                if text_input.strip():
                    texts_to_predict = [text_input.strip()]
                    
            elif input_method == "Múltiples textos":
                st.info("Separa cada texto con una línea nueva")
                multi_text_input = st.text_area(
                    "Ingresa múltiples textos:",
                    placeholder="Texto 1: La energía solar es renovable...\nTexto 2: El acceso al agua potable...",
                    height=200
                )
                if multi_text_input.strip():
                    texts_to_predict = [t.strip() for t in multi_text_input.split('\n') if t.strip()]
                    
            else:  # Archivo CSV/Excel
                uploaded_file = st.file_uploader(
                    "Sube un archivo CSV o Excel:", 
                    type=['csv', 'txt', 'xlsx', 'xls'],
                    accept_multiple_files=False,
                    help="Formatos soportados: CSV, Excel (.xlsx, .xls). El archivo debe tener textos a clasificar."
                )
                if uploaded_file:
                    try:
                        # Detectar tipo de archivo y leer apropiadamente
                        file_extension = uploaded_file.name.lower().split('.')[-1]
                        
                        if file_extension in ['xlsx', 'xls']:
                            # Leer archivo Excel
                            df = pd.read_excel(uploaded_file)
                            st.info(f"📊 Archivo Excel leído correctamente")
                        else:
                            # Leer archivo CSV
                            df = pd.read_csv(uploaded_file, encoding='utf-8')
                            st.info(f"📄 Archivo CSV leído correctamente")
                        
                        # Mostrar las columnas disponibles
                        st.info(f"Columnas encontradas: {', '.join(df.columns.tolist())}")
                        
                        # Buscar columnas que contengan texto
                        possible_text_columns = []
                        for col in df.columns:
                            col_lower = col.lower()
                            if any(word in col_lower for word in ['texto', 'text', 'content', 'contenido', 'descripcion', 'description']):
                                possible_text_columns.append(col)
                        
                        # Si no encuentra 'texto' exacto, permitir seleccionar columna
                        if 'texto' in df.columns:
                            selected_column = 'texto'
                        elif len(possible_text_columns) > 0:
                            st.warning("⚠️ No se encontró columna 'texto'. Selecciona la columna correcta:")
                            selected_column = st.selectbox(
                                "Columna que contiene los textos:",
                                possible_text_columns + [col for col in df.columns if col not in possible_text_columns]
                            )
                        else:
                            st.warning("⚠️ No se encontró columna 'texto'. Selecciona la columna correcta:")
                            selected_column = st.selectbox(
                                "Columna que contiene los textos:",
                                df.columns.tolist()
                            )
                        
                        if selected_column and selected_column in df.columns:
                            # Filtrar textos válidos
                            df_clean = df.dropna(subset=[selected_column])
                            texts_to_predict = df_clean[selected_column].astype(str).tolist()
                            
                            # Mostrar preview de los datos
                            st.success(f"✅ {len(texts_to_predict)} textos cargados desde columna '{selected_column}'")
                            
                            if len(texts_to_predict) > 0:
                                with st.expander("Preview de los primeros 3 textos"):
                                    for i, texto in enumerate(texts_to_predict[:3]):
                                        st.text(f"{i+1}. {texto[:150]}{'...' if len(texto) > 150 else ''}")
                                        
                                if len(texts_to_predict) > 50:
                                    st.warning(f"Archivo grande ({len(texts_to_predict)} textos). El procesamiento puede tardar varios minutos.")
                        else:
                            st.error("❌ Selecciona una columna válida para procesar")
                            
                    except UnicodeDecodeError:
                        try:
                            # Intentar con otra codificación para CSV
                            df = pd.read_csv(uploaded_file, encoding='latin-1')
                            st.info("📄 Archivo CSV leído con codificación latin-1")
                            # Repetir lógica de selección de columna...
                            possible_text_columns = []
                            for col in df.columns:
                                col_lower = col.lower()
                                if any(word in col_lower for word in ['texto', 'text', 'content', 'contenido']):
                                    possible_text_columns.append(col)
                            
                            if possible_text_columns:
                                selected_column = st.selectbox("Columna de texto:", possible_text_columns)
                                if selected_column:
                                    texts_to_predict = df[selected_column].dropna().astype(str).tolist()
                                    st.success(f"✅ {len(texts_to_predict)} textos cargados")
                        except Exception as e:
                            st.error(f"❌ Error de codificación: {e}")
                            st.info("💡 Para CSV: intenta guardar con codificación UTF-8")
                    except Exception as e:
                        st.error(f"❌ Error al leer archivo: {e}")
                        st.info("💡 Verifica que el archivo sea válido (CSV/Excel) y contenga texto para clasificar")
            
            # Botón de predicción
            if st.button("Clasificar Texto(s)", type="primary", disabled=not texts_to_predict):
                if texts_to_predict:
                    with st.spinner("Clasificando textos..."):
                        results = predict_text(texts_to_predict, model_path)
                    
                    if results:
                        # Guardar resultados en session state para análisis
                        st.session_state.prediction_results = results
                        
                        st.success(f"✅ Clasificación completada para {len(results)} texto(s)")
                        
                        # Mostrar resultados
                        for i, result in enumerate(results):
                            with st.expander(f"Resultado {i+1}: {result['texto'][:50]}...", expanded=True):
                                col_res1, col_res2 = st.columns([2, 1])
                                
                                with col_res1:
                                    ods_pred = result['prediccion']
                                    confianza = result['confianza']
                                    
                                    if ods_pred in ODS_MAPPING:
                                        st.markdown(f"**📍 ODS Predicho:** {ODS_MAPPING[ods_pred]}")
                                    else:
                                        st.markdown(f"**⚠️ ODS Predicho:** ODS {ods_pred} (No disponible en este modelo)")
                                        st.warning("Este ODS no está en el conjunto de entrenamiento actual")
                                    
                                    st.markdown(f"**🎯 Confianza:** {confianza:.1%}")
                                    
                                    # Interpretación de confianza
                                    if confianza > 0.7:
                                        st.success("🟢 Alta confianza - Predicción muy probable")
                                    elif confianza > 0.4:
                                        st.warning("🟡 Confianza moderada - Revisar contexto")
                                    else:
                                        st.error("🔴 Baja confianza - Texto ambiguo o fuera de dominio")
                                    
                                    # Barra de confianza
                                    confidence_color = "green" if confianza > 0.7 else "orange" if confianza > 0.4 else "red"
                                    st.markdown(f"""
                                    <div style="background-color: #f0f0f0; border-radius: 10px; padding: 5px;">
                                        <div style="background-color: {confidence_color}; width: {confianza*100}%; height: 20px; border-radius: 8px;"></div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col_res2:
                                    # Mostrar texto original
                                    st.text_area("Texto original:", result['texto'], height=100, disabled=True)
                    else:
                        st.error("Error al realizar la predicción")
                        
        with col_info:
            # Panel de información organizado
            with st.container():
                if modelos_disponibles:
                    st.info("**Modelos Disponibles**")
                    for modelo in modelos_disponibles[-3:]:
                        st.text(f"• {modelo}")
                
                st.info("**ODS Disponibles**")
                for ods_num, ods_desc in ODS_MAPPING.items():
                    st.text(f"{ods_num}. {ods_desc}")
                
                st.caption("Este modelo fue entrenado con 3 categorías ODS")
    
    # TAB 2: RE-ENTRENAMIENTO
    with tab2:
        st.header("🔄 Re-entrenamiento del Modelo")
        
        # Layout organizado para re-entrenamiento
        col_main, col_sidebar = st.columns([3, 1])
        
        with col_main:
            st.subheader("Nuevos Ejemplos de Entrenamiento")
            
            # Inicializar estado
            if 'training_examples' not in st.session_state:
                st.session_state.training_examples = []
            
            # Método de entrada para re-entrenamiento
            retrain_method = st.radio("Método de entrada:", ["Manual (uno por uno)", "Archivo CSV/Excel"], key="retrain_method")
            
            if retrain_method == "Manual (uno por uno)":
                # Agregar nuevo ejemplo manual
                with st.form("add_example_form"):
                    new_text = st.text_area("Nuevo texto:", placeholder="Ejemplo: La educación técnica mejora las oportunidades laborales...")
                    new_ods = st.selectbox("ODS correspondiente:", list(ODS_MAPPING.keys()), 
                                         format_func=lambda x: f"{x}. {ODS_MAPPING[x]}")
                    
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.caption("**Ejemplos por ODS:**")
                        st.caption("1️⃣ Programas sociales, microcréditos, comedores")
                    with col_info2:
                        st.caption("3️⃣ Servicios médicos, vacunación, salud mental")
                        st.caption("4️⃣ Educación, capacitación, alfabetización")
                    
                    if st.form_submit_button("Agregar Ejemplo"):
                        if new_text.strip():
                            st.session_state.training_examples.append({
                                'texto': new_text.strip(),
                                'ods': new_ods
                            })
                            st.success("✅ Ejemplo agregado")
                            st.rerun()
            
            else:  # Archivo CSV/Excel
                st.subheader("📂 Carga desde Archivo")
                
                uploaded_retrain_file = st.file_uploader(
                    "Sube archivo CSV/Excel para re-entrenamiento:", 
                    type=['csv', 'xlsx', 'xls'],
                    accept_multiple_files=False,
                    help="Debe contener columnas: 'texto' (o similar) y 'ods' (o 'labels', 'categoria')",
                    key="retrain_file"
                )
                
                if uploaded_retrain_file:
                    try:
                        # Detectar tipo de archivo y leer
                        file_extension = uploaded_retrain_file.name.lower().split('.')[-1]
                        
                        if file_extension in ['xlsx', 'xls']:
                            df_retrain = pd.read_excel(uploaded_retrain_file)
                        else:
                            df_retrain = pd.read_csv(uploaded_retrain_file, encoding='utf-8')
                        
                        st.info(f"📋 Columnas encontradas: {', '.join(df_retrain.columns.tolist())}")
                        
                        # Buscar columnas de texto
                        possible_text_cols = []
                        possible_label_cols = []
                        
                        for col in df_retrain.columns:
                            col_lower = col.lower()
                            if any(word in col_lower for word in ['texto', 'text', 'content', 'contenido']):
                                possible_text_cols.append(col)
                            if any(word in col_lower for word in ['ods', 'label', 'categoria', 'category', 'class']):
                                possible_label_cols.append(col)
                        
                        # Seleccionar columnas
                        col_select1, col_select2 = st.columns(2)
                        
                        with col_select1:
                            text_column = st.selectbox(
                                "Columna de textos:",
                                possible_text_cols + [col for col in df_retrain.columns if col not in possible_text_cols],
                                key="text_col_retrain"
                            )
                        
                        with col_select2:
                            label_column = st.selectbox(
                                "Columna de ODS/Labels:",
                                possible_label_cols + [col for col in df_retrain.columns if col not in possible_label_cols],
                                key="label_col_retrain"
                            )
                        
                        if text_column and label_column and st.button("Cargar Ejemplos desde Archivo", key="load_retrain"):
                            # Procesar el archivo
                            df_clean = df_retrain.dropna(subset=[text_column, label_column])
                            
                            # Filtrar solo ODS válidos (1, 3, 4)
                            df_clean = df_clean[df_clean[label_column].isin([1, 3, 4])]
                            
                            if len(df_clean) > 0:
                                # Agregar a los ejemplos de entrenamiento
                                for _, row in df_clean.iterrows():
                                    st.session_state.training_examples.append({
                                        'texto': str(row[text_column]),
                                        'ods': int(row[label_column])
                                    })
                                
                                st.success(f"✅ {len(df_clean)} ejemplos cargados desde archivo")
                                st.rerun()
                            else:
                                st.error("❌ No se encontraron ejemplos válidos (ODS 1, 3, 4)")
                                
                    except Exception as e:
                        st.error(f"❌ Error al procesar archivo: {e}")

            
            # Mostrar ejemplos agregados
            if st.session_state.training_examples:
                st.subheader(f"Ejemplos para Re-entrenamiento ({len(st.session_state.training_examples)})")
                
                examples_df = pd.DataFrame(st.session_state.training_examples)
                examples_df['ODS'] = examples_df['ods'].map(lambda x: f"{x}. {ODS_MAPPING[x]}")
                
                st.dataframe(examples_df[['texto', 'ODS']], use_container_width=True)
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("Re-entrenar Modelo", type="primary"):
                        texts = [ex['texto'] for ex in st.session_state.training_examples]
                        labels = [ex['ods'] for ex in st.session_state.training_examples]
                        
                        # Validaciones antes de re-entrenar
                        if len(texts) < 3:
                            st.error("Se necesitan al menos 3 ejemplos para re-entrenar")
                        else:
                            # Mostrar resumen antes de re-entrenar
                            ods_distribution = {}
                            for label in labels:
                                ods_distribution[label] = ods_distribution.get(label, 0) + 1
                            
                            # SELECCIÓN DE DATASET BASE PARA RE-ENTRENAMIENTO
                            st.markdown("---")
                            st.markdown("**📚 Seleccionar Dataset Base para Re-entrenamiento:**")
                            
                            # Opciones de datasets de entrenamiento
                            training_datasets = {
                                "datos_aumentados": {
                                    "name": "🔹 Datos Aumentados (2,376 ejemplos) - RECOMENDADO",
                                    "file": "data/train/DatosAumentadosTrain.xlsx", 
                                    "text_col": "textos",
                                    "label_col": "labels",
                                    "examples": 2376,
                                    "description": "Dataset base oficial - Mejor balance entre ODS",
                                    "time_estimate": "5-10 minutos"
                                },
                                "datos_etapa1": {
                                    "name": "Datos Etapa 1 (2,424 ejemplos)",
                                    "file": "data/train/Datos_etapa1.xlsx",
                                    "text_col": "textos",
                                    "label_col": "labels", 
                                    "examples": 2424,
                                    "description": "Dataset original alternativo",
                                    "time_estimate": "5-10 minutos"
                                },

                            }
                            
                            # Selector de dataset base
                            dataset_choice = st.selectbox(
                                "Dataset base:",
                                list(training_datasets.keys()),
                                format_func=lambda x: training_datasets[x]["name"],
                                key="training_dataset_selector"
                            )
                            
                            selected_training_dataset = training_datasets[dataset_choice]
                            
                            # Nota informativa sobre el dataset base oficial
                            if dataset_choice == "datos_aumentados":
                                st.success("**Dataset Base Oficial**: Los Datos Aumentados son el dataset recomendado para re-entrenamiento por su mejor balance entre categorías ODS.")
                            elif dataset_choice == "datos_etapa1":
                                st.info("**Dataset Alternativo**: Este es el dataset original. Se recomienda usar Datos Aumentados para mejor rendimiento.")
                            elif dataset_choice == "dataset_rapido":
                                st.warning("**Solo para Pruebas**: Este dataset pequeño es únicamente para verificar funcionalidad, no para uso en producción.")
                            
                            # Mostrar información del dataset seleccionado
                            col_dataset_info1, col_dataset_info2 = st.columns(2)
                            with col_dataset_info1:
                                st.metric("Ejemplos base", f"{selected_training_dataset['examples']:,}")
                            with col_dataset_info2:
                                st.metric("Tiempo estimado", selected_training_dataset['time_estimate'])
                            
                            st.caption(f"{selected_training_dataset['description']}")
                            
                            # Resumen dinámico del re-entrenamiento
                            st.info(f"**Resumen del Re-entrenamiento:**")
                            st.write(f"• **Nuevos ejemplos:** {len(texts)}")
                            st.write(f"• **Dataset base:** {selected_training_dataset['examples']:,} ejemplos ({selected_training_dataset['file'].split('/')[-1]})")
                            st.write(f"• **Total final:** ~{selected_training_dataset['examples'] + len(texts):,} ejemplos")
                            
                            # Distribución de ODS nuevos
                            if ods_distribution:
                                st.write("**Distribución de nuevos ejemplos:**")
                                for ods, count in ods_distribution.items():
                                    ods_name = ODS_MAPPING.get(ods, f"ODS {ods}")
                                    st.write(f"  • **ODS {ods}** ({ods_name}): {count} ejemplos")
                            
                            # Actualizar información del resumen
                            total_examples = selected_training_dataset['examples'] + len(texts)
                            
                            # Compatibilidad hacia atrás
                            use_reduced_dataset = (dataset_choice == "dataset_rapido")
                            
                            # Calcular tiempo estimado y tamaño del dataset basado en la selección
                            estimated_time = selected_training_dataset['time_estimate']
                            dataset_size = f"~{total_examples:,} ejemplos"
                            base_info = f"{selected_training_dataset['examples']:,} ejemplos base ({selected_training_dataset['file'].split('/')[-1]})"
                            
                            # Mostrar advertencia según el dataset seleccionado
                            if dataset_choice == "dataset_rapido":
                                st.info("**Re-entrenamiento Rápido** - Ideal para pruebas de funcionalidad")
                            elif dataset_choice == "datos_aumentados":
                                st.success(f"""
                                ✨ **Re-entrenamiento con Datos Aumentados**
                                - Dataset más balanceado: {selected_training_dataset['examples']:,} ejemplos base
                                - Tiempo estimado: {estimated_time}
                                - Distribución equilibrada entre ODS
                                - Modelo potencialmente más robusto
                                """)
                            else:  # datos_etapa1
                                st.warning(f"""
                                **Re-entrenamiento con Dataset Original**
                                - Procesando {selected_training_dataset['examples']:,} ejemplos base + {len(texts)} nuevos
                                - Tiempo estimado: {estimated_time}
                                - No cierres la ventana durante el proceso
                                - Dataset original validado
                                """)
                            
                            with st.spinner(f"Re-entrenando modelo con {dataset_size}... ({base_info})"):
                                progress_bar = st.progress(0)
                                status_text = st.empty()
                                time_text = st.empty()
                                
                                # Simular progreso más realista según el dataset
                                if use_reduced_dataset:
                                    steps = ["Cargando dataset base...", "Combinando datos...", "Entrenando modelo...", "Guardando modelo..."]
                                    sleep_time = 0.3
                                else:
                                    steps = [
                                        "📂 Cargando dataset base (2,424 ejemplos)...",
                                        "🔗 Combinando con nuevos datos...", 
                                        "🧠 Entrenando modelo (esto toma más tiempo)...",
                                        "⚙️ Optimizando hiperparámetros...",
                                        "🔍 Validando modelo...",
                                        "💾 Guardando modelo mejorado..."
                                    ]
                                    sleep_time = 1.0
                                
                                start_time = time.time()
                                for i, step in enumerate(steps):
                                    status_text.text(step)
                                    progress_bar.progress((i + 1) * (100 // len(steps)))
                                    
                                    elapsed = time.time() - start_time
                                    time_text.text(f"Tiempo transcurrido: {elapsed:.1f}s")
                                    time.sleep(sleep_time)
                                
                                success, result = retrain_model(texts, labels, model_path, selected_training_dataset)
                                
                                progress_bar.progress(100)
                                total_time = time.time() - start_time
                                status_text.text(f" ¡Completado en {total_time:.1f} segundos!")
                                time_text.text(f"Tiempo total: {total_time:.1f}s")
                            
                            if success:
                                st.success("🎉 ¡Modelo re-entrenado exitosamente!")
                                
                                # Mostrar información del nuevo modelo
                                if isinstance(result, dict):
                                    st.subheader(" Información del Nuevo Modelo")
                                    
                                    # Extraer información del modelo
                                    model_path = result.get('model_path', 'N/A')
                                    metadata = result.get('metadata', {})
                                    
                                    # Nombre del modelo (solo la parte final)
                                    model_name = model_path.split('/')[-1] if model_path != 'N/A' else 'N/A'
                                    
                                    # Métricas principales organizadas
                                    st.subheader("Métricas del Nuevo Modelo")
                                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                                    
                                    with col_m1:
                                        st.metric(" Nuevo Modelo", model_name[:15] + "..." if len(model_name) > 15 else model_name)
                                    
                                    with col_m2:
                                        base_examples = metadata.get('n_base', 'N/A')
                                        st.metric(" Ejemplos Base", f"{base_examples:,}" if base_examples != 'N/A' else base_examples)
                                    
                                    with col_m3:
                                        # F1-Score del cross-validation con mejor interpretación
                                        score_info = metadata.get('score', {})
                                        f1_cv = score_info.get('f1_macro_cv', 0)
                                        
                                        if f1_cv >= 0.9:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Excelente", delta_color="normal")
                                        elif f1_cv >= 0.8:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Muy Bueno", delta_color="normal")
                                        elif f1_cv >= 0.7:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Bueno", delta_color="normal")
                                        else:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Mejorable", delta_color="inverse")
                                    
                                    with col_m4:
                                        total_examples = metadata.get('n_total', metadata.get('n_samples', 'N/A'))
                                        st.metric("� Total Ejemplos", f"{total_examples:,}" if total_examples != 'N/A' else total_examples)
                                    
                                    # SEGUNDA FILA DE MÉTRICAS ADICIONALES
                                    col_m5, col_m6, col_m7, col_m8 = st.columns(4)
                                    
                                    with col_m5:
                                        # Ejemplos base vs nuevos
                                        base_examples = metadata.get('n_base', 'N/A')
                                        new_examples = metadata.get('n_new', len(texts))
                                        st.metric(" Ejemplos Base", base_examples)
                                        st.metric(" Ejemplos Nuevos", new_examples)
                                    
                                    
                                    # MÉTRICAS ADICIONALES MEJORADAS
                                    st.markdown("---")
                                    col_extra1, col_extra2, col_extra3 = st.columns(3)
                                    
                                    with col_extra1:
                                        # F1-Score con interpretación visual
                                        score_info = metadata.get('score', {})
                                        f1_cv = score_info.get('f1_macro_cv', 0)
                                        
                                        if f1_cv >= 0.9:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Excelente ⭐", delta_color="normal")
                                        elif f1_cv >= 0.8:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Muy Bueno ✨", delta_color="normal")
                                        elif f1_cv >= 0.7:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Bueno ✅", delta_color="normal")
                                        else:
                                            st.metric("🎯 F1-Score (CV)", f"{f1_cv:.3f}", delta="Mejorable ⚠️", delta_color="inverse")
                                    
                                    with col_extra2:
                                        # Parámetros del modelo
                                        params = metadata.get('params', {})
                                        alpha = params.get('clasificador__alpha', 'N/A')
                                        if isinstance(alpha, (int, float)):
                                            st.metric("⚙️ Alpha (NB)", f"{alpha:.4f}")
                                        else:
                                            st.metric("⚙️ Alpha (NB)", str(alpha))
                                    
                                    with col_extra3:
                                        # Calidad general del modelo
                                        if f1_cv >= 0.85:
                                            st.success("🟢 Modelo de Alta Calidad")
                                        elif f1_cv >= 0.75:
                                            st.info("🔵 Modelo de Buena Calidad") 
                                        elif f1_cv >= 0.65:
                                            st.warning("🟡 Modelo Aceptable")
                                        else:
                                            st.error("🔴 Modelo Necesita Mejoras")
                                    
                                    # Información adicional
                                    st.subheader("📋 Detalles del Entrenamiento")
                                    
                                    col_detail1, col_detail2 = st.columns(2)
                                    with col_detail1:
                                        st.info(f"""
                                        **📂 Dataset Base:** {metadata.get('dataset_base', 'N/A')}  
                                        **📝 Columna Texto:** {metadata.get('text_col', 'N/A')}  
                                        **🏷️ Columna Label:** {metadata.get('label_col', 'N/A')}  
                                        **📊 Ejemplos Base:** {metadata.get('n_base', 'N/A')} (dataset original)
                                        """)
                                    
                                    with col_detail2:
                                        # Gráfico de distribuc
                                        # ión de ODS
                                        if len(ods_distribution) > 1:
                                            import plotly.express as px
                                            
                                            ods_names = [f"ODS {k}" for k in ods_distribution.keys()]
                                            ods_counts = list(ods_distribution.values())
                                            
                                            fig_dist = px.pie(
                                                values=ods_counts,
                                                names=ods_names,
                                                title="Distribución de Nuevos Ejemplos"
                                            )
                                            fig_dist.update_traces(textinfo='label+value')
                                            st.plotly_chart(fig_dist, use_container_width=True)
                                        else:
                                            st.info("**Distribución de Nuevos Ejemplos:**")
                                            for ods, count in ods_distribution.items():
                                                st.write(f"• ODS {ods} ({ODS_MAPPING[ods]}): {count} ejemplos")
                                    
                                    # Evaluar el modelo recién entrenado (opcional)
                                    st.subheader("Evaluación del Nuevo Modelo")
                                    
                                    col_eval1, col_eval2 = st.columns(2)
                                    
                                    
                                    with col_eval2:
                                        st.info("""
                                        **Interpretación de Métricas:**
                                        
                                        • **Accuracy**: % de predicciones correctas  
                                        • **Precision**: De las predicciones positivas, % correctas  
                                        • **Recall**: % de casos positivos identificados  
                                        • **F1-Score**: Balance entre precisión y recall  
                                        
                                        **🎯 Valores objetivo:** > 0.7 es bueno, > 0.8 es excelente
                                        """)
                                
                                # Limpiar ejemplos de entrenamiento
                                st.session_state.training_examples = []  # Limpiar ejemplos
                                
                                # Mensaje simple de éxito
                                st.success("🎉 ¡Nuevo modelo creado y disponible!")
                                st.info("� El modelo aparecerá automáticamente en la lista del sidebar")

                                # BOTÓN PARA ACTUALIZAR LISTA DE MODELOS
                                col_update1, col_update2 = st.columns([1, 2])
                                with col_update1:
                                    if st.button("🔄 Actualizar Lista de Modelos", key="update_models_btn", 
                                               help="Actualiza la lista de modelos disponibles sin recargar la página"):
                                        # Forzar recarga de modelos en session_state
                                        if 'models_cache' in st.session_state:
                                            del st.session_state['models_cache']
                                        
                                        # Obtener lista actualizada
                                        try:
                                            response = requests.get(f"{API_BASE_URL}/models/")
                                            if response.status_code == 200:
                                                nuevos_modelos = response.json().get("models", [])
                                                st.session_state['models_cache'] = nuevos_modelos
                                                st.success(f"Lista actualizada! {len(nuevos_modelos)} modelos disponibles")
                                                st.rerun()  # Actualizar la interfaz
                                            else:
                                                st.error(" Error al obtener modelos actualizados")
                                        except Exception as e:
                                            st.error(f" Error de conexión: {str(e)}")
                                
                                with col_update2:
                                    st.info(" Usa este botón para ver tu nuevo modelo en la lista")
                                
                                # Mostrar modelos disponibles actuales
                                try:
                                    current_models_response = requests.get(f"{API_BASE_URL}/models/", timeout=3)
                                    if current_models_response.status_code == 200:
                                        current_models = current_models_response.json().get("models", [])
                                        if current_models:
                                            st.info(f" **Modelos disponibles actualmente:** {len(current_models)}")
                                            with st.expander(" Ver lista completa de modelos"):
                                                for i, modelo in enumerate(current_models[-10:], 1):  # Últimos 10
                                                    model_name = modelo.split('/')[-1].replace('.pkl', '')
                                                    st.text(f"{i}. {model_name}")
                                                if len(current_models) > 10:
                                                    st.caption(f"... y {len(current_models) - 10} modelos más")
                                except:
                                    st.warning(" No se pudo verificar la lista actual de modelos")
                                    
                            else:
                                st.error(f"❌ **Error en re-entrenamiento:**")
                                st.code(result)
                                
                                # Información de debug
                                with st.expander("🔍 Información de Debug"):
                                    st.write("**Datos enviados:**")
                                    debug_info = {
                                        "Número de textos nuevos": len(texts),
                                        "Número de labels": len(labels),
                                        "Labels únicos": list(set(labels)),
                                        "Archivo base": "data/train/Datos_etapa1.xlsx" if not use_reduced_dataset else "data/ejemplo_clasificacion.csv",
                                        "Dataset reducido": use_reduced_dataset,
                                        "Timeout configurado": "300 segundos (5 minutos)",
                                        "API URL": f"{API_BASE_URL}/retrain/json"
                                    }
                                    st.json(debug_info)
                                    
                                    # Test de conectividad
                                    try:
                                        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
                                        st.write(f"**API Health Check:** ✅ {health_response.status_code}")
                                    except:
                                        st.write("**API Health Check:** ❌ No disponible")
                                
                                st.info("💡 **Posibles soluciones:**")
                                st.write("• Verifica que la API esté corriendo")
                                st.write("• Asegúrate de que hay ejemplos de diferentes ODS")
                                st.write("• Intenta con más ejemplos de entrenamiento")
                                st.write("• Revisa los logs de la API para más detalles")
                
                with col_btn2:
                    if st.button("Limpiar Ejemplos"):
                        st.session_state.training_examples = []
                        st.rerun()
        
        with col_sidebar:
            st.info("**Consejos para Re-entrenamiento:**")
            st.text("• Agrega ejemplos diversos")
            st.text("• Solo ODS 1, 3 y 4 disponibles")
            st.text("• Textos claros y específicos")
            st.text("• Mínimo 5-10 ejemplos por ODS")
            st.text("")
            
            # Sección de evaluación de modelos (siempre visible)
            st.subheader("Evaluación de Modelos")
            
            # Seleccionar modelo para evaluar
            modelos_para_evaluar = get_available_models()
            if modelos_para_evaluar:
                modelo_a_evaluar = st.selectbox(
                    "Selecciona modelo a evaluar:",
                    modelos_para_evaluar,
                    key="eval_model_select"
                )
                
                # SELECCIÓN DE CONJUNTO DE DATOS PARA EVALUACIÓN
                st.markdown("---")
                st.markdown("**Seleccionar Conjunto de Datos para Evaluación:**")
                
                # Opciones de datasets de evaluación
                test_datasets = {
                    "Datos_etapa 2.xlsx": {
                        "name": "Datos Etapa 2 (99 ejemplos)",
                        "file": "Datos_etapa 2.xlsx", 
                        "text_col": "textos",
                        "label_col": "labels",
                        "description": "Dataset de prueba de la etapa 2"
                    },
                    "DatosAumentadosTest.xlsx": {
                        "name": "Datos Aumentados Test (792 ejemplos)",
                        "file": "DatosAumentadosTest.xlsx",
                        "text_col": "textos", 
                        "label_col": "labels",
                        "description": "Dataset grande y comprehensivo"
                    }
                }
                
                # Selector de dataset
                dataset_choice = st.selectbox(
                    "Conjunto de datos:",
                    list(test_datasets.keys()),
                    format_func=lambda x: test_datasets[x]["name"],
                    key="dataset_selector"
                )
                
                # Mostrar información del dataset seleccionado
                selected_dataset = test_datasets[dataset_choice]
                st.caption(f"📝 {selected_dataset['description']}")
                
                # Mostrar advertencia para datasets grandes
                if "792" in selected_dataset["name"]:
                    st.warning("Evaluación con 792 ejemplos puede tomar 30-60 segundos")
                elif "99" in selected_dataset["name"]:
                    st.info("Evaluación con 99 ejemplos tardará unos segundos")
                else:
                    st.success("Evaluación rápida con 15 ejemplos")

                if st.button("Evaluar Modelo Seleccionado", key="eval_button_main"):
                    with st.spinner(f"Evaluando modelo con {selected_dataset['name']}..."):
                        # Asegurar que el nombre del modelo tenga la extensión .pkl
                        model_name = modelo_a_evaluar if modelo_a_evaluar.endswith('.pkl') else f"{modelo_a_evaluar}.pkl"
                        
                        # Usar el dataset seleccionado
                        eval_success, eval_result = evaluate_model(
                            model_name, 
                            selected_dataset["file"],
                            selected_dataset["text_col"],
                            selected_dataset["label_col"]
                        )
                    
                    if eval_success:
                        st.success(f"✅ Evaluación completada con {selected_dataset['name']}")
                        
                        # Mostrar información del dataset usado
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.metric("📊 Ejemplos evaluados", eval_result.get('n_samples', 0))
                        with col_info2:
                            st.metric("📁 Dataset utilizado", selected_dataset['file'])
                        
                        # Destacar el tipo de evaluación
                        st.markdown("**📊 Métricas en Datos de Prueba (Test Set)**")
                        st.caption("⚠️ Estos valores pueden ser diferentes a los del Cross-Validation durante el entrenamiento")
                        
                        # Mostrar métricas de evaluación
                        col_eval_a, col_eval_b, col_eval_c = st.columns(3)
                        
                        with col_eval_a:
                            st.metric("🎯 Accuracy", f"{eval_result.get('accuracy', 0):.3f}")
                        
                        with col_eval_b:
                            st.metric("📊 Precision", f"{eval_result.get('precision_macro', 0):.3f}")
                        
                        with col_eval_c:
                            st.metric("🔄 Recall", f"{eval_result.get('recall_macro', 0):.3f}")
                        
                        st.write("**F1-Scores:**")
                        f1_col1, f1_col2, f1_col3 = st.columns(3)
                        with f1_col1:
                            st.metric("F1 Macro", f"{eval_result.get('f1_macro', 0):.3f}")
                        with f1_col2:
                            st.metric("F1 Micro", f"{eval_result.get('f1_micro', 0):.3f}")
                        with f1_col3:
                            st.metric("F1 Weighted", f"{eval_result.get('f1_weighted', 0):.3f}")
                    
                    else:
                        st.error(f"❌ Error en evaluación: {eval_result}")
                        
                        # Información de debug para ayudar a resolver problemas
                        with st.expander("🔍 Información de Debug"):
                            st.write(f"**Modelo seleccionado:** {modelo_a_evaluar}")
                            st.write(f"**Nombre enviado a API:** {model_name}")
                            st.write("**Archivo de prueba:** test_evaluation.csv")
                            st.write("**Ruta esperada:** data/test/test_evaluation.csv")
                            
                            # Verificar si el archivo existe
                            import os
                            test_file_path = os.path.join("data", "test", "test_evaluation.csv")
                            if os.path.exists(test_file_path):
                                st.success("✅ Archivo de prueba encontrado")
                            else:
                                st.error("❌ Archivo de prueba no encontrado")
                            
                            # Verificar si el modelo existe
                            model_file_path = os.path.join("models", model_name)
                            if os.path.exists(model_file_path):
                                st.success("✅ Modelo encontrado")
                            else:
                                st.error("❌ Modelo no encontrado")
            else:
                st.warning("No hay modelos disponibles para evaluar")
            
            st.info("**Dataset Real:**")
            st.text("📁 /data/train/DatosAumentadosTrain.xlsx")
            st.caption("2,376 ejemplos del dataset base oficial con mejor balance entre ODS")
    
    # TAB 3: ANÁLISIS
    with tab3:
        st.header("📊 Análisis y Métricas")
        
        # Importación local para asegurar disponibilidad
        import plotly.express as px
        
        # Verificar si hay resultados disponibles en session state
        if 'prediction_results' in st.session_state and st.session_state.prediction_results:
            results = st.session_state.prediction_results
            
            # Métricas generales
            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
            
            with col_metric1:
                st.metric("Total Textos", len(results))
            
            with col_metric2:
                avg_confidence = sum(r['confianza'] for r in results) / len(results)
                st.metric("Confianza Promedio", f"{avg_confidence:.1%}")
            
            with col_metric3:
                high_conf_count = sum(1 for r in results if r['confianza'] > 0.7)
                st.metric("🟢 Alta Confianza", f"{high_conf_count}/{len(results)}")
            
            with col_metric4:
                unique_ods = len(set(r['prediccion'] for r in results))
                st.metric("ODS Únicos", unique_ods)
            
            st.markdown("---")
            
            # Análisis por ODS
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Gráfico de distribución de predicciones
                if len(results) > 1:
                    pred_counts = {}
                    for result in results:
                        ods = result['prediccion']
                        pred_counts[ods] = pred_counts.get(ods, 0) + 1
                    
                    # Gráfico de barras con nombres de ODS
                    ods_names = [f"ODS {k}: {ODS_MAPPING.get(k, 'Desconocido')}" for k in pred_counts.keys()]
                    
                    fig = px.bar(
                        x=ods_names,
                        y=list(pred_counts.values()),
                        title="Distribución de Predicciones por ODS",
                        labels={'x': 'ODS', 'y': 'Cantidad'},
                        color=list(pred_counts.values()),
                        color_continuous_scale='viridis'
                    )
                    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                # Gráfico de confianza
                confidences = [r['confianza'] for r in results]
                fig_conf = px.histogram(
                    x=confidences,
                    title="Distribución de Niveles de Confianza",
                    labels={'x': 'Confianza', 'y': 'Frecuencia'},
                    nbins=min(10, len(confidences)),
                    color_discrete_sequence=['#2E86AB']
                )
                fig_conf.add_vline(x=0.7, line_dash="dash", line_color="green", 
                                  annotation_text="Alta Confianza (>70%)")
                fig_conf.add_vline(x=0.4, line_dash="dash", line_color="orange", 
                                  annotation_text="Confianza Mínima (>40%)")
                st.plotly_chart(fig_conf, use_container_width=True)
            
            # Análisis detallado por ODS
            st.subheader("Análisis Detallado por ODS")
            
            for ods_num in sorted(set(r['prediccion'] for r in results)):
                ods_results = [r for r in results if r['prediccion'] == ods_num]
                ods_confidences = [r['confianza'] for r in ods_results]
                
                with st.expander(f"ODS {ods_num}: {ODS_MAPPING.get(ods_num, 'Desconocido')} ({len(ods_results)} textos)"):
                    col_ods1, col_ods2, col_ods3 = st.columns(3)
                    
                    with col_ods1:
                        st.metric("Cantidad", len(ods_results))
                    
                    with col_ods2:
                        avg_conf = sum(ods_confidences) / len(ods_confidences)
                        st.metric("Confianza Promedio", f"{avg_conf:.1%}")
                    
                    with col_ods3:
                        max_conf = max(ods_confidences)
                        st.metric("Confianza Máxima", f"{max_conf:.1%}")
                    
                    # Mostrar textos con mayor confianza
                    st.write("**Textos con mayor confianza:**")
                    sorted_results = sorted(ods_results, key=lambda x: x['confianza'], reverse=True)[:3]
                    for i, res in enumerate(sorted_results, 1):
                        st.text(f"{i}. ({res['confianza']:.1%}) {res['texto'][:100]}...")
            
            # Matriz de confusión simulada (si hay etiquetas esperadas)
            st.subheader("Métricas de Rendimiento")
            
            # Tabla resumen completa
            df_results = pd.DataFrame(results)
            df_results['ODS_Descripcion'] = df_results['prediccion'].map(ODS_MAPPING)
            df_results['Confianza_Categoria'] = df_results['confianza'].apply(
                lambda x: 'Alta (>70%)' if x > 0.7 else 'Media (40-70%)' if x > 0.4 else 'Baja (<40%)'
            )
            
            # Estadísticas por categoría de confianza
            conf_stats = df_results.groupby('Confianza_Categoria').size().reset_index(name='Cantidad')
            
            col_table1, col_table2 = st.columns(2)
            
            with col_table1:
                st.write("**Distribución por Confianza:**")
                st.dataframe(conf_stats, use_container_width=True)
            
            with col_table2:
                st.write("**Estadísticas de Confianza:**")
                stats_dict = {
                    'Métrica': ['Promedio', 'Mediana', 'Desv. Estándar', 'Mínimo', 'Máximo'],
                    'Valor': [
                        f"{df_results['confianza'].mean():.3f}",
                        f"{df_results['confianza'].median():.3f}",
                        f"{df_results['confianza'].std():.3f}",
                        f"{df_results['confianza'].min():.3f}",
                        f"{df_results['confianza'].max():.3f}"
                    ]
                }
                st.dataframe(pd.DataFrame(stats_dict), use_container_width=True)
            
            # Tabla resumen final
            st.subheader("📋 Resumen Completo de Resultados")
            df_display = df_results[['texto', 'prediccion', 'ODS_Descripcion', 'confianza', 'Confianza_Categoria']]
            st.dataframe(df_display, use_container_width=True)
            
            # Opción de descarga
            csv_data = df_display.to_csv(index=False)
            st.download_button(
                label="Descargar Resultados CSV",
                data=csv_data,
                file_name=f"clasificacion_ods_resultados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        else:
            st.info("📊 Realiza algunas predicciones en la pestaña de **Predicción** para ver el análisis detallado aquí")
            
            st.markdown("""
            ### 📋 Métricas Disponibles en el Análisis:
            
            **📈 Métricas Generales:**
            - **Total de textos** procesados
            - **Confianza promedio** de las predicciones  
            - **Porcentaje de alta confianza** (>70%)
            - **Número de ODS únicos** predichos
            
            **🎯 Análisis por ODS:**
            - **Distribución de predicciones** por cada ODS
            - **Confianza promedio** por ODS
            - **Textos más representativos** de cada categoría
            
            **📊 Métricas Estadísticas:**
            - **Media, mediana, desviación estándar** de confianza
            - **Categorización** por niveles de confianza
            - **Descarga de resultados** en formato CSV
            
            ---
            
            **💡 Instrucciones:**
            1. Ve a la pestaña **"🔮 Predicción"**
            2. Ingresa texto o sube un archivo
            3. Realiza predicciones
            4. Regresa aquí para ver el análisis completo
            """)
    
    
    # TAB 4: GESTIÓN
    with tab4:
        st.header("⚙️ Gestión de Modelos y Archivos")
        
        # Layout organizado para gestión
        col_models, col_files = st.columns([1, 1])
        
        with col_models:
            with st.container():
                st.subheader("Modelos Disponibles")
                if modelos_disponibles:
                    for modelo in modelos_disponibles:
                        st.text(f"• {modelo}")
                else:
                    st.warning("No hay modelos disponibles")
        
        with col_files:
            with st.container():
                st.subheader("Subir Archivo de Entrenamiento")
            uploaded_train_file = st.file_uploader("Archivo CSV/Excel:", type=['csv', 'xlsx'])
            
            if uploaded_train_file and st.button("Subir Archivo"):
                if upload_file(uploaded_train_file.getvalue(), uploaded_train_file.name):
                    st.success("Archivo subido exitosamente")
                else:
                    st.error("Error al subir archivo")

# Ejecutar aplicación
if __name__ == "__main__":
    main()
