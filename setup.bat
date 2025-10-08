@echo off
REM Project Drishti - Quick Setup Script for Windows

echo ==========================================
echo Project Drishti - Quick Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
echo.
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo WARNING: Please edit .env file and add your GOOGLE_API_KEY
    echo    Get your API key from: https://makersuite.google.com/app/apikey
    echo.
) else (
    echo .env file already exists
)

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist uploads mkdir uploads
if not exist temp_extractions mkdir temp_extractions

REM Ingest sample data
echo.
set /p response=Would you like to ingest sample data? (y/n): 
if /i "%response%"=="y" (
    echo.
    echo Ingesting sample case 1...
    python ingest_data.py --path ./ufdr_sample_reports/case_001_cyber_fraud_ring
    
    echo.
    echo Ingesting sample case 2...
    python ingest_data.py --path ./ufdr_sample_reports/case_002_drug_trafficking
    
    echo.
    echo Ingesting sample case 3...
    python ingest_data.py --path ./ufdr_sample_reports/case_003_terrorism_network
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your GOOGLE_API_KEY
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Run the application: streamlit run app.py
echo.
echo Documentation: README.md
echo ==========================================

pause
