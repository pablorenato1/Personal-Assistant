from queue import Queue

shared_queue = Queue()
shared_speech_queue = Queue(maxsize=2)