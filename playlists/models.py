from django.db import models
from django.conf import settings


class Playlist(models.Model):
    """User playlist model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    thumbnail = models.URLField(blank=True, null=True, help_text="YouTube thumbnail URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'playlists'
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name
    
    def song_count(self):
        return self.songs.count()


class PlaylistSong(models.Model):
    """Many-to-many relationship between playlists and songs"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    song_id = models.CharField(max_length=100)  # YouTube Music video ID
    title = models.CharField(max_length=300)
    artist = models.CharField(max_length=300)
    album = models.CharField(max_length=300, blank=True, default='')
    duration = models.CharField(max_length=20, blank=True, default='')
    thumbnail = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'playlist_songs'
        verbose_name = 'Playlist Song'
        verbose_name_plural = 'Playlist Songs'
        unique_together = ['playlist', 'song_id']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"


class RecentlyPlayed(models.Model):
    """Track recently played songs for each user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recently_played')
    song_id = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    artist = models.CharField(max_length=300)
    album = models.CharField(max_length=300, blank=True, default='')
    duration = models.CharField(max_length=20, blank=True, default='')
    thumbnail = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    played_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recently_played'
        verbose_name = 'Recently Played'
        verbose_name_plural = 'Recently Played'
        ordering = ['-played_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"


class FavoriteSong(models.Model):
    """User's favorite/liked songs"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_songs')
    song_id = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    artist = models.CharField(max_length=300)
    album = models.CharField(max_length=300, blank=True, default='')
    duration = models.CharField(max_length=20, blank=True, default='')
    thumbnail = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favorite_songs'
        verbose_name = 'Favorite Song'
        verbose_name_plural = 'Favorite Songs'
        unique_together = ['user', 'song_id']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
