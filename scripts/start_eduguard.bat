@echo off
setlocal EnableExtensions

rem Resolve the project root from this script, so the project can be moved intact.
for %%I in ("%~dp0..") do set "EDUGUARD_ROOT=%%~fI"
set "EDUGUARD_PYTHON=%EDUGUARD_ROOT%\venv\Scripts\python.exe"
set "EDUGUARD_SERVER=%EDUGUARD_ROOT%\venv\Scripts\waitress-serve.exe"

if not exist "%EDUGUARD_PYTHON%" (
    echo EduGuard AI could not find the project virtual environment.
    echo Expected: "%EDUGUARD_PYTHON%"
    exit /b 1
)

if not exist "%EDUGUARD_SERVER%" (
    echo Waitress is not installed in the project virtual environment.
    echo Run: "%EDUGUARD_PYTHON%" -m pip install -r requirements.txt
    exit /b 1
)

cd /d "%EDUGUARD_ROOT%"
set "EDUGUARD_ENV=development"
set "FLASK_DEBUG=0"

rem Avoid a second EduGuard server. A different listener on port 5000 is reported clearly.
powershell -NoProfile -Command "try { $response = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 http://127.0.0.1:5000/health; if ($response.StatusCode -eq 200 -and $response.Content -match '\"status\"\s*:\s*\"ok\"') { exit 0 }; exit 1 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    echo EduGuard AI is already running at http://127.0.0.1:5000
    exit /b 0
)

powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    echo Port 5000 is already in use by another application. EduGuard AI was not started.
    exit /b 1
)

if /I "%~1"=="--foreground" (
    "%EDUGUARD_SERVER%" --host=127.0.0.1 --port=5000 --call app:create_app
    exit /b %errorlevel%
)

start "EduGuard AI Local Server" /min "%EDUGUARD_SERVER%" --host=127.0.0.1 --port=5000 --call app:create_app
echo EduGuard AI is starting at http://127.0.0.1:5000
echo Verify readiness at http://127.0.0.1:5000/health
exit /b 0
