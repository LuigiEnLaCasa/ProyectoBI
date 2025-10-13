# 🌍 Clasificador ODS - Objetivos de Desarrollo Sostenible

## 📋 Descripción del Proyecto

Este proyecto es una aplicación web completa para la **clasificación automática de textos** según los **17 Objetivos de Desarrollo Sostenible (ODS)** de las Naciones Unidas. La aplicación utiliza técnicas de Machine Learning para identificar automáticamente a qué ODS pertenece un texto dado.

### 🎯 Funcionalidades Principales

- **🔮 Predicción en tiempo real**: Clasificación de textos individuales o por lotes
- **📊 Análisis avanzado**: Métricas, gráficos y estadísticas de confianza
- **🔄 Re-entrenamiento**: Capacidad de mejorar el modelo con nuevos datos
- **⚙️ Gestión de modelos**: Administración de múltiples versiones de modelos
- **📁 Carga de archivos**: Soporte para CSV y Excel
- **🎨 Interfaz intuitiva**: Dashboard web con Streamlit

---

## 🏗️ Arquitectura del Sistema

```
📦 Proyecto1/
├── 🚀 api/                    # Backend FastAPI
│   ├── app.py                 # Aplicación principal de la API
│   └── routes/                # Endpoints de la API
├── 📊 data/                   # Datasets y archivos
│   ├── train/                 # Datos de entrenamiento
│   └── test/                  # Datos de prueba
├── 🤖 models/                 # Modelos ML entrenados
├── 💻 src/                    # Código fuente del ML
├── 🌐 streamlit_app.py        # Frontend web
└── 📄 requirements.txt        # Dependencias Python
```

### 🔧 Componentes Técnicos

- **Backend**: FastAPI con endpoints REST
- **Frontend**: Streamlit para interfaz web
- **ML Pipeline**: scikit-learn con MultinomialNB
- **Procesamiento**: NLTK para procesamiento de lenguaje natural
- **Visualización**: Plotly para gráficos interactivos

---

## 🚀 Instalación y Configuración

### 📋 Prerrequisitos

- **Python 3.8+** (Recomendado: Python 3.10-3.11)
- **Git** (para clonar el repositorio)
- **pip** (gestor de paquetes de Python)

### 1️⃣ Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/LuigiEnLaCasa/ProyectoBI.git

# Navegar al directorio del proyecto
cd ProyectoBI/Proyecto1
```

### 2️⃣ Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### 4️⃣ Configurar Datos Iniciales

Los datasets necesarios ya están incluidos en el repositorio:
- `data/train/DatosAumentadosTrain.xlsx` (2,376 ejemplos - Dataset principal)
- `data/train/Datos_etapa1.xlsx` (2,424 ejemplos - Dataset alternativo)

---

## ▶️ Ejecución del Proyecto

### 🔥 Método 1: Ejecución Automática (Recomendado)

```bash
# Ejecutar el script de inicio automático
./start_app.bat  # En Windows
```

O manualmente:

```bash
# 1. Iniciar el backend (Terminal 1)
cd api
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# 2. Iniciar el frontend (Terminal 2 - Nueva ventana)
streamlit run streamlit_app.py --server.port 8501
```

### 🌐 Acceder a la Aplicación

Una vez iniciados ambos servicios:

- **🌟 Aplicación Web**: http://localhost:8501
- **📡 API Backend**: http://127.0.0.1:8000
- **📖 Documentación API**: http://127.0.0.1:8000/docs

---

## 🎮 Guía de Uso

### 1️⃣ **Pestaña Predicción** 🔮
- Ingresa texto manualmente o sube archivos CSV/Excel
- Obtén clasificaciones ODS con porcentajes de confianza
- Descarga resultados en formato CSV

### 2️⃣ **Pestaña Re-entrenamiento** 🔄
- Selecciona dataset base (DatosAumentados por defecto)
- Carga nuevos ejemplos de entrenamiento
- Entrena modelo mejorado automáticamente

### 3️⃣ **Pestaña Análisis** 📊
- Visualiza métricas de predicciones realizadas
- Gráficos de distribución por ODS
- Estadísticas de confianza y rendimiento

### 4️⃣ **Pestaña Gestión** ⚙️
- Administra modelos disponibles
- Sube nuevos archivos de entrenamiento
- Actualiza lista de modelos

---

## 📁 Archivos Importantes

### 📋 **Archivos Esenciales (NO ELIMINAR)**

```
├── streamlit_app.py           # ⭐ Aplicación web principal
├── api/app.py                 # ⭐ Backend FastAPI
├── api/routes/                # ⭐ Endpoints de la API
├── src/                       # ⭐ Código ML y pipeline
├── data/train/                # ⭐ Datasets de entrenamiento
├── requirements.txt           # ⭐ Dependencias Python
└── start_app.bat             # ⭐ Script de inicio automático
```

### 📊 **Datasets Incluidos**

- **DatosAumentadosTrain.xlsx**: Dataset principal (2,376 ejemplos)
- **Datos_etapa1.xlsx**: Dataset alternativo (2,424 ejemplos)
- Ambos incluyen columnas: `texto` y `ods` (1, 3, 4)

### 🤖 **Modelos ML**

Los modelos se generan automáticamente en `/models/` al entrenar:
- Formato: `modelo_ods_YYYYMMDD_HHMMSS.pkl`
- Incluyen pipeline completo (vectorización + clasificador)

---

## 🔧 Configuración Avanzada

### 🌐 **Configurar URLs de API**

Si necesitas cambiar las URLs por defecto:

```python
# En streamlit_app.py, línea ~29
API_BASE_URL = "http://127.0.0.1:8000"  # Cambiar aquí si es necesario
```

### 🎨 **Personalizar Puerto Streamlit**

```bash
streamlit run streamlit_app.py --server.port PUERTO_DESEADO
```

### 📊 **Agregar Nuevos Datasets**

1. Colocar archivo Excel/CSV en `data/train/`
2. Asegurar columnas: `texto` y `ods`
3. Valores ODS válidos: 1, 3, 4
4. Reiniciar aplicación para detectar nuevo dataset

---

## 🐛 Solución de Problemas

### ❌ **Error: "No module named 'X'"**
```bash
pip install -r requirements.txt --force-reinstall
```

### ❌ **Error: "API no conectada"**
```bash
# Verificar que el backend esté ejecutándose
curl http://127.0.0.1:8000/health
# O visitar en navegador: http://127.0.0.1:8000/docs
```

### ❌ **Error: "Puerto ocupado"**
```bash
# Cambiar puerto de Streamlit
streamlit run streamlit_app.py --server.port 8502

# O matar procesos
taskkill /f /im python.exe  # Windows
pkill -f streamlit          # Linux/Mac
```

### ❌ **Problemas con modelos**
```bash
# Limpiar cache de modelos
rm -rf models/*.pkl
# Entrenar nuevo modelo desde la aplicación web
```

---

## 🚢 Despliegue en Producción

### 🐳 **Docker (Recomendado)**

```dockerfile
# Dockerfile ejemplo
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Exponer puertos
EXPOSE 8000 8501

# Script de inicio
CMD ["sh", "-c", "uvicorn api.app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
```

### ☁️ **Servicios en la Nube**

- **Heroku**: Usar `Procfile` con gunicorn
- **AWS EC2**: Instalar nginx como proxy reverso
- **Google Cloud Run**: Containerizar con Docker
- **Azure Container Instances**: Deployment directo

---

## 👥 Equipo de Desarrollo

- **Desarrollador Principal**: Luis Alberto Pinilla
- **Tecnologías**: Python, FastAPI, Streamlit, scikit-learn
- **Repositorio**: [GitHub - ProyectoBI](https://github.com/LuigiEnLaCasa/ProyectoBI)

---

## 📝 Notas de Versión

### v1.0.0 - Octubre 2025
- ✅ Clasificación automática ODS (1, 3, 4)
- ✅ Interfaz web completa con Streamlit
- ✅ API REST con FastAPI
- ✅ Re-entrenamiento dinámico de modelos
- ✅ Análisis y visualizaciones avanzadas
- ✅ Gestión de múltiples datasets
- ✅ Exportación de resultados CSV

---

## 🆘 Soporte y Contacto

Para reportar problemas o solicitar nuevas funcionalidades:

1. **Crear Issue**: En el repositorio de GitHub
2. **Email**: Contactar al desarrollador
3. **Documentación**: Revisar `/docs/` para detalles técnicos

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

---

**🎉 ¡Listo para clasificar textos ODS! 🌍**