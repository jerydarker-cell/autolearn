#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "Da cai xong. Nhan Enter de thoat."
read
