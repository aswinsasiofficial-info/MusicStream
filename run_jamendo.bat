@echo off
REM Quick Start Script for Jamendo Music Platform
REM This script helps you set up and run the music platform

echo ============================================
echo  Music Platform - Jamendo Integration
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [INFO] .env file not found. Creating from .env.example...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit .env file and add your JAMENDO_CLIENT_ID
    echo Get your free API key from: https://devportal.jamendo.com/
    echo.
    echo After updating .env, run this script again.
    pause
    exit /b 0
)

echo [OK] .env file found
echo.

REM Check if requests library is installed
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required dependencies...
    pip install requests
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)
echo.

REM Run database migrations
echo [INFO] Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [WARNING] Migration encountered some issues
    echo You can continue, but some features may not work
)
echo.

REM Prompt for Jamendo Client ID
echo ============================================
echo  IMPORTANT: Jamendo API Configuration
echo ============================================
echo.
echo To use this application, you need a FREE Jamendo API Client ID.
echo.
echo Steps to get your Client ID:
echo 1. Visit: https://devportal.jamendo.com/
echo 2. Create an account or login
echo 3. Go to "My Applications"
echo 4. Click "Create a new application"
echo 5. Copy your Client ID
echo.
echo Current .env file contents (JAMENDO_CLIENT_ID line):
findstr /C:"JAMENDO_CLIENT_ID" .env
echo.
echo If the Client ID is missing or shows 'your-jamendo-client-id-here',
echo please edit the .env file with your actual Client ID.
echo.
echo ============================================
echo.

REM Start the server
echo Starting Django development server...
echo.
echo Access the application at: http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Try to load environment variables using dotenv if available
python -c "import dotenv; dotenv.read_dotenv()" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] python-dotenv found, loading environment variables...
    python manage.py runserver
) else (
    echo [INFO] python-dotenv not found, using system environment variables
    echo [TIP] Install python-dotenv for easier configuration: pip install python-dotenv
    echo.
    python manage.py runserver
)

pause
