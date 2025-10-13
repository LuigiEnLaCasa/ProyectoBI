# Aplicación Web ODS Classifier - Sección 3

## 🌍 Descripción del Proyecto

Esta aplicación web desarrollada con **Streamlit** cumple con los requisitos de la **Sección 3** del proyecto de analítica de textos. Permite a los usuarios interactuar de manera intuitiva con el modelo de clasificación de Objetivos de Desarrollo Sostenible (ODS).

## 🎯 Características Implementadas

### ✅ Requisitos Cumplidos (Sección 3)

1. **Aplicación Web Interactiva**: Interface desarrollada con Streamlit
2. **Predicción con Probabilidades**: Muestra tanto la predicción como el nivel de confianza
3. **Re-entrenamiento del Modelo**: Permite agregar nuevos ejemplos y reentrenar
4. **Gestión de Archivos**: Subida y listado de datasets y modelos

### 🔧 Funcionalidades Principales

#### 🔮 **Módulo de Predicción**
- Clasificación de texto individual
- Procesamiento de múltiples textos
- Carga de archivos CSV para clasificación masiva
- Visualización de confianza con barras gráficas
- Mapeo completo de los 17 ODS

#### 🔄 **Módulo de Re-entrenamiento**
- Interface para agregar nuevos ejemplos
- Selección del ODS correspondiente
- Visualización de ejemplos agregados
- Ejecución de re-entrenamiento incremental
- Feedback en tiempo real del proceso

#### 📊 **Módulo de Análisis**
- Gráficos de distribución de predicciones
- Histogramas de niveles de confianza
- Tablas resumen de resultados
- Métricas visuales interactivas

#### 📋 **Módulo de Gestión**
- Listado de modelos disponibles
- Subida de nuevos archivos de entrenamiento
- Selección de modelo activo
- Monitoreo del estado de la API

## 🚀 Instalación y Ejecución

### Método 1: Ejecución Automática
```bash
# Desde la carpeta Proyecto1
./start_app.bat
```

### Método 2: Ejecución Manual
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar API (Terminal 1)
uvicorn api.app:app --reload

# 3. Iniciar Streamlit (Terminal 2)
streamlit run streamlit_app.py
```

## 🌐 URLs de Acceso

- **Aplicación Web**: http://localhost:8501
- **API Swagger**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 👥 Usuarios Objetivo y Casos de Uso

### **Perfil de Usuario: Analista de Sostenibilidad**
- **Rol**: Profesional que clasifica textos relacionados con ODS
- **Conexión con el negocio**: Evaluación de cumplimiento de objetivos sostenibles
- **Proceso apoyado**: Clasificación automática de documentos, reportes y propuestas
- **Importancia**: Automatiza el proceso manual de categorización

### **Casos de Uso Principales**

1. **Clasificación de Documentos Corporativos**
   - Evaluar reportes de sostenibilidad
   - Categorizar propuestas de proyectos
   - Analizar comunicaciones institucionales

2. **Re-entrenamiento Adaptativo**
   - Mejorar precisión con ejemplos específicos del dominio
   - Adaptar el modelo a terminología organizacional
   - Incorporar nuevos patrones de texto

3. **Monitoreo y Evaluación**
   - Seguimiento de métricas de clasificación
   - Análisis de distribución de ODS en documentos
   - Validación de resultados del modelo

## 💻 Recursos Informáticos Requeridos

### **Hardware Mínimo**
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Almacenamiento**: 1 GB disponible
- **Red**: Conexión a internet para dependencias

### **Hardware Recomendado**
- **CPU**: 4 cores, 2.5 GHz+
- **RAM**: 8 GB+
- **Almacenamiento**: 5 GB+ (para datasets grandes)
- **Red**: Conexión estable

### **Software**
- **SO**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Python**: 3.8 - 3.12
- **Navegador**: Chrome, Firefox, Safari (versiones recientes)

## 🏢 Integración Organizacional

### **Integración con Procesos de Negocio**
1. **Flujo de Documentos**: Integración con sistemas de gestión documental
2. **Workflow de Aprobación**: Clasificación automática antes de revisión humana
3. **Reportería**: Generación de dashboards de cumplimiento ODS
4. **Auditoría**: Trazabilidad completa de clasificaciones

### **Conexión con Sistemas Existentes**
- **API REST**: Fácil integración con sistemas enterprise
- **Formato JSON**: Compatible con la mayoría de plataformas
- **Logs detallados**: Integración con sistemas de monitoreo
- **Escalabilidad**: Arquitectura preparada para crecimiento

### **Disposición del Usuario Final**
- **Interface intuitiva**: Diseño familiar tipo dashboard
- **Feedback inmediato**: Resultados en tiempo real
- **Capacitación mínima**: Interface auto-explicativa
- **Soporte multi-dispositivo**: Accesible desde cualquier dispositivo

## ⚠️ Riesgos y Consideraciones

### **Riesgos Técnicos**
1. **Disponibilidad de API**: Dependencia del servicio backend
   - *Mitigación*: Implementar health checks y reconexión automática
   
2. **Precisión del Modelo**: Posibles clasificaciones incorrectas
   - *Mitigación*: Mostrar nivel de confianza y permitir corrección
   
3. **Escalabilidad**: Rendimiento con grandes volúmenes
   - *Mitigación*: Procesamiento por lotes y optimización de consultas

### **Riesgos Operacionales**
1. **Dependencia de Conexión**: Requiere conectividad para funcionar
   - *Mitigación*: Implementar modo offline para funciones básicas
   
2. **Curva de Aprendizaje**: Adaptación de usuarios a nueva herramienta
   - *Mitigación*: Documentación completa y interface intuitiva
   
3. **Calidad de Datos**: Resultados dependen de calidad del input
   - *Mitigación*: Validaciones de entrada y guías de uso

### **Riesgos de Seguridad**
1. **Exposición de Datos**: Textos sensibles procesados por el sistema
   - *Mitigación*: Implementar HTTPS y políticas de retención de datos
   
2. **Acceso no Autorizado**: Uso indebido de la aplicación
   - *Mitigación*: Implementar autenticación y logs de auditoría

## 🔧 Arquitectura Técnica

### **Stack Tecnológico**
- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI
- **ML Pipeline**: Scikit-learn
- **Visualizaciones**: Plotly
- **Comunicación**: REST API (JSON)

### **Flujo de Datos**
1. Usuario ingresa texto → Streamlit
2. Streamlit envía petición → FastAPI
3. FastAPI procesa texto → Pipeline ML
4. Pipeline retorna predicción → FastAPI
5. FastAPI envía respuesta → Streamlit
6. Streamlit muestra resultado → Usuario

### **Persistencia**
- **Modelos**: Archivos .pkl en filesystem
- **Logs**: Archivos de texto estructurados
- **Configuración**: Variables de entorno y archivos config

## 📈 Métricas y Monitoreo

### **KPIs de Rendimiento**
- **Tiempo de respuesta**: < 2 segundos por predicción
- **Disponibilidad**: > 99% uptime
- **Precisión**: Nivel de confianza promedio > 70%

### **Métricas de Uso**
- **Clasificaciones por día**: Contador de predicciones
- **Re-entrenamientos**: Frecuencia de mejoras del modelo
- **Usuarios activos**: Sesiones únicas por período

### **Alertas y Notificaciones**
- **API no disponible**: Notificación inmediata
- **Baja confianza**: Alertas cuando confianza < 50%
- **Errores del modelo**: Logs detallados para debugging

---

## 📋 Checklist de Implementación ✅

- [x] Interface web funcional con Streamlit
- [x] Integración completa con API REST
- [x] Predicción con niveles de confianza
- [x] Módulo de re-entrenamiento interactivo
- [x] Visualizaciones y análisis de resultados
- [x] Gestión de modelos y archivos
- [x] Documentación completa
- [x] Script de inicio automatizado
- [x] Manejo de errores y validaciones
- [x] Interface responsiva y user-friendly

**✅ Sección 3 completamente implementada y funcional**