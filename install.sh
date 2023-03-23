VERSION=${1:-0.0.1-dev}
OS=${2:-linux}

DATA='assets/:assets'
if [ "$OS" = "win" ]; then
    DATA='assets;assets'
fi

pyinstaller --onefile --windowed --name 'QuantumPathways-v$VERSION-$OS' --add-data $DATA main.py
chmod +x "dist/QuantumPathways-v$VERSION-$OS"
