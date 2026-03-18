/**
 * YouTube Player Integration
 * Embeds YouTube player for actual audio streaming
 */

class YouTubePlayer {
    constructor() {
        this.player = null;
        this.currentVideoId = null;
        this.isPlaying = false;
        
        // Load YouTube IFrame API
        this.loadYouTubeAPI();
    }
    
    loadYouTubeAPI() {
        // Check if API is already loaded
        if (window.YT && window.YT.Player) {
            this.onYouTubeIframeAPIReady();
            return;
        }
        
        // Load the IFrame Player API code asynchronously
        const tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
    
    onYouTubeIframeAPIReady() {
        // Create invisible player container (but keep it functional)
        let playerContainer = document.getElementById('youtube-player-container');
        if (!playerContainer) {
            playerContainer = document.createElement('div');
            playerContainer.id = 'youtube-player-container';
            // Make it invisible but still functional
            playerContainer.style.cssText = 'position: absolute; top: -9999px; left: -9999px; visibility: hidden;';
            document.body.appendChild(playerContainer);
        }
        
        // Initialize player with better settings for audio-only
        this.player = new YT.Player('youtube-player-container', {
            height: '200',
            width: '200',
            videoId: '',
            playerVars: {
                'autoplay': 1,
                'controls': 0,
                'modestbranding': 1,
                'rel': 0,
                'iv_load_policy': 3, // Hide annotations
                'fs': 0 // Hide fullscreen button
            },
            events: {
                'onReady': this.onPlayerReady.bind(this),
                'onStateChange': this.onPlayerStateChange.bind(this),
                'onError': this.onPlayerError.bind(this)
            }
        });
    }
    
    onPlayerReady(event) {
        console.log('✓ YouTube player ready');
        // Set initial volume
        this.player.setVolume(100);
    }
    
    onPlayerError(event) {
        console.error('✗ YouTube player error:', event.data);
        const errorMessages = {
            2: 'Invalid video ID',
            5: 'HTML5 playback error',
            100: 'Video not found',
            101: 'Video cannot be played in embedded player',
            150: 'Video cannot be played in embedded player'
        };
        const message = errorMessages[event.data] || 'Unknown error';
        showToast(`Playback error: ${message}`, 'danger');
    }
    
    onPlayerStateChange(event) {
        // YT.PlayerState.PLAYING = 1
        // YT.PlayerState.PAUSED = 2
        // YT.PlayerState.ENDED = 0
        
        if (event.data === YT.PlayerState.PLAYING) {
            this.isPlaying = true;
            if (window.musicPlayer) {
                window.musicPlayer.updatePlayPauseButton();
            }
        } else if (event.data === YT.PlayerState.PAUSED) {
            this.isPlaying = false;
            if (window.musicPlayer) {
                window.musicPlayer.updatePlayPauseButton();
            }
        } else if (event.data === YT.PlayerState.ENDED) {
            this.isPlaying = false;
            if (window.musicPlayer) {
                window.musicPlayer.handleSongEnd();
            }
        }
    }
    
    playVideo(videoId) {
        if (!this.player || !this.player.loadVideoById) {
            console.error('✗ YouTube player not initialized');
            showToast('Player not ready, please wait a moment...', 'warning');
            return;
        }
        
        console.log('▶ Playing video:', videoId);
        this.currentVideoId = videoId;
        
        // Use loadVideoById which automatically starts playing
        this.player.loadVideoById(videoId);
        this.isPlaying = true;
        
        // Double-check playback after a short delay
        setTimeout(() => {
            const playerState = this.player.getPlayerState();
            if (playerState !== YT.PlayerState.PLAYING) {
                console.log('Retrying playback...');
                this.player.playVideo();
            }
        }, 500);
    }
    
    pauseVideo() {
        if (!this.player || !this.player.pauseVideo) return;
        
        this.player.pauseVideo();
        this.isPlaying = false;
    }
    
    resumeVideo() {
        if (!this.player || !this.player.playVideo) return;
        
        this.player.playVideo();
        this.isPlaying = true;
    }
    
    stopVideo() {
        if (!this.player || !this.player.stopVideo) return;
        
        this.player.stopVideo();
        this.isPlaying = false;
    }
    
    seekTo(seconds) {
        if (!this.player || !this.player.seekTo) return;
        
        this.player.seekTo(seconds, true);
    }
    
    getCurrentTime() {
        if (!this.player || !this.player.getCurrentTime) return 0;
        
        return this.player.getCurrentTime();
    }
    
    getDuration() {
        if (!this.player || !this.player.getDuration) return 0;
        
        return this.player.getDuration();
    }
    
    setVolume(volume) {
        if (!this.player || !this.player.setVolume) return;
        
        this.player.setVolume(volume);
    }
}

// Initialize YouTube player
const youTubePlayer = new YouTubePlayer();
window.youTubePlayer = youTubePlayer;
