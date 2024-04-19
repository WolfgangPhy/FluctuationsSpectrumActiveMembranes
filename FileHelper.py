import json
import os
import shutil


class FileHelper:
    
    @staticmethod
    def init_calculation_directory():
        with open("Parameters.json") as file:
            parameters = json.load(file)
        
        directory_name = f"{parameters['spectrum_function']}_{parameters['inverse_fourier_transform_method']}"
        
        calculation_directory = os.path.join("Calculations", directory_name)
        
        if not os.path.exists(calculation_directory):
            os.makedirs(calculation_directory)
        elif input("Calculations with this spectrum was already done, do you want to redo these calculations "+
                   "(this will overwrite previous calculations) ? (y/n): ") == "y":
            return os.path.join(calculation_directory, "OutputPaths.json")
        else:
            raise FileExistsError("You chose to not overwrite the previous calculations.")
        
        plot_directory = os.path.join(calculation_directory, "Plots")
        datas_directory = os.path.join(calculation_directory, "Datas")
        
        os.makedirs(plot_directory)
        os.makedirs(datas_directory)
        
        shutil.copy("Parameters.json", calculation_directory)
        shutil.copy("OutputPaths.json", calculation_directory)
        
        with open(os.path.join(calculation_directory, 'OutputPaths.json'), 'r') as file:
            paths = json.load(file)
            
        paths["computed_parameters"] = os.path.join('./', calculation_directory, paths['computed_parameters'][2:])
        paths["computed_correlation"] = os.path.join('./', calculation_directory, paths['computed_correlation'][2:])
        paths["true_correlation"] = os.path.join('./', calculation_directory, paths['true_correlation'][2:])
        paths["frequency_spectrum"] = os.path.join('./', calculation_directory, paths['frequency_spectrum'][2:])
        paths["frequency_plot"] = os.path.join('./', calculation_directory, paths['frequency_plot'][2:])
        paths["correlation_plot"] = os.path.join('./', calculation_directory, paths['correlation_plot'][2:])
        paths["comparison_plot"] = os.path.join('./', calculation_directory, paths['comparison_plot'][2:])
        paths["true_correlation_plot"] = os.path.join('./', calculation_directory, paths['true_correlation_plot'][2:])
        
        with open(os.path.join(calculation_directory, 'OutputPaths.json'), 'w') as new_output_file:
                json.dump(paths, new_output_file, indent=4)
                
        return os.path.join(calculation_directory, 'OutputPaths.json')
    
    
    @staticmethod
    def give_output_path(output_file_path, key):
        """
        Retrieves a specific value from a given configuration file.

        # Args:
        - `config_file_path (str)`: Path to the configuration file.
        - `key (str)`: Key for the desired value in the configuration file.

        # Returns:
        - `Any`: The value associated with the specified key in the configuration file.
        """
        with open(output_file_path) as config_file:
            config = json.load(config_file)
        
        value = config[key]
        
        config_file.close()
        return value
        