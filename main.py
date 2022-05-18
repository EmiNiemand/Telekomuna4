import pyaudio

import send_receive as sr
import threading


def main():
    port = 2137
    ip = "192.168.0.18"
    audio_setup = (1024, pyaudio.paInt16, 2, 44100)
    user_choice = ''
    while user_choice != '4':
        print(f"IP:PORT\n{ip}:{port}")
        print(audio_setup_to_string(audio_setup), "\n")
        print("Wybierz opcję:\n",
              "(0) Tryb Setup (podaj wszystko i połącz)\n",
              "(1) Podaj parametry audio\n",
              "(2) Podaj parametry przesyłu (port i adres hosta)\n",
              "(3) Rozpocznij połączenie\n",
              "(4) Wyjdź z programu\n")
        user_choice = input("> ")
        if user_choice == 0:
            audio_setup = get_audio_parameters()
            ip, port = get_transmission_parameters()
            begin_transmission(port, ip, audio_setup)
        elif user_choice == 1:
            audio_setup = get_audio_parameters()
        elif user_choice == 2:
            ip, port = get_transmission_parameters()
        elif user_choice == 3:
            begin_transmission(port, ip, audio_setup)
        else:
            continue


def audio_setup_to_string(audio_setup: [int, int, int, int]):
    chunk, input_format, channel_number, rate = audio_setup
    return f"Rozdzielczość: {chunk}\n" + \
           f"Format wejściowy: {input_format}\n" + \
           f"Liczba kanałów: {channel_number}\n" + \
           f"Próbkowanie: {rate}"


def get_audio_parameters():
    chunk = int(input("Podaj rozdzielczość: "))

    audio_input_formats = [pyaudio.paInt8, pyaudio.paInt16, pyaudio.paInt24, pyaudio.paInt32]
    print("Podaj format wejściowy: ",
          "(1) Int8\n",
          "(2) Int16\n",
          "(3) Int24\n",
          "(4) Int32\n")
    input_format = int(input(""))
    input_format = audio_input_formats[input_format - 1]

    channel_number = int(input("Wprowadź liczbę kanałów 1 lub 2: "))

    rate = int(input("Podaj częstotliwość próbkowania[Hz]: "))

    return chunk, input_format, channel_number, rate


def get_transmission_parameters():
    ip = str(input("Podaj adres ip: "))
    port = int(input("Podaj numer portu: "))
    return ip, port


def begin_transmission(port, ip, audio_setup: [int, int, int, int]):
    sender_thread = threading.Thread(target=sr.send, args=(audio_setup, (ip, port)))
    receiver_thread = threading.Thread(target=sr.receive, args=(audio_setup, port))

    try:
        print("[Ctrl+C by przerwać]")
        receiver_thread.start()
        input("Naciśnij enter aby rozpocząć połączenie")
        sender_thread.start()
    except KeyboardInterrupt:
        input("Przerwano połączenie. Naciśnij dowolny klawisz, by kontynuować...")


if __name__ == '__main__':
    main()

