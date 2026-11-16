@echo off
REM Double-click this file to start the Student Attendance website.
REM The website opens in your browser. Close this window to stop it.

REM Go to the folder this file is in.
cd /d "%~dp0"

echo Starting the Student Attendance website...
echo.
echo Keep this window open while you use the website.
echo Close this window to stop the website.
echo.

REM Open the browser after 3 seconds, so the website has time to start.
start "" /b cmd /c "timeout /t 3 >nul && start http://127.0.0.1:5000"

REM Use the project's venv if it exists, otherwise the normal Python.
if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" "Python Code\app.py"
) else (
    python "Python Code\app.py"
)

pause
