import time
import os
import base64
import json
from datetime import datetime, timedelta
from urllib.parse import urlencode
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from project.static.python.shared_queue import shared_queue
import requests
import webbrowser
from dotenv import load_dotenv

# Load env files
load_dotenv()

viewAuth = 'http://localhost:8000/backend_request/' # Did i use it ?

# Create Function

# That will verify if the token, if true, do not try to get info of devices

class SpotifyAssistant:

    def __init__(self):
        with open("project\static\python/auth.json", 'r') as file:
            json_data = json.load(file)
        self.admin = None
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tokenExpireTime = datetime.fromisoformat(json_data['TOKEN_TIME'])
        self.authorizationCode = None
        self.accessToken = json_data["ACCESS_TOKEN"]
        self.deviceId = "Unknown"
        self.isPlaying = "Unknown" # If it's playing the moment it request
        
        if json_data["REFRESH_TOKEN"] == "": self.refresh = False # There's not refresh Token
        else: self.refresh = True # There's a refresh Token

    def getVariableFromJson(self, arg=[]):
        # print("Asking for variable") #Debug purpose
        with open("project\static\python/auth.json", 'r') as file: # Read the data from json file
            json_data = json.load(file)

        response = {} # Create a dict to save the variables that asked for
        for var in arg:
            response[var] = json_data[var] # Kinda transfer them from one to another
        return response

    def updateOnJson(self, refresh=[False, None], playback=[False, None]):
        # print("Asking to Update") #Debug purpose
        with open("project\static\python/auth.json", 'r') as file:
                json_data = json.load(file)

        jsonToSave = {
            "ACCESS_TOKEN":self.accessToken,
            "DEVICE_ID": self.deviceId,
            "TOKEN_TIME": self.tokenExpireTime.isoformat(),
            "FIRST_TIME": json_data['FIRST_TIME']
        }
        if refresh[0]: jsonToSave['REFRESH_TOKEN'] = refresh[1]
        elif self.refresh: jsonToSave['REFRESH_TOKEN'] = json_data['REFRESH_TOKEN']
        else: jsonToSave['REFRESH_TOKEN'] = ""

        if playback[0]: jsonToSave['DEVICE'] = playback[1]
        else: jsonToSave['DEVICE'] = json_data['DEVICE']

        with open("project\static\python/auth.json", 'w') as file:
            json.dump(jsonToSave, file, indent=4)
        return

    def isTheTokenValid(self, getNewOne=False):
        # print("Asking for a Validation") #Debug purpose
        if self.tokenExpireTime > datetime.now(): # Return True if still valid
            return True
        
        elif getNewOne: # Already expired and will try get a new one
            if not self.refresh: # Does not have Refresh Token
                # self.refresh = False
                self.getSpotifyAuthorization(view=False)

            for _ in range(3):
                self.requestAToken()
                if self.accessToken: # True
                    break
            self.updateOnJson()
            return True
        return False
 
    def getSpotifyAuthorization(self, view=True):
        # print("Asking for a Auth") #Debug purpose
        auth_url = 'https://accounts.spotify.com/authorize?'
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': 'http://localhost:8000/token',
            'scope': 'user-read-playback-state user-modify-playback-state'
        }
        authorization_url = f"{auth_url}{urlencode(params)}"
        if view:
            return authorization_url
        webbrowser.open(authorization_url)
        time.sleep(15)

    def requestAToken(self): 
        # print("Asking for a Token") #Debug purpose
        # Should only be evoked in the view when the button is clicked and in the isTheTokenValid function, because of the logic implemented
        # Creating headers 'Authorization' value 
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        if self.refresh: # Get token using Refresh Token
            body = {
                'grant_type': 'refresh_token',
                'refresh_token': self.getVariableFromJson(["REFRESH_TOKEN"])["REFRESH_TOKEN"]
            }
            refresh_token= ""
            
        else: # Get a new Token (Not using Refresh Token)  
            body = {
                'grant_type': 'authorization_code',
                'code': self.authorizationCode,
                'redirect_uri': 'http://localhost:8000/token' # This is defined in the API settings on spotify (Can be change)
            }
            

        token_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-type": "application/x-www-form-urlencoded"
        }

        response = requests.post(token_url, headers=headers, data=body)

        if response.status_code == 200: # OK
            try:
                json_response = json.loads(response.content)
                self.accessToken = json_response['access_token']
                try:
                    refresh_token = json_response['refresh_token']
                    self.refresh = True
                    self.updateOnJson(refresh=[True, refresh_token])
                except: pass
                datetime_to_str = datetime.now() + timedelta(hours=1)
                self.tokenExpireTime = datetime_to_str

                self.updateOnJson()
                return True # All the changes were saved and was OK
            except json.JSONDecodeError:
                print('Error: Invalid JSON response while get a token.')
        else:
            print('Error(Token Response):', response.status_code)
        return False

    def getDevice(self):
        # print("Asking for a Device") #Debug purpose
        temp = requests.get("https://api.spotify.com/v1/me/player/devices", headers={"Authorization": f'Bearer {self.accessToken}'})

        if temp.status_code == 200:
            temp = json.loads(temp.content)
            if not temp["devices"]: # If spotify is closed or it's not 'sync', response = {'devices':[]}
                spotify_path = os.getenv("SPOTIFY_PATH") # My path to spotify
                os.system(f'"{spotify_path}"')
                return self.getDevice()

            for device in temp['devices']:
                if device['type'].lower() == 'computer':
                    url_request_transfer = "https://api.spotify.com/v1/me/player"
                    self.deviceId = device['id']
                    self.isPlaying = device['is_active'] 
                    self.updateOnJson()

                    headers_t = {
                        "Authorization": f'Bearer {self.accessToken}',
                        "Content-Type": "application/json"
                    }
                    data = {
                        "device_ids": [self.deviceId]
                    }
                    transferPlayback = requests.put(url_request_transfer, headers=headers_t, json=data)
                    print(f"Response change of device: {transferPlayback.status_code}")
                    return True
        print(f'Error {temp.status_code}: This error occurred while getting devices.')
        return False
    
    def getPlayBack(self):
        print("Asking for a Playback") #Debug purpose
        response = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": f'Bearer {self.accessToken}'})

        if response.status_code == 200: # OK
            try:
                json_response = json.loads(response.content)
                self.isPlaying = json_response['is_playing']
                self.deviceId = json_response['device']['id']
                self.updateOnJson(playback=[True, json_response])
            except json.JSONDecodeError:
                print('Error: Invalid JSON response.')
            return True # Was able to obtain the current playback state

        elif response.status_code == 204:
            if self.getDevice():
                return True
            time.sleep(5)
            spotify_path = os.getenv('SPOTIFY_PATH')
            os.system(f'"{spotify_path}"')
            print("Error: Response 204, when getting devices")
            return False
        
        else:
            print('Error[Getting Device Data]:', response.status_code)
        print('Error[Getting Device Data]:', response.status_code)
        return False

    def spotifyPlaybackControl(self, command):
        # print("Asking for a Command") #Debug purpose

        if self.deviceId == "Unknown":
            getDeviceStatus = self.getPlayBack()
            if not getDeviceStatus:
                print("There's some error, please check it out.")
                shared_queue.put("There's some error, please check it out.")
                return HttpResponse("There is some error, please check it out.")
            
        if not self.isTheTokenValid(getNewOne=True):
            print("There's some problem, I will not be able to execute your request.")
            return HttpResponse("There's some problem, I will not be able to execute your request.")

        url_request = "https://api.spotify.com/v1/me/player"
        headers = {
            "Authorization": f'Bearer {self.accessToken}'
        }
        
        if self.isPlaying and command == "play":
            command = "pause"
        print('Executing spotify-control:', command)
        if command == 'play':
            response = requests.put(f'{url_request}/play/?device_id={self.deviceId}', headers=headers)
            result = "Playing"

            shared_queue.put('Ok, playing music')
            # self.admin.speech('Ok, playing music')
            self.isPlaying = True
        elif command == 'pause':
            response = requests.put(f'{url_request}/pause/?device_id={self.deviceId}', headers=headers)
            result = "Music Paused"

            shared_queue.put('Ok, pausing music on Spotify')
            self.admin.speech('Paused')
            self.isPlaying = False
        elif command == 'next':
            response = requests.post(f'{url_request}/next/?device_id={self.deviceId}', headers=headers)

            result = "Next Music"
            shared_queue.put('Skipping to the next Music')
            # self.admin.speech('Skipping to the next Music')
        elif command == "prev":
            response = requests.post(f'{url_request}/previous/?device_id={self.deviceId}', headers=headers)

            result = "Previous Music"
            shared_queue.put('Ok, go back to the previous Music')
            # self.admin.speech('Ok, go back to the previous Music')

        else:
            result = "Invalid command."

        # try:
        #     print(f'Response to command "{command}": ', response.status_code)
        # except:
        #     pass
        return HttpResponse(result)
