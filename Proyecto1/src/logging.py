import os, logging
from logging.handlers import RotatingFileHandler


BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # raíz del proyecto
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")       # logs dentro de /data
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name="app", level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:  # evitar duplicados al recargar
        return logger
    logger.setLevel(level)

    # archivo con rotación
    fh = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # salida en consola
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger