/**
 * Main JavaScript file for MusicStream
 * Handles UI interactions, API calls, and general functionality
 */

// CSRF token helper
function getCookie(name) {
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

// Load user playlists for sidebar
async function loadUserPlaylists() {
    try {
        const response = await fetch('/api/playlists/');
        const data = await response.json();
        
        const container = document.getElementById('user-playlists');
        if (!container) return;
        
        if (data.length === 0) {
            container.innerHTML = '<p class="text-secondary px-3">No playlists yet</p>';
            return;
        }
        
        container.innerHTML = '';
        data.forEach(playlist => {
            const link = document.createElement('a');
            link.href = `/playlist/${playlist.id}/`;
            link.className = 'nav-link text-secondary';
            link.style.cssText = 'padding: 8px 16px; font-size: 14px;';
            link.innerHTML = `
                <i class="bi bi-music-note-list"></i>
                <span>${playlist.name}</span>
            `;
            container.appendChild(link);
        });
    } catch (error) {
        console.error('Error loading playlists:', error);
    }
}

// Create playlist
async function createPlaylist(name, description = '') {
    try {
        const response = await fetch('/api/playlists/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: name,
                description: description
            })
        });
        
        if (response.ok) {
            const playlist = await response.json();
            loadUserPlaylists(); // Refresh playlist list
            return playlist;
        } else {
            throw new Error('Failed to create playlist');
        }
    } catch (error) {
        console.error('Error creating playlist:', error);
        alert('Failed to create playlist. Please try again.');
        return null;
    }
}

// Add song to playlist
async function addSongToPlaylist(playlistId, song) {
    try {
        const response = await fetch(`/api/playlist-songs/${playlistId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
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
        
        if (response.ok) {
            return true;
        } else {
            throw new Error('Failed to add song to playlist');
        }
    } catch (error) {
        console.error('Error adding song to playlist:', error);
        alert('Failed to add song to playlist. Please try again.');
        return false;
    }
}

// Initialize create playlist modal
function initCreatePlaylistModal() {
    const createBtn = document.getElementById('createPlaylistBtn');
    if (!createBtn) return;
    
    createBtn.addEventListener('click', async () => {
        const nameInput = document.getElementById('playlistName');
        const descInput = document.getElementById('playlistDescription');
        
        const name = nameInput.value.trim();
        const description = descInput.value.trim();
        
        if (!name) {
            alert('Please enter a playlist name');
            return;
        }
        
        const playlist = await createPlaylist(name, description);
        
        if (playlist) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('createPlaylistModal'));
            if (modal) modal.hide();
            
            // Clear form
            nameInput.value = '';
            descInput.value = '';
            
            // Reload playlists
            loadUserPlaylists();
        }
    });
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Infinite scroll handler
function setupInfiniteScroll(callback) {
    let page = 1;
    let isLoading = false;
    
    window.addEventListener('scroll', () => {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        
        if (scrollTop + clientHeight >= scrollHeight - 5 && !isLoading) {
            isLoading = true;
            page++;
            callback(page).then(() => {
                isLoading = false;
            });
        }
    });
}

// Format duration from seconds to MM:SS
function formatDuration(seconds) {
    if (!seconds) return '';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Parse duration string to seconds
function parseDuration(durationStr) {
    if (!durationStr) return 0;
    const parts = durationStr.split(':');
    if (parts.length === 2) {
        return parseInt(parts[0]) * 60 + parseInt(parts[1]);
    } else if (parts.length === 3) {
        return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60 + parseInt(parts[2]);
    }
    return 0;
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.messages-container');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Lazy load images
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize create playlist modal
    initCreatePlaylistModal();
    
    // Setup lazy loading for images
    setupLazyLoading();
    
    // Add smooth transitions
    document.body.classList.add('loaded');
    
    // Check if we need to update the player with current song
    const currentSongData = localStorage.getItem('currentSong');
    if (currentSongData && window.musicPlayer) {
        try {
            const song = JSON.parse(currentSongData);
            // Don't auto-play, just restore state
            console.log('Restored song state:', song);
        } catch (e) {
            console.error('Error restoring song state:', e);
        }
    }
});

// Save current song to localStorage for persistence
function saveCurrentSong(song) {
    try {
        localStorage.setItem('currentSong', JSON.stringify(song));
    } catch (e) {
        console.error('Error saving song state:', e);
    }
}

// Clear saved song state
function clearSavedSong() {
    try {
        localStorage.removeItem('currentSong');
    } catch (e) {
        console.error('Error clearing song state:', e);
    }
}

// Export functions for use in other scripts
window.MusicStream = {
    loadUserPlaylists,
    createPlaylist,
    addSongToPlaylist,
    getCookie,
    debounce,
    setupInfiniteScroll,
    formatDuration,
    parseDuration,
    showToast,
    saveCurrentSong,
    clearSavedSong
};
