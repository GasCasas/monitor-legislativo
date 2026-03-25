@echo off
title Monitor Legislativo
echo Iniciando o Monitor Legislativo...
cd /d "%~dp0"
python -m streamlit run app.py
pause
