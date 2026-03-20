/**
 * Music Player Controller
 * Handles audio playback, controls, and state management
 */

class MusicPlayer {
    constructor() {
        this.audio = new Audio();
        this.isPlaying = false;
        this.currentSong = null;
        this.queue = [];
        this.currentIndex = 0;
        this.isShuffle = false;
        this.repeatMode = 'none'; // 'none', 'all', 'one'
        
        this.initElements();
        this.initEventListeners();
        this.initAudioEvents();
    }
    
    initElements() {
        // Player elements
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.shuffleBtn = document.getElementById('shuffleBtn');
        this.repeatBtn = document.getElementById('repeatBtn');
        this.likeBtn = document.getElementById('likeBtn');
        this.volumeSlider = document.getElementById('volumeSlider');
        this.progressBar = document.getElementById('progressBar');
        this.progressFill = document.getElementById('progressFill');
        
        // Now playing info
        this.currentThumbnail = document.getElementById('currentThumbnail');
        this.currentTitle = document.getElementById('currentTitle');
        this.currentArtist = document.getElementById('currentArtist');
        
        // Set initial volume
        if (this.volumeSlider) {
            this.audio.volume = this.volumeSlider.value / 100;
        }
    }
    
    initEventListeners() {
        // Play/Pause button
        if (this.playPauseBtn) {
            this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        }
        
        // Previous/Next buttons
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.playPrevious());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.playNext());
        }
        
        // Shuffle button
        if (this.shuffleBtn) {
            this.shuffleBtn.addEventListener('click', () => this.toggleShuffle());
        }
        
        // Repeat button
        if (this.repeatBtn) {
            this.repeatBtn.addEventListener('click', () => this.toggleRepeat());
        }
        
        // Like button
        if (this.likeBtn) {
            this.likeBtn.addEventListener('click', () => this.toggleLike());
        }
        
        // Volume slider
        if (this.volumeSlider) {
            this.volumeSlider.addEventListener('input', (e) => {
                const volume = e.target.value;
                // Update HTML5 audio volume
                this.audio.volume = volume / 100;
                // Update YouTube player volume
                if (window.youTubePlayer && window.youTubePlayer.setVolume) {
                    window.youTubePlayer.setVolume(parseInt(volume));
                }
            });
        }
        
        // Progress bar
        if (this.progressBar) {
            this.progressBar.addEventListener('click', (e) => {
                const rect = this.progressBar.getBoundingClientRect();
                const percent = (e.clientX - rect.left) / rect.width;
                this.audio.currentTime = percent * this.audio.duration;
            });
        }
    }
    
    initAudioEvents() {
        // Time update - update progress bar
        this.audio.addEventListener('timeupdate', () => {
            if (this.progressFill && this.audio.duration) {
                const percent = (this.audio.currentTime / this.audio.duration) * 100;
                this.progressFill.style.width = `${percent}%`;
            }
        });
        
        // Song ended
        this.audio.addEventListener('ended', () => {
            this.handleSongEnd();
        });
        
        // Loaded metadata
        this.audio.addEventListener('loadedmetadata', () => {
            this.updateDuration();
        });
        
        // Error handling
        this.audio.addEventListener('error', (e) => {
            console.error('Audio error event:', e);
            const error = this.audio.error;
            let message = 'Audio error occurred';
            
            if (error) {
                switch (error.code) {
                    case error.MEDIA_ERR_ABORTED:
                        message = 'Playback aborted by user';
                        break;
                    case error.MEDIA_ERR_NETWORK:
                        message = 'Network error while loading audio';
                        break;
                    case error.MEDIA_ERR_DECODE:
                        message = 'Audio decoding failed';
                        break;
                    case error.MEDIA_ERR_SRC_NOT_SUPPORTED:
                        message = 'Audio format not supported or file not found';
                        break;
                }
            }
            showToast(message, 'danger');
        });
    }
    
    loadAndPlay(song) {
        if (!song) return;
        
        // Stop current playback before starting new one
        if (this.currentSong && this.currentSong.audio_url) {
            this.audio.pause();
            this.audio.src = '';
        } else if (window.youTubePlayer && window.youTubePlayer.stopVideo) {
            window.youTubePlayer.stopVideo();
        }
        
        this.currentSong = song;
        
        // Update UI
        if (this.currentThumbnail) {
            this.currentThumbnail.src = song.thumbnail || 'https://via.placeholder.com/56';
        }
        if (this.currentTitle) {
            this.currentTitle.textContent = song.title;
        }
        if (this.currentArtist) {
            this.currentArtist.textContent = song.artist;
        }
        
        // Check if it's a Jamendo track (has audio_url)
        if (song.audio_url) {
            console.log('🎵 Playing Jamendo track:', song.title, '| ID:', song.id);
            this.playJamendoTrack(song.audio_url);
        } else {
            // Fallback to YouTube player
            const videoId = song.video_id || song.id;
            console.log('🎵 Attempting to play via YouTube:', song.title, '| Video ID:', videoId);
            
            if (videoId && window.youTubePlayer) {
                window.youTubePlayer.playVideo(videoId);
                
                // Show toast notification
                showToast(`Playing: ${song.title} by ${song.artist}`, 'success');
            } else {
                console.error('✗ No video ID or player not available');
                showToast('Unable to play song - no audio source', 'danger');
            }
        }
    }
    
    playJamendoTrack(audioUrl) {
        // Load and play Jamendo MP3 stream
        if (!audioUrl) {
            showToast('No audio URL available', 'danger');
            return;
        }
        
        console.log('🔊 Loading audio from:', audioUrl);
        
        // Stop any current playback
        this.audio.pause();
        
        // Set audio source
        this.audio.src = audioUrl;
        this.audio.load(); // Explicitly load the new source
        
        // Play the audio
        this.audio.play().then(() => {
            this.isPlaying = true;
            this.updatePlayPauseButton();
            showToast(`Playing: ${this.currentSong.title} by ${this.currentSong.artist}`, 'success');
        }).catch(error => {
            console.error('Error playing audio:', error);
            
            // Provide more specific error message based on the error
            let message = 'Error loading audio stream';
            if (error.name === 'NotAllowedError') {
                message = 'Playback blocked by browser. Please click play to start.';
            } else if (error.name === 'NotSupportedError') {
                message = 'Audio format not supported by your browser.';
            }
            
            showToast(message, 'danger');
        });
    }
    
    getStreamUrl(song) {
        // Since we can't directly stream copyrighted content from YouTube,
        // we'll use a preview URL or redirect to YouTube Music
        // This is a placeholder for where you'd integrate with a proper streaming service
        
        // Option 1: Use YouTube embed (requires iframe, not audio element)
        // Option 2: Use a third-party service that provides music previews
        // Option 3: Backend proxy to fetch and serve audio stream
        
        // For now, return null to trigger the notice
        return null;
    }
    
    showStreamingNotice(song) {
        // Display a message that the song would play in a real implementation
        console.log('Would play:', song);
        
        // Update UI to show "playing" state
        this.isPlaying = true;
        this.updatePlayPauseButton();
        
        // Show toast notification
        showToast(`Playing: ${song.title} by ${song.artist}`, 'success');
    }
    
    play() {
        if (this.currentSong && this.currentSong.audio_url) {
            // Jamendo track
            this.audio.play().then(() => {
                this.isPlaying = true;
                this.updatePlayPauseButton();
            }).catch(error => {
                console.error('Error playing Jamendo track:', error);
            });
        } else if (window.youTubePlayer && window.youTubePlayer.resumeVideo) {
            // YouTube track
            window.youTubePlayer.resumeVideo();
            this.isPlaying = true;
            this.updatePlayPauseButton();
        }
    }
    
    pause() {
        if (this.currentSong && this.currentSong.audio_url) {
            // Jamendo track
            this.audio.pause();
        } else if (window.youTubePlayer && window.youTubePlayer.pauseVideo) {
            // YouTube track
            window.youTubePlayer.pauseVideo();
        }
        this.isPlaying = false;
        this.updatePlayPauseButton();
    }
    
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    playPrevious() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.loadAndPlay(this.queue[this.currentIndex]);
        }
    }
    
    playNext() {
        if (this.currentIndex < this.queue.length - 1) {
            this.currentIndex++;
            this.loadAndPlay(this.queue[this.currentIndex]);
        } else if (this.repeatMode === 'all') {
            this.currentIndex = 0;
            this.loadAndPlay(this.queue[this.currentIndex]);
        }
    }
    
    toggleShuffle() {
        this.isShuffle = !this.isShuffle;
        if (this.shuffleBtn) {
            this.shuffleBtn.classList.toggle('active', this.isShuffle);
        }
        
        if (this.isShuffle) {
            // Shuffle the queue
            this.shuffleQueue();
        }
    }
    
    shuffleQueue() {
        // Fisher-Yates shuffle
        for (let i = this.queue.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.queue[i], this.queue[j]] = [this.queue[j], this.queue[i]];
        }
    }
    
    toggleRepeat() {
        // Cycle through: none -> all -> one -> none
        const modes = ['none', 'all', 'one'];
        const currentIndex = modes.indexOf(this.repeatMode);
        this.repeatMode = modes[(currentIndex + 1) % modes.length];
        
        if (this.repeatBtn) {
            this.repeatBtn.innerHTML = this.getRepeatIcon();
        }
    }
    
    getRepeatIcon() {
        switch (this.repeatMode) {
            case 'all':
                return '<i class="bi bi-repeat"></i>';
            case 'one':
                return '<i class="bi bi-repeat-1"></i>';
            default:
                return '<i class="bi bi-repeat"></i>';
        }
    }
    
    handleSongEnd() {
        if (this.repeatMode === 'one') {
            this.audio.currentTime = 0;
            this.play();
        } else if (this.repeatMode === 'all' || this.currentIndex < this.queue.length - 1) {
            this.playNext();
        }
    }
    
    toggleLike() {
        if (!this.currentSong) return;
        
        if (this.likeBtn) {
            this.likeBtn.classList.toggle('liked');
            const isLiked = this.likeBtn.classList.contains('liked');
            
            // Save to favorites
            if (isLiked) {
                this.addToFavorites(this.currentSong);
            } else {
                this.removeFromFavorites(this.currentSong);
            }
        }
    }
    
    async addToFavorites(song) {
        try {
            await fetch('/api/favorites/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    song_id: song.id || song.video_id,
                    title: song.title,
                    artist: song.artist,
                    album: song.album || '',
                    duration: song.duration || '',
                    thumbnail: song.thumbnail
                })
            });
        } catch (error) {
            console.error('Error adding to favorites:', error);
        }
    }
    
    async removeFromFavorites(song) {
        try {
            await fetch(`/api/favorites/${song.id || song.video_id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            });
        } catch (error) {
            console.error('Error removing from favorites:', error);
        }
    }
    
    updatePlayPauseButton() {
        if (!this.playPauseBtn) return;
        
        const icon = this.playPauseBtn.querySelector('i');
        if (this.isPlaying) {
            icon.className = 'bi bi-pause-fill';
        } else {
            icon.className = 'bi bi-play-fill';
        }
    }
    
    updateDuration() {
        // Could display current time and total duration here
    }
    
    showError() {
        console.error('Error loading audio');
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize player when DOM is ready
let musicPlayer;
document.addEventListener('DOMContentLoaded', function() {
    musicPlayer = new MusicPlayer();
    window.musicPlayer = musicPlayer;
});
