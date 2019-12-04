import socket

from core.connector.shell import Shell
from core.connector.webshell import _random_str


class BindShellConnector(Shell):
    """
    This payload could only used on Linux
    """

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port if isinstance(port, int) else int(port)

        self._conn = socket.create_connection((self._ip, self._port),
                                              timeout=self.TIMEOUT)

        super().__init__(self._conn)

    def exec(self, cmd) -> str:
        if not isinstance(cmd, bytes):
            cmd = cmd.encode()
        token = _random_str()
        self._conn.sendall(cmd + b'; echo ' + token.encode() + b'\n')
        output = self._recv_until(token)
        return output.decode(errors='ignore')

    def _recv_until(self, token) -> bytes:
        if not isinstance(token, bytes):
            token = token.encode()

        buffer = []
        while True:
            try:
                buffer.append(self._conn.recv(1))
                if len(buffer) >= len(token) and b''.join(
                        buffer[-len(token):]) == token:
                    break
            except Exception:
                break
        return b''.join(buffer[:-len(token)])
