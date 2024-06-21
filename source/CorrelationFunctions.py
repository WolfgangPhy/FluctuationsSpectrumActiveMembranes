import numpy as np

from scipy import constants as const
from scipy.special import kn as bessel_second_kind


class CorrelationFunctions:
    """
    Class to store the different correlation functions that can be used in the calculations.
    
    # Remarks:
        The correlation functions are only used to test the algorithms.

    # Returns:
        numpy.ndarray: The correlation function.
    """
    @staticmethod
    def base_correlation_function(x : np.ndarray, y : np.ndarray, temperature : float, capillary_frequency : float, curvature_frequency : float, surface_tension : float) -> np.ndarray:
        """
        Base correlation function used to calibrate and test the algorithms.

        Args:
            x (numpy.ndarray): x coordinates.
            y (numpy.ndarray): y coordinates.
            temperature (float): temperature of the system.
            capillary_frequency (float): capillary frequency.
            curvature_frequency (float): curvature frequency.
            surface_tension (float): surface tension of the system.

        Returns:
            numpy.ndarray: the correlation function.
        """
        distance : np.ndarray = (x ** 2 + y ** 2) ** 0.5
        
        factor : float = const.k * temperature / (2 * const.pi * surface_tension)
        bessel_capillary : np.ndarray = bessel_second_kind(0, distance * capillary_frequency)
        bessel_curvature : np.ndarray = bessel_second_kind(0, distance * curvature_frequency)
        return factor * (bessel_capillary - bessel_curvature)
