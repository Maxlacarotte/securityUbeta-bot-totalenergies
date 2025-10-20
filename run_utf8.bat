@echo off
REM Configuration complète UTF-8 pour Windows

REM Change code page console vers UTF-8
chcp 65001 > nul

REM Variables d'environnement Python
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=0
set LANG=en_US.UTF-8
set LC_ALL=en_US.UTF-8

REM Import du pythonrc si disponible
set PYTHONSTARTUP=%~dp0pythonrc.py

echo Lancement de Streamlit avec encodage UTF-8...
echo.

python -X utf8 -m streamlit run app.py

pause