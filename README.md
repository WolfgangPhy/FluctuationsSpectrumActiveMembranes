# FluctuationsSpectrumActiveMembranes

# Description

This repository contains the code used to find the correlation function corresponding to a given spectrum of fluctuations. The code is written in Python : 


# Installation

to install the code, you can clone the following repository: https://github.com/WolfgangPhy/FluctuationsSpectrumActiveMembranes.git using the following command:

```bash
git clone https://github.com/WolfgangPhy/FluctuationsSpectrumActiveMembranes.
```

You can also download the code as a zip file by clicking on the green button "Code" and then "Download ZIP".

# Documentation

The documentation is contained in the code itself using docstrings. You can use the help function in python to access it.

# How it works ?

The code is build such that all parameters are tunable from the "Parameters.json" file in the source directory. When you
run the code (see *How to run the code ?*), it will automatically create a directory for the output files and plots in
the "Calculations" directory. Eache calculation will be stored in a subdirectory named using this format :

```
SPECTRUMNAME_INVERSEFOURIERMETHODNAME
```

The calculation directory will have the following structure :

```
Directory
│
└───OutputPaths.json
|
└───Parameters.json
|
└───Datas
│   │   computed_correlation.csv
│   │   computed_parameters.json
│   │   frequency_spectrum.csv
│   │   true_correlation.csv (if is_accuracy_test = true)
└───Plots
    │   comparison_plot.png (if is_accuracy_test = true)
    │   correlation_plot.png
    │   frequency_plot.png
    |   true_correlation_plot.png (if is_accuracy_test = true)

```

# Structure of the code

This code is build using the single responsibility principle. Each class has a single responsibility and the code is organized in a way that makes it easy to understand and to modify. Each class is in its own file and the code is organized in the following way:

- `MainProgram.py` : This is the main file of the code. It get the parameters from the "Parameters.json" file and run the calculations accordingly.
- `FourierTransform.py` : This file contains the FourierTransform class that contain static methods to compute the Fourier transform with different techniques.
- `CorrelationFunctions.py` : This file contains the CorrelationFunctions class that contain static methods to compute different correlation functions. This class and its methods are only used for testing purposes.
- `Spectrums.py` : This file contains the Spectrum class that contain static methods, one for each spectrum.
- `FileHelper.py` : This file contains the FileHelper class that contain static methods to create directories and get output paths.
- `Visualizer.py` : This file contains the Visualizer class that contain static methods to plot the results of the calculations.

# How to run the code ?

To run the code you need to have the following dependencies installed :
- numpy
- pandas
- seaborn
- matplotlib

Then you can run the code by running the MainProgram.py file.

```bash
python MainProgram.py
```

If you want to really control the lauch of the code you need to create an instance of the `MainProgram` class and call
 the `execute()` method :
 
 ```python
 from MainProgram import MainProgram
 main_program = MainProgram()
 main_program.execute()
```

# Parameters

The `Parameters.json` file looks like this :

```json
{
    "temperature": 1000,
    "volumic_mass": 1000,
    "surface_tension": 72.8,
    "kappa": 4.1e-21,
    "area": 1e-6,
    "spectrum_function": "base_spectrum",
    "inverse_fourier_transform_method": "inverse_fft",
    "resolution": 100,
    "is_accuracy_test": true,
    "ft_normalization": "symmetric"
}
```

The parameters are the following :
- `temperature` : The temperature of the system in Kelvin.
- `volumic_mass` : The volumic mass of the membrane in kg/m^3.
- `surface_tension` : The surface tension of the membrane in N/m.
- `kappa` : The bending rigidity of the membrane in J.
- `area` : The area of the membrane in m^2.
- `spectrum_function` : The name of the method in the Spectrum class that will return the spectrum of fluctuations.
- `inverse_fourier_transform_method` : The name of the method in the FourierTransform class that will compute the inverse Fourier transform.
- `resolution` : The number of points in the frequency spectrum.
- `is_accuracy_test` : A boolean that indicates if the code should compute the correlation function for the true spectrum of fluctuations.
- `ft_normalization` : The normalization of the Fourier transform. Can be "symmetric", "asymmetric_ft" or "asymmetric_ift".
    - `symmetric`: the normalization factor is considered to have been applied to the Fourier Transform and 
        so it will be applied to the inverse Fourier Transform.
    - `asymmetric_ft`: The squared normalisation factor is considered to have been applied asymmetrically
        to the Fourier Transform and so it will not be applied to the inverse Fourier Transform.
    - `asymmetric_ift`: The squared normalisation factor is considered to not have been applied to the Fourier 
        Transform and so it will be applied to the inverse Fourier Transform.

# How to compute the correlation function for my spectrum ?

Fist you need to create a new statuc method in the Spectrum class that will return the spectrum of fluctuations. (If you want to change the number 
of parameters and the nature of the parameters, you will need to edit a little bit the code in the MainProgram.py file, see *Improve the code* part). Once you have created the method, you have to set the `spectrum_function` parameters to the name of the method you just created in the "Parameters.json" file. Then you can run the code by running the MainProgram.py file.

# Improve the code 

The first thing to improve this code is, of course to successfully retrieve the `base_correlation_function` from the `Spectrum` class. 
When this is done you can start to test the code for more spectrums.

But for this you will maybe need to change the number of parameters and the nature of the parameters. An improvement of the code would be to make the code more flexible by allowing the user to add more parameters to the `Parameters.json` file without having to change the code.
