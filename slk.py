import os
import argparse

from modules.ssh import SshClient
from modules.utils import YamlParser, ParseCommands
from modules.exceptions import DangerException


__author__ = "Rondineli Gomes de Araujo"
__version__ = "1.0.0"



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
