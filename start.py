import librosa
import json

# Cargar canción
filename = 'SHE IS A YAQUI LADY.mp3'
y, sr = librosa.load(filename)

# Separar componente armónica (melodía como guitarra)
harmonic, _ = librosa.effects.hpss(y)

# Obtener fuerza de los onsets solo del componente armónico
onset_env = librosa.onset.onset_strength(y=harmonic, sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='frames')
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Función para obtener color según frecuencia dominante
def get_color_from_freq(freq):
    if freq < 150:
        return "red"
    elif freq < 300:
        return "blue"
    elif freq < 600:
        return "green"
    else:
        return "yellow"

# Estimar frecuencia para cada onset
frame_length = 2048
hop_length = 512
notes = []

for i, frame in enumerate(onset_frames):
    # Tomamos una pequeña ventana alrededor del onset
    start = max(0, frame - 2)
    end = frame + 2
    y_segment = harmonic[start * hop_length:end * hop_length]

    if len(y_segment) < 2048:
        continue  # Evitar errores si el segmento es muy corto

    # Estimar la frecuencia dominante
    f0 = librosa.yin(y_segment, fmin=80, fmax=1000, sr=sr)
    freq = float(f0[0]) if len(f0) > 0 else 0

    color = get_color_from_freq(freq)

    notes.append({
        "id": i % 4,  # Nota para jugar
        "color": color,
        "freq": round(freq, 2),
        "time_seconds": round(float(librosa.frames_to_time(frame, sr=sr)), 3)
    })

# Guardar como JSON
with open("notas_guitarra.json", "w") as f:
    json.dump(notes, f, indent=2)

print(f"✅ {len(notes)} notas generadas y guardadas en notas_guitarra.json")
