@echo off
setlocal EnableExtensions

for %%I in ("%~dp0..") do set "EDUGUARD_ROOT=%%~fI"
set "EDUGUARD_START=%EDUGUARD_ROOT%\scripts\start_eduguard.bat"
set "EDUGUARD_TASK=EduGuard AI Local Server"
set "EDUGUARD_USER=%USERDOMAIN%\%USERNAME%"

if not exist "%EDUGUARD_START%" (
    echo EduGuard startup script was not found:
    echo "%EDUGUARD_START%"
    exit /b 1
)

rem /F updates the same task instead of creating duplicates. It runs at the current user's logon.
schtasks.exe /Create /TN "%EDUGUARD_TASK%" /TR "\"%EDUGUARD_START%\" --foreground" /SC ONLOGON /RU "%EDUGUARD_USER%" /RL LIMITED /IT /F
if errorlevel 1 (
    echo Unable to create the EduGuard AI Local Server task.
    echo Run this file from your Windows account and approve Task Scheduler if Windows asks.
    exit /b 1
)

echo Installed or updated the "%EDUGUARD_TASK%" task.
echo It will start EduGuard at the next Windows logon without Flask debug mode.
exit /b 0
