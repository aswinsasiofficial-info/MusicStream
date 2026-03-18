from django.contrib import admin
from .models import Playlist, PlaylistSong, RecentlyPlayed, FavoriteSong


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'song_count', 'is_public', 'created_at', 'updated_at']
    list_filter = ['is_public', 'created_at', 'updated_at']
    search_fields = ['name', 'user__email', 'description']
    ordering = ['-updated_at']
    
    def song_count(self, obj):
        return obj.songs.count()
    song_count.short_description = 'Songs'


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'playlist', 'added_at']
    list_filter = ['playlist', 'added_at']
    search_fields = ['title', 'artist', 'playlist__name']
    ordering = ['-added_at']


@admin.register(RecentlyPlayed)
class RecentlyPlayedAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'user', 'played_at']
    list_filter = ['user', 'played_at']
    search_fields = ['title', 'artist', 'user__email']
    ordering = ['-played_at']


@admin.register(FavoriteSong)
class FavoriteSongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'user', 'added_at']
    list_filter = ['user', 'added_at']
    search_fields = ['title', 'artist', 'user__email']
    ordering = ['-added_at']
