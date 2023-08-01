from datetime import datetime
import os
import time
from django.shortcuts import redirect
import keyboard
import pyttsx3
from gtts import gTTS
import threading
import speech_recognition as sr
from project.static.python.spotify import *
from project.static.python.shared_queue import info_logger, debug_logger, error_logger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import multiprocessing as mp

os.environ['PYTHONUNBUFFERED'] = '1'
semaphore = threading.Semaphore(1)
targetWord = 'friday'

# Setting pyttsx3 Lib config
engine =pyttsx3.init()
voices = engine.getProperty('voice')
engine.setProperty('voice', voices[1])

# Setting rate
engine.setProperty('rate', 220)
class PersonalAssistant:
    def __init__(self, spotify):
        self.Status = False
        self.spotify = spotify
        self.spotify_word_list = ['play', 'pause', 'next', 'previous', 'spotify', 'skip', 'stop','go', 'back']
        self.output_path = (
            os.getenv('AUDIO_PATH')
            if '__main__' in __name__
            else "project//static//python//output.mp3"
        )

    def speech(self, text):

        
        engine.say(text)
        engine.runAndWait()
        

    def get_audio(self, text='You can talk now.'):
        
        while not keyboard.is_pressed('esc'):
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source: # Uses the current available input (mic)
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source, timeout=5) # Listening 
                    try:
                        said = r.recognize_google(audio) # Using google gTTS to try recognize what is being said
                        debug_logger.debug(f"Said: {said}")
                        return said.lower()
                    except sr.RequestError as e:
                        error_logger.error(f"Could not request results from Google Speech Recognition Service; {e}")
            except:
                continue
        return ""

    def processCommand(self, command):
        # Check if the command contains the trigger word "friday"

        if targetWord in command: # That represent a command
            self.send_websocket_message(message_type='user', message=command)
            debug_logger.debug(f'The command is processing the command: "{command}"')
            temp = set(command.split())
            if len(list(temp.intersection(self.spotify_word_list))) >= 1:
                self.spotify.isTheTokenValid(getNewOne=True)
                if "stop" in command or "pause" in command: # Check if the word 'pause' is in the sentence
                    self.spotify.spotifyPlaybackControl('pause')

                elif "skip" in command or "next" in command: # Check if the word 'next' is in the sentence
                    self.spotify.spotifyPlaybackControl('next')

                elif ('go' in command and 'back' in command) or "previous" in command: # Check if the word 'previous' is in the sentence
                    self.spotify.spotifyPlaybackControl('prev')

                elif "play" in command: # Check if the word 'play' is in the sentence
                    self.spotify.spotifyPlaybackControl('play')

                elif "open spotify" in command: # Check if the word 'open spotify' is in the sentence
                    self.spotify.getDevice()
                else:
                    self.send_websocket_message(message_type='user', message='Can you repeat?')
                    # self.speech("Sorry, I didn't understand the music command.")
                    self.get_audio()

            elif "shut down" in command: # Check if the word 'shut down' is in the sentence
                self.personalAssistant_status = False
                self.send_websocket_message(message_type='personalAssistant', message=f'Shutting down the personal Assistant')
                redirect('index')
                return self.personalAssistant_status

        else: # I did not use friday in the sentence
            debug_logger.debug(f"The word {targetWord} not founded.")
            self.send_websocket_message(message_type='personalAssistant', message=f"Sorry, I didn't recognize the trigger word '{targetWord}'.")


    def send_websocket_message(self,message_type, message):
        channel_layer = get_channel_layer()

        group_name = 'backend_response'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type':'send_group_message',
                'type-message':message_type,
                'data':message
            }
        )
        
    def main(self):
        self.personalAssistant_status = True
        time.sleep(2)
        self.send_websocket_message(message_type='personalAssistant', message='Turning Personal Assistant On...')
        time.sleep(1)
        self.send_websocket_message(message_type='personalAssistant', message='You can talk now.')

        while self.personalAssistant_status: # Run 'forever'
            if keyboard.is_pressed('esc'):
                break
            time.sleep(0.1)
            audio = self.get_audio()
            processingCommand = mp.Process(target=self.processCommand, args=(audio,))
            processingCommand.start()

        self.send_websocket_message(message_type='personalAssistant', message='Personal Assistant is offline')
        self.speech("Turning off.")

    



if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.main()
