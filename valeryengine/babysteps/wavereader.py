from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np


samplerate, data = wavfile.read('wave_files/hey0.wav')

print(data[::2, 1])
