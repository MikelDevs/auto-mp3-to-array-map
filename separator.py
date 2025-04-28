import librosa
import soundfile as sf
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import json

# 1. Cargar la canción
y, sr = librosa.load('SHE IS A YAQUI LADY.mp3', sr=None)

# 2. Separar en componentes armónicos y percusivos
harmonic, percussive = librosa.effects.hpss(y)

# 3. Guardar sólo la parte armónica (opcional)
sf.write('harmonic_only.wav', harmonic, sr)

# 4. Detectar onsets (golpes o notas)
onset_frames = librosa.onset.onset_detect(y=harmonic, sr=sr, backtrack=True)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# 5. Crear una lista de notas estilo Guitar Hero
notes = []
for idx, time in enumerate(onset_times):
    note = {
        "id": idx + 1.25,
        "time_seconds": round(float(time), 3)  # Redondeamos a 3 decimales
    }
    notes.append(note)

# 6. Guardar la lista como un archivo JSON
with open('notes_detected.json', 'w') as f:
    json.dump(notes, f, indent=4)

# 7. Mostrar visualmente las notas
plt.figure(figsize=(14, 5))
librosa.display.waveshow(harmonic, sr=sr)
plt.vlines(onset_times, -1, 1, color='r')
plt.title('Notas detectadas')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.show()

print(f"Notas detectadas y guardadas en notes_detected.json ({len(notes)} notas).")
