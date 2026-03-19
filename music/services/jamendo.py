"""
Jamendo API Service for fetching music data from Jamendo
Documentation: https://api.jamendo.com/v3.0/
"""
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class JamendoService:
    """Service class to interact with Jamendo API"""
    
    BASE_URL = "https://api.jamendo.com/v3.0"
    
    def __init__(self):
        self.client_id = getattr(settings, 'JAMENDO_CLIENT_ID', None)
        if not self.client_id:
            logger.warning("JAMENDO_CLIENT_ID not configured in settings")
        
    def search_tracks(self, query, limit=20):
        """
        Search for tracks on Jamendo
        
        Args:
            query: Search query string
            limit: Maximum number of results (default: 20)
            
        Returns:
            List of track results in standardized format
        """
        if not query or not self.client_id:
            return []
        
        url = f"{self.BASE_URL}/tracks/"
        params = {
            'client_id': self.client_id,
            'search': query,
            'limit': limit,
            'audioformat': 'mp31',  # MP3 format
            'include': 'musicinfo',  # Include additional music info
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for track in data.get('results', []):
                processed = self._process_track(track)
                if processed:
                    results.append(processed)
            
            return results
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout searching for '{query}'")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching tracks: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
    
    def get_track_by_id(self, track_id):
        """
        Get detailed information about a specific track
        
        Args:
            track_id: Jamendo track ID
            
        Returns:
            Track details in standardized format
        """
        if not track_id or not self.client_id:
            return None
        
        url = f"{self.BASE_URL}/tracks/"
        params = {
            'client_id': self.client_id,
            'id': track_id,
            'audioformat': 'mp31',
            'include': 'musicinfo',
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results'):
                return self._process_track(data['results'][0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting track {track_id}: {e}")
            return None
    
    def get_popular_tracks(self, limit=20):
        """
        Get popular/trending tracks
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of popular tracks
        """
        if not self.client_id:
            return []
        
        url = f"{self.BASE_URL}/tracks/"
        params = {
            'client_id': self.client_id,
            'order': 'popularity_week',
            'limit': limit,
            'audioformat': 'mp31',
            'include': 'musicinfo',
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for track in data.get('results', []):
                processed = self._process_track(track)
                if processed:
                    results.append(processed)
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting popular tracks: {e}")
            return []
    
    def _process_track(self, data):
        """
        Process track data into standardized format
        
        Args:
            data: Raw track data from Jamendo API
            
        Returns:
            Standardized track dictionary
        """
        if not data:
            return None
        
        # Get audio URL - Jamendo provides audiodownload for full track
        audio_url = data.get('audio', '')
        if not audio_url:
            # Fallback to download URL if audio not available
            audio_url = data.get('audiodownload', '')
        
        # Get image - use album image if available
        image_url = ''
        if data.get('album_image'):
            # Try to get larger image
            images = data['album_image']
            if isinstance(images, dict):
                # Prefer larger sizes
                image_url = images.get('500x500-1', '') or images.get('300x300-1', '') or images.get('100x100-1', '')
            elif isinstance(images, str):
                image_url = images
        
        return {
            'id': str(data.get('id', '')),
            'title': data.get('name', ''),
            'artist': data.get('artist_name', ''),
            'album': data.get('album_name', ''),
            'duration': data.get('duration', 0),
            'thumbnail': image_url,
            'audio_url': audio_url,
            'jamendo_url': f"https://www.jamendo.com/track/{data.get('id', '')}",
            'type': 'song',
            'license': data.get('license_ccurl', ''),
            'tags': data.get('musicinfo', {}).get('tags', {}).get('tags', []) if data.get('musicinfo') else [],
        }


# Global instance
jamendo = JamendoService()
