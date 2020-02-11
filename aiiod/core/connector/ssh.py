import paramiko

import aiiod.core.exceptions as exceptions
from aiiod.core.connector.shell import Shell


class SSHConnector(Shell):
    def __init__(self, ip, user, pwd=None, key_path=None, port=22):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if pwd is not None:
                self._client.connect(ip, port, user, pwd, timeout=self.TIMEOUT)
            else:
                key = paramiko.RSAKey.from_private_key_file(key_path)
                self._client.load_system_host_keys()
                self._client.connect(
                    ip, port, user, pkey=key, timeout=self.TIMEOUT)

            channel = self._client.invoke_shell()
            super().__init__(channel)

        except paramiko.ssh_exception.AuthenticationException:
            raise exceptions.SSHAuthenticationException
        except paramiko.ssh_exception.SSHException:
            raise exceptions.SSHConnectException

    def exec(self, cmd) -> str:
        try:
            _, stdout, stderr = self._client.exec_command(cmd)
            status = stdout.channel.recv_exit_status()

            output = None
            if status == 0:
                output = stdout.read()
            else:
                output = stderr.read()

            output = output.decode(errors='ignore')
            return output

        except Exception:
            raise exceptions.SSHExecCommandException

    def _set_timeout(self, timeout):
        self._channel.settimeout(timeout)

    def upload_file(self, src_path, dst_path):
        if not hasattr(self, '_sftp'):
            self._sftp = self._client.open_sftp()

        try:
            self._sftp.put(src_path, dst_path)
        except IOError:
            raise exceptions.SftpUploadFileException

    def download_file(self, dst_path, src_path):
        if not hasattr(self, '_sftp'):
            self._sftp = self._client.open_sftp()

        try:
            self._sftp.get(dst_path, src_path)
        except IOError:
            raise exceptions.SftpDownloadFileException

    def __del__(self):
        try:
            self._client.close()
            self._channel.close()
            if hasattr(self, '_sftp'):
                self._sftp.close()
        except Exception:
            pass