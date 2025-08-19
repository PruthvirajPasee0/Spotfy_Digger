from flask import Flask, request, send_file, render_template, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import os
import zipfile
import shutil
import threading
import platform
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

DOWNLOAD_DIR = "downloaded_songs"
ZIP_FILE = "spotify_songs.zip"

# Global vars for progress tracking
progress = {"status": "idle", "current": 0, "total": 0, "message": ""}

def setup_spotify():
    credentials = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=credentials)

def get_track_info(sp, track_url):
    track_id = track_url.split("/")[-1].split("?")[0]
    track = sp.track(track_id)
    return [f"{track['name']} - {track['artists'][0]['name']}"]

def get_playlist_tracks(sp, playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    return [f"{item['track']['name']} - {item['track']['artists'][0]['name']}" for item in results['items']]

def download_song(query, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{query}"])
        return True
    except Exception:
        return False

def create_zip(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.basename(file))

def download_task(url):
    global progress
    sp = setup_spotify()

    # Reset progress
    progress["status"] = "downloading"
    progress["current"] = 0

    # Clean up
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)
    os.makedirs(DOWNLOAD_DIR)

    # Fetch tracks
    if "/track/" in url:
        tracks = get_track_info(sp, url)
    elif "/playlist/" in url:
        tracks = get_playlist_tracks(sp, url)
    progress["total"] = len(tracks)

    # Download songs
    successful_downloads = 0
    for i, track in enumerate(tracks, 1):
        progress["current"] = i
        progress["message"] = f"Downloading: {track}"
        if download_song(track, DOWNLOAD_DIR):
            successful_downloads += 1

    # Create ZIP
    if successful_downloads > 0:
        progress["message"] = "Creating ZIP file..."
        create_zip(DOWNLOAD_DIR, ZIP_FILE)
        shutil.rmtree(DOWNLOAD_DIR)
        progress["status"] = "done"
        progress["message"] = "Download complete!"
    else:
        shutil.rmtree(DOWNLOAD_DIR)
        progress["status"] = "error"
        progress["message"] = "Failed to download any tracks."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['spotify_url']
        if not url or not ("track" in url or "playlist" in url):
            return render_template('index.html', error="Please enter a valid Spotify track or playlist URL.")

        # Start download in a separate thread
        threading.Thread(target=download_task, args=(url,)).start()
        return render_template('index.html', error=None, downloading=True)

    return render_template('index.html', error=None, downloading=False)

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/download')
def download():
    if os.path.exists(ZIP_FILE) and progress["status"] == "done":
        return send_file(ZIP_FILE, as_attachment=True, download_name="spotify_songs.zip")
    return "File not ready yet.", 400



if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # respects host-provided PORT (Render, etc.)

    if platform.system() == "Windows":
        from waitress import serve
        print("Running with Waitress on Windows...")
        serve(app, host="0.0.0.0", port=port)
    else:
        from gunicorn.app.base import BaseApplication

        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            'bind': f'0.0.0.0:{port}',  # <- IMPORTANT: use $PORT in prod
            'workers': 1,
            'timeout': 600
        }
        StandaloneApplication(app, options).run()


# if __name__ == '__main__':

#     from gunicorn.app.base import BaseApplication
#     class StandaloneApplication(BaseApplication):
#         def __init__(self, app, options=None):
#             self.options = options or {}
#             self.application = app
#             super().__init__()

#         def load_config(self):
#             for key, value in self.options.items():
#                 self.cfg.set(key.lower(), value)

#         def load(self):
#             return self.application

#     options = {
#         'bind': '0.0.0.0:5000',  # Listen on all interfaces, port 5000
#         'workers': 1,           # Single worker for simplicity
#         'timeout': 600          # Increase timeout for long downloads
#     }
#     StandaloneApplication(app, options).run()