import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

from FileHelper import FileHelper


class Visualizer:
    """
    Class that manages the visualization of the results of the calculations.
    """
    def __init__(self, calculation_paths_file_path):
        """
        Constructor of the Visualizer class.

        # Args:
            calculation_paths_file_path (str): Path to the current calculation directory.
        """
        self.max_distance = None
        self.min_distance = None
        self.max_frequency = None
        self.min_frequency = None
        self.curvature_frequency = None
        self.capillary_frequency = None
        self.resolution = None
        self.area = None
        self.kappa = None
        self.surface_tension = None
        self.volumic_mass = None
        self.temperature = None
        self.frequency_spectrum = None
        self.true_correlation_function_df = None
        self.computed_correlation_function_df = None
        self.frequency_spectrum_file = None
        self.true_correlation_function = None
        self.computed_correlation_function_file = None
        self.calculation_directory_path = calculation_paths_file_path
        self.get_files_path()
        self.load_datas()

    def get_files_path(self):
        """
        Retrieves the paths to the files containing the results of the calculations.
        """
        self.computed_correlation_function_file = FileHelper.give_output_path(self.calculation_directory_path,
                                                                              "computed_correlation")
        self.true_correlation_function = FileHelper.give_output_path(self.calculation_directory_path, "true_correlation")
        self.frequency_spectrum_file = FileHelper.give_output_path(self.calculation_directory_path, "frequency_spectrum")

    def load_datas(self):
        """
        Loads the data from the files containing the results of the calculations.
        """
        self.computed_correlation_function_df = pd.read_csv(self.computed_correlation_function_file)
        self.true_correlation_function_df = pd.read_csv(self.true_correlation_function)
        self.frequency_spectrum = pd.read_csv(self.frequency_spectrum_file)

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

    def compare_correlation_functions(self):
        """
        Plots the comparison between the computed correlation function and the true correlation function.
        """
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

    def plot_computed_correlation_function(self):
        """
        Plots the computed correlation function.
        """
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

    def plot_true_correlation_function(self):
        """
        Plots the true correlation function.
        """
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

    def plot_frequency_spectrum(self):
        """
        Plots the frequency spectrum.
        """
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