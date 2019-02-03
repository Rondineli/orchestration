import yaml

from modules.exceptions import MissConfigurationError


class YamlParser(object):
    def __init__(self, yaml_path):
        self.yaml_file = yaml_path
        with open(self.yaml_file, 'r') as stream:
            self.yaml_obj = yaml.load(stream)

        self.check_keys_config()

    def check_keys_config(self):
        if not self.yaml_obj.get("jobs"):
            raise MissConfigurationError(
                "\33[1;31;40m Check your yaml file, key 'jobs' is necessary"
            )
