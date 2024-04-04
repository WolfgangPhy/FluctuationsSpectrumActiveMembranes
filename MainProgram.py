import json
import numpy as np
from Spectrums import SpatialSpectrums
from Spectrums import FrequencySpectrums
from Visualizer import Visualizer
import scipy.constants as const
import pandas as pd



class MainProgram:

    def __init__(self):
        self.capillary_frequency = None
        self.curvature_frequency = None
        self.area = None
        self.max_frequency = None
        self.min_frequency = None
        self.surface_tension = None
        self.volumic_mass = None
        self.temperature = None
        self.spectrum_function = None
        self.parameters = None
        self.wave_vector_array = None
        self.space_array = None
        self.true_space_spectrum = None
        self.frequency_spectrum = None
        self.space_spectrum = None
        self.spectrum_filename = None
        self.get_parameters_from_json()
        self.set_parameters()
        self.get_files_path()
        self.init_arrays()
        
    def get_files_path(self):
        with open("Config.json") as file:
            self.spectrum_filename = json.load(file)["spectrum_filename"]
            

    def get_parameters_from_json(self):
        """
        Loads parameters from the "Parameters.json" file and assigns them to the MainProgram `parameters` attribute.
        """
        with open("Parameters.json") as file:
            self.parameters = json.load(file)

    def set_parameters(self):
        self.temperature = self.parameters["temperature"]
        self.volumic_mass = self.parameters["volumic_mass"]
        self.surface_tension = self.parameters["surface_tension"]
        self.min_frequency = self.parameters["min_frequency"]
        self.max_frequency = self.parameters["max_frequency"]
        self.area = self.parameters["area"]
        self.curvature_frequency = self.parameters["curvature_frequency"]
        self.capillary_frequency = self.parameters["capillary_frequency"]
        self.check_and_assign_spectrum_function(self.parameters["spectrum_function"])

    def check_and_assign_spectrum_function(self, spectrum_function):
        spectrum_method = getattr(FrequencySpectrums, spectrum_function, None)
        if spectrum_method is not None and callable(spectrum_method):
            self.spectrum_function = spectrum_method
        else:
            raise ValueError("The spectrum function provided in the parameters is not valid.")

    def init_arrays(self):
        self.wave_vector_array = np.linspace(self.min_frequency, self.max_frequency, 1000)
        self.space_array = np.linspace(0.03, 300, 1000)
        self.true_space_spectrum = np.zeros(1000)

    def compute_true_space_spectrum(self):
        self.true_space_spectrum = SpatialSpectrums.base_spectrum(self.space_array, self.temperature,
                                                                  self.capillary_frequency, self.curvature_frequency,
                                                                  self.surface_tension)

    def compute_true_frequency_spectrum(self):
        kappa = const.k * self.temperature
        self.frequency_spectrum = self.spectrum_function(self.wave_vector_array, self.temperature,
                                                         self.volumic_mass, self.surface_tension, self.area,
                                                         kappa)

    def compute_inverse_fourier_transform(self):
        self.space_spectrum = np.fft.ifft(self.frequency_spectrum)

    def save_results(self):
        true_spectrum_df = pd.DataFrame({'spectrum': self.true_space_spectrum, 'space': self.space_array})
        fft_spectrum_df = pd.DataFrame({'spectrum': self.space_spectrum, 'space': self.space_array})

        true_spectrum_df.to_csv("true_spectrum.csv", index=False)
        fft_spectrum_df.to_csv(self.spectrum_filename, index=False)

    def execute(self):
        self.compute_true_space_spectrum()
        self.compute_true_frequency_spectrum()
        self.compute_inverse_fourier_transform()
        self.save_results()
        
        visualizer = Visualizer(self.spectrum_filename)
        visualizer.compare_spectrums()
        
        
if __name__ == "__main__":
    main = MainProgram()
    main.execute()