@echo off
SET VENV_DIR=""
CALL %VENV_DIR%\Scripts\activate.bat
streamlit run main.py
CALL %VENV_DIR%\Scripts\deactivate.bat