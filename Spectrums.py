import scipy.constants as const


class FrequencySpectrums:

    @staticmethod
    def base_spectrum(wave_vector_x, wave_vector_y, temperature, volumic_mass, surface_tension, area, kappa):
        wave_vector_norm = (wave_vector_x ** 2 + wave_vector_y ** 2) ** 0.5
        
        spectrum = 1.0 / area * const.k * temperature / (
                    volumic_mass * const.g + surface_tension * wave_vector_norm ** 2
                    + kappa * wave_vector_norm ** 4)
        return spectrum
