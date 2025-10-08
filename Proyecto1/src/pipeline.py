"""
Pipeline de procesamiento y clasificación de texto:
- Función Basica
- Carga
- Entrenamiento
- Predicción

"""

# ----------------------------------------------------------------------
# Librerías
# ----------------------------------------------------------------------

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from src.preprocess import PreprocesadorTexto