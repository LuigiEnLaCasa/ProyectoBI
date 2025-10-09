# api/app.py
from fastapi import FastAPI
from api.routes import predict, train, retrain, files

app = FastAPI(title="ODS Classifier API", version="2.0.0")

# enchufa módulos de endpoints
# /files/*
app.include_router(files.router) 
 # /train/*   
app.include_router(train.router)  
# /retrain/* 
app.include_router(retrain.router)  
# /predict/*
app.include_router(predict.router)  

#---------------
# ENDPOINTS 
#--------------

# ruta básica de prueba
@app.get("/health")
def health():
    return {"status": "ok"}