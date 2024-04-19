import numpy as np


class FourierTransform:
    
    @staticmethod
    def inverse_fft(spectrum, resolution):
        return np.fft.irfft(spectrum, resolution)