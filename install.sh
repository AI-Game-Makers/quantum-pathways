python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

VERSION=${1:-0.0.1-dev}
OS=${2:-linux}

# Check OS is valid
if [ "$OS" != "linux" ] && [ "$OS" != "windows" ] && [ "$OS" != "macos" ]; then
    echo "Invalid OS: $OS, must be one of: linux, windows, macos"
    exit 1
fi

DATA='assets/:assets'
if [ "$OS" = "windows" ]; then
    DATA='assets;assets'
fi

pyinstaller --onefile --windowed --name "QuantumPathways-v$VERSION-$OS" --icon assets/icon.icns --add-data $DATA main.py
chmod +x "dist/QuantumPathways-v$VERSION-$OS"

deactivate