@echo off
REM ==========================================================================
REM  KDD PMO Copilot - Instalador interactivo para Windows
REM  Uso: doble clic en este fichero. Te guia paso a paso.
REM ==========================================================================

setlocal enabledelayedexpansion
title KDD PMO Copilot - Instalador
color 0B

echo.
echo  ===================================================================
echo                  KDD PMO Copilot - Instalador
echo  ===================================================================
echo.
echo   Este asistente va a:
echo     [1] Comprobar que tienes Python y Git instalados
echo     [2] Descargar el repositorio del proyecto
echo     [3] Crear un entorno virtual aislado
echo     [4] Instalar las dependencias necesarias
echo     [5] Pedirte las credenciales (.env) de forma guiada
echo     [6] Arrancar la aplicacion
echo.
echo  ===================================================================
echo.
pause

REM ── [1] Comprobar Python ──────────────────────────────────────────
echo.
echo  [1/6] Comprobando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python no esta instalado o no esta en el PATH.
    echo.
    echo  SOLUCION:
    echo     1) Descargate Python desde: https://www.python.org/downloads/
    echo     2) Durante la instalacion MARCA la casilla "Add Python to PATH"
    echo     3) Cierra y vuelve a abrir este instalador
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo      OK - %%v

REM ── [2] Comprobar Git ─────────────────────────────────────────────
echo.
echo  [2/6] Comprobando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Git no esta instalado.
    echo.
    echo  SOLUCION:
    echo     1) Descargate Git desde: https://git-scm.com/download/win
    echo     2) Instalalo con valores por defecto
    echo     3) Cierra y vuelve a abrir este instalador
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('git --version') do echo      OK - %%v

REM ── [3] Clonar repositorio ────────────────────────────────────────
echo.
echo  [3/6] Descargando el repositorio...

set "INSTALL_DIR=%USERPROFILE%\KDD-PMO-Copilot"

if exist "%INSTALL_DIR%\agent\app.py" (
    echo      Ya existe en: %INSTALL_DIR%
    echo      Actualizando...
    cd /d "%INSTALL_DIR%"
    git pull
) else (
    echo      Clonando en: %INSTALL_DIR%
    git clone https://github.com/alejandromontalban-sketch/spec-driven.git "%INSTALL_DIR%"
    if errorlevel 1 (
        echo  ERROR clonando el repositorio. Revisa tu conexion o credenciales.
        pause
        exit /b 1
    )
    cd /d "%INSTALL_DIR%"
)

REM ── [4] Crear entorno virtual ─────────────────────────────────────
echo.
echo  [4/6] Creando entorno virtual...
if not exist "%INSTALL_DIR%\.venv\Scripts\python.exe" (
    python -m venv "%INSTALL_DIR%\.venv"
    if errorlevel 1 (
        echo  ERROR creando el entorno virtual.
        pause
        exit /b 1
    )
)
echo      OK - entorno virtual en .venv\

REM ── [5] Instalar dependencias ─────────────────────────────────────
echo.
echo  [5/6] Instalando dependencias (puede tardar 1-2 minutos)...
call "%INSTALL_DIR%\.venv\Scripts\activate.bat"
python -m pip install --upgrade pip --quiet
pip install -r "%INSTALL_DIR%\agent\requirements.txt" --quiet
if errorlevel 1 (
    echo  ERROR instalando dependencias.
    pause
    exit /b 1
)
echo      OK - dependencias instaladas

REM ── [6] Configurar .env interactivamente ─────────────────────────
echo.
echo  [6/6] Configuracion de credenciales
echo  -------------------------------------------------------------------
set "ENV_FILE=%INSTALL_DIR%\agent\.env"

if exist "%ENV_FILE%" (
    echo      Ya existe un fichero .env en %ENV_FILE%
    set /p RECONFIGURE="     ¿Quieres reconfigurarlo? (s/n): "
    if /i not "!RECONFIGURE!"=="s" goto :LAUNCH
)

echo.
echo   Vamos a pedirte unos datos. Si no tienes alguno, pulsa Enter
echo   y lo podras rellenar despues editando: %ENV_FILE%
echo.

set /p PMO_EMAIL="   1) Tu correo de PMO (recibira notificaciones): "
echo.
echo   2) GitHub Token (necesario para llamar a la IA y commitear specs)
echo      Obtener en: https://github.com/settings/personal-access-tokens/new
echo      Permisos: Models:Read + Contents:Read-and-Write
set /p GH_TOKEN="      Pega tu token: "
echo.
set /p GH_REPO="   3) Repositorio (formato usuario/repo) [alejandromontalban-sketch/spec-driven]: "
if "!GH_REPO!"=="" set "GH_REPO=alejandromontalban-sketch/spec-driven"
echo.
echo   4) Mailjet (para enviar emails al PMO). Si no lo tienes deja en blanco
set /p MJ_KEY="      API Key: "
set /p MJ_SECRET="      API Secret: "
set /p SENDER="      Email remitente verificado: "

REM Escribir .env
(
    echo # Generado por install.bat el %DATE% %TIME%
    echo PMO_EMAIL=!PMO_EMAIL!
    echo GITHUB_TOKEN=!GH_TOKEN!
    echo GITHUB_REPO=!GH_REPO!
    echo MAILJET_API_KEY=!MJ_KEY!
    echo MAILJET_API_SECRET=!MJ_SECRET!
    echo SENDER_EMAIL=!SENDER!
    echo STREAMLIT_PORT=8501
) > "%ENV_FILE%"

echo.
echo      OK - configuracion guardada en %ENV_FILE%

REM ── Generar datos de prueba si no existen ─────────────────────────
if not exist "%INSTALL_DIR%\actas\prueba_1" (
    echo.
    echo  Generando datos de prueba...
    cd /d "%INSTALL_DIR%\agent"
    python generate_test_data.py
)

:LAUNCH
echo.
echo  ===================================================================
echo                    INSTALACION COMPLETADA
echo  ===================================================================
echo.
echo   Ruta:        %INSTALL_DIR%
echo   Para usar:   doble clic en  start.bat   (en %INSTALL_DIR%)
echo.
echo  ¿Quieres arrancar la app ahora? (s/n)
set /p LAUNCH_NOW=" "
if /i "!LAUNCH_NOW!"=="s" (
    echo.
    echo  Arrancando KDD PMO Copilot en http://localhost:8501 ...
    echo  ^(cierra esta ventana o pulsa Ctrl+C para parar la app^)
    echo.
    cd /d "%INSTALL_DIR%\agent"
    start "" http://localhost:8501
    "%INSTALL_DIR%\.venv\Scripts\python.exe" -m streamlit run app.py
)

endlocal
pause

