import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from FileHelper import FileHelper
import pandas as pd
import seaborn as sns
import json

class Visualizer:
    
    def __init__(self, outputfile_path):
        self.outputfile_path = outputfile_path
        self.get_files_path()
        self.load_datas()
        
    def get_files_path(self): 
        self.computed_corralation_function_file = FileHelper.give_output_path(self.outputfile_path, "computed_correlation")
        self.true_correlation_function = FileHelper.give_output_path(self.outputfile_path, "true_correlation")
        self.frequency_spectrum_file = FileHelper.give_output_path(self.outputfile_path, "frequency_spectrum")
        
    def load_datas(self):
        self.computed_correlation_function_df = pd.read_csv(self.computed_corralation_function_file)
        self.true_correlation_function_df = pd.read_csv(self.true_correlation_function)
        self.frequency_spectrum = pd.read_csv(self.frequency_spectrum_file)
        
        with open("Parameters.json") as file:
            parameters = json.load(file)
        self.temperature = parameters["temperature"]
        self.volumic_mass = parameters["volumic_mass"]
        self.surface_tension = parameters["surface_tension"]
        self.kappa = parameters["kappa"]
        self.area = parameters["area"]
        self.resolution = parameters["resolution"]
        
        with open("ComputedParameters.json") as file:
            computed_parameters = json.load(file)
        self.capillary_frequency = computed_parameters["capillary_frequency"]
        self.curvature_frequency = computed_parameters["curvature_frequency"]
        self.min_frequency = computed_parameters["min_frequency"]
        self.max_frequency = computed_parameters["max_frequency"]
        self.min_distance = computed_parameters["min_distance"]
        self.max_distance = computed_parameters["max_distance"]
        
    def compare_correlation_functions(self):
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="distance", y="correlation_function", data=self.true_correlation_function_df, color="green",
                    ax=ax, label="True correlation function", errorbar=None)
        sns.lineplot(x="distance", y="correlation_function", data=self.computed_correlation_function_df, color="purple",
                     ax=ax, label="Computed correlation function", errorbar=None)
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1/self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1/self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        #ax.set_ylim(-1e-25, 1e-21)
        #ax.set_yscale("symlog", linthresh=1e-25)
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.set_title("Computed Correlation Function vs. True Correlation Function 2D")
        plt.savefig(FileHelper.give_output_path(self.outputfile_path, "comparison_plot"))
        
    def plot_computed_correlation_function(self):
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="distance", y="correlation_function", data=self.computed_correlation_function_df, color="purple",
                     ax=ax, label="Computed correlation function", errorbar=None)
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1/self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1/self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.set_title("Computed Correlation Function vs. Distance 2D")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e'))
        plt.savefig(FileHelper.give_output_path(self.outputfile_path, "correlation_plot"))
        
    def plot_true_correlation_function(self):
        sns.set_theme()
        _, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="distance", y="correlation_function", data=self.true_correlation_function_df, color="green", ax=ax,
                    label="True correlation function", errorbar=None)
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1/self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1/self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        ax.set_yscale("symlog")
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.set_title("True Correlation Function vs. Distance 2D")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e')) 
        plt.savefig(FileHelper.give_output_path(self.outputfile_path, "true_correlation_plot"))
        
    def plot_frequency_spectrum(self):
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
        plt.savefig(FileHelper.give_output_path(self.outputfile_path, "frequency_plot"))
        