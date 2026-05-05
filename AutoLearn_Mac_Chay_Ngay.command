#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
python3 -m pip install -r requirements.txt
open http://localhost:8501
python3 -m streamlit run app.py
