import csv
import json

import numpy as np

from CorrelationFunctions import CorrelationFunctions
from FileHelper import FileHelper
from FourierTransform import FourierTransform
from Spectrums import FrequencySpectrums
from Visualizer import Visualizer


class MainProgram:
    """
    MainProgram class manages the main functionalities of the program, including parameter loading, calculation,
    and result saving.

    # Attributes:
        - `kappa (float)`: The bending rigidity modulus.
        - `max_distance (float)`: The upper bound of the distance.
        - `min_distance (float)`: The lower bound of the distance.
        - `ft_normalization (str)`: The normalization method for Fourier Transform.
        - `is_accuracy_test (bool)`: Flag indicating if it's an accuracy test.
        - `normalisation_factor (float)`: The normalization factor of the Fourier Transform.
        - `space_array_y (ndarray)`: The array representing space in y dimension.
        - `space_array_x (ndarray)`: The array representing space in x dimension.
        - `wave_vector_array_y (ndarray)`: The array representing wave vectors in y dimension.
        - `wave_vector_array_x (ndarray)`: The array representing wave vectors in x dimension.
        - `inverse_fourier_transform_method` (callable): The method for inverse Fourier Transform.
        - `frequency_spectrum_path (str)`: The path to save the frequency spectrum.
        - `true_correlation_function_path (str)`: The path to save the true correlation function.
        - `capillary_frequency (float)`: The capillary frequency.
        - `curvature_frequency (float)`: The curvature frequency.
        - `area (float)`: The area of the cell.
        - `max_frequency (float)`: The upper bound of the frequency.
        - `min_frequency (float)`: The lower bound of the frequency.
        - `surface_tension (float)`: The surface tension.
        - `volumic_mass (float)`: The volumic mass.
        - `temperature (float)`: The temperature.
        - `spectrum_function (callable)`: The function to calculate the spectrum.
        - `parameters (dict)`: Dictionary containing loaded parameters.
        - `true_correlation_function (ndarray)`: The true correlation function.
        - `frequency_spectrum (ndarray)`: The frequency spectrum.
        - `computed_correlation_function (ndarray)`: The computed correlation function.
        - `correlation_function_path (str)`: The path to save the computed correlation function.
        - `resolution (int)`: The resolution (number of points in the space and frequency arrays).
        - `outputfile_path (str)`: The path for output files.

    # Methods:
        - `get_files_path()`: Gets the paths for output files.
        - `get_parameters_from_json()`: Loads parameters from "Parameters.json" file.
        - `set_parameters()`: Sets the parameters.
        - `save_computed_parameters()`: Saves computed parameters to a file.
        - `check_and_assign_spectrum_function()`: Checks and assigns the spectrum function.
        - `check_and_assign_inverse_fourier_transform_method()`: Checks and assigns the inverse Fourier
        Transform method.
        - `init_arrays()`: Initializes arrays.
        - `compute_true_correlation_function()`: Computes the true correlation function.
        - `compute_frequency_spectrum()`: Computes the frequency spectrum.
        - `assign_normalisation_factor()`: Assigns the normalization factor.
        - `compute_inverse_fourier_transform()`: Computes the inverse Fourier Transform.
        - `save_results()`: Saves the results to CSV files.
        - `execute()`: Executes the main program flow.
    """
    def __init__(self):
        """
        Initializes the MainProgram object and sets the default values for the attributes.
        """
        self.kappa = None
        self.max_distance = None
        self.min_distance = None
        self.ft_normalization = None
        self.is_accuracy_test = None
        self.normalisation_factor = None
        self.space_array_y = None
        self.space_array_x = None
        self.wave_vector_array_y = None
        self.wave_vector_array_x = None
        self.inverse_fourier_transform_method = None
        self.frequency_spectrum_path = None
        self.true_correlation_function_path = None
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
        """
        Gets the paths for the output files from OutputPaths.json file.
        """
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
        """
        Sets the parameters from the loaded parameters dictionary.
        """
        self.temperature = self.parameters["temperature"]
        self.volumic_mass = self.parameters["volumic_mass"]
        self.surface_tension = self.parameters["surface_tension"]
        self.kappa = self.parameters["kappa"]
        self.area = self.parameters["area"]
        self.resolution = self.parameters["resolution"]
        self.is_accuracy_test = self.parameters["is_accuracy_test"]
        self.ft_normalization = self.parameters["ft_normalization"]
        self.capillary_frequency = np.sqrt(self.volumic_mass / self.surface_tension)
        self.curvature_frequency = np.sqrt(self.surface_tension / self.kappa)
        self.min_frequency = self.curvature_frequency * 1e-13
        self.max_frequency = self.curvature_frequency * 10
        self.min_distance = 1 / self.max_frequency
        self.max_distance = 1 / self.min_frequency
        self.save_computed_parameters()
        self.check_and_assign_spectrum_function(self.parameters["spectrum_function"])
        self.check_and_assign_inverse_fourier_transform_method(self.parameters["inverse_fourier_transform_method"])

    def save_computed_parameters(self):
        """
        Saves the computed parameters in the current calculation directory.
        """
        computed_parameters = {"capillary_frequency": self.capillary_frequency,
                               "curvature_frequency": self.curvature_frequency, "min_frequency": self.min_frequency,
                               "max_frequency": self.max_frequency, "min_distance": self.min_distance,
                               "max_distance": self.max_distance}

        with open(FileHelper.give_output_path(self.outputfile_path, "computed_parameters"), "w") as file:
            json.dump(computed_parameters, file, indent=4)

    def check_and_assign_spectrum_function(self, spectrum_function):
        """
        Checks if the spectrum function provided in the parameters is valid (correspond to an existing method in
        Spectrums.py) and assigns it to the MainProgram

        # Args:
            spectrum_function (str): The name of the spectrum function to be checked and assigned.

        # Raises:
            ValueError: If the spectrum function provided in the parameters is not valid.
        """
        spectrum_method = getattr(FrequencySpectrums, spectrum_function, None)
        if spectrum_method is not None and callable(spectrum_method):
            self.spectrum_function = spectrum_method
        else:
            raise ValueError("The spectrum function provided in the parameters is not valid.")

    def check_and_assign_inverse_fourier_transform_method(self, inverse_fourier_transform_method):
        """
        Checks if the inverse fourier transform method provided in the parameters is valid (correspond to an existing

        # Args:
            inverse_fourier_transform_method (str): The name of the inverse fourier transform method to be checked and
            assigned.

        # Raises:
            ValueError: If the inverse fourier transform method provided in the parameters is not valid.
        """
        inverse_fourier_transform_method = getattr(FourierTransform, inverse_fourier_transform_method, None)
        if inverse_fourier_transform_method is not None and callable(inverse_fourier_transform_method):
            self.inverse_fourier_transform_method = inverse_fourier_transform_method
        else:
            raise ValueError("The inverse fourier transform method provided in the parameters is not valid.")

    def init_arrays(self):
        """
        Initializes arrays for space, wave vectors, and the true correlation function.
        """
        wave_vector_array = np.logspace(np.log10(self.min_frequency), np.log10(self.max_frequency), self.resolution)
        space_array = np.linspace(self.min_distance, self.max_distance, self.resolution)

        self.wave_vector_array_x, self.wave_vector_array_y = np.meshgrid(wave_vector_array, wave_vector_array)
        self.space_array_x, self.space_array_y = np.meshgrid(space_array, space_array)
        self.true_correlation_function = np.zeros((self.resolution, self.resolution))

    def compute_true_correlation_function(self):
        """
        Computes the true correlation function using the base_correlation_function method from CorrelationFunctions.py.
        """
        self.true_correlation_function = CorrelationFunctions.base_correlation_function(self.space_array_x,
                                                                                        self.space_array_y,
                                                                                        self.temperature,
                                                                                        self.capillary_frequency,
                                                                                        self.curvature_frequency,
                                                                                        self.surface_tension)

    def compute_frequency_spectrum(self):
        """
        Computes the frequency spectrum using the spectrum function provided in the parameters.
        """
        self.frequency_spectrum = self.spectrum_function(self.wave_vector_array_x, self.wave_vector_array_y,
                                                         self.temperature,
                                                         self.volumic_mass, self.surface_tension, self.area,
                                                         self.kappa)

    def assign_normalisation_factor(self):
        """
        Assigns the normalisation factor based on the Fourier Transform normalization method provided in the parameters.
        
        # Remarks:
            The normalisation factor is : sqrt(Area) / (2 * pi).\n
            This normalisation factor is only valid for 2 dimensionnal Fourier Transform.\n
            The normalisation factor can be:
            - `symmetric`: the normalization factor is considered to have been applied to the Fourier Transform and 
            so it will be applied to the inverse Fourier Transform.
            - `asymmetric_ft`: The squared normalisation factor is considered to have been applied asymmetrically
            to the Fourier Transform and so it will not be applied to the inverse Fourier Transform.
            - `asymmetric_ift`: The squared normalisation factor is considered to not have been applied to the Fourier 
            Transform and so it will be applied to the inverse Fourier Transform.
        """
        if self.ft_normalization == "symmetric":
            self.normalisation_factor = np.sqrt(self.area) / (2 * np.pi)
        elif self.ft_normalization == "asymmetric_ft":
            self.normalisation_factor = 1
        elif self.ft_normalization == "asymmetric_ift":
            self.normalisation_factor = self.area / (2 * np.pi) ** 2

    def compute_inverse_fourier_transform(self):
        """
        Computes the inverse Fourier Transform using the inverse Fourier Transform method provided in the parameters.
        """
        self.computed_correlation_function = self.normalisation_factor * self.inverse_fourier_transform_method(
            self.frequency_spectrum)

    def save_results(self):
        """
        Saves the results to CSV files in the current calculation directory.
        """
        if self.is_accuracy_test:
            with open(self.true_correlation_function_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y', 'distance', 'correlation_function'])
                for i in range(self.resolution):
                    for j in range(self.resolution):
                        writer.writerow([self.space_array_x[i, j],
                                         self.space_array_y[i, j],
                                         np.sqrt(self.space_array_x[i, j] ** 2 + self.space_array_y[i, j] ** 2),
                                         self.true_correlation_function[i, j]])

        with open(self.correlation_function_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x', 'y', 'distance', 'correlation_function'])
            for i in range(self.resolution):
                for j in range(self.resolution):
                    writer.writerow([self.space_array_x[i, j],
                                     self.space_array_y[i, j],
                                     np.sqrt(self.space_array_x[i, j] ** 2 + self.space_array_y[i, j] ** 2),
                                     self.computed_correlation_function[i, j]])

        with open(self.frequency_spectrum_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['kx', 'ky', 'norm', 'spectrum'])
            for i in range(self.resolution):
                for j in range(self.resolution):
                    writer.writerow([self.wave_vector_array_x[i, j],
                                     self.wave_vector_array_y[i, j],
                                     np.sqrt(self.wave_vector_array_x[i, j] ** 2 + self.wave_vector_array_y[i, j] ** 2),
                                     self.frequency_spectrum[i, j]])

    def execute(self):
        """
        Executes the main program flow, including computing the true correlation function, the frequency spectrum,
        the inverse Fourier Transform, and saving the results.
        
        # Remarks:
            If the `is_accuracy_test` attribute is set to True, the true correlation function will be computed and
             saved and
            comparison plots will be generated.
        """
        if self.is_accuracy_test:
            self.compute_true_correlation_function()
        self.compute_frequency_spectrum()
        self.compute_inverse_fourier_transform()
        self.save_results()

        visualizer = Visualizer(self.outputfile_path)
        if self.is_accuracy_test:
            visualizer.compare_correlation_functions()
            visualizer.plot_true_correlation_function()
        visualizer.plot_frequency_spectrum()
        visualizer.plot_computed_correlation_function()


if __name__ == "__main__":
    main = MainProgram()
    main.execute()
