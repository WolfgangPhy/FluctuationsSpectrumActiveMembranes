import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

class Visualizer:
    
    def __init__(self, spectrum_filename):
        self.spectrum_filename = spectrum_filename
        self.load_datas()
        
    def load_datas(self):
        self.spectrum_dataframe = pd.read_csv(self.spectrum_filename)
        self.true_spectrum_dataframe = pd.read_csv("true_spectrum.csv")
        
    def compare_spectrums(self):
        sns.set_theme()
        _, ax = plt.subplots(1, 2, figsize=(15, 5))
        # set horizontal spacing between plots
        plt.subplots_adjust(wspace=0.5)
        sns.lineplot(x="space", y="spectrum", data=self.spectrum_dataframe, ax=ax[0])
        sns.lineplot(x="space", y="spectrum", data=self.true_spectrum_dataframe, ax=ax[1])
        #Invert y axis
        # Set log scales
        ax[0].set_yscale("log")
        ax[0].set_xscale("log")
        ax[1].set_yscale("log")
        ax[1].set_xscale("log")
        ax[0].set_title("Estimated spectrum")
        ax[1].set_title("True spectrum")
        ax[0].set_xlabel("Distance (nm)")
        ax[1].set_xlabel("Distance (nm)")
        ax[0].set_ylabel("Spectrum")
        ax[1].set_ylabel("Spectrum")
        plt.savefig("Spectrums_comparison.png")
        
    def true_space_spectrum(self):
        sns.set_theme()
        plt.figure(figsize=(10, 5))
        sns.lineplot(x="space", y="spectrum", data=self.true_spectrum_dataframe)
        plt.title("True spectrum")
        plt.xlabel("Distance (nm)")
        plt.ylabel("Spectrum")
        plt.savefig("True_spectrum.png")