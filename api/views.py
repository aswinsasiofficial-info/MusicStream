from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from playlists.models import Playlist, PlaylistSong, RecentlyPlayed, FavoriteSong
from .serializers import (
    PlaylistSerializer, 
    PlaylistSongSerializer, 
    RecentlyPlayedSerializer,
    FavoriteSongSerializer
)


class PlaylistViewSet(viewsets.ModelViewSet):
    """Viewset for managing playlists"""
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlaylistSongViewSet(viewsets.ViewSet):
    """Viewset for managing playlist songs"""
    permission_classes = [IsAuthenticated]
    
    def create(self, request, playlist_id=None):
        """Add a song to playlist"""
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        
        data = request.data.copy()
        data['playlist'] = playlist.id
        
        serializer = PlaylistSongSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, playlist_id=None, pk=None):
        """Remove a song from playlist"""
        playlist_song = get_object_or_404(
            PlaylistSong, 
            id=pk, 
            playlist__id=playlist_id,
            playlist__user=request.user
        )
        playlist_song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recently_played(request):
    """Get user's recently played songs"""
    recent = RecentlyPlayed.objects.filter(user=request.user)[:50]
    serializer = RecentlyPlayedSerializer(recent, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_recently_played(request):
    """Add a song to recently played"""
    serializer = RecentlyPlayedSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorite_songs(request):
    """Get or add favorite songs"""
    if request.method == 'GET':
        favorites = FavoriteSong.objects.filter(user=request.user)
        serializer = FavoriteSongSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Check if already favorited
        existing = FavoriteSong.objects.filter(
            user=request.user, 
            song_id=request.data.get('song_id')
        ).first()
        
        if existing:
            return Response({'message': 'Already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FavoriteSongSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, song_id):
    """Remove a song from favorites"""
    favorite = FavoriteSong.objects.filter(
        user=request.user, 
        song_id=song_id
    ).first()
    
    if favorite:
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
