# Personal Assistant Django Project

This is a Django project for a simple personal assistant with voice interaction and Spotify integration.

<style>
.warning {
    padding: 1em;
    border: 2px solid #f0ad4e;
    background-color: #fcf8e3;
    border-radius: 5px;
}
.warning h3 {
    margin-top: 0;
    margin-bottom: 0.5em;
    color: Orange;
}
.warning p {
    margin-top: 0;
    color: black
}
</style>


<div class="warning" markdown="1">

### Important Notice

This project is currently under development, and certain features may not be fully functional or stable. 

</div>


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
- `pyaudio`
- `pygame`
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
git clone https://github.com/your-username/personal-assistant-django.git
cd personal-assistant-django
```

### Set up environment variables:

Create a .env file in the project root directory and add the necessary environment variables:

```plaintext
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
AUDIO_PATH=/path/to/save/audio/output.mp3
SPOTIFY_PATH=/path/to/spotify.exe (Optional: Path to your Spotify executable, if using Windows)
```
#### How to get CLIENT_ID and CLIENT_SECRET:
* Well both can be found in you https://developer.spotify.com/dashboard
    *  If you don't have an 'app' on dashboard create one with the name as you prefer
    * In the "Redirect URIs" option you should put: http://localhost:8000/token
### Install project dependencies:

```
pip install -r requirements.txt
```
* Change the name of the json file on **/project/static/python** to auth.json
## How to use
### Run the Django development server:

```bash
python manage.py runserver
```
### Access the personal assistant web interface:

Open your web browser and go to http://localhost:8000/

### Get Spotify Authorization:

* Click on the "Authorize Spotify" button to authenticate with Spotify and grant the necessary permissions.
* Follow the authentication process to obtain the access token.
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


