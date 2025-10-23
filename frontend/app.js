// app.js - central SPA loader, music player, and render helpers

document.addEventListener('DOMContentLoaded', () => {
    initNavLinks();
    initHorizontalScroll();
    initMusicPlayer();

    // Example artists data and render on startup
    const artists = [
        { name: 'Rema', type: 'Artist', imageUrl: 'https://i.scdn.co/image/ab676161000051747952358e33599027ae3c7f37' },
        { name: 'Taylor Swift', type: 'Artist', imageUrl: 'https://www.billboard.com/wp-content/uploads/media/taylor-swift-press-wim-2019-cr-Valheria-Roche-billboard-1548.jpg?w=942&h=623&crop=1' },
        { name: 'The Weeknd', type: 'Artist', imageUrl: 'https://www.stereofox.com/wp-content/uploads/2016/05/the-weeknd-artist-profile.jpg' },
        { name: 'Beyonce', type: 'Artist', imageUrl: 'https://cdn.britannica.com/59/204159-050-5055F2A9/Beyonce-2013.jpg' },
    ];
    renderArtists(artists);
});

/* ---------------- SPA Navigation ---------------- */
function initNavLinks() {
    document.querySelectorAll('.nav .nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const page = link.dataset.page || link.getAttribute('href');
            if (!page || page === '#') return; // ignore non-page links
            e.preventDefault();
            loadPage(page, true);
        });
    });
}

async function loadPage(pagePath, push = true) {
    try {
        // If loading index.html and we're already on the index (no need to fetch)
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        if (pagePath === 'index.html' && (currentPath === '' || currentPath === 'index.html')) {
            updateActiveLink(pagePath);
            if (push) history.pushState({ page: pagePath }, '', './');
            return;
        }

        const res = await fetch(pagePath, { cache: 'no-store' });
        if (!res.ok) throw new Error('Failed to fetch ' + pagePath);
        const text = await res.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');

        // Prefer .main in fetched doc
        let newMain = doc.querySelector('.main');
        if (!newMain) {
            // fallback: use body content if no .main
            newMain = doc.body.cloneNode(true);
        }

        const currentMain = document.querySelector('.main');
        if (!currentMain) {
            console.warn('Current document has no .main to replace.');
            return;
        }

        // Replace current .main with the fetched one
        currentMain.parentNode.replaceChild(newMain, currentMain);

        // Update active nav link classes
        updateActiveLink(pagePath);

        // Push history state
        if (push) {
            const url = pagePath === 'index.html' ? './' : pagePath;
            window.history.pushState({ page: pagePath }, '', url);
        }

        // Reinitialize behaviors for newly injected content
        initHorizontalScroll();
        initMusicPlayer(); // re-wire player elements if present in the injected .main

    } catch (err) {
        console.error(err);
    }
}

window.addEventListener('popstate', (e) => {
    const path = window.location.pathname.split('/').pop() || 'index.html';
    const page = path === '' ? 'index.html' : path;
    loadPage(page, false);
});

function updateActiveLink(pagePath) {
    document.querySelectorAll('.nav .nav-link').forEach(n => n.classList.remove('active'));
    const match = document.querySelector('.nav .nav-link[data-page="' + pagePath + '"]') || document.querySelector('.nav .nav-link[href="' + pagePath + '"]');
    if (match) match.classList.add('active');
}

/* ---------------- Horizontal Scroll ---------------- */
function initHorizontalScroll(root = document) {
    root.querySelectorAll('.horizontal-scroll').forEach(el => {
        // ensure we don't attach duplicate listeners: remove existing by cloning
        const clone = el.cloneNode(true);
        el.parentNode.replaceChild(clone, el);
        clone.addEventListener('wheel', (e) => {
            if (e.deltaY === 0) return;
            e.preventDefault();
            clone.scrollLeft += e.deltaY;
        }, { passive: false });
    });
}

/* ---------------- Music Player ---------------- */
function initMusicPlayer() {
    const playPause = document.getElementById('play-pause');
    const audio = document.getElementById('audio-player');
    const progress = document.getElementById('progress');
    const currentTime = document.getElementById('current-time');
    const totalDuration = document.getElementById('total-duration');

    // Volume controls in the footer player
    const volumeBar = document.getElementById('volume-bar');
    const volumeProgress = document.getElementById('volume-progress');
    const volumeButton = document.querySelector('.player-volume-controls .control-btn-icon');
    let lastVolume = 0.5; // store previous volume for mute/unmute

    if (!audio || !playPause || !progress) return; // nothing to attach to

    // play/pause toggle
    playPause.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            playPause.innerHTML = '&#10074;&#10074;';
        } else {
            audio.pause();
            playPause.innerHTML = '&#9658;';
        }
    });

    // update progress and current time
    audio.addEventListener('timeupdate', () => {
        if (!audio.duration) return;
        const pct = (audio.currentTime / audio.duration) * 100;
        progress.style.width = pct + '%';
        if (currentTime) currentTime.textContent = formatTime(audio.currentTime);
        if (totalDuration) totalDuration.textContent = formatTime(audio.duration);
    });

    // click to seek on progress bar
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        progressBar.addEventListener('click', (e) => {
            const rect = progressBar.getBoundingClientRect();
            const pct = (e.clientX - rect.left) / rect.width;
            if (audio.duration) audio.currentTime = pct * audio.duration;
        });
    }

    // when metadata loads, set total duration
    audio.addEventListener('loadedmetadata', () => {
        if (totalDuration && audio.duration) totalDuration.textContent = formatTime(audio.duration);
    });

    // ---- Volume logic ----
    if (audio) {
        // initialize volume (use stored audio.volume if available)
        if (typeof audio.volume === 'number') {
            const vol = Math.max(0, Math.min(1, audio.volume || lastVolume));
            audio.volume = vol;
            if (volumeProgress) volumeProgress.style.width = (vol * 100) + '%';
        }

        // Click to set volume on volumeBar
        if (volumeBar) {
            const setVolumeFromEvent = (e) => {
                const rect = volumeBar.getBoundingClientRect();
                const x = (e.clientX !== undefined) ? e.clientX : (e.touches && e.touches[0] && e.touches[0].clientX);
                const pct = Math.max(0, Math.min(1, (x - rect.left) / rect.width));
                audio.volume = pct;
                if (volumeProgress) volumeProgress.style.width = (pct * 100) + '%';
                // update mute state icon if present
                if (volumeButton) updateVolumeIcon(audio.volume, volumeButton);
            };

            volumeBar.addEventListener('click', setVolumeFromEvent);

            // support dragging (pointer events)
            let pointerActive = false;
            volumeBar.addEventListener('pointerdown', (e) => {
                pointerActive = true;
                volumeBar.setPointerCapture(e.pointerId);
                setVolumeFromEvent(e);
            });
            window.addEventListener('pointermove', (e) => {
                if (!pointerActive) return;
                setVolumeFromEvent(e);
            });
            window.addEventListener('pointerup', (e) => {
                if (!pointerActive) return;
                pointerActive = false;
            });
        }

        // Mute/unmute button
        if (volumeButton) {
            volumeButton.addEventListener('click', (e) => {
                // toggle mute: remember lastVolume
                if (audio.volume > 0) {
                    lastVolume = audio.volume;
                    audio.volume = 0;
                } else {
                    audio.volume = lastVolume || 0.5;
                }
                if (volumeProgress) volumeProgress.style.width = (audio.volume * 100) + '%';
                updateVolumeIcon(audio.volume, volumeButton);
            });
        }
    }
}

function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function updateVolumeIcon(volume, buttonEl) {
    if (!buttonEl) return;
    const icon = buttonEl.querySelector('i');
    if (!icon) return;
    // choose icon based on volume level
    if (volume === 0) {
        icon.className = 'fa-solid fa-volume-xmark';
    } else if (volume < 0.33) {
        icon.className = 'fa-solid fa-volume-low';
    } else if (volume < 0.66) {
        icon.className = 'fa-solid fa-volume-high';
    } else {
        icon.className = 'fa-solid fa-volume-up';
    }
}

/* ---------------- Render Artists ---------------- */
function renderArtists(artists) {
    const container = document.querySelector('.horizontal-scroll');
    if (!container) return;
    container.innerHTML = '';
    artists.forEach(artist => {
        const article = document.createElement('article');
        article.className = 'artist-card';
        article.innerHTML = `
            <img src="${artist.imageUrl}" alt="${escapeHtml(artist.name)}">
            <div class="artist-meta">
                <div class="artist-name">${escapeHtml(artist.name)}</div>
                <div class="artist-type">${escapeHtml(artist.type)}</div>
            </div>
        `;
        container.appendChild(article);
    });
}

function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function (s) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[s];
    });
}
