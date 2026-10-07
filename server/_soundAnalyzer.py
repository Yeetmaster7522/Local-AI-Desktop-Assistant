from scipy.io import wavfile
import numpy as np

def get_normalized_amplitude():
    epsilon = 1e-10
    _, data = wavfile.read("speech.wav")
    dbs = 20 * np.log10(np.abs(data) + epsilon)
    
    return (dbs - dbs.min()) / (dbs.max() - dbs.min())