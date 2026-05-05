#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
chmod +x *.command
xattr -dr com.apple.quarantine .
echo "Da sua quyen. Nhan Enter de thoat."
read
