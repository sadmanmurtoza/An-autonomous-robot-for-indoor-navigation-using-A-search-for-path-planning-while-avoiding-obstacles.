@echo off
REM ============================================================
REM setup_and_run.bat
REM Double-click this file on Windows to prepare and run project.
REM ============================================================

REM Show a clear title in the Command Prompt window.
title A-Star Robot Project Setup

REM Check whether the command "python" already works.
python --version >nul 2>&1

REM If Python works, jump to the RUN_PROJECT section.
if %errorlevel%==0 goto RUN_PROJECT

REM If "python" did not work, also try the Windows "py" launcher.
py --version >nul 2>&1

REM If the py launcher works, jump to RUN_WITH_PY.
if %errorlevel%==0 goto RUN_WITH_PY

REM Python was not found, so explain what we are doing.
echo Python was not found on this computer.
echo Trying to install Python 3.12 automatically with Windows Package Manager...

REM Check whether Windows Package Manager (winget) exists.
winget --version >nul 2>&1

REM If winget is missing, jump to the manual instructions.
if not %errorlevel%==0 goto NO_WINGET

REM Install official Python 3.12 automatically.
winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements

REM Tell the user that Windows may need a fresh terminal after installation.
echo.
echo Python installation command finished.
echo If the project does not start now, close this window and double-click this file again.
echo.

REM Try Python again after installation.
python --version >nul 2>&1

REM If Python now works, run the project.
if %errorlevel%==0 goto RUN_PROJECT

REM Try the py launcher again too.
py --version >nul 2>&1

REM If py works now, use it.
if %errorlevel%==0 goto RUN_WITH_PY

REM Otherwise show manual instructions.
goto NO_WINGET

:RUN_PROJECT
REM No pip libraries are needed, because this project uses Python built-in modules only.
echo Python is ready.
echo No extra pip packages are required.
echo Starting the robot simulator...
python "%~dp0main.py"
REM Keep this window open if the Python program closes because of an error.
pause
exit /b

:RUN_WITH_PY
REM No pip libraries are needed here either.
echo Python is ready through the Windows py launcher.
echo No extra pip packages are required.
echo Starting the robot simulator...
py "%~dp0main.py"
REM Keep this window open if there is an error.
pause
exit /b

:NO_WINGET
REM This part is used only when automatic Python installation is not possible.
echo.
echo Automatic Python installation is not available on this Windows setup.
echo Please install Python 3.12 or newer from python.org.
echo IMPORTANT: during installation, tick "Add python.exe to PATH".
echo Tkinter is normally included with the official Windows Python installer.
echo Then double-click setup_and_run.bat again.
pause
