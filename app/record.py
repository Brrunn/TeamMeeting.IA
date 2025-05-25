import pyaudio
import wave
import time

# Actuellement pas utilisé car on peut glisser un fichier wav 

def record_audio(filename="reunion.wav", duration=None):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    
    # Ouvrir le flux
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("Enregistrement démarré...")
    frames = []
    
    try:
        # Pour un enregistrement avec durée spécifiée
        if duration:
            for i in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
        # Pour un enregistrement jusqu'à interruption manuelle
        else:
            while True:
                data = stream.read(CHUNK)
                frames.append(data)
    except KeyboardInterrupt:
        print("Enregistrement arrêté.")
    finally:
        # Arrêter et fermer le flux
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Sauvegarder l'enregistrement
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"Enregistrement sauvegardé sous {filename}")
        return filename

if __name__ == "__main__":
    record_audio("/data/reunion1.wav")


