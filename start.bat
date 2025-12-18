@echo off
echo ============================================================
echo TeeVee Launcher
echo ============================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python de python.org
    pause
    exit /b 1
)

echo Iniciando TeeVee...
echo.

python start.py

pause
