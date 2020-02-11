class SSHAuthenticationException(Exception):
    """SSH authentication exception occured"""


class SSHConnectException(Exception):
    """SSH connection exception occured"""


class SSHExecCommandException(Exception):
    """SSH run command exception occured"""


class SftpUploadFileException(Exception):
    """upload exception occured via sftp"""


class SftpDownloadFileException(Exception):
    """download exception occured via sftp"""


class WebShellExecTimeoutException(Exception):
    """timeout when execute command via webshell"""


class BehinderWebshellKeyExchangeException(Exception):
    """exception occured while exchanging behinder key"""


class DatabaseExecError(Exception):
    """exception occured while database query"""


class DatabaseNotSupported(Exception):
    """database type is not supported"""


class WebShellUploadError(Exception):
    """upload file error"""
