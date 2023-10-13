from datetime import datetime
import os
import sys
import time
from django.shortcuts import redirect
import keyboard
import pyttsx3
from gtts import gTTS
import threading
import speech_recognition as sr
from project.static.python.spotify import *
from project.static.python.shared_queue import info_logger, debug_logger, error_logger, shared_queue
import multiprocessing as mp
from queue import Queue

os.environ['PYTHONUNBUFFERED'] = '1'
semaphore = threading.Semaphore(1)
targetWord = 'friday'
userInputQueue = Queue()

# Setting pyttsx3 Lib config
engine = pyttsx3.init()
voices = engine.getProperty('voice')
engine.setProperty('voice', voices[1])

# Setting rate
engine.setProperty('rate', 200)
class PersonalAssistant:
    def __init__(self, spotify):
        self.Status = False
        self.spotify = spotify
        self.spotify_word_list = {
            "play": "play",
            "pause": "pause",
            "next": "next",
            "previous": "prev",
            "spotify": "spotify",
            "skip": "next",
            "stop": "pause",
            "go back": "prev",
            "shut down":"shut down",
            "shutdown":"shut down"
        } # Commands that the algorithm will associate to spotify

    def speech(self, text):
        engine.say(text)
        engine.runAndWait()
        

    def get_audio(self, text='You can talk now.'):
        
        while not keyboard.is_pressed('esc'):
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source: # Uses the current available input (mic)
                    r.adjust_for_ambient_noise(source, 1.1)
                    audio = r.listen(source, timeout=5) # Listening 
                    try:
                        said = r.recognize_google(audio) # Using google gTTS to try recognize what is being said
                        debug_logger.debug(f"Said: {said}")
                        return said.lower()
                    except sr.RequestError as e:
                        error_logger.error(f"Could not request results from Google Speech Recognition Service; {e}")
            except:
                # Is printing a lot message errors
                # error_logger.error(f"Error: Microphone input not founded.")
                continue
        return ""

    def find_string_in_list(self, string, dict_of_strings):
        for key, value in dict_of_strings.items():
            if key in string:
                return value
        return None

    def processCommand(self, command):
        
        string = self.find_string_in_list(command, self.spotify_word_list)
        print(string)
        if command == "spotify":
            return self.spotify.getDevice()
        elif string == "shut down":
            self.personalAssistant_status = False
            print(self.personalAssistant_status)
        elif string == None:
            return print(f"Sorry, I didn't recognize the command '{command}'.")
        else:
            return self.spotify.send_command(string)
        
    def main(self):
        self.personalAssistant_status = True
        

        textProcessingPool = mp.Pool(processes=2)
        while True:
            if keyboard.is_pressed('esc') or not self.personalAssistant_status:
                print('Test')
                break
            time.sleep(0.1)

            textTranscribed = self.get_audio()
            # This area should be the process by NLP algorithm
            print(f"What I said: {textTranscribed}") # DEBUG
            textProcessingPool.apply(self.processCommand, args=(textTranscribed,))

        textProcessingPool.close()
        textProcessingPool.join()

        self.speech("Turning off.")

if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.main()
