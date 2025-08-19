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
    return render_template('index.html', error=None, downloading=False)

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/download')
def download():
    if os.path.exists(ZIP_FILE) and progress["status"] == "done":
        return send_file(ZIP_FILE, as_attachment=True, download_name="spotify_songs.zip")
    return "File not ready yet.", 400


@app.route('/list_tracks', methods=['POST'])
def list_tracks():
    url = request.json.get('spotify_url')
    if not url or not "playlist" in url:
        return jsonify({"error": "Invalid playlist URL"}), 400

    sp = setup_spotify()
    try:
        tracks = get_playlist_tracks(sp, url)
        if not tracks:
            return jsonify({"error": "No tracks found in the playlist or playlist is private."}), 404

        # You might want to modify get_playlist_tracks to return a better format
        # Currently, it returns "Name - Artist". Let's change it for better JSON.
        #
        # Let's adjust get_playlist_tracks to return a list of dictionaries,
        # each with 'name' and 'artist' keys.
        # This is a much better way to handle data on the frontend.
        # Let's assume you've updated your get_playlist_tracks function for this.

        # (See the updated get_playlist_tracks function below)
        return jsonify({"tracks": tracks})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update the get_playlist_tracks function to return a list of dictionaries
def get_playlist_tracks(sp, playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    # This is the key change: return a list of dictionaries
    return [{'name': item['track']['name'], 'artist': item['track']['artists'][0]['name']} for item in results['items']]

# app.py

# ... (keep all your existing code)

@app.route('/download_selected', methods=['POST'])
def download_selected():
    # The frontend will now send a JSON payload with a list of songs to download
    selected_songs = request.json.get('songs')
    if not selected_songs:
        return jsonify({"error": "No songs selected for download."}), 400

    # The download task needs to be updated to accept a list of song queries
    threading.Thread(target=download_task, args=(selected_songs,)).start()
    return jsonify({"status": "download started"}), 202

# Update the download_task function to handle a list of queries
def download_task(queries):
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

    # Now the 'queries' is the list of tracks to download
    tracks_to_download = [f"{track['name']} - {track['artist']}" for track in queries]
    progress["total"] = len(tracks_to_download)

    # Download songs
    successful_downloads = 0
    for i, query in enumerate(tracks_to_download, 1):
        progress["current"] = i
        progress["message"] = f"Downloading: {query}"
        if download_song(query, DOWNLOAD_DIR):
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