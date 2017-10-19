from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class YamlReader():

    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            yaml_file = load(file)

        print(yaml_file['facts']['fact1']['args'])

