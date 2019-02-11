import yaml
import os
import uuid
import jinja2

from modules.utils.templates import Templates
from modules.ssh import SshClient
from modules.exceptions import MissConfigurationError


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class ParseTemplates(object):
    def __init__(self, template):
       self.template = template
       with open(self.template, 'r') as stream:
            self.yaml = yaml.load(stream)
       
       if not self.yaml.get("jobs"):
          raise MissConfigurationError(
                "\33[1;31;40m Check your yaml file, key 'jobs' is necessary"
            )

    def get_yaml(self):
        return self.yaml

    def render(self, path, filename, context=None):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path)
        ).get_template(filename).render(context)


class ParseCommands(ParseTemplates):
    def __init__(self, template):
        super(ParseCommands, self).__init__(template)

    def get_notify(self, **notify_list):
        """
        list of notifys
        """
        pass

    def execute_notify(self, **notifys):
        """
        execute notify
        """
        pass

    def dirs_executions(self, **dirs):
        for dir_metadata in dirs:
            if dir_location.get("notify"):
                #self.check_errors(
                #    self.execute_notify(
                #        dir_location.get("notify")
                #    )
                #)
                print("notifying: {}".format(dir_location.get("notify")))
            
            output = self.render(
                path="{}/../templates/".format(BASE_DIR),
                filename="dir.jinja2",
                context=dir_metadata
            )
            


            
