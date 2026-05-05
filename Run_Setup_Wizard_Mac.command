#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
python3 -m pip install streamlit
open http://localhost:8502
python3 -m streamlit run setup_wizard.py --server.port 8502
