import pyaudio

import send_receive as sr
import threading

PORT = 2137

audio_setup = (1024, pyaudio.paInt16, 2, 44100)

sender_thread = threading.Thread(target=sr.send, args=(audio_setup, ("192.168.1.101", PORT)))
receiver_thread = threading.Thread(target=sr.receive, args=(audio_setup, PORT))

receiver_thread.start()
input("Naciśnij enter aby rozpocząć połączenie")
sender_thread.start()

