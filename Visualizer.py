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
        _, ax = plt.subplots(1, 2)
        sns.lineplot(x="space", y="spectrum", data=self.spectrum_dataframe, ax=ax[0])
        sns.lineplot(x="space", y="spectrum", data=self.true_spectrum_dataframe, ax=ax[1])
        ax[0].set_title("Estimated spectrum")
        ax[1].set_title("True spectrum")
        plt.savefig("Spectrums_comparison.png")