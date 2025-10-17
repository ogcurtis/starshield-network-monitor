@echo off
echo Starting Starshield Network Monitor...
echo Features: Interface selection, last down time, worst latency, bandwidth tracking, Fast.com integration
echo Access at: http://localhost:8080
echo.

REM Activate virtual environment
call .\.venv\Scripts\activate.bat

if errorlevel 1 (
    echo Error: Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Run the Flask application
python app.py

echo.
echo Monitor stopped.
echo.
pause