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


# ----------------------------------------------------------------------
# Funciones funcionales jajaj. (POSIBLE FUENTE DE ERRORES: GUARDAR EL MODELO Y VISUALIZARLO.)
# Esto es una herrameinta para solo meterle datos y que entrene el modelo solito 
# ----------------------------------------------------------------------

def entrenar_modelo(X, y):
    pipe = construir_pipeline()
    params = {"clasificador__alpha": [0.05, 0.1, 0.3, 0.5, 1.0],}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    gs = GridSearchCV(pipe, params, scoring="f1_macro", cv=cv, n_jobs= 1, refit="f1_macro")
    gs.fit(X, y)
    return gs.best_estimator_, gs.best_params_, gs.best_score_


# Permitirá hacer que nuestro modelo intente predecir
def predecir(pipe, textos):
    return pipe.predict(textos)

# Retornará la info de probabilidades con la que decidió
def probabilidades(pipe, textos):
    return pipe.predict_proba(textos)

# Guarda el modelo para no tener que entrenarlo cada vez
def guardar_modelo(pipe, ruta_base="models/model_nb", metadata: dict | None = None):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta = f"{ruta_base}_{ts}.pkl"
    os.makedirs(os.path.dirname(ruta_base), exist_ok=True)
    bundle = {"model": pipe, "metadata": metadata or {}}
    joblib.dump(bundle, ruta)
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

def cargar_modelo(ruta="models/model_nb.pkl"):
    obj = joblib.load(ruta)
    if isinstance(obj, dict) and "model" in obj:
        return obj  # {'model': pipe, 'metadata': {...}}
    # retrocompatibilidad: era solo el pipeline
    return {"model": obj, "metadata": {}}

# Devuelve etiquetas y nivel de confianza de forma legible.
def visualizar_resultado(pipe, textos):
   
    y_pred = pipe.predict(textos)
    probs = pipe.predict_proba(textos)
    conf = probs.max(axis=1)
    return [
        {"texto": t, "prediccion": int(lbl), "confianza": round(float(cf), 3)}
        for t, lbl, cf in zip(textos, y_pred, conf)
    ]


