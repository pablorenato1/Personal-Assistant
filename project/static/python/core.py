from datetime import datetime
import os
import time
import keyboard
import pygame
import pyaudio
import playsound
from gtts import gTTS
import threading
import speech_recognition as sr
from project.static.python.spotify import *
from project.static.python.shared_queue import shared_queue, shared_speech_queue

os.environ['PYTHONUNBUFFERED'] = '1'
semaphore = threading.Semaphore(1)

class PersonalAssistant:

    def __init__(self, spotify):
        self.Status = False
        self.spotify = spotify
        self.spotify_word_list = ['play', 'pause', 'next', 'previous', 'spotify']
        self.output_path = (
            os.getenv('AUDIO_PATH')
            if '__main__' in __name__
            else "project//static//python//output.mp3"
        )

    def speech(self, text):
        semaphore.acquire()
        language = "en"
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(self.output_path)

        # Initialize pygame mixer (if not already initialized)
        pygame.mixer.init()

        # Get the full path to the 'output.mp3' file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        output_mp3_path = os.path.join(current_directory, 'output.mp3')

        # Load the MP3 file as a sound
        sound = pygame.mixer.Sound(output_mp3_path)

        # Play the sound
        sound.play()

        # Wait until the playback is finished
        pygame.time.wait(int(sound.get_length() * 1000))  # Convert seconds to milliseconds

        # Stop the sound (optional, but useful if you want to interrupt the playback)
        sound.stop()

        # Delete the 'output.mp3' file after playback is finished
        os.remove(output_mp3_path)
        semaphore.release()

    def get_audio(self, text='You can talk now.'):
        shared_queue.put(text)
        while not keyboard.is_pressed('esc'):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print(text)
                audio = r.listen(source)
                try:
                    said = r.recognize_google(audio)
                    print(said)
                    shared_speech_queue.put(said)
                    return said.lower()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

    def process_command(self, command):
        # Check if the command contains the trigger word "friday"
        if "friday" in command:
            temp = set(command.split())
            if len(list(temp.intersection(self.spotify_word_list))) >= 1:
                self.spotify.isTheTokenValid(getNewOne=True)
                if "pause" in command:
                    self.spotify.spotifyPlaybackControl('pause')

                elif "skip" in command or "next" in command:
                    self.spotify.spotifyPlaybackControl('next')

                elif "previous" in command:
                    self.spotify.spotifyPlaybackControl('prev')

                elif "play" in command:
                    self.spotify.spotifyPlaybackControl('play')

                elif "open spotify" in command:
                    self.spotify.getDevice()
                else:
                    self.speech("Sorry, I didn't understand the music command.")
                    self.get_audio('Can you repeat.')

            elif "shut down" in command:
                self.personalAssistant_status = False
                shared_queue.put("Personal Assistant Turning Off...")
                redirect('index')
                return self.personalAssistant_status

        else:
            shared_queue.put("Sorry, I didn't recognize the trigger word 'friday'.")
            print("Sorry, I didn't recognize the trigger word 'friday'.")

    def main(self):
        self.personalAssistant_status = True

        while self.personalAssistant_status: # Run 'for ever'
            if keyboard.is_pressed('esc'):
                break
            audio = self.get_audio()
            self.process_command(audio)

            time.sleep(0.1)
        print('Personal Assistant is offline')



if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.main()
