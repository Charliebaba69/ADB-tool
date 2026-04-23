@echo off
title Android IAP Sandbox Validator - Auto Setup

echo ============================================
echo  ANDROID IAP SANDBOX VALIDATOR SETUP
echo ============================================

:: Check if Conda exists
where conda >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda not found.
    echo Please install Anaconda or Miniconda first.
    pause
    exit /b
)

:: Create local environment if not exists
IF NOT EXIST venv (
    echo Creating local Conda environment...
    conda create --prefix ./venv python=3.10 -y
) ELSE (
    echo Local environment already exists.
)

:: Activate environment
call conda activate ./venv

echo Installing required libraries...
pip install --upgrade pip
pip install customtkinter pyinstaller

:: Check platform-tools folder
IF NOT EXIST platform-tools\adb.exe (
    echo ERROR: platform-tools folder or adb.exe not found!
    echo Please download Android Platform Tools and place inside project folder.
    pause
    exit /b
)

echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

echo Building portable EXE...
pyinstaller --onedir --windowed ^
--add-data "platform-tools;platform-tools" ^
--name IAP_Android_Sandbox_Validator ^
app\iap_android_sandbox_pro.py

echo ============================================
echo BUILD COMPLETE!
echo ============================================
echo Your distributable tool is inside:
echo dist\IAP_Android_Sandbox_Validator\
echo.
pause