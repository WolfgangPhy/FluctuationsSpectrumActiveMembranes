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
    def base_correlation_function(x, y, temperature, capillary_frequency, curvature_frequency, surface_tension):
        distance = (x ** 2 + y ** 2) ** 0.5
        
        factor = const.k * temperature / (2 * const.pi * surface_tension)
        bessel_capillary = bessel_second_kind(0, distance * capillary_frequency)
        bessel_curvature = bessel_second_kind(0, distance * curvature_frequency)
        return factor * (bessel_capillary - bessel_curvature)