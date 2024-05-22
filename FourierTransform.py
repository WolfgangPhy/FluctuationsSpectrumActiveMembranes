import numpy as np


class FourierTransform:
    
    @staticmethod
    def inverse_fft_2d(spectrum):
        return np.fft.irfft2(spectrum)