# MusicStream - Full-Stack Music Streaming Platform

A Spotify-inspired music streaming web application built with Django and Bootstrap 5, integrating **Jamendo API** for free music discovery from independent artists.

![MusicStream](https://img.shields.io/badge/version-2.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎵 Features

### Core Features
- **User Authentication**
  - Email + password registration and login
  - Google OAuth integration
  - Secure password hashing
  - User profiles with avatars and bios

- **Music Browsing**
  - Search songs using **Jamendo API** (free, legal music)
  - Popular/trending sections
  - Rich metadata with thumbnails and duration
  - Lazy loading for performance

- **Music Player** ⭐ NEW!
  - Persistent bottom player (Spotify-style)
  - **Direct MP3 streaming from Jamendo**
  - HTML5 audio playback
  - Play, pause, next, previous controls
  - Seek bar and volume control
  - Shuffle and repeat modes
  - Like/favorite songs

- **Playlists**
  - Create, edit, delete playlists
  - Add/remove songs from playlists
  - Private user playlists stored in database
  - Playlist management UI

- **UI/UX**
  - Modern dark theme inspired by Spotify
  - Sidebar navigation (Home, Search, Library)
  - Fully responsive design (mobile + desktop)
  - Smooth transitions and hover effects
  - Bootstrap 5 components

- **Bonus Features**
  - Recently played tracking
  - Favorite/liked songs
  - AJAX-based search (no page reload)
  - Loading spinners
  - Debounced search input

## 🛠️ Tech Stack

### Backend
- **Django 5.0.6** - Web framework
- **Requests 2.31.0** - HTTP library for API calls
- **Jamendo API v3.0** - Free music streaming integration
- **Django REST Framework 3.15.1** - API development
- **SQLite** - Database (default)

### Frontend
- **HTML5, CSS3, JavaScript (ES6+)**
- **Bootstrap 5.3.0** - Responsive layout
- **Bootstrap Icons** - Icon library
- **Vanilla JS** - No heavy frameworks
- **HTML5 Audio API** - Music playback

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Jamendo API Client ID (FREE - get from https://devportal.jamendo.com/)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation & Setup

### Quick Setup (Recommended)

**Windows:**
```bash
run_jamendo.bat
```

**PowerShell:**
```powershell
.\setup.ps1
```

### Manual Setup

### 1. Install Dependencies

```bash
cd "c:\Users\sasii\Desktop\Music Platform\music_Settings"
pip install requests
pip install -r requirements.txt
```

This will install:
- Django 5.0.6+
- Django REST Framework
- Requests (HTTP library for Jamendo API)
- Pillow (image processing)

### 2. Configure Jamendo API

**Get your FREE API key:**
1. Visit: https://devportal.jamendo.com/
2. Create account / Login
3. Go to "My Applications" → "Create new application"
4. Copy your Client ID

**Create `.env` file in project root:**
```bash
JAMENDO_CLIENT_ID=your_actual_client_id_here
```

See `JAMENDO_SETUP.md` for detailed configuration guide.

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account with email and password.

### 5. Start Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000/`
Admin panel at: `http://localhost:8000/admin/`

**Quick Test:**
```bash
python test_jamendo.py
```

## 📁 Project Structure

```
music_Settings/
├── accounts/                 # User authentication app
│   ├── models.py            # Custom User model
│   ├── forms.py             # Registration and profile forms
│   ├── views.py             # Auth views
│   └── urls.py              # Auth routes
├── api/                      # REST API app
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API endpoints
│   └── urls.py              # API routes
├── music/                    # Music browsing app
│   ├── services/            # API integrations
│   │   ├── __init__.py
│   │   └── jamendo.py       # Jamendo API service
│   ├── views.py             # Music views
│   └── urls.py              # Music routes
├── playlists/                # Playlist management app
│   ├── models.py            # Playlist and song models
│   └── ...
├── templates/                # HTML templates
│   ├── base.html            # Base template with player
│   ├── accounts/            # Auth templates
│   ├── music/               # Music browsing templates
│   └── playlists/           # Playlist templates
├── static/                   # Static files
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       ├── player.js        # Music player controller (Jamendo)
│       └── main.js          # Main JavaScript
├── media/                    # User uploads (avatars)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── JAMENDO_SETUP.md          # Jamendo API setup guide
├── IMPLEMENTATION_SUMMARY.md # Technical documentation
└── test_jamendo.py           # API integration test
```

## 🎯 Usage Guide

### Quick Start

1. **Get Jamendo API Key** (FREE)
   - Visit: https://devportal.jamendo.com/
   - Create account and get Client ID
   - Add to `.env` file: `JAMENDO_CLIENT_ID=your_id`

2. **Start the Server**
   ```bash
   python manage.py runserver
   ```

3. **Browse Music**
   - Visit: http://localhost:8000/search/
   - Type any artist/song name
   - Click play to start streaming!

### Registration & Login

1. Visit `http://localhost:8000/accounts/register/`
2. Enter email and password (username optional)
3. Or use "Continue with Google" for OAuth login

### Browsing Music

1. **Home Page**: View popular/trending songs from Jamendo
2. **Search**: Use the search bar to find any song or artist
3. **Real-time Results**: Results appear as you type (no page reload)

### Using the Player ⭐

1. Click on any song card to play it
2. **Direct MP3 streaming** from Jamendo
3. Use player controls:
   - Play/Pause button
   - Previous/Next buttons
   - Shuffle mode
   - Repeat mode (None → All → One)
   - Volume slider
   - Progress bar with seek
4. Click heart icon to like/favorite a song

### Managing Playlists

1. **Create Playlist**: 
   - Click "Create Playlist" in sidebar
   - Enter name and description
   
2. **Add Songs to Playlist**:
   - While browsing, click "Add to Playlist" on any song
   - Select target playlist

3. **View Your Playlists**:
   - Go to "Your Library" → "Playlists" tab
   - Click on any playlist to view songs

### Profile Management

1. Click on your avatar/username in sidebar footer
2. Update username, bio, and avatar
3. View your statistics

## 🔌 API Endpoints

### Music APIs (Jamendo Integration)
- `GET /api/search/?q=query&limit=20` - Search for tracks
- `GET /api/popular/` - Get popular/trending tracks
- `GET /api/track/<track_id>/` - Get track details

### Playlist APIs (Authentication Required)
- `GET /api/playlists/` - List user playlists
- `POST /api/playlists/` - Create playlist
- `PUT /api/playlists/<id>/` - Update playlist
- `DELETE /api/playlists/<id>/` - Delete playlist
- `POST /api/playlist-songs/<playlist_id>/` - Add song to playlist
- `DELETE /api/playlist-songs/<playlist_id>/<pk>/` - Remove song

### User APIs (Authentication Required)
- `GET /api/recently-played/` - Get recently played songs
- `POST /api/recently-played/add/` - Add to recently played
- `GET /api/favorites/` - Get favorite songs
- `POST /api/favorites/` - Add to favorites
- `DELETE /api/favorites/<song_id>/` - Remove from favorites

## 🎨 Customization

### Theme Colors

Edit CSS variables in `static/css/style.css`:

```css
:root {
    --bg-primary: #121212;      /* Main background */
    --bg-secondary: #181818;     /* Sidebar/player bg */
    --accent-color: #1db954;     /* Spotify green */
    --text-primary: #ffffff;     /* Main text */
}
```

### Branding

Change the brand name in `templates/base.html`:

```html
<a href="{% url 'home' %}" class="brand">
    <i class="bi bi-soundwave"></i>
    YourBrandName
</a>
```

## ⚠️ Important Notes

### Copyright & Legal

This application uses the **Jamendo API** to stream music from independent artists.

✅ **Legal & Licensed:**
- All music on Jamendo is freely available under Creative Commons licenses
- Artists voluntarily upload their music to Jamendo for free distribution
- No copyright restrictions for personal listening
- Perfect for discovering independent and emerging artists

🎵 **How It Works:**
- Direct MP3 streaming from Jamendo's servers
- No audio files are downloaded or stored locally
- Only metadata and stream URLs are fetched
- Fully compliant with Jamendo's Terms of Service

### Jamendo API Limits

- **Free Tier:** Limited requests per day (check current limits)
- **Commercial Use:** Requires separate agreement with Jamendo
- **Attribution:** Required for some tracks (check individual licenses)

Monitor your usage at: https://devportal.jamendo.com/analytics

### Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Set `JAMENDO_CLIENT_ID` in environment variables
3. Use a production-ready database (PostgreSQL recommended)
4. Configure proper web server (Nginx + Gunicorn)
5. Set up HTTPS with SSL certificates
6. Implement rate limiting and caching
7. Set up CDN for static files
8. Monitor Jamendo API usage limits
3. Configure proper web server (Nginx + Gunicorn)
4. Set up HTTPS with SSL certificates
5. Use environment variables for sensitive data
6. Implement rate limiting and caching
7. Set up CDN for static files

## 🐛 Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```bash
pip install -r requirements.txt --upgrade
```

**Issue: Database errors**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic
```

**Issue: Google OAuth not working**
- Verify redirect URIs in Google Cloud Console
- Check Client ID and Secret in `.env`
- Ensure allauth is properly configured

**Issue: No search results**
- Check JAMENDO_CLIENT_ID in .env file
- Test API: `python test_jamendo.py`
- Verify network connection

**Issue: Audio doesn't play**
- Check browser console for errors
- Some tracks may have geographic restrictions
- Verify audio_url exists in track data

## 📝 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review Jamendo API documentation: https://developer.jamendo.com/v3.0
- See `JAMENDO_SETUP.md` for detailed setup guide
- Run `python test_jamendo.py` to verify your setup

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Uses [Jamendo API](https://www.jamendo.com/) for free music streaming
- UI inspired by [Spotify](https://spotify.com)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)
- HTTP requests powered by [Requests](https://requests.readthedocs.io/)

---

**Enjoy discovering and streaming independent music! 🎵**

## 📚 Additional Documentation

- **Quick Start Guide**: `QUICKSTART_JAMENDO.md` - 3-minute setup
- **Detailed Setup**: `JAMENDO_SETUP.md` - Complete configuration guide
- **Technical Details**: `IMPLEMENTATION_SUMMARY.md` - Architecture and features
- **Test Script**: `test_jamendo.py` - Verify your API integration
- **Windows Launcher**: `run_jamendo.bat` - One-click startup
