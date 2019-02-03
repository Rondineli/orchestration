import os
import argparse

from modules.ssh import SshClient
from modules.utils import YamlParser, ParseCommands
from modules.exceptions import DangerException
from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ["Server", "Task", "Command", "Status", "Exception"]


__author__ = "Rondineli Gomes de Araujo"
__version__ = "1.0.0"


def check_succces(server, task, execution, stdin, stdout, stderr):
    status = "SUCCESS"

    error = str(stderr.read().decode('ascii'))

    if len(error) > 0:
        print("\33[1;31;40m ERROR>{}".format(error))
        status = "FAILED"

        table.add_row([server, task, execution, status, error])
        return

    table.add_row([server, task, execution, status, None])
    return


def setup(args):

    yaml_tasks = YamlParser(args.config)

    all_servers_connections = []

    for server in args.servers:
        if ":" in server:
            host = server.split(":")[0]
            port = server.split(":")[1]
        else:
            host = server
            port = 22

        all_servers_connections.append(
            SshClient(
                host=host,
                host_port=port,
                user=args.username,
                host_key=args.ssh_key,
                password=args.password
            )
        )

    for conn in all_servers_connections:
        commands = ParseCommands(yaml_tasks.yaml_obj)
        # Before Install
        for execution in commands.check_before_install():
            print("Executing: {}:{}".format(conn.host, execution))
            stdin, stdout, stderr = conn.exec(execution)
            check_succces(
                conn.host,
                "Before Install",
                execution,
                stdin,
                stdout,
                stderr
            )

        # Install all packages
        for execution in commands.check_install():
            print("Executing: {}:{}".format(conn.host, execution))
            stdin, stdout, stderr = conn.exec(execution)
            check_succces(
                conn.host,
                "Install",
                execution,
                stdin,
                stdout,
                stderr
            )

        # Create all dirs
        for execution in commands.check_dirs():
            print("Executing: {}:{}".format(conn.host, execution))
            stdin, stdout, stderr = conn.exec(execution)
            check_succces(
                conn.host,
                "Dirs",
                execution,
                stdin,
                stdout,
                stderr
            )

        # Set all templates
        for template in commands.check_templates():
            print(
                "copying local:{} to remote: {}".format(
                    template["file"],
                    template["destination"]
                )
            )
            sftp = conn.open_sftp()
            if template["destination"] == "/":
                raise DangerException(
                    "\33[1;31;40m ERROR> Are you sure you want this???"
                )

            sftp.put(template["file"], template["destination"])
            stdin, stdout, stderr = conn.exec(template["command"])
            check_succces(
                conn.host,
                "templates",
                template["command"],
                stdin,
                stdout,
                stderr
            )

        # After Templates - execution
        for execution in commands.check_execute():
            print("Executing: {}:{}".format(conn.host, execution))
            stdin, stdout, stderr = conn.exec(execution)
            check_succces(
                conn.host,
                "Execute",
                execution,
                stdin,
                stdout,
                stderr
            )

    print(table)


def main():
    description = 'Manage my default app'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-c',
        '--config',
        default='./config.yaml',
        type=str
    )

    parser.add_argument(
        '-u',
        '--username',
        default='ubuntu',
        type=str
    )

    parser.add_argument(
        '-s',
        '--servers',
        default=['localhost'],
        nargs='+'
    )

    parser.add_argument(
        '--ssh-key',
        help='Path ssh key to connect to the server',
        default=None,
        type=str
    )

    parser.add_argument(
        '--password',
        help='Password to connect',
        default=os.getenv("SSH_PASSWORD"),
        type=str
    )

    args, extra_params = parser.parse_known_args()
    setup(args)


if __name__ == "__main__":
    main()
