@echo off
echo Setting up Starshield Network Monitor...
echo.

REM Create virtual environment if it doesn't exist
if not exist ".\.venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment. Make sure Python is installed.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the monitor, run: start.bat
echo.
echo Features:
echo - Real-time network monitoring
echo - Interface selection dropdown
echo - Latency and uptime tracking
echo - Bandwidth monitoring
echo - Fast.com speed testing
echo - Performance history
echo - Last down time tracking
echo.
pause