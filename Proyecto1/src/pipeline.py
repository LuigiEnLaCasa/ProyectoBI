"""
Pipeline de procesamiento y clasificación de texto:
- Función Basica de pipeline
- GridSearch para optimizar hiperparámetros
- Funciones para entrenar, predecir, guardar y cargar modelos

"""

# ----------------------------------------------------------------------
# Librerías
# ----------------------------------------------------------------------
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import glob
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from src.preprocess import PreprocesadorTexto
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from datetime import datetime
import numpy as np


# ----------------------------------------------------------------------
# Definimos el pipeline
# ----------------------------------------------------------------------


def construir_pipeline(alpha=0.1):
    """Construye el pipeline completo: limpieza, vectorización , modelo"""
    return Pipeline([
        ("preprocesamiento", PreprocesadorTexto()), 
        ("vectorizador", CountVectorizer(token_pattern=r"(?u)\b[a-z]{2,}\b", min_df=3, max_df=0.90, ngram_range=(1,2))),
        ("clasificador", MultinomialNB(alpha=alpha)) 
    ])

def entrenar_con_grid(X, y):
    pipe = construir_pipeline()
    params = {"clasificador__alpha": [0.05, 0.1, 0.3, 0.5, 1.0], "vectorizador__min_df": [2,3,5], "vectorizador__max_df": [0.8,0.9],}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    gs = GridSearchCV(pipe, params, scoring="f1_macro", cv=cv, n_jobs=-1, refit=True)
    gs.fit(X, y)
    return gs.best_estimator_, gs.best_params_, gs.best_score_


# ----------------------------------------------------------------------
# Funciones funcionales jajaj. (POSIBLE FUENTE DE ERRORES: GUARDAR EL MODELO Y VISUALIZARLO.)
# ----------------------------------------------------------------------

# Permitirá meterle datos para entrenar el modelo
def entrenar_modelo(X, y, alpha=0.1):
    pipe = construir_pipeline(alpha)
    pipe.fit(X, y)
    return pipe

# Permitirá hacer que nuestro modelo intente predecir
def predecir(pipe, textos):
    return pipe.predict(textos)

# Retornará la info de probabilidades con la que decidió
def probabilidades(pipe, textos):
    return pipe.predict_proba(textos)

# Guarda el modleo para no tener que entrenarlo cada vez
def guardar_modelo(pipe, ruta_base="models/model_nb"):
    """Guarda el modelo con timestamp y devuelve la ruta final."""
    from datetime import datetime
    os.makedirs(os.path.dirname(ruta_base), exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"{ruta_base}_{timestamp}.pkl"
    joblib.dump(pipe, ruta)
    print(f"-> Modelo guardado en: {ruta}")
    return ruta

# muestra los modelos que hay guardados
def listar_modelos(ruta_base="models/model_nb"):
    """Lista todos los modelos guardados disponibles."""
    modelos = sorted(glob.glob(f"{ruta_base}_*.pkl"))
    if not modelos:
        print("-> No hay modelos guardados aún.")
    else:
        print("\nModelos disponibles:")
        for i, m in enumerate(modelos, 1):
            print(f"{i}. {m}")
    return modelos

# carga el modelo seleccionado
def cargar_modelo(ruta):
    """Carga el modelo seleccionado por el usuario."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el modelo: {ruta}")
    print(f"-> Cargando modelo desde: {ruta}")
    return joblib.load(ruta)

# Devuelve etiquetas y nivel de confianza de forma legible.
def visualizar_resultado(pipe, textos):
   
    y_pred = pipe.predict(textos)
    probs = pipe.predict_proba(textos)
    conf = probs.max(axis=1)
    return [
        {"texto": t, "prediccion": int(lbl), "confianza": round(float(cf), 3)}
        for t, lbl, cf in zip(textos, y_pred, conf)
    ]


