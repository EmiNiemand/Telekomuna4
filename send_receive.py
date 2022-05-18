import socket
import pyaudio

def send(audio_setup: [], ip_port: [str, int]):
    p = pyaudio.PyAudio()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(ip_port)

        try:
            stream = p.open(format=audio_setup[1], channels=audio_setup[2], rate=audio_setup[3],
                            frames_per_buffer=audio_setup[0], input=True)
            while True:
                data = stream.read(audio_setup[0])
                client_socket.sendall(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()


def receive(audio_setup: [], port):
    p = pyaudio.PyAudio()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("", port))
        server_socket.listen()
        conn, addr = server_socket.accept()
        print(f"Połączono z: {addr}")

        try:
            stream = p.open(format=audio_setup[1], channels=audio_setup[2], rate=audio_setup[3],
                            frames_per_buffer=audio_setup[0], input=True)

            while True:
                data = conn.recv(1024)
                stream.write(data)

        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

