from modules.utils.templates import Templates


class ParseCommands(object):
    def __init__(self, obj):
        self.yaml_obj = obj
        self.template = Templates()

    def get_before(self, metadata):
        if metadata.get("before"):
            before = metadata.get("before").split(":")
            commands = self.yaml_obj["jobs"][before[0]]

            for command in commands:
                if command.get("name") == before[1]:
                    exec_command = command["metadata"]["shell"]

                    if metadata["sudo"]:
                        exec_ecommand = "sudo {}".format(exec_command)
                        return exec_ecommand
                    return exec_ecommand

        return None

    def get_notify(self, metadata):
        if metadata.get("notify"):
            notify = metadata.get("notify").split(":")
            commands = self.yaml_obj["jobs"][notify[0]]

            for command in commands:
                if command.get("name") == notify[1]:
                    exec_command = command["metadata"]["shell"]

                    if metadata["sudo"]:
                        exec_ecommand = "sudo {}".format(exec_command)
                        return exec_ecommand
                    return exec_ecommand

        return None

    def mount_commands_metadata(self, metadata, principal_command=None,
                                notify_execute=None, before=None):

        if not principal_command:
            principal_command = "echo 'Done!'"

        if before:
            principal_command = "{} && {}".format(before, principal_command)

        env_vars = self.check_env_vars()

        owner_command = "echo 'owner'"
        chmod_command = "echo 'chmod'"

        if metadata.get("owner"):
            owner_command = "chown -R {}: {}".format(
                metadata["owner"],
                metadata["destination"]
            )

        if metadata.get("chmod"):
            chmod_command = "chmod {} {}".format(
                metadata["chmod"],
                metadata["destination"]
            )

        if metadata.get("sudo"):
            command = "sudo {} {} && sudo {} && sudo {}".format(
                env_vars,
                principal_command,
                owner_command,
                chmod_command
            )

        else:
            command = "{} {} && sudo {} && sudo {}".format(
                env_vars,
                principal_command,
                owner_command,
                chmod_command
            )

        if notify_execute:
            command = "{} && {}".format(command, notify_execute)

        return command

    def check_templates(self):

        filenames = []

        for templates in self.yaml_obj["jobs"]["templates"]:
            metadata = templates.get("metadata", {"metadata": {}})

            metadata["destination"] = templates["destination"]

            before_execute = self.get_before(metadata)
            notify_execute = self.get_notify(metadata)

            commands = self.mount_commands_metadata(
                metadata,
                notify_execute=notify_execute,
                before=before_execute
            )

            if type(metadata["content"]) == str:
                self.content = metadata["content"]
                filenames.append({
                    "file": self.template.template_by_content(
                        metadata["content"]
                    ),
                    "destination": metadata["destination"],
                    "command": commands
                })

            if type(metadata["content"]) == dict:
                if metadata["content"].get("template"):
                    filenames.append({
                        "file": self.template.template_by_file(
                            metadata["content"]["template"]
                        ),
                        "destination": metadata["destination"],
                        "command": commands
                    })

                if metadata["content"].get("vars"):
                    self.template.template_dir = metadata["content"]["template"] # noqa
                    filenames.append({
                        "file": self.template.template_by_var(
                            **metadata["content"]["vars"]
                        ),
                        "destination": metadata["destination"],
                        "command": commands
                    })

        return filenames

    def check_before_install(self):
        commands_extra = []
        env_vars = self.check_env_vars()

        for command in self.yaml_obj["jobs"]["before_install"]:
            metadata = command.get("metadata", {"metadata": {}})
            before_execute = self.get_before(metadata)
            notify_execute = self.get_notify(metadata)

            to_execute = command["shell"]
            if metadata.get("sudo"):
                to_execute = "sudo {} {}".format(
                    env_vars,
                    to_execute,
                    before_execute=before_execute
                )

            if notify_execute:
                to_execute = "{} && {}".format(
                    to_execute,
                    notify_execute,
                    before_execute=before_execute
                )

            commands_extra.append(to_execute)
        return commands_extra

    def check_execute(self):
        commands_to_execute = []
        for command in self.yaml_obj["jobs"]["execute"]:
            metadata = command.get("metadata", {"metadata": {}})
            before_execute = self.get_before(metadata)
            notify_execute = self.get_notify(metadata)

            to_execute = command["metadata"]["shell"]
            if metadata.get("sudo"):
                to_execute = "sudo {}".format(to_execute)

            if notify_execute:
                to_execute = "{} && {}".format(to_execute, notify_execute)

            if before_execute:
                to_execute = "{} && {}".format(before_execute, to_execute)

            commands_to_execute.append(to_execute)

        return commands_to_execute

    def check_install(self):
        commands_to_install = []
        packages = []
        env_vars = self.check_env_vars()
        for package in self.yaml_obj["jobs"]["install"]:
            to_install = "apt-get install {} -yq".format(package["package"])
            packages.append(package["package"])
            metadata = package.get("metadata", {"metadata": {}})
            before_execute = self.get_before(metadata)
            notify_execute = self.get_notify(metadata)

            if metadata.get("sudo"):
                to_install = "sudo {} {}".format(env_vars, to_install)

            if notify_execute:
                to_install = "{} && {}".format(to_install, notify_execute)

            if before_execute:
                to_install = "{} && {}".format(before_execute, to_install)

            commands_to_install.append(to_install)

        return commands_to_install

    def check_dirs(self):
        commands_create_dir = []
        for directory in self.yaml_obj["jobs"]["dirs"]:
            metadata = directory.get("metadata", {"metadata": {}})
            before_execute = self.get_before(metadata)
            notify_execute = self.get_notify(metadata)
            metadata["destination"] = directory["destination"]
            create_command = "mkdir -p {}".format(directory["destination"])
            to_execute = self.mount_commands_metadata(
                metadata,
                create_command,
                notify_execute,
                before=before_execute
            )
            commands_create_dir.append(to_execute)

        return commands_create_dir

    def check_env_vars(self):
        return " ".join(self.yaml_obj["jobs"]["env_vars"])
