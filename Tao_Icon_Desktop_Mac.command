#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
DESK="$HOME/Desktop/AutoLearn Ultra Production v15.command"
cat > "$DESK" <<EOF
#!/bin/bash
cd "$DIR"
open http://localhost:8501
python3 -m streamlit run app.py
EOF
chmod +x "$DESK"
echo "Da tao launcher tren Desktop: $DESK"
read
