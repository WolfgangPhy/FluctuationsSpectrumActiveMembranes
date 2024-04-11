import scipy.constants as const
import scipy.special

class FrequencySpectrums:
    
    @staticmethod
    def base_spectrum(wave_vector, temperature, volumic_mass, surface_tension,  area, kappa):
        BOLTZMANN_NM = const.k*1e18
        EARTH_GRAVITY = 9.81*1e9
        spectrum = 1.0/area * BOLTZMANN_NM * temperature/(volumic_mass*EARTH_GRAVITY + surface_tension*wave_vector**2
                                                     + kappa*wave_vector**4)
        return spectrum
class SpatialSpectrums:
    
    @staticmethod
    def base_spectrum(distance, temperature, capillary_frequency, curvature_frequency, surface_tension):
        #Convert to nanometers
        BOLTZMANN_NM = const.k*1e18
                
        factor =  BOLTZMANN_NM*temperature/(2*const.pi*surface_tension)
        bessel_capillary = scipy.special.kn(0, distance*capillary_frequency)
        bessel_curvature = scipy.special.kn(0, distance*curvature_frequency)
        return factor*(bessel_capillary-bessel_curvature)
    
    
