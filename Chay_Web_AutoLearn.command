#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
open http://localhost:8501
python3 -m streamlit run app.py
