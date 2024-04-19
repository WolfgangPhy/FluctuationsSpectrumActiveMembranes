import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.constants as const
import json

class Visualizer:
    
    def __init__(self, spectrum_filename):
        self.spectrum_filename = spectrum_filename
        self.load_datas()
        
    def load_datas(self):
        self.spectrum_dataframe = pd.read_csv(self.spectrum_filename)
        self.true_spectrum_dataframe = pd.read_csv("true_spectrum.csv")
        self.frequency_spectrum = pd.read_csv("frequency_spectrum.csv")
        
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
        
    def compare_spectrums(self):
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="space", y="spectrum", data=self.true_spectrum_dataframe, color="green", ax=ax,
                    label="True correlation function")
        sns.lineplot(x="space", y="spectrum", data=self.spectrum_dataframe, color="purple", ax=ax,
                       label="Approximated spectrum")
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1/self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1/self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        #ax.set_ylim(-1e-25, 1e-21)
        #ax.set_yscale("symlog", linthresh=1e-25)
        ax.set_xscale("log")
        ax.set_xlabel("Distance (nm)")
        ax.set_ylabel("Correlation function")
        plt.savefig("Spectrums_comparison.png")
        
    def true_space_spectrum(self):
        sns.set_theme()
        _, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="space", y="spectrum", data=self.true_spectrum_dataframe, color="green", ax=ax,
                    label="True correlation function")
        ax.axhline(0, color='grey', linestyle='--')
        ax.axvline(1/self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(1/self.curvature_frequency, color='grey', linestyle='--')
        ax.legend()
        ax.set_yscale("symlog")
        ax.set_xscale("log")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("$<\zeta(0)\zeta(r_\parallel)> (m^2)$")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e')) 
        plt.savefig("True_correration_function.png")
        
    def plot_frequency_spectrum(self):
        sns.set_theme()
        _, ax = plt.subplots()
        sns.lineplot(x="frequency", y="spectrum", data=self.frequency_spectrum, color="purple", ax=ax,
                     label="Frequency spectrum")
        ax.axvline(self.capillary_frequency, color='grey', linestyle='--')
        ax.axvline(self.curvature_frequency, color='grey', linestyle='--')
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Spectrum")
        plt.savefig("Frequency_spectrum.png")