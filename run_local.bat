@echo off
setlocal

cd /d "%~dp0"

echo.
echo ========================================
echo   MoodTune AI - Local Streamlit Runner
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo Failed to create the virtual environment.
        echo Make sure Python is installed and available on PATH.
        pause
        exit /b 1
    )
)

echo Installing/updating Python dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Failed to install dependencies.
    pause
    exit /b 1
)

if not exist ".env" (
    echo.
    echo No .env file found. Creating one from .env.example...
    copy ".env.example" ".env" >nul
    echo Add your Spotify credentials to .env for live Spotify recommendations.
)

echo.
echo Starting MoodTune AI...
echo Open http://localhost:8501 in your browser.
echo Press Ctrl+C in this window to stop the app.
echo.

".venv\Scripts\streamlit.exe" run streamlit_app.py --server.address 127.0.0.1 --server.port 8501

endlocal
