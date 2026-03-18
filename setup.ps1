# Quick Setup Script for MusicStream
# Run this after installing dependencies

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MusicStream Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Installing dependencies..." -ForegroundColor Yellow
pip install django djangorestframework ytmusicapi pillow requests
Write-Host "Dependencies installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Running migrations..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "Migrations complete!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Creating admin user..." -ForegroundColor Yellow
Write-Host "Please create a superuser manually with:" -ForegroundColor Gray
Write-Host "  python manage.py createsuperuser" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 4: Starting development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "Access the app at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Admin panel at: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python manage.py runserver
