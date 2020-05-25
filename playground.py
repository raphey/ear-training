from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 44100

FREQUENCY = 440

t = np.linspace(0., 1., SAMPLE_RATE)
amplitude = np.iinfo(np.int16).max
amplitude = 1
data = amplitude * np.sin(2. * np.pi * FREQUENCY * t)
print(data)
write('example.wav', SAMPLE_RATE, data)
