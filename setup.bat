@echo off
echo ======================================
echo MusicStream Setup
echo ======================================
echo.
echo Step 1: Installing dependencies...
pip install django djangorestframework ytmusicapi pillow requests
echo Dependencies installed!
echo.
echo Step 2: Running migrations...
python manage.py migrate
echo Migrations complete!
echo.
echo ======================================
echo Setup Complete!
echo Access the app at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin
echo ======================================
echo.
echo Starting development server...
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
