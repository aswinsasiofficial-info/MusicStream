# MusicStream - Full-Stack Music Streaming Platform

A Spotify-inspired music streaming web application built with Django and Bootstrap 5, integrating YouTube Music API for music discovery.

![MusicStream](https://img.shields.io/badge/version-1.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎵 Features

### Core Features
- **User Authentication**
  - Email + password registration and login
  - Google OAuth integration
  - Secure password hashing
  - User profiles with avatars and bios

- **Music Browsing**
  - Search songs, albums, artists using ytmusicapi
  - Trending/recommended sections
  - Rich metadata with thumbnails
  - Lazy loading for performance

- **Music Player**
  - Persistent bottom player (Spotify-style)
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
  - Infinite scroll support
  - Debounced search input
  - AJAX/Fetch for dynamic updates

## 🛠️ Tech Stack

### Backend
- **Django 5.0.6** - Web framework
- **Django REST Framework 3.15.1** - API development
- **ytmusicapi 1.3.2** - YouTube Music integration
- **django-allauth 0.63.6** - Social authentication
- **SQLite** - Database (default)

### Frontend
- **HTML5, CSS3, JavaScript (ES6+)**
- **Bootstrap 5.3.0** - Responsive layout
- **Bootstrap Icons** - Icon library
- **Vanilla JS** - No heavy frameworks

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation & Setup

### Quick Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**PowerShell:**
```powershell
.\setup.ps1
```

### Manual Setup

### 1. Install Dependencies

```bash
cd "c:\Users\sasii\Desktop\Music Platform\music_Settings"
pip install -r requirements.txt
```

This will install:
- Django 5.0.6+
- Django REST Framework
- ytmusicapi (YouTube Music integration)
- Pillow (image processing)
- requests (HTTP library)

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account with email and password.

### 4. Start Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000/`
Admin panel at: `http://localhost:8000/admin/`

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
│   ├── services.py          # ytmusicapi integration
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
│       ├── player.js        # Music player controller
│       └── main.js          # Main JavaScript
├── media/                    # User uploads (avatars)
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## 🎯 Usage Guide

### Registration & Login

1. Visit `http://localhost:8000/accounts/register/`
2. Enter email and password (username optional)
3. Or use "Continue with Google" for OAuth login

### Browsing Music

1. **Home Page**: View trending songs and recommendations
2. **Search**: Use the search bar to find any song, artist, album, or playlist
3. **Filters**: Filter results by Songs, Albums, Artists, or Playlists

### Using the Player

1. Click on any song card to play it
2. Use player controls:
   - Play/Pause button
   - Previous/Next buttons
   - Shuffle mode
   - Repeat mode (None → All → One)
   - Volume slider
3. Click heart icon to like/favorite a song

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

### Music APIs
- `GET /api/search/?q=query&type=songs` - Search music
- `GET /api/trending/` - Get trending songs
- `GET /api/home-content/` - Get home page content
- `GET /api/song/<song_id>/` - Get song details

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

This application uses the ytmusicapi library to fetch metadata from YouTube Music. 

- **No audio files are downloaded or stored** - only metadata is fetched
- **Streaming is not implemented** in this demo due to copyright restrictions
- For production use, you would need:
  - Proper music licensing agreements
  - Integration with a licensed streaming service
  - Or use royalty-free music sources

### Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production-ready database (PostgreSQL recommended)
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

## 📝 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review ytmusicapi documentation: https://ytmusicapi.readthedocs.io/

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Uses [ytmusicapi](https://github.com/sigma67/ytmusicapi) for YouTube Music integration
- UI inspired by [Spotify](https://spotify.com)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)

---

**Enjoy discovering and organizing your music!** 🎵
