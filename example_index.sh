export PYTHONPATH="$PWD"

if command -v "python3" >/dev/null; then
    python3 scripts/build_index.py
else
    python scripts/build_index.py
fi
