import os
import yaml

class ParameterReader:
    """
    A class to read parameters from a YAML file.
    """
    def __init__(self, filename):
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(script_dir, filename) # the name of the YAML file
        self.parameters = {} # a dictionary to store the parameters and values

    def read_file(self):
        # open the file in read mode
        with open(self.filename, "r") as f:
            # load the YAML file into the parameters dictionary
            self.parameters = yaml.safe_load(f)

    def get_parameter(self, key):
        # return the value of the parameter if it exists, otherwise None
        return self.parameters.get(key, None)
    

cls = ParameterReader("config.yaml")
cls.read_file()
print(f'database type: {cls.get_parameter("ui_default_date")}')