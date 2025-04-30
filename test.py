import json
import time
import numpy as np
import sounddevice as sd
import pygame

# --- Generar tono para notas ---
def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.3 * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32)

# --- Colores por ID ---
colors = {
    "red": ('\033[91m', '🟥'),  # rojo
    "yellow": ('\033[93m', '🟨'),  # amarillo
    "green": ('\033[92m', '🟩'),  # verde
    "blue": ('\033[94m', '🟦')   # azul
}
RESET = '\033[0m'

# --- Cargar notas desde JSON ---
with open('notas_guitarra.json') as f:
    notes = json.load(f)

# --- Reproducir canción ---
pygame.mixer.init()
pygame.mixer.music.load("SHE IS A YAQUI LADY.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

# --- Iniciar cronómetro ---
start_time = time.time()

# --- Reproducir notas sincronizadas ---
for note in notes:
    while (time.time() - start_time) < note['time_seconds']:
        time.sleep(0.001)

    note_id = note['id']

    color_code, emoji = colors[note['color']]
    print(f"{color_code}{emoji} Nota {note['color']} - {note['time_seconds']}s{RESET}")

print("✅ Prueba terminada")
