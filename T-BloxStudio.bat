@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0T-BloxStudio\Launch-TBloxStudio.ps1"
if errorlevel 1 (
    echo.
    echo Nao foi possivel iniciar o T-BloxStudio.
    pause
)