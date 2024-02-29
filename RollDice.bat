@REM This rolls dices
@echo off

@REM Activate the virtual environment
call .venv\Scripts\activate.bat
cd src

@REM Run python program
python main.py

pause
