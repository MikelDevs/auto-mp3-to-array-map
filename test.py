import soundfile as sf
import sounddevice as sd
import json
import numpy as np
import time
import threading

# Cargar las notas
with open('notes_detected.json', 'r') as f:
    notes = json.load(f)


def generate_tone(frequency, duration, samplerate=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)  # 0.5 para no saturar el volumen
    return tone

# Función para reproducir la canción de fondo
def play_background_music():
    # Cargar archivo de música de fondo
    music_data, music_samplerate = sf.read('SHE IS A YAQUI LADY.mp3')
    
    # Reproducir la canción de fondo a un volumen bajo
    while True:
        sd.play(music_data * 0.1, music_samplerate)  # Multiplicar por 0.1 para bajarlo de volumen
        sd.wait()

print("🎵 ¡Empieza la canción! 🎵")


background_thread = threading.Thread(target=play_background_music, daemon=True)
background_thread.start()
start_time = time.time()

for note in notes:
    while (time.time() - start_time) < note['time_seconds']:
        time.sleep(0.001)

    tone = generate_tone(440, 0.001)  # Duración de 0.5 segundos
    sd.play(tone, 44100)

    print(f"🎸 Nota {note['id']} - {note['time_seconds']}s")
    
    sd.wait()  # Esperar a que termine de sonar antes de seguir

print("✅ ¡Todas las notas ejecutadas!")
