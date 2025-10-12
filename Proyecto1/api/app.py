# api/app.py
from fastapi import FastAPI, Request
from api.routes import predict, train, retrain, files, evaluate
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.logging import get_logger  
import time, json, os

app = FastAPI(title="ODS Classifier API", version="2.0.0")
logger = get_logger("api")

# enchufa módulos de endpoints (routers)
# /files/*
app.include_router(files.router) 
 # /train/*   
app.include_router(train.router)  
# /retrain/* 
app.include_router(retrain.router)  
# /predict/*
app.include_router(predict.router)  
# /evaluate/*
app.include_router(evaluate.router) 

# ----------------------------------------------------------------------
# Logging Middleware (detallado)
# ----------------------------------------------------------------------
ALLOWED_PREFIXES = {"/predict", "/train", "/retrain", "/evaluate", "/files"}
SKIP_PATHS = {"/docs", "/openapi.json", "/redoc", "/favicon.ico"}
MAX_BODY_CHARS = 1000 
def _preview_bytes(b: bytes) -> str:
    if not b:
        return "<empty>"
    s = b.decode("utf-8", errors="replace")
    return s if len(s) <= MAX_BODY_CHARS else s[:MAX_BODY_CHARS] + f"... <truncated {len(s)-MAX_BODY_CHARS} chars>"


@app.middleware("http")
async def log_requests(request: Request, call_next):
    path = request.url.path
    method = request.method

    # ignora swagger/estáticos
    if path in SKIP_PATHS or any(path.startswith(p) for p in ("/static", "/apple-touch-icon")):
        return await call_next(request)

    # solo rutas de negocio
    business = any(path.startswith(p) for p in ALLOWED_PREFIXES)

    start = time.perf_counter()

    # --- request body (siempre intentamos leer; si no es JSON igual mostramos preview) ---
    req_body_txt = None
    raw_req = b""
    try:
        raw_req = await request.body()
        if raw_req:
            req_body_txt = _preview_bytes(raw_req)
        else:
            req_body_txt = "<empty>"
        # reinyecta el body para que el endpoint pueda leerlo
        async def receive():
            return {"type": "http.request", "body": raw_req}
        request = Request(request.scope, receive)
    except Exception:
        req_body_txt = "<error reading request body>"

    if business:
        logger.info(f"{method} {path} REQ={req_body_txt}")
    else:
        logger.info(f"{method} {path}")

    # --- ejecutar endpoint y capturar respuesta ---
    response = await call_next(request)
    dur_ms = round((time.perf_counter() - start) * 1000, 2)

    # siempre capturamos el body de la respuesta y reconstruimos
    resp_preview = ""
    try:
        body_chunks = []
        async for chunk in response.body_iterator:
            body_chunks.append(chunk)
        body_bytes = b"".join(body_chunks)
        resp_preview = _preview_bytes(body_bytes)

        # reconstruir respuesta para no romper el flujo
        response = Response(
            content=body_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
    except Exception:
        resp_preview = "<error reading response body>"

    if business:
        logger.info(f"{method} {path} → {response.status_code} | {dur_ms}ms RESP={resp_preview}")
    else:
        logger.info(f"{method} {path} → {response.status_code} | {dur_ms}ms")

    return response




#---------------
# ENDPOINTS 
#--------------

# ruta básica de prueba
@app.get("/health")
def health():
    return {"status": "ok"}