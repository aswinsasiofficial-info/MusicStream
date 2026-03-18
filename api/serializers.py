from rest_framework import serializers
from playlists.models import Playlist, PlaylistSong, RecentlyPlayed, FavoriteSong


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer for Playlist model"""
    song_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 'thumbnail', 'created_at', 
                  'updated_at', 'is_public', 'song_count']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_song_count(self, obj):
        return obj.songs.count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PlaylistSongSerializer(serializers.ModelSerializer):
    """Serializer for PlaylistSong model"""
    
    class Meta:
        model = PlaylistSong
        fields = ['id', 'playlist', 'song_id', 'title', 'artist', 'album', 
                  'duration', 'thumbnail', 'added_at']
        read_only_fields = ['id', 'added_at']


class RecentlyPlayedSerializer(serializers.ModelSerializer):
    """Serializer for RecentlyPlayed model"""
    
    class Meta:
        model = RecentlyPlayed
        fields = ['id', 'song_id', 'title', 'artist', 'album', 
                  'duration', 'thumbnail', 'played_at']
        read_only_fields = ['id', 'played_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # Check if already exists, update if so
        obj, created = RecentlyPlayed.objects.update_or_create(
            user=validated_data['user'],
            song_id=validated_data['song_id'],
            defaults=validated_data
        )
        return obj


class FavoriteSongSerializer(serializers.ModelSerializer):
    """Serializer for FavoriteSong model"""
    
    class Meta:
        model = FavoriteSong
        fields = ['id', 'song_id', 'title', 'artist', 'album', 
                  'duration', 'thumbnail', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
