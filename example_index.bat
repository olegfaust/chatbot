@ECHO OFF
setlocal
set PYTHONPATH=%cd%
python scripts/build_index.py data/small.csv
endlocal