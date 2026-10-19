@echo off
setlocal
rem Double-click helper for users who want to launch the default test in Explorer.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
set "EXITCODE=%ERRORLEVEL%"
echo.
if not "%EXITCODE%"=="0" echo The simulation ended with an error. Review the message above.
pause
exit /b %EXITCODE%
