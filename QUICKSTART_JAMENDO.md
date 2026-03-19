# 🚀 Quick Start Guide - Jamendo Music Platform

## 3-Minute Setup

### Step 1: Get Your API Key (2 minutes)
1. Visit: https://devportal.jamendo.com/
2. Create account / Login
3. Go to "My Applications" → "Create new application"
4. Copy your **Client ID**

### Step 2: Configure Environment (30 seconds)
Create a `.env` file in project root:
```bash
JAMENDO_CLIENT_ID=your_actual_client_id_here
```

### Step 3: Install & Run (30 seconds)
```bash
# Install dependency
pip install requests

# Run the test script
python test_jamendo.py

# Start server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 📁 What Was Built

### Backend Files
- `music/services/jamendo.py` - API integration
- `music/views.py` - Updated for Jamendo
- `music/urls.py` - New routes

### Frontend Files  
- `templates/music/search.html` - Search UI
- `templates/music/home.html` - Home page
- `static/js/player.js` - Audio player

### Documentation
- `JAMENDO_SETUP.md` - Detailed setup guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `test_jamendo.py` - Test script
- `run_jamendo.bat` - Windows launcher

---

## ✅ Verify It Works

1. Open browser: http://127.0.0.1:8000/search/
2. Type any artist/song name
3. Click play button on any track
4. Music should start playing!

---

## 🐛 Common Issues

**No results when searching?**
- Check JAMENDO_CLIENT_ID in .env
- Verify API key at: https://devportal.jamendo.com/

**Audio doesn't play?**
- Check browser console for errors
- Some tracks have geographic restrictions

**Server won't start?**
- Run: `python manage.py migrate`
- Then: `python manage.py runserver`

---

## 📖 Next Steps

### Explore Features
- Search for your favorite artists
- Browse popular tracks on home page
- Create playlists (if implemented)
- Like/favorite songs

### Customize
- Modify CSS in `static/css/style.css`
- Adjust player settings in `static/js/player.js`
- Change theme colors in templates

### Deploy to Production
- Set environment variables on hosting platform
- Configure ALLOWED_HOSTS
- Enable HTTPS
- Collect static files

---

## 🆘 Need Help?

**Documentation:**
- Setup guide: `JAMENDO_SETUP.md`
- Implementation: `IMPLEMENTATION_SUMMARY.md`
- Jamendo API: https://developer.jamendo.com/v3.0

**Test your setup:**
```bash
python test_jamendo.py
```

---

**That's it! Happy listening! 🎵**
