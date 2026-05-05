@echo off
cd /d "%~dp0"
py -m pip install streamlit
start http://localhost:8502
py -m streamlit run setup_wizard.py --server.port 8502
pause
