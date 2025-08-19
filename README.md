# Spotify Digger: Local Music Downloader


## Project Overview

**Spotify Digger** is a Python-based web application developed using Flask that allows users to fetch and download music from Spotify playlists or individual tracks. This project serves as an **educational and experimental demonstration** of interacting with the Spotify API and leveraging yt-dlp for media extraction.
<img width="1400" height="625" alt="image" src="https://github.com/user-attachments/assets/eb4c8ad6-cc6a-461f-b4b5-0e3ab181a2cb" />



## Features

* **Track Download:** Download individual Spotify tracks.
* **Playlist Track Listing:** List all tracks within a given Spotify playlist.
* **Selective Playlist Download:** Choose specific songs from a playlist to download.
* **MP3 Conversion:** Automatically converts downloaded audio to MP3 format.
* **ZIP Packaging:** Compiles all downloaded songs into a single, convenient ZIP archive.
* **Progress Tracking:** Provides real-time progress updates during the download process.


## Getting Started
To set up and run Spotify Digger locally, follow these steps:


### Prerequisites
* Python 3.8+
* pip (Python package installer)
* [FFmpeg](https://ffmpeg.org/download.html) (required by yt-dlp for audio processing and conversion). Ensure FFmpeg is installed and accessible in your system's PATH.


### Installation
1. **Clone the Repository:** 
```git clone https://github.com/your-username/Spotify-Digger.git```
``` cd Spotify-Digger ```

3. **Create a Virtual Environment (Recommended):** 
```python -m venv venv ```
# On Windows 
```.\venv\Scripts\activate ```
# On macOS/Linux 
```source venv/bin/activate```

3. **Install Dependencies:** 
```pip install -r requirements.txt```

4. **Set up Spotify API Credentials:**
    * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    * Log in and create a new application.
    * Note down your **Client ID** and **Client Secret**.
    * Create a **.env file** in the root directory of your project (the same directory as app.py) and add the following lines, replacing the placeholders with your actual credentials: \
      
```SPOTIFY_CLIENT_ID=your_spotify_client_id ```
```SPOTIFY_CLIENT_SECRET=your_spotify_client_secret```



## Usage
1. **Run the Flask Application:** 
```python app.py```

The application will typically run on http://127.0.0.1:5000 or http://0.0.0.0:5000.
3. Access the Web Interface:
Open your web browser and navigate to the address where the application is running.
4. **Enter Spotify URL:**
    * **For a Playlist:** Enter the URL of a Spotify playlist. The application will then display a list of all songs in that playlist, allowing you to select individual tracks for download.
    * **For a Single Track:** Enter the URL of a Spotify track directly to download it.
5. Download:
Initiate the download, and the application will provide progress updates. Once complete, a download link for the ZIP archive will appear.


## Disclaimer

This application is developed solely for **educational purposes and as an experimental project**. It is designed to demonstrate concepts related to API interaction, web development, and media processing.

**Users are solely responsible for adhering to the terms of service of Spotify, YouTube, and any other content platforms.** Downloading copyrighted material without permission may be illegal in your jurisdiction and is a violation of these platforms' terms of service. The developers of this project do not endorse or encourage any illegal activities, and are not responsible for any misuse of this software. By using this application, you acknowledge and agree to take full responsibility for your actions.

<img width="2560" height="1811" alt="image" src="https://github.com/user-attachments/assets/c89c5688-7cfe-491d-884d-8584db8f4539" />

