@echo off
setlocal
cd /d "%~dp0"
echo ABOGADO Y ASOCIADOS - DEMO PUBLICA
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3 -B demo.py
    exit /b
)
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python -B demo.py
    exit /b
)
echo Python 3.10 o superior no esta disponible en PATH.
echo Instale Python desde https://www.python.org/downloads/
pause
exit /b 1
