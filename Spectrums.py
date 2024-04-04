import scipy.constants as const
import scipy.special

class FrequencySpectrums:
    
    @staticmethod
    def base_spectrum(wave_vector, temperature, volumic_mass, surface_tension,  area, kappa):
        spectrum = 1.0/area * const.k * temperature/(volumic_mass*const.g + surface_tension*wave_vector**2
                                                     + kappa*wave_vector**4)
        return spectrum
class SpatialSpectrums:
    
    @staticmethod
    def base_spectrum(distance, temperature, capillary_frequency, curvature_frequency, surface_tension):
        factor =  const.k*temperature/(2*const.pi*surface_tension)
        bessel_capillary = scipy.special.kn(0, distance*capillary_frequency)
        bessel_curvature = scipy.special.kn(0, distance*curvature_frequency)
        return factor*(bessel_capillary-bessel_curvature)
    
