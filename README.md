**Comando para ejecutar la API**

- Activar entorno virtual (si no está activo):  
  source envQueSea/bin/activate  
- Ejecutar la API con recarga automática:  
  uvicorn api.app:app --reload  
- Acceder a la interfaz de prueba (Swagger):  
  http://127.0.0.1:8000/docs  

---

# ODS Classifier API

Proyecto de clasificación de textos asociados a los Objetivos de Desarrollo Sostenible (ODS).  
Implementa un pipeline de procesamiento de texto, entrenamiento de modelos, reentrenamiento incremental, evaluación y despliegue mediante una API REST construida con FastAPI.

---

## Estructura general del proyecto

**src/**  
Contiene la lógica principal:  
- **preprocess.py:** Limpieza, normalización y tokenización del texto.  
- **pipeline.py:** Construcción del pipeline completo con CountVectorizer y MultinomialNB, además de funciones para entrenar, predecir, guardar y cargar modelos.  
- **train_utils.py:** Funciones para preparar datos, leer archivos, entrenar desde CSV/Excel y reentrenar modelos con muestras adicionales.  
- **evaluate.py:** Carga un modelo y calcula métricas de rendimiento sobre un dataset de prueba.  
- **logging.py:** Configura el registro de logs (ubicados en data/logs/).  

**api/**  
Contiene los módulos de rutas que definen los endpoints:  
- **app.py:** Archivo principal que crea la aplicación FastAPI, registra los routers y configura el middleware de logging.  
- **routes/files.py:** Permite subir y listar archivos en la carpeta /data.  
- **routes/predict.py:** Endpoint para realizar predicciones con modelos entrenados.  
- **routes/train.py:** Entrenamiento de modelos a partir de archivos CSV o Excel.  
- **routes/retrain.py:** Reentrenamiento de modelos agregando nuevas muestras.  
- **routes/evaluate.py:** Evalúa un modelo cargado con un dataset de prueba.  

**data/**  
Carpeta donde se almacenan los archivos de entrenamiento, pruebas y logs:  
- data/train/ contiene datasets de entrenamiento.  
- data/test/ contiene datasets de prueba.  
- data/logs/ guarda los registros generados por la API.  

**models/**  
Almacena los modelos entrenados en formato .pkl junto con su metadata.  

**docs/**  
Contiene la documentación y entregables del proyecto:  
- Enunciado oficial de la Etapa 2.  
- Notebook de la Etapa 1 en formato .ipynb.  
- Notebook de la Etapa 1 exportado en formato PDF.  
- Documento de sustentación con el resumen técnico y la descripción de resultados.  

---

## Endpoints principales

**1. /predict**  
- Método: POST  
- Descripción: Realiza una predicción sobre uno o varios textos usando el modelo seleccionado.  
- Entrada (JSON):  
  - textos: lista de cadenas de texto.  
  - modelo_path: nombre del modelo .pkl a utilizar.  
- Salida: Lista con texto, predicción (número de ODS) y nivel de confianza.  

**2. /train**  
- Método: POST  
- Descripción: Entrena un modelo nuevo a partir de un archivo .csv o .xlsx.  
- El modelo se guarda automáticamente en la carpeta /models con timestamp.  

**3. /retrain**  
- Método: POST  
- Descripción: Reentrena un modelo existente concatenando nuevas muestras a su dataset base.  
- Entrada: textos y labels nuevos (listas JSON).  
- Genera un nuevo modelo con metadata actualizada.  

**4. /evaluate**  
- Método: POST  
- Descripción: Evalúa un modelo .pkl existente usando un archivo de test.  
- Calcula métricas de rendimiento: accuracy, precision, recall y F1-score (macro, micro, weighted).  

**5. /files**  
- /files/upload: Subir archivos al directorio data/.  
- /files/list: Listar los archivos existentes en data/.  
- /files/models: Listar los modelos guardados en models/.  

**6. /health**  
- Verifica el estado de la API.  
- Devuelve { "status": "ok" } si el servidor está activo.  

---

## Logging y monitoreo

Cada petición HTTP registrada en la API se almacena en data/logs/api.log.  
El middleware de logging:  
- Registra método, ruta, estado HTTP, duración y cuerpo JSON de la petición y respuesta.  
- Ignora rutas estáticas y la interfaz /docs.  
- Muestra cuerpos recortados si exceden el tamaño máximo configurado.  

Esto permite rastrear fácilmente el comportamiento de los usuarios y depurar fallos durante las pruebas o despliegues.

---

## Flujo general de uso

1. Subir el dataset inicial en /data/ mediante /files/upload.  
2. Entrenar el modelo con /train.  
3. Consultar los modelos disponibles con /files/models.  
4. Realizar predicciones usando /predict.  
5. Si se obtienen nuevos datos, reentrenar el modelo con /retrain.  
6. Evaluar el rendimiento con /evaluate.  

---

## Tecnología

- Lenguaje: Python 3.12  
- Framework: FastAPI  
- Modelos: Scikit-learn (MultinomialNB)  
- Preprocesamiento: Limpieza personalizada con PreprocesadorTexto.  
- Persistencia: joblib para almacenar pipelines y metadata.  
- Métricas: Precision, Recall, F1-score, Accuracy.  

---

## Consideraciones finales

- Todos los modelos se guardan con timestamp y metadata (ruta del dataset, número de muestras, parámetros y métricas).  
- El reentrenamiento utiliza un esquema batch incremental, que combina datos antiguos y nuevos para mantener la estabilidad del modelo.  
- Los logs permiten auditar cada petición y resultado, asegurando trazabilidad completa del sistema.  
- La API está diseñada para integrarse fácilmente con una interfaz web o móvil en fases posteriores del proyecto.  
- La carpeta docs contiene todos los documentos de referencia necesarios para evaluación y sustentación.