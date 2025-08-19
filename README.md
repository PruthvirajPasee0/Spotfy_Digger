# Spotify Downloader UI

A Python-based web application that allows users to download Spotify tracks or playlists as MP3 files, packaged in a ZIP. Built with Flask, it integrates the Spotify API for track metadata and yt-dlp for audio downloads, featuring a responsive Bootstrap UI with a progress bar.

**Live Demo**: (Add your Render URL here after deployment, e.g., `https://spotify-downloader.onrender.com`)

## Features
- Download single Spotify tracks or entire playlists.
- User-friendly web interface with real-time progress tracking.
- Outputs a ZIP file containing MP3s (192kbps quality).
- Responsive design powered by Bootstrap.

## How It Works
1. Users enter a Spotify track URL (e.g., `https://open.spotify.com/track/...`) or playlist URL (e.g., `https://open.spotify.com/playlist/...`).
2. The app fetches track metadata via the Spotify API.
3. Audio is sourced from YouTube using yt-dlp and converted to MP3 with FFmpeg.
4. Downloaded files are zipped and served to the user.

## Prerequisites
- Python 3.11+ (tested with 3.13.2)
- FFmpeg installed (for audio conversion)
- Spotify API credentials (Client ID and Secret)

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/GodSpeedn/Spotify-Downloader-UI.git
   cd Spotify-Downloader-UI
Install Dependencies:

pip install -r requirements.txt
Ensure FFmpeg is installed:
On macOS: brew install ffmpeg
On Ubuntu: sudo apt-get install ffmpeg
On Windows: Download from ffmpeg.org and add to PATH.
Add Spotify Credentials:
Get your Client ID and Secret from Spotify Developer Dashboard.

Open app.py and replace:
python

SPOTIFY_CLIENT_ID = "your_client_id"or "mine is in the file already "
SPOTIFY_CLIENT_SECRET = "your_client_secret"
Run the App:



python app.py
Open http://127.0.0.1:5000/ in your browser.
Usage
Visit the web app (locally at http://127.0.0.1:5000/ or the deployed URL).
Enter a Spotify track or playlist URL in the input field.
Click "Download" and watch the progress bar.
Once complete, click "Download ZIP" to get your MP3s.
Example Inputs
Track: https://open.spotify.com/track/2zQE8TE5BQDJA11ggnope9
Playlist: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
Deployment
To deploy online (e.g., on Render):


Technologies Used
Python: Core logic
Flask: Web framework
Spotipy: Spotify API integration
yt-dlp: YouTube audio downloading
FFmpeg: Audio conversion
Bootstrap: Frontend styling
jQuery/AJAX: Progress updates




Notes

Legal: This is a proof-of-concept. Downloading copyrighted music may violate Spotify and YouTube terms of service—use responsibly for educational purposes.
Limitations: Free hosting (e.g., Render) may time out on large playlists; progress is track-based, not time-based.
Author

Narayan Rakhecha (GitHub: GodSpeedn)
