import numpy as np


class FourierTransform:
    """
    Class to store the different Fourier Transform techniques that can be used in the calculations.
    """

    @staticmethod
    def inverse_fft(spectrum: np.ndarray) -> np.ndarray:
        """
        Method to compute the inverse Fast Fourier Transform of a given spectrum.

        Args:
            spectrum (numpy.ndarray): The spectrum to compute the inverse Fast Fourier Transform of.

        Returns:
            numpy.ndarray: The inverse Fast Fourier Transform of the given spectrum.
        """
        return np.fft.irfft2(spectrum)
