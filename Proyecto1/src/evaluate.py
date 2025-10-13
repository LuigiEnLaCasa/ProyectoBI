import os
from typing import Dict
from src.train_utils import read_file, prepare_data
from src.pipeline import cargar_modelo, predecir
from sklearn.metrics import accuracy_score,f1_score,precision_score, recall_score


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR   = os.path.join(PROJECT_ROOT, "models")
DATA_DIR     = os.path.join(PROJECT_ROOT, "data")
DATA_TEST    = os.path.join(DATA_DIR, "test")




# La idea es cargar un modelo .pkl con un archivo csv o excel. para evaluar métricas de rendimiento. 
def evaluate_model_on_file(model_name,file_name,text_col, label_col):
    # Manejar rutas con subcarpetas (ej: retrained/model_nb_2025-10-13.pkl)
    if model_name.endswith('.pkl'):
        model_path = os.path.join(MODELS_DIR, model_name)
    else:
        model_path = os.path.join(MODELS_DIR, f"{model_name}.pkl")
    
    bundle = cargar_modelo(model_path)
    
    pipe = bundle["model"]

    file_path = os.path.join(DATA_TEST, file_name)
    df = read_file(file_path)
    X,y = prepare_data(df,text_col,label_col)
    y_pred = predecir(pipe,X)


    acc = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average="macro")
    recall = recall_score(y, y_pred, average="macro")
    f1_macro = f1_score(y, y_pred, average="macro")
    f1_micro = f1_score(y, y_pred, average="micro")
    f1_weighted = f1_score(y, y_pred, average="weighted")


    resultados = {
        "n_samples": len(y),
        "accuracy": float(acc),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "f1_macro": float(f1_macro),
        "f1_micro": float(f1_micro),
        "f1_weighted": float(f1_weighted)
    }
    return resultados
