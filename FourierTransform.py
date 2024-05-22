import numpy as np


class FourierTransform:
    
    @staticmethod
    def inverse_fft(spectrum):
        return np.fft.irfft2(spectrum)
