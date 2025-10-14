# Clasificador ODS - Objetivos de Desarrollo Sostenible

## Descripción del Proyecto

Aplicación web para la clasificación automática de textos según los Objetivos de Desarrollo Sostenible (ODS) de las Naciones Unidas. Utiliza técnicas de Machine Learning para identificar automáticamente a qué ODS pertenece un texto dado.

### Funcionalidades Principales

- Predicción de textos individuales o por lotes
- Re-entrenamiento de modelos con nuevos datos
- Análisis de métricas y estadísticas
- Gestión de múltiples versiones de modelos
- Soporte para archivos CSV y Excel
- Interfaz web intuitiva

## Arquitectura del Sistema

```
Proyecto1/
├── api/                    # Backend FastAPI
│   ├── app.py             # Aplicación principal de la API
│   └── routes/            # Endpoints de la API
├── data/                  # Datasets y archivos
│   ├── train/             # Datos de entrenamiento
│   └── test/              # Datos de prueba
├── models/                # Modelos ML entrenados
├── src/                   # Código fuente del ML
├── streamlit_app.py       # Frontend web
└── requirements.txt       # Dependencias Python
```

### Componentes Técnicos

- **Backend**: FastAPI con endpoints REST
- **Frontend**: Streamlit para interfaz web
- **ML Pipeline**: scikit-learn con MultinomialNB
- **Procesamiento**: NLTK para procesamiento de lenguaje natural
- **Visualización**: Plotly para gráficos interactivos

## Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior (Recomendado: Python 3.10-3.11)
- Git para clonar el repositorio
- pip como gestor de paquetes de Python

### Instalación

1. **Clonar el Repositorio**
```bash
git clone https://github.com/LuigiEnLaCasa/ProyectoBI.git
cd ProyectoBI/Proyecto1
```

2. **Crear Entorno Virtual (Recomendado)**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

4. **Verificar Datos**
Los datasets necesarios están incluidos en el repositorio:
- `data/train/DatosAumentadosTrain.xlsx` (2,376 ejemplos)
- `data/train/Datos_etapa1.xlsx` (2,424 ejemplos)

## Ejecución de la Aplicación Streamlit

### Método 1: Ejecución Automática

```bash
# Windows
start_app.bat
```

### Método 2: Ejecución Manual

**Opción A: Solo Streamlit (Sin API Backend)**
```bash
streamlit run streamlit_app.py
```
*Nota: Algunas funcionalidades como re-entrenamiento no estarán disponibles sin la API.*

**Opción B: Con API Backend (Funcionalidad Completa)**

Terminal 1 - Backend:
```bash
set PYTHONPATH=.
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```

Terminal 2 - Frontend:
```bash
streamlit run streamlit_app.py --server.port 8501
```

### Acceso a la Aplicación

Una vez iniciado Streamlit:
- **Aplicación Web**: http://localhost:8501
- **API Backend** (si está ejecutándose): http://127.0.0.1:8000
- **Documentación API**: http://127.0.0.1:8000/docs

### Configuración de Puertos

Si el puerto 8501 está ocupado, puede especificar otro:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## Uso de la Aplicación Streamlit

### Interfaz Principal

La aplicación web está organizada en pestañas principales:

1. **Predicción**
   - Clasificación de textos individuales o por lotes
   - Carga de archivos CSV/Excel
   - Descarga de resultados en formato CSV

2. **Re-entrenamiento** (Requiere API Backend)
   - Selección de dataset base
   - Adición de nuevos ejemplos de entrenamiento
   - Entrenamiento automático de modelo mejorado

3. **Análisis**
   - Métricas de predicciones realizadas
   - Estadísticas de confianza y rendimiento
   - Análisis detallado por ODS

4. **Gestión** (Requiere API Backend)
   - Administración de modelos disponibles
   - Carga de nuevos archivos de entrenamiento
   - Actualización de lista de modelos

## Archivos del Proyecto

### Archivos Principales

```
streamlit_app.py           # Aplicación web principal
api/app.py                 # Backend FastAPI
src/                       # Código de Machine Learning
data/train/                # Datasets de entrenamiento
requirements.txt           # Dependencias Python
start_app.bat              # Script de inicio
```

### Datasets

- **DatosAumentadosTrain.xlsx**: Dataset principal (2,376 ejemplos)
- **Datos_etapa1.xlsx**: Dataset alternativo (2,424 ejemplos)
- Estructura requerida: columnas `texto` y `ods` (valores: 1, 3, 4)

### Modelos

Los modelos se generan automáticamente en `/models/` con formato:
`modelo_ods_YYYYMMDD_HHMMSS.pkl`

## Configuración

### Configurar URL de API

Para cambiar la URL de conexión a la API:

```python
# En streamlit_app.py, línea aproximada 29
API_BASE_URL = "http://127.0.0.1:8000"
```

### Agregar Nuevos Datasets

1. Colocar archivo Excel/CSV en `data/train/`
2. Asegurar columnas: `texto` y `ods`
3. Valores ODS válidos: 1, 3, 4
4. Reiniciar aplicación

## Solución de Problemas

### Error: "No module named 'X'"
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: "API no conectada"
```bash
# Verificar que el backend esté ejecutándose
# Visitar: http://127.0.0.1:8000/docs
```


## Especificaciones Técnicas

### Dependencias Principales

- Python 3.8+
- Streamlit para la interfaz web
- FastAPI para el backend
- scikit-learn para machine learning
- NLTK para procesamiento de texto
- Plotly para visualizaciones

### Puertos por Defecto

- Streamlit: 8501
- API Backend: 8000

### Formatos Soportados

- Archivos CSV y Excel para carga de datos
- Modelos en formato pickle (.pkl)
- Exportación de resultados en CSV


