@echo off
setlocal EnableExtensions

set "EDUGUARD_TASK=EduGuard AI Local Server"
schtasks.exe /Delete /TN "%EDUGUARD_TASK%" /F >nul 2>&1
if errorlevel 1 (
    echo No "%EDUGUARD_TASK%" task was found, or Windows denied access.
    exit /b 1
)

echo Removed the "%EDUGUARD_TASK%" task.
exit /b 0
