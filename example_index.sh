export PYTHONPATH="$PWD"

if command -v "python3" >/dev/null; then
    python3 scripts/build_index.py data/small.csv
else
    python scripts/build_index.py data/small.csv
fi
