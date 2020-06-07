export PYTHONPATH="$PWD"

if command -v "python3" >/dev/null; then
    python3 scripts/chatbot_console.py
else
    python scripts/chatbot_console.py
fi
