"""
Preprocesamiento de texto para ODS:
- lower
- quitar acentos y caracteres raros (áéíóúñ -> aeioun)
- limpiar puntuación/caracteres raros (conserva %, / y -)
- tokenizar (split por espacios)
- eliminar stopwords (NLTK español)
- stemming (Snowball en español)
- join a string final
"""

# ----------------------------------------------------------------------
# Librerías
# ----------------------------------------------------------------------

import unicodedata as unicodedata
import re
import nltk 
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.base import BaseEstimator, TransformerMixin

try:
    from nltk.corpus import stopwords
    STOPWORDS_ES = set(stopwords.words("spanish"))
except LookupError:
    import nltk
    nltk.download("stopwords")
    from nltk.corpus import stopwords
    STOPWORDS_ES = set(stopwords.words("spanish"))

# ----------------------------------------------------------------------
# Funcioncitas atomizadas y lindas
# ----------------------------------------------------------------------

# Pasamos todo a lowercase
def eliminar_mayusculas(texto):
    return texto.lower()

# Quitamos tildes y cualquier otro tipo de acento raro. 
def eliminar_acentos(texto):
    "esta función es más robusta que usar regex porque maneja caracteres raros raros (ñ, ü, etc)"
    textico = unicodedata.normalize("NFD",texto)
    limpio = "".join(c for c in textico if unicodedata.category(c) != "Mn")
    return limpio

# Limpia puntuación (conserva % / -)
# Usamos variables compiladas para eficiencia
PUNCT = re.compile(r"[^a-z0-9/\-\s%]", re.I)
SPACES = re.compile(r"\s+")
def limpiar_puntuacion(texto):
    texto = PUNCT.sub(" ", texto)
    return SPACES.sub(" ", texto).strip()


# Tokeniza (split por espacios)
def tokenizar(texto):
    return texto.split()

# Elimina stopwords (NLTK español)
STEMMER_ES = SnowballStemmer("spanish")
def eliminar_stopwords(texto):
    nuevo_texto = [palabra for palabra in texto if palabra not in STOPWORDS_ES]
    return nuevo_texto

# Pasamos las palabras a su raíz
# Función grande que hace todo el preprocesamiento
# Usamos variables globales para eficiencia (no cargar siempre la info del stemmer y stopwords)

def stemmear_texto(tokens):
    lematizados = [STEMMER_ES.stem(token) for token in tokens]
    return lematizados

# Como los vectorizadores (Bow , TF-IDF etc.) de scikitlearn esperan una línea de texto string, toca unir los tokens limpios
def join_tokens(tokens):
    return " ".join(tokens)


# ----------------------------------------------------------------------
# Función grande que hace todo el preprocesamiento
# ----------------------------------------------------------------------

def preprocesar_texto(texto):

    texto = eliminar_mayusculas(texto)
    texto = eliminar_acentos(texto)
    texto = limpiar_puntuacion(texto)
    tokens = tokenizar(texto)
    tokens = [t for t in tokens if t not in STOPWORDS_ES]
    tokens = [STEMMER_ES.stem(t) for t in tokens]
    return join_tokens(tokens)

def preprocesar_varios(textos):
    return [preprocesar_texto(t) for t in textos]



# Caso 1: texto normal
texto1 = "¡La Educación pública en Colombia es esencial para la igualdad!"
print("Entrada 1:", texto1)
print("Salida 1:", preprocesar_texto(texto1))
print("-" * 50)

# Caso 2: texto con acentos, números y símbolos
texto2 = "El 50% de los niños aún no tienen acceso a salud básica - ¡urgente!"
print("Entrada 2:", texto2)
print("Salida 2:", preprocesar_texto(texto2))


# ----------------------------------------------------------------------
# Masticar para el pipeline de sklearn
# ----------------------------------------------------------------------


class PreprocesadorTexto(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self
    def transform(self, X):   return [preprocesar_texto(t) for t in X]

