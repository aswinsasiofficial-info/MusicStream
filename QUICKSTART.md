# 🎵 MusicStream - Quick Start Guide

## ✅ Setup Complete!

Your full-stack music streaming platform is now ready to use!

## 🚀 What's Been Built

### Backend (Django)
- ✅ Custom User authentication system with email
- ✅ Database models for Playlists, Songs, Favorites, and Recently Played
- ✅ REST API endpoints for all CRUD operations
- ✅ YouTube Music API integration via ytmusicapi
- ✅ Secure user sessions and CSRF protection

### Frontend (Bootstrap 5 + Vanilla JS)
- ✅ Spotify-inspired dark theme UI
- ✅ Responsive design (mobile + desktop)
- ✅ Persistent music player with full controls
- ✅ Search functionality with debouncing
- ✅ AJAX/Fetch for dynamic updates
- ✅ Lazy loading and infinite scroll support

### Features Implemented
1. **User System**
   - Registration with email + password
   - Login/Logout functionality
   - User profiles with avatars and bios
   
2. **Music Browsing**
   - Home page with trending/recommended sections
   - Search songs, albums, artists, playlists
   - Filter results by type
   
3. **Music Player**
   - Play/Pause/Next/Previous controls
   - Seek bar and volume control
   - Shuffle and repeat modes
   - Like/favorite songs
   
4. **Playlists**
   - Create, edit, delete playlists
   - Add/remove songs from playlists
   - View all your playlists in library
   
5. **Bonus Features**
   - Recently played tracking
   - Favorite songs collection
   - Smooth animations and transitions

## 📖 How to Use

### First Time Setup

The server is already running at: **http://127.0.0.1:8000**

1. **Create an Admin Account** (in a new terminal):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set email and password.

2. **Access the Application**:
   - Main app: http://127.0.0.1:8000
   - Admin panel: http://127.0.0.1:8000/admin

### Using the App

#### 1. Register/Login
- Click "Sign Up" to create an account
- Use email + password or username (optional)
- After registration, you'll be automatically logged in

#### 2. Browse Music
- **Home**: View trending songs and recommendations
- **Search**: Type in the search bar to find any song, artist, album
- Use filters to narrow down results (All, Songs, Albums, Artists, Playlists)

#### 3. Play Music
- Click on any song card to play it
- Use the persistent player at the bottom:
  - ▶️ Play/Pause
  - ⏮️ Previous track
  - ⏭️ Next track
  - 🔀 Shuffle mode
  - 🔁 Repeat (None → All → One)
  - ❤️ Like button to favorite songs
  - Volume slider for audio control

#### 4. Create Playlists
1. Click "Create Playlist" in the sidebar
2. Enter name and description
3. Click "Create"

#### 5. Add Songs to Playlists
- While browsing, click on a song
- Look for "Add to Playlist" option
- Select the target playlist

#### 6. Manage Your Library
- Click "Your Library" in sidebar
- View tabs:
  - **Playlists**: All your created playlists
  - **Favorites**: Songs you've liked
  - **Recently Played**: Your listening history

#### 7. Edit Profile
- Click your avatar/username in sidebar footer
- Click "Edit Profile"
- Update username, bio, or upload avatar
- Click "Save Changes"

## 🎨 Customization

### Change Theme Colors
Edit `static/css/style.css`:
```css
:root {
    --accent-color: #1db954;  /* Change this green */
    --bg-primary: #121212;     /* Main background */
    --text-primary: #ffffff;   /* Text color */
}
```

### Change Brand Name
Edit `templates/base.html`:
```html
<a href="{% url 'home' %}" class="brand">
    <i class="bi bi-soundwave"></i>
    YourAppName
</a>
```

## 🔧 Troubleshooting

### Server Won't Start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed, or use different port
python manage.py runserver 8001
```

### Dependencies Missing?
```bash
pip install django djangorestframework ytmusicapi pillow requests
```

### Database Issues?
```bash
python manage.py migrate
```

### Static Files Not Loading?
```bash
python manage.py collectstatic --noinput
```

## 📊 API Endpoints

Test these in your browser or Postman:

### Public Endpoints
- `GET /api/search/?q=adele&type=songs` - Search music
- `GET /api/trending/` - Get trending songs
- `GET /api/home-content/` - Get home page content

### Authenticated Endpoints (Login Required)
- `GET /api/playlists/` - List your playlists
- `POST /api/playlists/` - Create playlist
- `GET /api/favorites/` - Get favorite songs
- `POST /api/favorites/` - Add to favorites
- `DELETE /api/favorites/{song_id}/` - Remove favorite
- `GET /api/recently-played/` - Get recently played
- `POST /api/recently-played/add/` - Add to recently played

## 🎯 Next Steps

### Optional Enhancements

1. **Enable Google OAuth** (for Google login):
   - Install: `pip install django-allauth`
   - Follow instructions in main README.md
   - Add to INSTALLED_APPS in settings.py

2. **Add CORS Support** (for frontend frameworks):
   - Install: `pip install django-cors-headers`
   - Add to INSTALLED_APPS and MIDDLEWARE
   - Configure CORS_ALLOWED_ORIGINS

3. **Production Deployment**:
   - Set DEBUG=False
   - Use PostgreSQL instead of SQLite
   - Set up Nginx + Gunicorn
   - Configure HTTPS

4. **Real Audio Streaming**:
   - This demo uses metadata only (no actual streaming)
   - For production, integrate with:
     - Licensed streaming APIs (Spotify, Apple Music)
     - YouTube Data API with proper licensing
     - Royalty-free music sources

## 📝 Important Notes

### Copyright & Legal
⚠️ **This application fetches metadata from YouTube Music but does NOT stream actual audio.**

- Only song metadata (title, artist, thumbnail) is stored
- No copyrighted audio files are downloaded or stored
- For real streaming, you need proper music licensing

### Current Limitations
- Music player shows song info but doesn't play actual audio (copyright restrictions)
- In production, you would either:
  1. Link out to YouTube Music/Spotify for playback
  2. Use licensed streaming APIs
  3. Host royalty-free music

## 🙌 You're All Set!

Your music streaming platform is live and ready to explore. Enjoy discovering and organizing music!

**Happy Listening! 🎵**

---

Need help? Check the main [README.md](README.md) for detailed documentation.
