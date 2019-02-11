import sys
import paramiko

class SshClient(object):
    def __init__(self, host, host_port, user, host_key=None, password=None, **kwargs):
        self.host = host
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.kwargs = kwargs
        self.host_port = host_port
        self.user = user
        self.host_key = host_key
        self.password = password
        self.connected = False
        self.green = "\033[0;32m"
        self.red = "\033[1;31m"
        print("\33[32m Connected to the host: {} ".format(self.host))

    @property
    def is_connected(self):
        return self.connected

    def connect(self):
        try:
            self.ssh.connect(
                host=self.host,
                username=self.user,
                port=self.host_port,
                key_filename=self.host_key,
                password=self.password,
                **self.kwargs
            )
            self.connected = True
            print("\033[0;32m Connected to the host: {}".format(self.host), end="")
        except Exception as e:
            self.connected = False
            print("\033[1;31m Error to connect to the server: { - {}}".format(self.host, str(e)), end="")
        return self.ssh

    def open_sftp(self):
        self.sftp = self.ssh.open_sftp()
        return self.sftp

    def exec(self, command=None):
        return self.ssh.exec_command(command)

    def close(self):
        self.ssh.close()

    def __str__(self):
        return "<Connection of {}>".format(self.host)
