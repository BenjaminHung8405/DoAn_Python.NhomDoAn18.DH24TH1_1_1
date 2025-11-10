from pygame import mixer
import tkinter as tk
import urllib.request
from io import BytesIO
from mutagen.mp3 import MP3
import os


class Track:
    def __init__(self, master, trackName, trackUrl, artist, image):

        self.title = trackName
        self.master = master
        self.artist = artist
        self.image = image

        self.track = None
        self.byteAudio = None
        # self.trackUrl = trackUrl
        self.TrackName = trackName
        self.songDuration = None
        self.player = None
        self.playButton = None
        self.stopButton = None
        self.slider = None
        self.sliderValue = tk.DoubleVar()
        self.volumeSlider = None
        self.volume = None
        self.currentTime = None
        self.endTime = None

        # Determine if trackUrl is a local file or remote URL
        if self.is_local_file(trackUrl):
            # Load from local file
            self.byteAudio = self.get_audio_from_file(trackUrl)
            self.byteAudio2 = self.get_audio_from_file(trackUrl)
        else:
            # Load from remote URL
            self.byteAudio = self.get_audio_from_url(trackUrl)
            self.byteAudio2 = self.get_audio_from_url(trackUrl)

        self.track = self.byteAudio
        self.load_music()
        self.get_duration(self.byteAudio2)

    def is_local_file(self, trackUrl):
        """
        Check if the trackUrl is a local file path.
        Returns True if it's a local file, False if it's a remote URL.
        """
        # Check if it starts with 'songs/' (local file pattern)
        if trackUrl.startswith('songs/') and trackUrl.endswith('.mp3'):
            return True

        # Check if it's an absolute path that exists
        if os.path.isabs(trackUrl) and os.path.exists(trackUrl):
            return True

        # Otherwise, treat as remote URL
        return False

    def get_audio_from_file(self, filePath):
        """
        Load audio from a local file path.
        """
        try:
            # If it's a relative path starting with 'songs/', make it absolute
            if filePath.startswith('songs/'):
                # Get the project root directory (go up from Music/track.py to project root)
                # Music/track.py -> Music/ -> project_root/
                current_dir = os.path.dirname(os.path.dirname(__file__))
                filePath = os.path.join(current_dir, filePath)

            # Read the file as bytes
            with open(filePath, 'rb') as f:
                byteAudio = BytesIO(f.read())
            return byteAudio
        except Exception as e:
            print(f"Error loading local file {filePath}: {e}")
            return None

    def get_audio_from_url(self, trackUrl):
        req = urllib.request.Request(trackUrl)
        resp = urllib.request.urlopen(req)
        byteAudio = BytesIO(resp.read())
        return byteAudio

    def get_duration(self, byteAudio):
        if byteAudio is None:
            self.songDuration = 0
            return

        song = MP3(byteAudio)
        duration = song.info.length
        self.songDuration = duration

    def load_music(self):
        if self.byteAudio is None:
            print(f"Cannot load music for {self.title} - no audio data")
            self.player = None
            return

        try:
            player = mixer
            player.init()
            player.music.load(self.track)
            player.music.set_volume(.70)
            self.player = player
        except Exception as e:
            print(f"Error loading music for {self.title}: {e}")
            self.player = None

    def Play(self):
        if self.player is None:
            print(f"Cannot play {self.title} - player not initialized")
            return

        try:
            from Pages.BottomMusicPage.bottomMusicPage import BottomMusicPage
            from Base.listOfPage import bottomPage
            from Base.listOfPage import bottomInstance

            if len(bottomPage) == 0:
                bottom = BottomMusicPage(bottomInstance[0],
                                         self.master,
                                         title=self.title,
                                         artist=self.artist,
                                         image=self.image)
                bottomPage.append(bottom)
                bottomInstance[0].show_frame(self.title)
                currentTime = 0
            else:
                currentTime = bottomPage[0].middle.sliderValue.get()
                bottom = bottomPage[0]

            self.player.music.play(start=currentTime)
            bottom.middle.TrackPlay(currentTime)
        except Exception as e:
            print(f"Error playing {self.title}: {e}")

    def Stop(self):
        if self.player is None:
            print(f"Cannot stop {self.title} - player not initialized")
            return

        try:
            if self.player.music.get_busy():
                self.player.music.stop()
        except Exception as e:
            print(f"Error stopping {self.title}: {e}")
