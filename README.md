# Personal Assistant Django Project

This is a Django project for a simple personal assistant with voice interaction and Spotify integration.


> **Warning:**
> This project is for personal uses and is currently under development, and certain features may not be fully functional. 



## Project Overview

The project includes the following components:

- Voice-to-text using Google Speech Recognition API
- Text-to-speech using gTTS library
- Spotify playback control with Spotify API integration
- Django web interface for user interactions and logging
- Notion integration for progress tracking and documentation

## Dependencies

To run the project, make sure you have the following dependencies installed:

- Python 3.x 
- `speech_recognition`
- `gtts`
- `keyboard`
- `pyttsx3`
- `requests`
- `Django`

You can install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```
## Getting Started
### Clone the repository:

```bash
git clone https://github.com/pablorenato1/Virtual-Assistant.git
```
```bash
cd Virtual-Assistant
```

### Set up environment variables:

Create a .env file in the project root directory "../project/static/python" and add these variables:

```plaintext
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
AUDIO_PATH=/path/to/save/audio/output.mp3
SPOTIFY_PATH=/path/to/spotify.exe (Optional: Path to your Spotify executable, if using Windows)
```
Obs.: The path to Spotify.exe is only necessary if you try to execute any operation without open you spotify.

#### How to get CLIENT_ID and CLIENT_SECRET:
* Both can be found in you https://developer.spotify.com/dashboard
    *  If you don't have an 'app' on dashboard create one with the name as you prefer
    * In the "Redirect URIs" option you should put: http://localhost:8000/token

Obs.: Only change the _Redirect URIs_ if you know what you are doing.
### Install project dependencies:

```
pip install -r requirements.txt
```
## How to use
### Run the Django development server:

```bash
python manage.py runserver
```
### Access the personal assistant web interface:

While pressing ```Ctrl```, click on the link in the terminal.

It's usually this link: http://127.0.0.1:8000/

### Get Spotify Authorization:

* Click on the "Authenticate" button to authenticate with Spotify and grant the necessary permissions to the program to work.
* Follow the authentication process to obtain the access token.

# Explanations
### Code: SpotifyAssistant
The SpotifyAssistant class in project/static/python/spotify.py handles Spotify authentication and playback control.

### You can use the class methods to interact with Spotify:

```Python
# Example usage of SpotifyAssistant class

from project.static.python.spotify import SpotifyAssistant

# Create an instance of SpotifyAssistant
spotify = SpotifyAssistant()

# Get Spotify authorization URL for initial authentication
authorization_url = spotify.getSpotifyAuthorization()

# After the user grants access, get the authorization code from the redirected URL and call the requestAToken method
spotify.authorizationCode = "YOUR_AUTHORIZATION_CODE"
spotify.requestAToken()

# Get the current playback state
spotify.getPlayBack()

# Control Spotify playback
spotify.spotifyPlaybackControl("play")     # Play music
spotify.spotifyPlaybackControl("pause")    # Pause music
spotify.spotifyPlaybackControl("next")     # Skip to the next track
spotify.spotifyPlaybackControl("prev")     # Go back to the previous track
```


