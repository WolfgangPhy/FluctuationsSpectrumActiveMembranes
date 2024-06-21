import scipy.constants as const
import numpy as np


class FrequencySpectrums:
    """
    Class to store the different frequency spectrums that can be used in the calculations.
    """
    @staticmethod
    def base_spectrum(wave_vector_x : np.ndarray, wave_vector_y : np.ndarray, temperature : float, volumic_mass : float, surface_tension : float, area : float, kappa : float) -> np.ndarray:
        """
        Base spectrum used to calibrate and test the algorithms.

        # Args:
            wave_vector_x (numpy.ndarray): wave vector in the x direction.
            wave_vector_y (numpy.ndarray): wave vector in the y direction.
            temperature (float): The temperature of the system.
            volumic_mass (float): The volumic mass of the system.
            surface_tension (float): The surface tension of the system.
            area (float): The area of the system.
            kappa (float): The bending rigidity modulus.

        # Returns:
            numpy.ndarray: The spectrum 
        """
        wave_vector_norm = (wave_vector_x ** 2 + wave_vector_y ** 2) ** 0.5
        
        spectrum = 1.0 / area * const.k * temperature / (
                    volumic_mass * const.g + surface_tension * wave_vector_norm ** 2
                    + kappa * wave_vector_norm ** 4)
        return spectrum
