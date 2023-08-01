
import time
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
import threading
from project.static.python.core import PersonalAssistant
from project.static.python.spotify import SpotifyAssistant
from project.static.python.shared_queue import shared_queue, shared_speech_queue


# Create your views here.
spotify = SpotifyAssistant()
personalAssistant = PersonalAssistant(spotify=spotify)
spotify.admin = personalAssistant

params = {}

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def index(request):
    if personalAssistant.Status:
        params['personalAssistantStatus'] = personalAssistant.Status
    if spotify.isTheTokenValid(): # return True if it is expired
        params['access_token'] = '1'
        params['code'] = '1'
    
    if shared_queue.qsize() > 0: # What the Assistant Said
        params['message'] = shared_queue.get()
    if shared_speech_queue.qsize() >0: # What i said
        params['whatISaid'] = shared_speech_queue.get()
    else:
        params['message'] = False

    return render(request, 'interface.html', params)

def updateOnInterface(request):

    if shared_queue.qsize() > 0:
        params['message'] = shared_queue.get()
    if shared_speech_queue.qsize() > 0:
        params['whatISaid'] = shared_speech_queue.get()
    
    return JsonResponse(params)

def requestSpotifyAuthorization(request=None):
    if spotify.isTheTokenValid():
        return render(request, 'interface.html', params)
    authorization_url = spotify.getSpotifyAuthorization(view=True)
    return redirect(authorization_url)

def handleSpotifyCallback(request):
    spotify.authorizationCode = request.GET.get('code')
    if spotify.authorizationCode:

        for _ in range(3): # Attempt to Request a Token three times
            if spotify.requestAToken():
                break
    else:
        print('Error: Try the authentication again')
        # Authorization code not available, handle the error
    return redirect('index')

def interfacePlaybackControl(request):
    if spotify.isTheTokenValid(getNewOne=True): # true
        try: command = request.GET.get('command')
        except: command = request
        
        return spotify.spotifyPlaybackControl(command)
    else:
        return HttpResponse("Your authorization expired or some error that I did not expect.")
    # Get the command data from the AJAX (js) request
    
def startPersonalAssistant(request):
    personalAssistant.Status = True
    params['personalAssistantStatus'] = personalAssistant.Status
    # Initializing the Thread/Personal Assistant
    invokePA = threading.Thread(target=personalAssistant.main)
    invokePA.start()
    time.sleep(0.5)
    return redirect('index')

