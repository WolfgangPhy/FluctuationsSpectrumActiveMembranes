import json
import shutil
from pathlib import Path


class FileHelper:
    """
    Helper class for file operations.
    """

    @staticmethod
    def init_calculation_directory() -> str:
        """
        Initializes the calculation directory and returns the path to the output path file.

        Raises:
            FileExistsError: When the calculation directory already exists and the user does not want to overwrite it.

        Returns:
            str: The path to the file that contain all the output paths for the current calculation.
        """
        with open("Parameters.json") as file:
            parameters: dict = json.load(file)

        directory_name: str = f"{parameters['spectrum_function']}_{parameters['inverse_fourier_transform_method']}"

        calculation_directory: Path = Path("..") / Path("Calculations") / directory_name

        if not calculation_directory.exists():
            calculation_directory.mkdir(parents=True)
        elif input("Calculations with this spectrum was already done, do you want to redo these calculations " +
                   "(this will overwrite previous calculations) ? (y/n): ") == "y":
            return str(calculation_directory / "OutputPaths.json")
        else:
            raise FileExistsError("You chose to not overwrite the previous calculations.")

        plot_directory: Path = calculation_directory / "Plots"
        datas_directory: Path = calculation_directory / "Datas"

        plot_directory.mkdir()
        datas_directory.mkdir()

        shutil.copy("Parameters.json", calculation_directory)
        shutil.copy("OutputPaths.json", calculation_directory)

        with open(calculation_directory / "OutputPaths.json", 'r') as file:
            paths: dict = json.load(file)

        paths["parameters"] = str(calculation_directory / Path(paths['parameters']))
        paths["computed_parameters"] = str(calculation_directory / Path(paths['computed_parameters']))
        paths["computed_correlation"] = str(calculation_directory / Path(paths['computed_correlation']))
        paths["true_correlation"] = str(calculation_directory / Path(paths['true_correlation']))
        paths["frequency_spectrum"] = str(calculation_directory / Path(paths['frequency_spectrum']))
        paths["frequency_plot"] = str(calculation_directory / Path(paths['frequency_plot']))
        paths["correlation_plot"] = str(calculation_directory / Path(paths['correlation_plot']))
        paths["comparison_plot"] = str(calculation_directory / Path(paths['comparison_plot']))
        paths["true_correlation_plot"] = str(calculation_directory / Path(paths['true_correlation_plot']))

        with open(calculation_directory / "OutputPaths.json", 'w') as new_output_file:
            json.dump(paths, new_output_file, indent=4)

        return str(calculation_directory / "OutputPaths.json")

    @staticmethod
    def give_output_path(output_file_path: str, key: str) -> str:
        """
        Retrieves a specific path from the given configuration file.

        # Args:
        - `config_file_path (str)`: Path to the configuration file.
        - `key (str)`: Key for the desired value in the configuration file.

        # Returns:
        - `str`: The value associated with the specified key in the configuration file.
        """
        with open(output_file_path) as config_file:
            config: dict = json.load(config_file)

        value: str = config[key]

        config_file.close()
        return value
