import os
import jinja2
import uuid

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Templates(object):
    def __init__(self, template=None, content=None):
        self.template_dir = template
        self.content = content

    def template_by_file(self, file_dir):
        return "{}/../templates/{}".format(BASE_PATH, file_dir)

    def template_by_content(self, content):
        filename = "/tmp/template_by_content_{}".format(str(uuid.uuid4()))
        file = open(filename, "w")
        file.write(content)
        file.close()
        return filename

    def template_by_var(self, **env_vars):
        output = self.render(
            path="{}/../templates/".format(BASE_PATH),
            filename=self.template_dir,
            context=env_vars
        )
        filename = "/tmp/template_by_content_{}".format(str(uuid.uuid4()))
        file = open(filename, "w")
        file.write(output)
        file.close()
        return filename

    def render(self, path, filename, context=None):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path)
        ).get_template(filename).render(context)
