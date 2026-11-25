@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "NO_PAUSE=0"
if /i "%~1"=="--no-pause" set "NO_PAUSE=1"

echo ===================================================
echo     ARBOR - MUSEUM OBJECT VISUALIZER
echo         Executable Build Pipeline
echo ===================================================
echo.

:: 1. Detect Python / Virtual Environment
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [INFO] Using virtual environment Python: .venv
) else if exist "venv\Scripts\python.exe" (
    set "PYTHON_EXE=venv\Scripts\python.exe"
    echo [INFO] Using virtual environment Python: venv
) else (
    echo [INFO] Using system Python from PATH
)

:: Verify Python executable
"%PYTHON_EXE%" --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found or is not accessible.
    echo Please ensure Python is installed and added to PATH, or activate your virtual environment.
    goto :build_failed
)

:: Verify PyInstaller is installed
"%PYTHON_EXE%" -m PyInstaller --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PyInstaller is not installed in the active environment.
    echo Please install it using: "%PYTHON_EXE%" -m pip install pyinstaller
    goto :build_failed
)

:: 2. Clean old build artifacts
echo.
echo [1/3] Cleaning previous build artifacts...
if exist "dist\Arbor.exe" (
    del /f /q "dist\Arbor.exe" 2>nul
    if exist "dist\Arbor.exe" (
        echo [ERROR] dist\Arbor.exe is currently running or locked by another process.
        echo Please close Arbor.exe before running the build pipeline.
        goto :build_failed
    )
)
if exist "build" (
    rmdir /s /q "build" 2>nul
)
if exist "dist" (
    rmdir /s /q "dist" 2>nul
)

:: 2b. Ensure offline demo dataset exists so it is bundled into Arbor.exe
if not exist "data\demo_collection.xlsx" (
    echo.
    echo [INFO] data\demo_collection.xlsx not found. Generating offline demo dataset...
    "%PYTHON_EXE%" scripts\create_demo_dataset.py
    if !ERRORLEVEL! NEQ 0 (
        echo [WARNING] Could not auto-generate data\demo_collection.xlsx.
    )
)

:: 3. Run PyInstaller build
echo.
echo [2/3] Building Arbor.exe via PyInstaller...
"%PYTHON_EXE%" -m PyInstaller --clean -y main.spec
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] PyInstaller build failed with exit code %ERRORLEVEL%.
    goto :build_failed
)

:: 4. Copy external resources to dist folder
echo.
echo [3/3] Copying readable user guides next to Arbor.exe...
if exist "USER_GUIDE.md" (
    copy /Y "USER_GUIDE.md" "dist\USER_GUIDE.md" >nul
    if !ERRORLEVEL! NEQ 0 (
        echo [WARNING] Failed to copy USER_GUIDE.md to dist.
    ) else (
        echo   - USER_GUIDE.md copied
    )
) else (
    echo [WARNING] USER_GUIDE.md not found in root.
)

if exist "MOBILE_COMPANION_USER_GUIDE.md" (
    copy /Y "MOBILE_COMPANION_USER_GUIDE.md" "dist\MOBILE_COMPANION_USER_GUIDE.md" >nul
    if !ERRORLEVEL! NEQ 0 (
        echo [WARNING] Failed to copy MOBILE_COMPANION_USER_GUIDE.md to dist.
    ) else (
        echo   - MOBILE_COMPANION_USER_GUIDE.md copied
    )
) else (
    echo [WARNING] MOBILE_COMPANION_USER_GUIDE.md not found in root.
)

:: ignored_words.json, data\demo_collection.xlsx and data\tutorial_images are bundled
:: inside Arbor.exe (see main.spec), so they are intentionally NOT copied here.

echo.
echo ===================================================
echo               BUILD SUCCESSFUL
echo ===================================================
echo.
echo Executable is ready at:
echo   %cd%\dist\Arbor.exe
echo.
if "%NO_PAUSE%"=="0" pause
exit /b 0

:build_failed
echo.
echo ===================================================
echo                 BUILD FAILED
echo ===================================================
echo Please inspect the error messages above.
echo.
if "%NO_PAUSE%"=="0" pause
exit /b 1
