from functools import reduce

from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 44100

FREQUENCY = 440


class Tone(object):
    sample_rate = 44100

    def __init__(self, frequency_hz, duration_seconds=1, amplitude=0.5):
        self.frequency = frequency_hz
        self.duration_seconds = duration_seconds
        self.amplitude = amplitude
        self.sample_times = np.linspace(0., duration_seconds, self.sample_rate)
        self.data = amplitude * np.sin(2. * np.pi * frequency_hz * self.sample_times)

    def get_data(self):
        return self.data.copy()

    def write_tone_to_file(self, save_path):
        write(save_path, self.sample_rate, self.get_data())


class Silence(Tone):
    def __init__(self, duration_seconds=1):
        self.sample_times = np.linspace(0., duration_seconds, self.sample_rate)
        self.data = np.zeros(len(self.sample_times))


class ToneSequence(Tone):
    def __init__(self, tone_frequencies, tone_durations=1, tone_amplitudes=0.5, gap_durations=1):
        self.tone_frequencies = tone_frequencies
        self.tone_durations = tone_durations
        self.tone_amplitudes = tone_amplitudes
        self.gap_durations = gap_durations
        self.silence_data = Silence(self.gap_durations).get_data()
        self.tones = [Tone(f, duration_seconds=tone_durations, amplitude=tone_amplitudes) for f in tone_frequencies]
        self.tones_data = [t.get_data() for t in self.tones]
        self.data = reduce(lambda a, b: np.concatenate((a, self.silence_data, b)), self.tones_data)






test_tone = Tone(440)
test_tone.write_tone_to_file('example2.wav')

test_tone = Silence()
test_tone.write_tone_to_file('example3.wav')

test_sequence = ToneSequence([440, 450, 460, 470])
test_sequence.write_tone_to_file('example4.wav')