# scripts/quick_train.py
import pandas as pd
from src.pipeline import entrenar_modelo, entrenar_con_grid, guardar_modelo

# === EDITA ESTAS 3 LÍNEAS SEGÚN TU ARCHIVO ===
FILE = "data/Datos_etapa1.xlsx"   # o "data/etapa1.csv"
TEXT_COL = "textos"          # nombre de la columna con el texto
LABEL_COL = "labels"           # nombre de la columna con la etiqueta (1/3/4)

# === LECTURA DEL ARCHIVO ===
if FILE.lower().endswith((".xlsx", ".xls")):
    df = pd.read_excel(FILE)
elif FILE.lower().endswith(".csv"):
    df = pd.read_csv(FILE)  # agrega sep/encoding si tu CSV lo necesita
else:
    raise ValueError("Formato no soportado. Usa .csv o .xlsx")

X = df[TEXT_COL].fillna("").astype(str).tolist()
y = df[LABEL_COL].tolist()

# === ENTRENA (elige una de las dos variantes) ===

USE_GRID = True   # pon False si quieres entrenar rápido sin grid

if USE_GRID:
    print("Entrenando con GridSearchCV…")
    pipe, best_params, best_score = entrenar_con_grid(X, y)
    print("Mejores parámetros:", best_params, "| F1_macro:", round(best_score, 4))
else:
    print("Entrenando con alpha=0.1…")
    pipe = entrenar_modelo(X, y, alpha=0.1)

# === GUARDA EL MODELO (.pkl con timestamp en /models) ===
ruta = guardar_modelo(pipe)
print("Modelo guardado en:", ruta)
print("Listo para usar en /predict")