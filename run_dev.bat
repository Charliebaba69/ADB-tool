@echo off
title Android IAP Validator - Dev Mode

echo Activating local environment...

IF NOT EXIST venv (
    echo ERROR: Local environment not found.
    echo Please run setup.bat first.
    pause
    exit /b
)

call conda activate ./venv

echo Starting Python application...
echo.

python app\iap_android_sandbox_pro.py

echo.
echo Application closed.
pause