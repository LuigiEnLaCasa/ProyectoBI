import os, shutil
import pandas as pd
from typing import List, Tuple, Optional, Dict
from src.pipeline import entrenar_modelo, guardar_modelo


# ----------------------------------------------------------------------
# Este archivo sirve para exponer herramientas que permitan entrenar en train.py
# ----------------------------------------------------------------------

# Transforma un excel o csv en un dataframe
def read_file(path:str):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx",".xls"):
        return pd.read_excel(path)
    elif ext == ".csv":
        return pd.read_csv(path)
    raise ValueError("Formato no soportado. Usa .csv o .xlsx")

# Agarra las columnas de interés texto y label de un dataset que puede ser grande 
def prepare_data(df, text_col:str, label_col:str):
    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(f"Columnas no encontradas. Columnas disponibles: {list(df.columns)}")
    df = df.dropna(subset=[text_col, label_col])
    X = df[text_col].astype(str).tolist()
    Y = df[label_col].tolist()
    return X,Y

# ----------------------------------------------------------------------
# Entrenamiento del modelo  (Diferentes casos)
# ----------------------------------------------------------------------

#Esto es para el entrenamiento inicial de un archivo.. desde 0. 
def train_from_file(file_path: str, text_col: str, label_col: str):
    df = read_file(file_path)
    X, y = prepare_data(df, text_col, label_col)
    pipe, best_params, best_score = entrenar_modelo(X, y)
    
    # metadatos para el dump y referencia del modelo
    meta = {
        "dataset_path": file_path,
        "text_col": text_col,
        "label_col": label_col,
        "n_samples": len(y),
        "params": best_params,
        "score": {"f1_macro_cv": float(best_score)},
    }

    ruta = guardar_modelo(pipe, metadata=meta)
    print(f"-> Modelo guardado en: {ruta}")
    return ruta, meta


# Esto te permite subir un par de textos para re-entrenar el modelo. 
def retrain_with_samples(base_file_path,text_col,label_col,nuevos_textos,nuevos_labels):
    if len(nuevos_labels)!= len(nuevos_textos):
        raise ValueError("textos y labels deben tener la misma longitud.")
    
    df_base = read_file(base_file_path)
    X_base,Y_base = prepare_data(df_base,text_col,label_col)

    X = X_base + list(map(str, nuevos_textos))
    Y = Y_base + list(nuevos_labels)

    pipe, best_params, best_score = entrenar_modelo(X, Y)
    meta = { "dataset_base": base_file_path,"text_col": text_col,"label_col": label_col,"n_base": len(Y_base),"n_new": len(nuevos_labels),"n_total": len(Y), "params": best_params,"score": {"f1_macro_cv": float(best_score)}}
    ruta = guardar_modelo(pipe,ruta_base="models/retrained/model_nb",metadata = meta)
    return ruta,meta

# Esto te permite cargar un CSV o un excel para re-entrenar los modelos
def retrain_with_file():
    return 0