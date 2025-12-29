@echo off
REM Script alternativo de instalação de dependências
REM Use este script se 'pip install -r requirements.txt' falhar

echo ========================================
echo Instalando dependencias do TeeVee
echo ========================================
echo.

echo [1/7] Instalando pygame...
pip install pygame==2.6.1
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar pygame
    pause
    exit /b 1
)

echo [2/7] Instalando psutil...
pip install psutil>=5.9.0
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar psutil
    pause
    exit /b 1
)

echo [3/7] Instalando requests...
pip install requests>=2.31.0
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar requests
    pause
    exit /b 1
)

echo [4/7] Instalando numpy...
pip install numpy>=1.24.0
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar numpy
    pause
    exit /b 1
)

echo [5/7] Instalando mutagen...
pip install mutagen>=1.47.0
if %errorlevel% neq 0 (
    echo AVISO: Falha ao instalar mutagen (necessario para metadados de musica)
)

echo [6/7] Instalando ollama (opcional)...
pip install ollama>=0.1.0
if %errorlevel% neq 0 (
    echo AVISO: Falha ao instalar ollama (opcional)
)

echo [7/7] Instalando Pillow...
pip install Pillow>=10.0.0
if %errorlevel% neq 0 (
    echo AVISO: Falha ao instalar Pillow (opcional)
)

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
pause
