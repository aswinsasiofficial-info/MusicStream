"""
Test script to verify Jamendo API integration
Run this to test your API configuration
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_Settings.settings')
django.setup()

from music.services.jamendo import jamendo


def test_api_configuration():
    """Test if Jamendo API is configured correctly"""
    print("=" * 60)
    print("Jamendo API Configuration Test")
    print("=" * 60)
    print()
    
    # Check if CLIENT_ID is set
    client_id = jamendo.client_id
    
    if not client_id:
        print("❌ ERROR: JAMENDO_CLIENT_ID is not configured!")
        print()
        print("To fix this:")
        print("1. Get a free API key from: https://devportal.jamendo.com/")
        print("2. Create/edit the .env file in your project root")
        print("3. Add: JAMENDO_CLIENT_ID=your_actual_client_id")
        print()
        return False
    
    print(f"✅ CLIENT_ID found: {client_id[:10]}...")
    print()
    return True


def test_search():
    """Test searching for tracks"""
    print("Testing search functionality...")
    print("-" * 60)
    
    query = "test"
    print(f"Searching for: '{query}'")
    
    try:
        results = jamendo.search_tracks(query, limit=5)
        
        if not results:
            print("⚠️  No results returned (this might be normal)")
            print("   The API might be rate-limited or the query returned nothing")
            return False
        
        print(f"✅ Found {len(results)} results")
        print()
        
        # Display first result
        track = results[0]
        print("Sample result:")
        print(f"  Title: {track.get('title', 'N/A')}")
        print(f"  Artist: {track.get('artist', 'N/A')}")
        print(f"  Album: {track.get('album', 'N/A')}")
        print(f"  Duration: {track.get('duration', 'N/A')} seconds")
        print(f"  Has audio URL: {'Yes' if track.get('audio_url') else 'No'}")
        print(f"  Has thumbnail: {'Yes' if track.get('thumbnail') else 'No'}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR during search: {str(e)}")
        print()
        return False


def test_popular_tracks():
    """Test getting popular tracks"""
    print("Testing popular tracks...")
    print("-" * 60)
    
    try:
        popular = jamendo.get_popular_tracks(limit=5)
        
        if not popular:
            print("⚠️  No popular tracks returned")
            print("   This might indicate an API issue")
            return False
        
        print(f"✅ Found {len(popular)} popular tracks")
        print()
        
        # Display first result
        track = popular[0]
        print("Sample popular track:")
        print(f"  Title: {track.get('title', 'N/A')}")
        print(f"  Artist: {track.get('artist', 'N/A')}")
        print(f"  Has audio URL: {'Yes' if track.get('audio_url') else 'No'}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR getting popular tracks: {str(e)}")
        print()
        return False


def test_audio_urls():
    """Test if audio URLs are accessible"""
    print("Testing audio URL accessibility...")
    print("-" * 60)
    
    try:
        results = jamendo.search_tracks("rock", limit=3)
        
        if not results:
            print("⚠️  No tracks to test")
            return False
        
        all_valid = True
        for i, track in enumerate(results, 1):
            audio_url = track.get('audio_url', '')
            if audio_url:
                print(f"✅ Track {i}: Audio URL present")
                print(f"   URL: {audio_url[:50]}...")
            else:
                print(f"⚠️  Track {i}: No audio URL")
                all_valid = False
        
        print()
        return all_valid
        
    except Exception as e:
        print(f"❌ ERROR testing audio URLs: {str(e)}")
        print()
        return False


def run_all_tests():
    """Run all tests and report results"""
    print()
    
    # Test 1: Configuration
    config_ok = test_api_configuration()
    
    if not config_ok:
        print("🛑 Configuration test failed. Please fix before continuing.")
        return
    
    # Test 2: Search
    search_ok = test_search()
    
    # Test 3: Popular tracks
    popular_ok = test_popular_tracks()
    
    # Test 4: Audio URLs
    urls_ok = test_audio_urls()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Search: {'✅ PASS' if search_ok else '❌ FAIL'}")
    print(f"Popular Tracks: {'✅ PASS' if popular_ok else '❌ FAIL'}")
    print(f"Audio URLs: {'✅ PASS' if urls_ok else '❌ FAIL'}")
    print()
    
    if all([config_ok, search_ok, popular_ok, urls_ok]):
        print("🎉 All tests passed! Your Jamendo integration is working correctly.")
        print()
        print("You can now start the server with:")
        print("  python manage.py runserver")
        print()
        print("Then visit: http://127.0.0.1:8000/")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        print()
        print("Common issues:")
        print("  - Invalid or missing JAMENDO_CLIENT_ID")
        print("  - Network connectivity problems")
        print("  - API rate limiting")
        print("  - Temporary API downtime")
        print()
        print("Refer to JAMENDO_SETUP.md for troubleshooting steps.")
    
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
