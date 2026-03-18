from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlaylistViewSet, 
    PlaylistSongViewSet, 
    recently_played, 
    add_recently_played,
    favorite_songs,
    remove_favorite
)

router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'playlist-songs', PlaylistSongViewSet, basename='playlist-song')

urlpatterns = [
    path('', include(router.urls)),
    path('recently-played/', recently_played, name='recently_played'),
    path('recently-played/add/', add_recently_played, name='add_recently_played'),
    path('favorites/', favorite_songs, name='favorite_songs'),
    path('favorites/<str:song_id>/', remove_favorite, name='remove_favorite'),
]
