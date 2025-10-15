@echo off
REM --- Configuration Variables ---
REM Python/Pip paths are critical. Using hardcoded paths for robustness.
set PYTHON=C:\Python311\python.exe
set PIP=C:\Python311\Scripts\pip.exe
set SCRIPT=AutoLogin.pyw
set EXENAME=AutoLogin
set DATA_FILE=credentials.txt

REM Get current directory absolute path
for %%I in ("%~dp0") do set CUR_DIR=%%~fI
set ICON=%CUR_DIR%icon.ico

REM --- Step 1: Install or Update Dependencies ---

echo Checking for PyInstaller...
"%PIP%" show pyinstaller || (echo PyInstaller not found. Installing it... & "%PIP%" install pyinstaller)

echo Checking for Playwright...
"%PIP%" show playwright >nul 2>&1
if errorlevel 1 (
    echo Playwright not found. Installing it...
    "%PIP%" install playwright
    
    REM Install Playwright browser binaries (no --with-deps to avoid admin prompt)
    echo Installing Playwright browser binaries...
    "%PYTHON%" -m playwright install
) else (
    echo Playwright is already installed.
)

REM --- Step 2: Build the .exe with icon (NO --add-data to keep credentials.txt external) ---
echo.
echo =========================================================
echo Starting PyInstaller Build (Output will be below this line)
echo =========================================================
echo.

REM CRITICAL FIX: Removed the --add-data flag to keep credentials.txt external
set "BUILD_CMD=%PYTHON% -m PyInstaller --onefile --noconsole --name %EXENAME% "%SCRIPT%""

if exist "%ICON%" (
    set "BUILD_CMD=%BUILD_CMD% --icon="%ICON%""
)

REM Use CALL to execute the dynamically constructed command string reliably
CALL %BUILD_CMD%

REM --- Step 3 & 4: Copy .exe and Clean up build artifacts ---
echo.
echo Attempting to clean up and copy executable...

if exist dist\%EXENAME%.exe (
    copy dist\%EXENAME%.exe .
    echo %EXENAME%.exe built and copied to this folder.
) else (
    echo BUILD FAILED or EXECUTABLE NOT FOUND. Check PyInstaller output above.
)

rmdir /s /q build
rmdir /s /q dist
del %EXENAME%.spec >nul 2>&1

echo.
echo Script finished.
pause
