import paramiko


class SshClient(object):
    def __init__(self, host, host_port, user, host_key=None, password=None):
        self.host = host
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if host_key and not password:
            self.ssh.connect(
                host,
                username=user,
                port=host_port,
                key_filename=host_key
            )

        if not host_key and password:
            self.ssh.connect(
                host,
                port=host_port,
                username=user,
                password=password
            )

        if host_key and password:
            self.ssh.connect(
                host,
                port=host_port,
                username=user,
                password=password,
                key_filename=host_key
            )

        print("\033[1;32;40m Connected to host: {}  \n".format(self.host))

    def get_connection(self):
        return self.ssh

    def open_sftp(self):
        self.sftp = self.ssh.open_sftp()
        return self.sftp

    def exec(self, command=None):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdin, stdout, stderr

    def close(self):
        self.ssh.close()

    def __str__(self):
        return "<Connection of {}>".format(self.host)
