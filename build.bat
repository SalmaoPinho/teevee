@echo off
echo ============================================================
echo TeeVee - Build Script
echo ============================================================
echo.

REM Verifica se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
)

echo.
echo Construindo executavel...
echo.

REM Constrói o executável usando o spec file
pyinstaller teevee.spec --clean

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao construir executavel!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Build concluido com sucesso!
echo ============================================================
echo.
echo Executavel criado em: dist\TeeVee.exe
echo.
pause
