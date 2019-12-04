import selectors
import sys
import socket
import _thread

import core.globals as g


class Shell(object):
    BUFSIZE = 1 << 10
    TIMEOUT = 10

    def __init__(self, channel):
        self._channel = channel
        self._selector = selectors.DefaultSelector()
        self._done = False

    def _set_timeout(self, timeout):
        """subclasses should inplement `_set_timeout` method"""

    def _posix_on_read(self):
        try:
            data = self._channel.recv(self.BUFSIZE)
            if not data:
                sys.stdout.flush()
                self._done = True

            sys.stdout.write(data.decode(errors='ignore'))
            sys.stdout.flush()

        except socket.timeout:
            self._done = True

    def _posix_on_write(self):
        try:
            line = sys.stdin.readline()
            if not line:
                self._done = True

            if not isinstance(line, bytes):
                line = line.encode()

            self._channel.send(line)

        except (EOFError, OSError):
            self._done = True

    def _posix_interactive(self):
        try:
            self._channel.settimeout(0.0)
            self._selector.register(
                self._channel,
                selectors.EVENT_READ, lambda: self._posix_on_read())
            self._selector.register(
                sys.stdin,
                selectors.EVENT_READ, lambda: self._posix_on_write())

            while True:
                if self._done:
                    break

                events = self._selector.select()
                for key, _ in events:
                    callback = key.data
                    callback()
        finally:
            self._selector.unregister(self._channel)
            self._selector.unregister(sys.stdin)
            self._set_timeout(self.TIMEOUT)

    def _windows_on_read(self):
        while True:
            if self._done:
                break
            try:
                buf = self._channel.recv(self.BUFSIZE)
                if not buf:
                    sys.stdout.flush()
                    self._done = True
                    break

                sys.stdout.write(buf.decode(errors='ignore'))
                sys.stdout.flush()

            except (EOFError, OSError):
                pass

    def _windows_on_write(self):
        while True:
            if self._done:
                break
            try:
                line = sys.stdin.readline()
                if not line:
                    self._done = True
                    break

                if not isinstance(line, bytes):
                    line = line.encode()

                self._channel.send(line)

            except (EOFError, OSError):
                self._done = True
                break

    def _windows_interactive(self):
        _thread.start_new_thread(self._windows_on_read, ())
        self._windows_on_write()

    def interactive(self):
        self._done = False
        if g.OS == 'Windows':
            self._windows_interactive()
        else:
            self._posix_interactive()