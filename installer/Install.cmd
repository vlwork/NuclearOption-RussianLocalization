@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "POWERSHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%POWERSHELL%" set "POWERSHELL=powershell.exe"

"%POWERSHELL%" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install.ps1"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
    echo Установка завершилась с ошибкой. Текст ошибки указан выше.
) else (
    echo Готово.
)
echo.
pause
exit /b %RC%
