import os, shutil
import pandas as pd
from typing import List, Tuple, Optional, Dict
from src.pipeline import entrenar_modelo, entrenar_con_grid, guardar_modelo


# ----------------------------------------------------------------------
# Importación de archivos y textos
# ----------------------------------------------------------------------

# Transforma un excel o csv en un dataframe
def read_file(path:str):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx",".xls"):
        return pd.read_excel(path)
    elif ext == ".csv":
        return pd.read_csv(path)
    raise ValueError("Formato no soportado. Usa .csv o .xlsx")

# agarra las columnas de interés texto y label de un dataset que puede ser grande 
def prepare_data(df, text_col:str, label_col:str):
    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(f"Columnas no encontradas. Columnas disponibles: {list(df.columns)}")
    
    df = df.dropna(subset=[text_col, label_col])
    X = df[text_col].astype(str).tolist()
    Y = df[label_col].tolist()
    return X,Y



