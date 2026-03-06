import socket
import numpy as np
import sounddevice as sd

UDP_IP = "0.0.0.0"  # escucha en todas las interfaces
UDP_PORT = 5005
SAMPLE_RATE = 8000
BUFFER_SIZE = 256  # debe coincidir con ESP32

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Escuchando UDP en puerto {UDP_PORT}")

def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE*2)  # 2 bytes por muestra
        audio = np.frombuffer(data, dtype=np.int16)
        if len(audio) < frames:
            outdata[:len(audio),0] = audio
            outdata[len(audio):,0] = 0
        else:
            outdata[:,0] = audio
    except BlockingIOError:
        outdata[:,0] = 0

print("Reproduciendo audio en tiempo real. Habla al micrófono...")

with sd.OutputStream(channels=1, samplerate=SAMPLE_RATE, dtype='int16', blocksize=BUFFER_SIZE, callback=audio_callback):
    try:
        while True:
            pass
    except KeyboardInterrupt:
        sock.close()
        print("Cerrando socket")