@echo off
cd /d "%~dp0"
start http://localhost:8501
py -m streamlit run app.py
