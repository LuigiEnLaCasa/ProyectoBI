@echo off
cls
echo ============================================
echo    🌍 ODS CLASSIFIER - STARTUP SCRIPT 🌍
echo ============================================
echo.

REM Verificar si estamos en el directorio correcto
if not exist "api\app.py" (
    echo ❌ ERROR: Debes ejecutar este script desde la carpeta Proyecto1
    echo 📁 Navega a la carpeta Proyecto1 y ejecuta de nuevo
    pause
    exit /b 1
)

echo ✅ Directorio correcto detectado: Proyecto1
echo.

echo [1/4] 🔍 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo [2/4] 📦 Instalando/Verificando dependencias...
echo    (Esto puede tomar unos minutos la primera vez)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo [3/4] 🚀 Iniciando API Backend en segundo plano...
start "🌐 ODS API Backend" cmd /c "cd /d %cd% && uvicorn api.app:app --reload --host 127.0.0.1 --port 8000"

echo [4/4] ⏳ Esperando a que la API se inicie...
echo    (Verificando conexión en 8 segundos...)
timeout /t 8 > nul

echo 🌐 Iniciando aplicación Streamlit...
echo.
echo ============================================
echo    ✨ APLICACION WEB DISPONIBLE EN:
echo    
echo    🖥️  LOCAL:    http://localhost:8501
echo    📡 API:      http://127.0.0.1:8000
echo    📖 DOCS:     http://127.0.0.1:8000/docs
echo    
echo ============================================
echo.
echo 💡 INSTRUCCIONES:
echo    - La aplicación se abrirá automáticamente
echo    - Para cerrar: Ctrl+C o cerrar esta ventana  
echo    - Ambos servicios se ejecutan simultáneamente
echo.

REM Abrir navegador automáticamente
timeout /t 3 > nul
start http://localhost:8501

streamlit run streamlit_app.py --server.port 8501

echo.
echo ✅ Aplicación cerrada correctamente
pause