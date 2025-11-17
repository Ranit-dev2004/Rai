@echo off
cd /d "%~dp0"
echo Starting Rai from %cd%...
call .venv\Scripts\activate
python rai_main.py
pause