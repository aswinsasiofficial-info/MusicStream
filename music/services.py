"""
YTMusic API Service for fetching music data from YouTube Music
"""
from ytmusicapi import YTMusic
import requests


class YTMusicService:
    """Service class to interact with YouTube Music API"""
    
    def __init__(self):
        self.ytmusic = YTMusic()
    
    def search(self, query, filter_type='songs', limit=20):
        """
        Search for music on YouTube Music
        
        Args:
            query: Search query string
            filter_type: Type of content to search (songs, albums, artists, playlists)
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        try:
            filters = {
                'songs': 'songs',
                'albums': 'albums',
                'artists': 'artists',
                'playlists': 'playlists'
            }
            
            search_filter = filters.get(filter_type, 'songs')
            results = self.ytmusic.search(query, filter=search_filter, limit=limit)
            
            # Process and standardize results
            processed_results = []
            for result in results:
                if result.get('_type') == 'song' or 'videoId' in result:
                    processed_results.append(self._process_song(result))
                elif result.get('_type') == 'album':
                    processed_results.append(self._process_album(result))
                elif result.get('_type') == 'artist':
                    processed_results.append(self._process_artist(result))
                elif result.get('_type') == 'playlist':
                    processed_results.append(self._process_playlist(result))
            
            return processed_results[:limit]
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def get_song(self, video_id):
        """Get detailed information about a song"""
        try:
            song = self.ytmusic.get_song(video_id)
            return self._process_song(song)
        except Exception as e:
            print(f"Error getting song: {e}")
            return None
    
    def get_artist(self, artist_id):
        """Get artist information and top songs"""
        try:
            artist = self.ytmusic.get_artist(artist_id)
            return {
                'id': artist_id,
                'name': artist.get('name', ''),
                'description': artist.get('description', ''),
                'subscribers': artist.get('subscribers', ''),
                'thumbnail': artist.get('thumbnails', [{}])[0].get('url', '') if artist.get('thumbnails') else '',
                'top_songs': [self._process_song(song) for song in artist.get('songs', [])[:10]],
            }
        except Exception as e:
            print(f"Error getting artist: {e}")
            return None
    
    def get_album(self, album_id):
        """Get album information and tracks"""
        try:
            album = self.ytmusic.get_album(album_id)
            return {
                'id': album_id,
                'title': album.get('title', ''),
                'artist': album.get('artists', [{}])[0].get('name', '') if album.get('artists') else '',
                'year': album.get('year', ''),
                'track_count': len(album.get('tracks', [])),
                'thumbnail': album.get('thumbnails', [{}])[0].get('url', '') if album.get('thumbnails') else '',
                'tracks': [self._process_song(track) for track in album.get('tracks', [])],
            }
        except Exception as e:
            print(f"Error getting album: {e}")
            return None
    
    def get_home(self):
        """Get home page content with recommendations"""
        try:
            home = self.ytmusic.get_home(limit=6)
            sections = []
            for section in home:
                sections.append({
                    'title': section.get('title', ''),
                    'contents': [self._process_item(content) for content in section.get('contents', [])[:10]]
                })
            return sections
        except Exception as e:
            print(f"Error getting home: {e}")
            return []
    
    def get_trending(self, country='US'):
        """Get trending songs"""
        try:
            # Use charts endpoint for trending
            charts = self.ytmusic.get_charts(country=country)
            trending_songs = charts.get('trending', {}).get('items', [])[:20]
            return [self._process_song(song) for song in trending_songs]
        except Exception as e:
            print(f"Error getting trending: {e}")
            return []
    
    def _process_song(self, data):
        """Process song data into standardized format"""
        # Handle different data structures from ytmusicapi
        video_id = (data.get('videoId') or 
                   data.get('id') or 
                   data.get('video_id') or
                   (data.get('videoDetails') or {}).get('videoId') or
                   '')
        
        # Get thumbnails - try multiple paths
        thumbnails = (data.get('thumbnails') or 
                     data.get('thumbnail') or
                     (data.get('videoDetails') or {}).get('thumbnail') or
                     [])
        
        thumbnail_url = ''
        if thumbnails:
            if isinstance(thumbnails, list) and len(thumbnails) > 0:
                # Use the largest thumbnail (usually last)
                thumbnail_url = thumbnails[-1].get('url', '')
            elif isinstance(thumbnails, dict):
                thumbnail_url = thumbnails.get('url', '')
        
        return {
            'id': video_id,
            'title': data.get('title', ''),
            'artist': self._get_artist_name(data),
            'album': data.get('album', {}).get('name', '') if isinstance(data.get('album'), dict) else '',
            'duration': data.get('duration') or (data.get('videoDetails') or {}).get('lengthSeconds', ''),
            'thumbnail': thumbnail_url,
            'video_id': video_id,
            'youtube_url': f"https://music.youtube.com/watch?v={video_id}",
            'type': 'song'
        }
    
    def _process_album(self, data):
        """Process album data into standardized format"""
        return {
            'id': data.get('browseId') or data.get('id', ''),
            'title': data.get('title', ''),
            'artist': self._get_artist_name(data),
            'year': data.get('year', ''),
            'thumbnail': data.get('thumbnails', [{}])[-1].get('url', '') if data.get('thumbnails') else '',
            'type': 'album',
        }
    
    def _process_artist(self, data):
        """Process artist data into standardized format"""
        return {
            'id': data.get('browseId') or data.get('artistId', ''),
            'name': data.get('artist', ''),
            'thumbnail': data.get('thumbnails', [{}])[-1].get('url', '') if data.get('thumbnails') else '',
            'subscribers': data.get('subscribers', ''),
            'type': 'artist',
        }
    
    def _process_playlist(self, data):
        """Process playlist data into standardized format"""
        return {
            'id': data.get('browseId') or data.get('playlistId', ''),
            'title': data.get('title', ''),
            'author': data.get('author', ''),
            'item_count': data.get('itemCount', 0),
            'thumbnail': data.get('thumbnails', [{}])[-1].get('url', '') if data.get('thumbnails') else '',
            'type': 'playlist',
        }
    
    def _get_artist_name(self, data):
        """Extract artist name from data"""
        if isinstance(data.get('artists'), list) and len(data['artists']) > 0:
            return data['artists'][0].get('name', '')
        elif isinstance(data.get('artist'), str):
            return data.get('artist', '')
        return ''
    
    def _process_item(self, item):
        """Generic processor for any item type"""
        if 'videoId' in item:
            return self._process_song(item)
        elif 'browseId' in item or 'playlistId' in item:
            if item.get('type') == 'album':
                return self._process_album(item)
            elif item.get('type') == 'artist':
                return self._process_artist(item)
            elif item.get('type') == 'playlist':
                return self._process_playlist(item)
        return {}


# Global instance
yt_music = YTMusicService()
