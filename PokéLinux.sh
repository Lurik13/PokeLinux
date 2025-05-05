SCRIPT_DIR=$(dirname "$(realpath "$0")")
python3 "$SCRIPT_DIR/main.py" $(tput cols) "$0"
