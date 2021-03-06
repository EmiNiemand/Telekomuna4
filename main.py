import pyaudio
import send_receive as sr
import threading


def get_input_format():
    audio_input_formats = [pyaudio.paInt8, pyaudio.paInt16, pyaudio.paInt24, pyaudio.paInt32]
    print("Podaj format wejściowy: \n",
          "1. Int8\n",
          "2. Int16\n",
          "3. Int24\n",
          "4. Int32")
    input_format = int(input(""))
    input_format = audio_input_formats[input_format - 1]
    return input_format


def begin_transmission(port, ip, audio_setup: []):
    sender_thread = threading.Thread(target=sr.send, args=(audio_setup, (ip, port)))
    receiver_thread = threading.Thread(target=sr.receive, args=(audio_setup, port))

    try:
        print("[Ctrl+C by przerwać]")
        receiver_thread.start()
        input("Naciśnij dowolny przycisk aby rozpocząć rozmowę")
        sender_thread.start()
    except KeyboardInterrupt:
        input("Przerwano połączenie.")


def main():
    port = int(input("Podaj numer portu: "))
    ip = str(input("Podaj ip: "))
    audio_setup = (1024, pyaudio.paInt16, 2, 44100)
    # chunk = int(input("Podaj rozdzielczość: "))
    # input_format = get_input_format()
    # channel_number = int(input("Podaj liczbę kanałów: "))
    # rate = int(input("Podaj próbkowanie: "))
    # audio_setup = (chunk, input_format, channel_number, rate)
    input("Naciśnij dowolny klawisz, aby rozpocząć")
    begin_transmission(port, ip, audio_setup)


if __name__ == '__main__':
    main()

