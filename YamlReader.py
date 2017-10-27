import ruamel.yaml as yaml

class YamlReader():

    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            yaml_file = yaml.safe_load(file)

        print(yaml_file['facts']['fact1']['args'])
#
