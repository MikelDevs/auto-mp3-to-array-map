import librosa
import librosa.display
import numpy as np
import json
import matplotlib.pyplot as plt

# Carga el archivo de audio
filename = 'SHE IS A YAQUI LADY.mp3'
y, sr = librosa.load(filename)

# Calcula la energía (Root Mean Square - RMS)
hop_length = 512
rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]

# Crea un array de tiempos
frames = range(len(rms))
times = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)

# Detecta picos automáticamente
threshold = np.mean(rms) * 1.3  # 1.2 veces la media
peak_indices = np.where(rms > threshold)[0]
peak_times = librosa.frames_to_time(peak_indices, sr=sr, hop_length=hop_length)

# Función para obtener la frecuencia dominante de una señal
def get_dominant_frequency(y_window, sr, hop_length):
    # Hacer la FFT para obtener las frecuencias
    D = np.abs(librosa.stft(y_window, n_fft=1024, hop_length=hop_length))
    # Obtener las frecuencias en Hz
    freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
    # Obtener la frecuencia dominante (la que tiene mayor magnitud)
    magnitude = np.sum(D, axis=1)
    dominant_freq = freqs[np.argmax(magnitude)]
    return dominant_freq

# Función para convertir frecuencia a nota
def frequency_to_note(freq):
    midi_note = librosa.hz_to_midi(freq)
    return librosa.midi_to_note(midi_note)

# Función para obtener las frecuencias y notas asociadas a los picos
def get_frequencies(y, sr, hop_length, peak_times):
    note_freqs = []
    for peak_time in peak_times:
        frame = librosa.time_to_frames(peak_time, sr=sr, hop_length=hop_length)
        # Extraer una ventana de audio alrededor del pico
        start = max(0, int(frame) - hop_length // 2)
        end = min(len(y), int(frame) + hop_length // 2)
        y_window = y[start:end]

        # Obtener la frecuencia dominante
        dominant_freq = get_dominant_frequency(y_window, sr, hop_length)
        note_freqs.append(dominant_freq)

    return note_freqs

# Extraer las frecuencias de cada pico
note_freqs = get_frequencies(y, sr, hop_length, peak_times)

# Convertir las frecuencias detectadas en notas
note_names = [frequency_to_note(freq) for freq in note_freqs]

# Crear una lista de objetos con los tiempos y las notas detectadas
notes_data = [{"time": time, "note": note} for time, note in zip(peak_times, note_names)]

# Guardar los resultados en un archivo JSON
file_path = 'notes_detected.json'
with open(file_path, 'w') as file:
    json.dump(notes_data, file, indent=4)

# Mostrar el resultado en consola
for item in notes_data:
    print(f"Tiempo: {item['time']:.2f} segundos - Nota: {item['note']}")

# Grafica
plt.figure(figsize=(14, 5))
plt.plot(times, rms, color='purple', label='Energía RMS')
plt.vlines(peak_times, ymin=0, ymax=max(rms), color='red', linestyle='--', label='Notas detectadas')
plt.title('Energía de la canción y notas detectadas')
plt.xlabel('Tiempo (s)')
plt.ylabel('Energía')
plt.legend()
plt.show()
