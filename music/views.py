from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
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
    """Search page view"""
    return render(request, 'music/search.html')


def library(request):
    """User library view"""
    return render(request, 'playlists/library.html')


@require_http_methods(["GET"])
@cache_page(60 * 10)  # Cache for 10 minutes
def search_api(request):
    """Search API endpoint"""
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', 'songs')
    limit = int(request.GET.get('limit', '20'))
    
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    
    from music.services import yt_music
    
    try:
        results = yt_music.search(query, filter_type=filter_type, limit=limit)
        return JsonResponse({'results': results})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def trending_api(request):
    """Trending songs API endpoint"""
    from music.services import yt_music
    
    try:
        trending = yt_music.get_trending()
        return JsonResponse({'trending': trending})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def home_content_api(request):
    """Home page content API"""
    from music.services import yt_music
    
    try:
        content = yt_music.get_home()
        return JsonResponse({'content': content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def song_detail_api(request, song_id):
    """Get detailed song information"""
    from music.services import yt_music
    
    try:
        song = yt_music.get_song(song_id)
        if song:
            return JsonResponse(song)
        return JsonResponse({'error': 'Song not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
