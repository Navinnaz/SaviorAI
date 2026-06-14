@echo off
REM SaviorAI Demo Runner - Windows Batch Script

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please create it first: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run demo runner with arguments
python -m backend.utils.demo_runner %*

REM Deactivate is automatic when script ends
