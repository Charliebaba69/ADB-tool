@echo off
title Android QA Console - Windows Master Build

echo ============================================
echo  ANDROID QA CONSOLE - WINDOWS BUILD
echo ============================================

:: Check if conda exists
where conda >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda not found.
    pause
    exit /b
)

:: Activate local environment
IF NOT EXIST venv (
    echo ERROR: Local environment not found.
    echo Run setup.bat first.
    pause
    exit /b
)

call conda activate ./venv

echo.
echo Installing required libraries (if missing)...
pip install --upgrade pip >nul
pip install pyinstaller customtkinter >nul

:: Verify platform-tools
IF NOT EXIST platform-tools\adb.exe (
    echo ERROR: platform-tools\adb.exe not found!
    echo Download Android Platform Tools and place inside project.
    pause
    exit /b
)

echo.
echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q IAP_QA_MASTER_PACKAGE 2>nul
del *.spec 2>nul

echo.
echo Building Windows EXE...

pyinstaller --onedir --windowed ^
--name IAP_Android_QA_Console ^
--add-data "platform-tools;platform-tools" ^
app\iap_android_sandbox_pro.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b
)

echo.
echo Creating MASTER PACKAGE structure...

mkdir IAP_QA_MASTER_PACKAGE
mkdir IAP_QA_MASTER_PACKAGE\Windows

xcopy /E /I /Y dist\IAP_Android_QA_Console IAP_QA_MASTER_PACKAGE\Windows >nul

echo.
echo ============================================
echo BUILD SUCCESSFUL!
echo ============================================
echo.
echo Your distributable folder is:
echo IAP_QA_MASTER_PACKAGE\Windows
echo.
echo Zip the IAP_QA_MASTER_PACKAGE folder and share.
echo.
pause