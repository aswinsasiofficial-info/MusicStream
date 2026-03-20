from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from playlists.models import RecentlyPlayed, FavoriteSong, Playlist, PlaylistSong
from music.services.jamendo import jamendo
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with some starter songs for all users'

    def handle(self, *args, **options):
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found. Please create a user first.'))
            return

        self.stdout.write('Fetching popular tracks from Jamendo...')
        tracks = jamendo.get_popular_tracks(limit=30)
        
        if not tracks:
            self.stdout.write(self.style.ERROR('Failed to fetch tracks from Jamendo. Check your API key.'))
            return

        for user in users:
            self.stdout.write(f'Populating data for user: {user.email}')
            
            # Add some recently played songs
            recent_tracks = random.sample(tracks, min(len(tracks), 10))
            for track in recent_tracks:
                RecentlyPlayed.objects.update_or_create(
                    user=user,
                    song_id=track['id'],
                    defaults={
                        'title': track['title'],
                        'artist': track['artist'],
                        'album': track['album'],
                        'duration': str(track['duration']),
                        'thumbnail': track['thumbnail'],
                        'audio_url': track['audio_url']
                    }
                )
            
            # Add some favorite songs
            fav_tracks = random.sample(tracks, min(len(tracks), 5))
            for track in fav_tracks:
                FavoriteSong.objects.update_or_create(
                    user=user,
                    song_id=track['id'],
                    defaults={
                        'title': track['title'],
                        'artist': track['artist'],
                        'album': track['album'],
                        'duration': str(track['duration']),
                        'thumbnail': track['thumbnail'],
                        'audio_url': track['audio_url']
                    }
                )
                
            # Create a "My Favorites" playlist if it doesn't exist
            playlist, created = Playlist.objects.get_or_create(
                user=user,
                name='My Favorites',
                defaults={'description': 'My favorite songs from Jamendo'}
            )
            
            # Add songs to the playlist
            playlist_tracks = random.sample(tracks, min(len(tracks), 8))
            for track in playlist_tracks:
                PlaylistSong.objects.get_or_create(
                    playlist=playlist,
                    song_id=track['id'],
                    defaults={
                        'title': track['title'],
                        'artist': track['artist'],
                        'album': track['album'],
                        'duration': str(track['duration']),
                        'thumbnail': track['thumbnail'],
                        'audio_url': track['audio_url']
                    }
                )
                
            if created:
                # Set the first song's thumbnail as the playlist thumbnail
                if playlist_tracks:
                    playlist.thumbnail = playlist_tracks[0]['thumbnail']
                    playlist.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated starter songs for all users!'))
