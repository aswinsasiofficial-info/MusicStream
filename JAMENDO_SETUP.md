# Jamendo Music Streaming Module - Setup Guide

This Django module integrates the Jamendo API for searching and streaming free music from independent artists.

## 📋 Prerequisites

- Python 3.11+
- Django (latest stable)
- A Jamendo API Client ID (free to obtain)

## 🔑 Getting Your Jamendo API Key

1. Visit [Jamendo Developer Portal](https://devportal.jamendo.com/)
2. Create a free account or login
3. Go to "My Applications" 
4. Click "Create a new application"
5. Fill in the required information:
   - Application name: Your choice (e.g., "Music Platform")
   - Description: Brief description of your project
   - Website: Can be `http://localhost` for development
6. After creation, you'll receive a **Client ID**

## ⚙️ Installation & Configuration

### Step 1: Install Dependencies

```bash
pip install requests
```

The `requests` library is used for making HTTP calls to the Jamendo API.

### Step 2: Configure Environment Variables

Create a `.env` file in your project root (same directory as `manage.py`):

```bash
# .env file
JAMENDO_CLIENT_ID=your_actual_client_id_here
```

**Important:** Never commit your `.env` file to version control!

### Step 3: Update settings.py (Already Done)

The settings.py has been configured to load the JAMENDO_CLIENT_ID from environment variables:

```python
import os
JAMENDO_CLIENT_ID = os.environ.get('JAMENDO_CLIENT_ID', '')
```

### Step 4: Verify URLs Configuration

Make sure your main `music_Settings/urls.py` includes the music app URLs:

```python
from django.urls import path, include

urlpatterns = [
    # ... other URLs
    path('', include('music.urls')),
]
```

## 🚀 Running the Application

### Option 1: Using manage.py directly

```bash
# Set environment variable (choose one method)

# Windows (Command Prompt)
set JAMENDO_CLIENT_ID=your_client_id_here
python manage.py runserver

# Windows (PowerShell)
$env:JAMENDO_CLIENT_ID="your_client_id_here"
python manage.py runserver

# Linux/Mac
export JAMENDO_CLIENT_ID=your_client_id_here
python manage.py runserver
```

### Option 2: Using python-dotenv (Recommended for Development)

Install python-dotenv:
```bash
pip install python-dotenv
```

Add to your `manage.py` (after the shebang line):
```python
import dotenv
dotenv.read_dotenv()
```

Then simply run:
```bash
python manage.py runserver
```

## 🎵 Features Implemented

### 1. Music Search
- Search bar with real-time AJAX search (no page reload)
- Debounced input for better performance
- Returns top 20 results by default
- Displays: song title, artist name, album image, duration

### 2. Music Streaming
- HTML5 `<audio>` player for direct MP3 streaming
- Uses Jamendo-provided audio URLs
- Smooth playback without page reload
- Full track control (play, pause, volume)

### 3. UI/UX
- Clean, modern dark theme (Spotify-inspired)
- Responsive layout using Bootstrap 5
- Track cards with hover effects and play overlays
- Loading spinners during API calls
- User-friendly error messages

### 4. Error Handling
- Empty search query handling
- API timeout protection (10 seconds)
- Invalid API key detection
- Network error handling
- Graceful fallbacks

## 📁 Project Structure

```
music/
├── services/
│   ├── __init__.py
│   └── jamendo.py          # Jamendo API integration
├── templates/music/
│   ├── home.html           # Home page with popular tracks
│   └── search.html         # Search interface
├── views.py                # Request handlers
├── urls.py                 # URL routing
└── static/js/
    └── player.js           # Audio player controller
```

## 🔧 API Endpoints

### Search Tracks
```
GET /api/search/?q=<query>&limit=20
```
Searches for tracks matching the query.

**Response:**
```json
{
  "results": [
    {
      "id": "12345",
      "title": "Song Title",
      "artist": "Artist Name",
      "album": "Album Name",
      "duration": 180,
      "thumbnail": "https://...",
      "audio_url": "https://...",
      "type": "song"
    }
  ]
}
```

### Popular Tracks
```
GET /api/popular/
```
Returns popular/trending tracks.

### Track Details
```
GET /api/track/<track_id>/
```
Returns detailed information about a specific track.

## 🎨 Frontend Components

### Search Page (`/search/`)
- Real-time search with debouncing
- Track cards with play buttons
- Duration display
- Album artwork
- Loading states and error handling

### Home Page (`/`)
- Popular/trending section
- Recently played (if implemented)
- Made for You recommendations

### Player Controls
- Play/Pause toggle
- Volume control
- Progress bar
- Next/Previous navigation
- Shuffle and repeat modes

## 🔒 Security Notes

✅ **DO:**
- Store CLIENT_ID in environment variables
- Keep `.env` file out of version control
- Use HTTPS in production
- Validate user inputs

❌ **DON'T:**
- Hardcode API keys in source code
- Commit `.env` files to Git
- Expose CLIENT_ID in frontend JavaScript
- Store downloaded audio files

## 🐛 Troubleshooting

### Issue: No results appear when searching

**Solution:**
1. Check browser console for errors
2. Verify JAMENDO_CLIENT_ID is set correctly
3. Test API access: https://api.jamendo.com/v3.0/tracks/?client_id=YOUR_ID&search=test
4. Check network tab for API response

### Issue: Audio doesn't play

**Solution:**
1. Check if `audio_url` exists in the track data
2. Verify CORS policy allows streaming
3. Check browser console for audio loading errors
4. Some tracks may have geographic restrictions

### Issue: API returns empty results

**Solution:**
1. Try different search terms
2. Verify API key is active
3. Check rate limits on Jamendo dev portal
4. Ensure proper encoding of special characters

## 📊 API Rate Limits

Jamendo API has the following limits (check their docs for current limits):
- Free tier: Limited requests per day
- Commercial use: Requires separate agreement

Monitor your usage at: https://devportal.jamendo.com/analytics

## 🚀 Production Deployment

### Environment Variables
Set `JAMENDO_CLIENT_ID` in your hosting platform's environment:

**Heroku:**
```bash
heroku config:set JAMENDO_CLIENT_ID=your_id
```

**Docker:**
```yaml
environment:
  - JAMENDO_CLIENT_ID=your_id
```

**AWS/GCP/Azure:**
Use their secret manager services

### Static Files
```bash
python manage.py collectstatic
```

### Settings Adjustments
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

## 🎯 Optional Enhancements

### 1. Caching (Redis)
```python
from django.core.cache import cache

def search_tracks_cached(query):
    cache_key = f'jamendo_search_{query}'
    results = cache.get(cache_key)
    
    if not results:
        results = jamendo.search_tracks(query)
        cache.set(cache_key, results, 3600)  # Cache for 1 hour
    
    return results
```

### 2. Pagination
```javascript
let currentPage = 1;
const limit = 20;

async function loadMore() {
    const offset = (currentPage - 1) * limit;
    const response = await fetch(`/api/search/?q=${query}&limit=${limit}&offset=${offset}`);
    // Append results...
    currentPage++;
}
```

### 3. Advanced Filters
- Filter by genre/tags
- Filter by duration
- Sort by popularity, rating, date

## 📝 Code Quality

The implementation follows these best practices:
- ✅ Separation of concerns (services layer)
- ✅ Error handling and logging
- ✅ DRY principles
- ✅ Responsive design
- ✅ Security best practices
- ✅ Performance optimization (debouncing, caching)

## 🆘 Support

For Jamendo API issues:
- Documentation: https://developer.jamendo.com/v3.0
- Support: https://devportal.jamendo.com/support

For Django issues:
- Documentation: https://docs.djangoproject.com/

## 📄 License

This module uses the Jamendo API which is subject to Jamendo's Terms of Service.
All music is licensed under Creative Commons licenses - check individual track licenses.

---

**Happy Coding! 🎵**
