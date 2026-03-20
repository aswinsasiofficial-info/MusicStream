from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime


def home(request):
    """Home page view"""
    # Get time of day for greeting
    hour = datetime.now().hour
    if hour < 12:
        time_of_day = 'morning'
    elif hour < 18:
        time_of_day = 'afternoon'
    else:
        time_of_day = 'evening'
    
    return render(request, 'music/home.html', {'time_of_day': time_of_day})


def search(request):
    """Search page view - Jamendo"""
    return render(request, 'music/search.html')


@login_required
def library(request):
    """User library view"""
    return render(request, 'playlists/library.html')


@require_http_methods(["GET"])
@cache_page(60 * 10)  # Cache for 10 minutes
def search_api(request):
    """Search API endpoint - Jamendo"""
    query = request.GET.get('q', '')
    limit = int(request.GET.get('limit', '20'))
    
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    
    from music.services.jamendo import jamendo
    
    try:
        results = jamendo.search_tracks(query, limit=limit)
        return JsonResponse({'results': results})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def popular_api(request):
    """Popular/trending songs API endpoint - Jamendo"""
    from music.services.jamendo import jamendo
    
    try:
        popular = jamendo.get_popular_tracks(limit=20)
        return JsonResponse({'popular': popular})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def track_detail_api(request, track_id):
    """Get detailed track information - Jamendo"""
    from music.services.jamendo import jamendo
    
    try:
        track = jamendo.get_track_by_id(track_id)
        if track:
            return JsonResponse(track)
        return JsonResponse({'error': 'Track not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def home_content_api(request):
    """Get content for home page"""
    from music.services.jamendo import jamendo
    
    try:
        # Get different categories of music
        recommended = jamendo.get_popular_tracks(limit=10)
        new_releases = jamendo.search_tracks("latest", limit=10)
        
        # Structure it as expected by the frontend
        return JsonResponse({
            'content': [
                {
                    'title': 'Recommended for You',
                    'contents': recommended
                },
                {
                    'title': 'New Releases',
                    'contents': new_releases
                }
            ]
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def playlist_detail(request, playlist_id):
    """Playlist detail page view"""
    from playlists.models import Playlist
    from django.shortcuts import get_object_or_404
    
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    songs = playlist.songs.all()
    
    return render(request, 'playlists/playlist_detail.html', {
        'playlist': playlist,
        'songs': songs
    })
