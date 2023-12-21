import os
import yaml

class ParameterReader:
    """
    A class to read parameters from a YAML file.

    Parameters:
        filename (str): The name of the YAML file to read; typically "config.yaml"
    """
    def __init__(self, filename):
        """
        Initializes a new instance of the ParameterReader class.

        Parameters:
            filename (str): The name of the YAML file from which to read parameters.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(script_dir, filename) # the name of the YAML file
        self.parameters = {} # a dictionary to store the parameters and values

    def read_file(self):
        """
        Reads parameters from the YAML file specified in the filename attribute.

        Raises:
            RuntimeError: If the file cannot be read.
        """
        try: 
            # open the file in read mode
            with open(self.filename, "r") as f:
                # load the YAML file into the parameters dictionary
                self.parameters = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f'Failed to read configuration file: {self.filename}. Error: {str(e)}')

    def get_parameter(self, key):
        """
        Returns the value of the specified parameter.

        Parameters:
            key (str): The name of the parameter.

        Returns:
            The value of the parameter, or None if the parameter is not found.
        """
        return self.parameters.get(key, None)