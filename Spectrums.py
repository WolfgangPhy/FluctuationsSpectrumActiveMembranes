import scipy.constants as const


class FrequencySpectrums:

    @staticmethod
    def base_spectrum(wave_vector, temperature, volumic_mass, surface_tension, area, kappa):
        spectrum = 1.0 / area * const.k * temperature / (
                    volumic_mass * const.g + surface_tension * wave_vector ** 2
                    + kappa * wave_vector ** 4)
        return spectrum
