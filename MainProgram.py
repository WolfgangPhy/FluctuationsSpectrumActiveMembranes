import json
import os
import numpy as np
from CorrelationFunctions import CorrelationFunctions
from Spectrums import FrequencySpectrums
from FourierTransform import FourierTransform
from Visualizer import Visualizer
from FileHelper import FileHelper
import scipy.constants as const
import pandas as pd
import csv


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
        self.true_correlation_function = None
        self.frequency_spectrum = None
        self.computed_correlation_function = None
        self.correlation_function_path = None
        self.resolution = None
        self.outputfile_path = FileHelper.init_calculation_directory()
        self.get_parameters_from_json()
        self.set_parameters()
        self.assign_normalisation_factor()
        self.get_files_path()
        self.init_arrays()
        
    def get_files_path(self):   
        self.correlation_function_path = FileHelper.give_output_path(self.outputfile_path, "computed_correlation")
        self.true_correlation_function_path = FileHelper.give_output_path(self.outputfile_path, "true_correlation")
        self.frequency_spectrum_path = FileHelper.give_output_path(self.outputfile_path, "frequency_spectrum")

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
        
        with open(FileHelper.give_output_path(self.outputfile_path, "computed_parameters"), "w") as file:
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
        wave_vector_array = np.logspace(np.log10(self.min_frequency), np.log10(self.max_frequency), self.resolution)
        space_array = np.linspace(self.min_distance, self.max_distance, self.resolution)
        
        self.wave_vector_array_x, self.wave_vector_array_y = np.meshgrid(wave_vector_array, wave_vector_array)
        self.space_array_x, self.space_array_y = np.meshgrid(space_array, space_array)
        self.true_correlation_function = np.zeros((self.resolution, self.resolution))
        
    

    def compute_true_correlation_function(self):
        self.true_correlation_function = CorrelationFunctions.base_correlation_function(self.space_array_x, self.space_array_y, self.temperature,
                                                                  self.capillary_frequency, self.curvature_frequency,
                                                                  self.surface_tension)

    def compute_frequency_spectrum(self):
        self.frequency_spectrum = self.spectrum_function(self.wave_vector_array_x, self.wave_vector_array_y, self.temperature,
                                                         self.volumic_mass, self.surface_tension, self.area,
                                                         self.kappa)

    def assign_normalisation_factor(self):
        if(self.ft_normalization == "symmetric"):
            self.normalisation_factor = np.sqrt(self.area)/(2*np.pi)
        elif(self.ft_normalization == "asymmetric_ft"):
            self.normalisation_factor = 1
        elif(self.ft_normalization == "asymmetric_ift"):
            self.normalisation_factor = self.area/(2*np.pi)**2
    
    def compute_inverse_fourier_transform(self):
        self.computed_correlation_function = self.normalisation_factor * self.inverse_fourier_transform_method(self.frequency_spectrum)

    def save_results(self):
        if(self.is_accuracy_test):    
            with open(self.true_correlation_function_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y', 'distance', 'correlation_function'])
                for i in range(self.resolution):
                    for j in range(self.resolution):
                        writer.writerow([self.space_array_x[i, j],
                                         self.space_array_y[i, j],
                                         np.sqrt(self.space_array_x[i, j]**2 + self.space_array_y[i, j]**2),
                                         self.true_correlation_function[i, j]])
            
        with open(self.correlation_function_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y', 'distance', 'correlation_function'])
                for i in range(self.resolution):
                    for j in range(self.resolution):
                        writer.writerow([self.space_array_x[i, j],
                                         self.space_array_y[i, j],
                                         np.sqrt(self.space_array_x[i, j]**2 + self.space_array_y[i, j]**2),
                                         self.computed_correlation_function[i, j]])
                        
        with open(self.frequency_spectrum_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['kx', 'ky', 'norm', 'spectrum'])  # Write the header
            for i in range(self.resolution):
                for j in range(self.resolution):
                    writer.writerow([self.wave_vector_array_x[i, j],
                                     self.wave_vector_array_y[i, j],
                                     np.sqrt(self.wave_vector_array_x[i, j]**2 + self.wave_vector_array_y[i, j]**2),
                                     self.frequency_spectrum[i, j]])

    def execute(self):
        if(self.is_accuracy_test):
            self.compute_true_correlation_function()
        self.compute_frequency_spectrum()
        self.compute_inverse_fourier_transform()
        self.save_results()
        
        visualizer = Visualizer(self.outputfile_path)
        if(self.is_accuracy_test):
            visualizer.compare_correlation_functions()
            visualizer.plot_true_correlation_function()  
        visualizer.plot_frequency_spectrum()
        visualizer.plot_computed_correlation_function()
        
        
if __name__ == "__main__":
    main = MainProgram()
    main.execute()
