# api/app.py
from fastapi import FastAPI
from api.routes import predict, train, retrain, files, evaluate
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.logging import get_logger  


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

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Registra todas las peticiones entrantes y su resultado"""
    logger.info(f" {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} → {response.status_code}")
    return response


#---------------
# ENDPOINTS 
#--------------

# ruta básica de prueba
@app.get("/health")
def health():
    return {"status": "ok"}



