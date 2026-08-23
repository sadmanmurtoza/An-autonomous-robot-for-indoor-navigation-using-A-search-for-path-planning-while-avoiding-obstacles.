@echo off
TITLE Group 6 A-Star Robot Project Setup

echo ======================================================
echo  Autonomous Indoor Navigation Robot - Automatic Setup
echo ======================================================
echo.

REM First check whether the command "python" already works.
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 GOTO RUNPROJECT

REM If "python" is missing, check the Windows "py" launcher.
py --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 GOTO RUNWITHPY

echo Python was not found.
echo Trying to install Python automatically using winget...
echo.

REM Try to install Python 3.12 automatically.
winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements

REM Check again after installation.
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 GOTO RUNPROJECT

py --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 GOTO RUNWITHPY

echo.
echo Automatic Python installation could not finish.
echo Please install Python 3 from python.org, then run this file again.
pause
exit /b

:RUNPROJECT
echo Python is ready.
echo No extra packages are needed.
echo Starting the project now...
python main.py
GOTO END

:RUNWITHPY
echo Python is ready through the Windows py launcher.
echo No extra packages are needed.
echo Starting the project now...
py main.py
GOTO END

:END
pause
