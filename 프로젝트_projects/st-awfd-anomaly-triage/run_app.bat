@echo off
setlocal
cd /d "%~dp0"
set "ST_AWFD_PYTHON=python"
if exist "%CD%\.venv\Scripts\python.exe" set "ST_AWFD_PYTHON=%CD%\.venv\Scripts\python.exe"
if not defined ST_AWFD_PORT set "ST_AWFD_PORT=8501"
"%ST_AWFD_PYTHON%" -m streamlit run "st_awfd_app.py" --server.port "%ST_AWFD_PORT%"
if errorlevel 1 (
    echo Streamlit exited with an error. Check the Python environment and README.md.
    pause
    exit /b 1
)
endlocal
