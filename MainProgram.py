import json
import numpy as np
from Spectrums import CorrelationFunctions
from Spectrums import FrequencySpectrums
from FourierTransform import FourierTransform
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
        self.true_correlation_function = None
        self.frequency_spectrum = None
        self.space_spectrum = None
        self.spectrum_filename = None
        self.resolution = None
        self.get_parameters_from_json()
        self.set_parameters()
        self.assign_normalisation_factor()
        self.get_files_path()
        self.init_arrays()
        
    def get_files_path(self):
        with open("OutputPaths.json") as file:
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
        self.kappa = self.parameters["kappa"]
        self.area = self.parameters["area"] 
        self.resolution = self.parameters["resolution"]
        self.is_accuracy_test = self.parameters["is_accuracy_test"]
        self.ft_normalization = self.parameters["ft_normalization"]
        self.capillary_frequency = np.sqrt(self.volumic_mass/self.surface_tension)
        self.curvature_frequency = np.sqrt(self.surface_tension/self.kappa)
        self.min_frequency = self.curvature_frequency*1e-13
        self.max_frequency = self.curvature_frequency*10
        self.min_distance = 1/self.max_frequency
        self.max_distance = 1/self.min_frequency
        self.save_computed_parameters()
        self.check_and_assign_spectrum_function(self.parameters["spectrum_function"])
        self.check_and_assign_inverse_fourier_transform_method(self.parameters["inverse_fourier_transform_method"])

    def save_computed_parameters(self):
        computed_parameters = {"capillary_frequency": self.capillary_frequency,
                               "curvature_frequency": self.curvature_frequency, "min_frequency": self.min_frequency,
                               "max_frequency": self.max_frequency, "min_distance": self.min_distance,
                               "max_distance": self.max_distance}
        with open("ComputedParameters.json", "w") as file:
            json.dump(computed_parameters, file, indent=4)

    def check_and_assign_spectrum_function(self, spectrum_function):
        spectrum_method = getattr(FrequencySpectrums, spectrum_function, None)
        if spectrum_method is not None and callable(spectrum_method):
            self.spectrum_function = spectrum_method
        else:
            raise ValueError("The spectrum function provided in the parameters is not valid.")
        
    def check_and_assign_inverse_fourier_transform_method(self, inverse_fourier_transform_method):
        inverse_fourier_transform_method = getattr(FourierTransform, inverse_fourier_transform_method, None)
        if inverse_fourier_transform_method is not None and callable(inverse_fourier_transform_method):
            self.inverse_fourier_transform_method = inverse_fourier_transform_method
        else:
            raise ValueError("The inverse fourier transform method provided in the parameters is not valid.")

    def init_arrays(self):
        self.wave_vector_array = np.logspace(np.log10(self.min_frequency), np.log10(self.max_frequency), self.resolution)
        self.space_array = np.linspace(self.min_distance, self.max_distance, self.resolution)
        self.true_correlation_function = np.zeros(self.resolution)

    def compute_true_correlation_function(self):
        self.true_correlation_function = CorrelationFunctions.base_correlation_function(self.space_array, self.temperature,
                                                                  self.capillary_frequency, self.curvature_frequency,
                                                                  self.surface_tension)

    def compute_frequency_spectrum(self):
        self.frequency_spectrum = self.spectrum_function(self.wave_vector_array, self.temperature,
                                                         self.volumic_mass, self.surface_tension, self.area,
                                                         self.kappa)
        
        spectrum_df = pd.DataFrame({'spectrum': self.frequency_spectrum, 'frequency': self.wave_vector_array})
        spectrum_df.to_csv("frequency_spectrum.csv", index=False)

    def assign_normalisation_factor(self):
        if(self.ft_normalization == "symmetric"):
            self.normalisation_factor = np.sqrt(self.area)/(2*np.pi)
        elif(self.ft_normalization == "asymmetric_ft"):
            self.normalisation_factor = 1
        elif(self.ft_normalization == "asymmetric_ift"):
            self.normalisation_factor = self.area/(2*np.pi)**2
    def compute_inverse_fourier_transform(self):
        self.space_spectrum = self.normalisation_factor * self.inverse_fourier_transform_method(self.frequency_spectrum, self.resolution)

    def save_results(self):
        true_spectrum_df = pd.DataFrame({'spectrum': self.true_correlation_function, 'space': self.space_array})
        fft_spectrum_df = pd.DataFrame({'spectrum': self.space_spectrum, 'space': self.space_array})

        true_spectrum_df.to_csv("true_spectrum.csv", index=False)
        fft_spectrum_df.to_csv(self.spectrum_filename, index=False)

    def execute(self):
        if(self.is_accuracy_test):
            self.compute_true_correlation_function()
        self.compute_frequency_spectrum()
        self.compute_inverse_fourier_transform()
        self.save_results()
        
        visualizer = Visualizer(self.spectrum_filename)
        if(self.is_accuracy_test):
            visualizer.compare_spectrums()
        visualizer.plot_frequency_spectrum()
        visualizer.true_space_spectrum()
        
        
if __name__ == "__main__":
    main = MainProgram()
    main.execute()
