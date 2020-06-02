from datetime import datetime
from functools import reduce
from random import choice
from random import randint

from scipy.io.wavfile import write
import numpy as np


class Tone(object):
    sample_rate = 44100
    envelope_samples = 100

    def __init__(self, frequency_hz, duration_seconds=1, amplitude=0.5):
        self.frequency = frequency_hz
        self.duration_seconds = duration_seconds
        self.amplitude = amplitude
        self.sample_times = np.linspace(0., duration_seconds, self.sample_rate)
        self.data = amplitude * np.sin(2. * np.pi * frequency_hz * self.sample_times)
        self.envelope_data()

    def envelope_data(self):
        if len(self.data) < 2 * self.envelope_samples:
            return
        for i in range(self.envelope_samples):
            ratio = float(i) / self.envelope_samples
            self.data[i] *= ratio
            self.data[-(i + 1)] *= ratio

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


class RandomTonePairSequence(ToneSequence):
    note_frequencies = [
        ('C3', 130.81),
        ('C#3', 138.59),
        ('D3', 146.83),
        ('D#3', 155.56),
        ('E3', 164.81),
        ('F3', 174.61),
        ('F#3', 185.00),
        ('G3', 196.00),
        ('G#3', 207.65),
        ('A3', 220.00),
        ('A#3', 233.08),
        ('B3', 246.94),
        ('C4', 261.63),
        ('C#4', 277.18),
        ('D4', 293.66),
        ('D#4', 311.13),
        ('E4', 329.63),
        ('F4', 349.23),
        ('F#4', 369.99),
        ('G4', 392.00),
        ('G#4', 415.30),
        ('A4', 440.00),
        ('A#4', 466.16),
        ('B4', 493.88),
        ('C5', 523.25),
        ('C#5', 554.37),
        ('D5', 587.33),
        ('D#5', 622.25),
        ('E5', 659.25),
        ('F5', 698.46),
        ('F#5', 739.99),
        ('G5', 783.99),
        ('G#5', 830.61),
        ('A5', 880.00),
    ]

    semitone_ratio = 2.0**(1.0 / 12)

    def __init__(self, tone_count, tuning_width, tone_durations=1, tone_amplitudes=0.5, gap_durations=1):
        self.base_key, self.base_f = choice(list(self.note_frequencies))
        self.tone_count = tone_count
        self.tuning_width = tuning_width
        self.random_bits = ''.join(str(randint(0, 1)) for _ in range(tone_count))
        tuning_ratio = self.semitone_ratio**self.tuning_width
        lo_f, hi_f = ((self.base_f, self.base_f * tuning_ratio) if self.random_bits[0] == '0' else
                      (self.base_f / tuning_ratio, self.base_f))
        frequencies = [lo_f if b == '0' else hi_f for b in self.random_bits]
        super(RandomTonePairSequence, self).__init__(tone_frequencies=frequencies,
                                                     tone_durations=tone_durations,
                                                     tone_amplitudes=tone_amplitudes,
                                                     gap_durations=gap_durations)

    def write_tone_to_file(self, save_path=None):
        if save_path is None:
            date_string = datetime.today().strftime('%Y%m%d-%H%M%S')
            save_path = '{}_{}_{}_{}.wav'.format(date_string, self.tuning_width, self.base_key, self.random_bits)
        super(RandomTonePairSequence, self).write_tone_to_file(save_path)


for _ in range(10):
    tps = RandomTonePairSequence(10, 0.15)
    tps.write_tone_to_file()
