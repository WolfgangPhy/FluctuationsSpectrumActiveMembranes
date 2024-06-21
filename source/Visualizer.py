import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

from FileHelper import FileHelper


class Visualizer:
    """
    Class that manages the visualization of the results of the calculations.
    
    # Attributes:
        `max_distance (float)`: The maximum distance.
        `min_distance (float)`: The minimum distance.
        `max_frequency (float)`: The maximum frequency.
        `min_frequency (float)`: The minimum frequency.
        `curvature_frequency (float)`: The curvature frequency.
        `capillary_frequency (float)`: The capillary frequency.
        `resolution (int)`: The resolution.
        `area (float)`: The area.
        `kappa (float)`: The bending rigidity modulus.
        `surface_tension (float)`: The surface tension.
        `volumic_mass (float)`: The volumic mass.
        `temperature (float)`: The temperature.
        `frequency_spectrum (float)`: The frequency spectrum.
        `true_correlation_function_df (pandas.DataFrame)`: The true correlation function.
        `computed_correlation_function_df (pandas.DataFrame)`: The computed correlation function.
        `frequency_spectrum_filepath (str)`: The path to the frequency spectrum file.
        `true_correlation_function_filepath (str)`: The path to the true correlation function file.
        `computed_correlation_function_filepath (str)`: The path to the computed correlation function file.
        `calculation_directory_path (str)`: The path to the current calculation directory.
        
    # Methods:
        `get_files_path()`: Retrieves the paths to the files containing the results of the calculations.
        `load_datas()`: Loads the data from the files containing the results of the calculations.
        `compare_correlation_functions()`: Plots the comparison between the computed correlation function and the true correlation function.
        `plot_computed_correlation_function()`: Plots the computed correlation function.
        `plot_true_correlation_function()`: Plots the true correlation function.
        `plot_frequency_spectrum()`: Plots the frequency spectrum.
    """
    def __init__(self, calculation_paths_file_path : str) -> None:
        """
        Constructor of the Visualizer class.

        # Args:
            calculation_paths_file_path (str): Path to the current calculation directory.
        # Returns:
            None
        """
        self.max_distance : float = None
        self.min_distance : float = None
        self.max_frequency : float = None
        self.min_frequency : float = None
        self.curvature_frequency : float = None
        self.capillary_frequency : float = None
        self.resolution : int = None
        self.area : float = None
        self.kappa : float = None
        self.surface_tension : float = None
        self.volumic_mass : float = None
        self.temperature : float = None
        self.frequency_spectrum : float = None
        self.true_correlation_function_df : pd.DataFrame = None
        self.computed_correlation_function_df : pd.DataFrame = None
        self.frequency_spectrum_filepath : str = None
        self.true_correlation_function_filepath : str = None
        self.computed_correlation_function_filepath : str = None
        self.calculation_directory_path : str = calculation_paths_file_path
        self.get_files_path()
        self.load_datas()

    def get_files_path(self) -> None:
        """
        Retrieves the paths to the files containing the results of the calculations.
        
        # Returns:
            None
        """
        self.computed_correlation_function_filepath = FileHelper.give_output_path(self.calculation_directory_path,
                                                                              "computed_correlation")
        self.true_correlation_function_filepath = FileHelper.give_output_path(self.calculation_directory_path, "true_correlation")
        self.frequency_spectrum_filepath = FileHelper.give_output_path(self.calculation_directory_path, "frequency_spectrum")

    def load_datas(self) -> None:
        """
        Loads the data from the files containing the results of the calculations.
        
        # Returns:
            None
        """
        self.computed_correlation_function_df = pd.read_csv(self.computed_correlation_function_filepath)
        self.true_correlation_function_df = pd.read_csv(self.true_correlation_function_filepath)
        self.frequency_spectrum = pd.read_csv(self.frequency_spectrum_filepath)

        with open(FileHelper.give_output_path(self.calculation_directory_path,"parameters")) as file:
            parameters = json.load(file)
        self.temperature = parameters["temperature"]
        self.volumic_mass = parameters["volumic_mass"]
        self.surface_tension = parameters["surface_tension"]
        self.kappa = parameters["kappa"]
        self.area = parameters["area"]
        self.resolution = parameters["resolution"]

        with open(FileHelper.give_output_path(self.calculation_directory_path, "computed_parameters")) as file:
            computed_parameters = json.load(file)
        self.capillary_frequency = computed_parameters["capillary_frequency"]
        self.curvature_frequency = computed_parameters["curvature_frequency"]
        self.min_frequency = computed_parameters["min_frequency"]
        self.max_frequency = computed_parameters["max_frequency"]
        self.min_distance = computed_parameters["min_distance"]
        self.max_distance = computed_parameters["max_distance"]

    def compare_correlation_functions(self) -> None:
        """
        Plots the comparison between the computed correlation function and the true correlation function.
        
        # Returns:
            None
        """
        ax : plt.Axes = None
        
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="distance", y="correlation_function", data=self.true_correlation_function_df, color="green",
                     ax=ax, label="True correlation function", errorbar=None)
        sns.lineplot(x="distance", y="correlation_function", data=self.computed_correlation_function_df, color="purple",
                     ax=ax, label="Computed correlation function", errorbar=None)
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1 / self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1 / self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        # ax.set_ylim(-1e-25, 1e-21)
        # ax.set_yscale("symlog", linthresh=1e-25)
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.set_title("Computed Correlation Function vs. True Correlation Function 2D")
        plt.savefig(FileHelper.give_output_path(self.calculation_directory_path, "comparison_plot"))

    def plot_computed_correlation_function(self) -> None:
        """
        Plots the computed correlation function.
        
        # Returns:
            None
        """
        ax : plt.Axes = None
        
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="distance", y="correlation_function", data=self.computed_correlation_function_df, color="purple",
                     ax=ax, label="Computed correlation function", errorbar=None)
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1 / self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1 / self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.set_title("Computed Correlation Function vs. Distance 2D")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e'))
        plt.savefig(FileHelper.give_output_path(self.calculation_directory_path, "correlation_plot"))

    def plot_true_correlation_function(self) -> None:
        """
        Plots the true correlation function.
        
        # Returns:
            None
        """
        ax : plt.Axes = None
        
        sns.set_theme()
        _, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="distance", y="correlation_function", data=self.true_correlation_function_df, color="green",
                     ax=ax,
                     label="True correlation function", errorbar=None)
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1 / self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1 / self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        ax.set_yscale("symlog")
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.set_title("True Correlation Function vs. Distance 2D")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e'))
        plt.savefig(FileHelper.give_output_path(self.calculation_directory_path, "true_correlation_plot"))

    def plot_frequency_spectrum(self) -> None:
        """
        Plots the frequency spectrum.
        
        # Returns:
            None
        """
        ax : plt.Axes = None
        
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="norm", y="spectrum", data=self.frequency_spectrum, color="purple", ax=ax,
                     label="Frequency spectrum", errorbar=None)
        ax.axvline(self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(self.curvature_frequency, color='grey', linestyle='--')
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Spectrum")
        ax.set_title("Frequency Spectrum vs. Frequency 2D")
        plt.savefig(FileHelper.give_output_path(self.calculation_directory_path, "frequency_plot"))
