@echo off
SET VENV_DIR="C:\Users\Ro\Documents\Python Workspace\Auto-APSI\venv"
CALL %VENV_DIR%\Scripts\activate.bat
streamlit run main.py %1
CALL %VENV_DIR%\Scripts\deactivate.bat