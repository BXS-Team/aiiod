class Target(object):
    def __init__(self, ips=None):
        self.ips = ips or []
        if not isinstance(ips, list):
            self.ips = []

    def __sub__(self, ip):
        if isinstance(ip, str):
            self.ips.remove(ip)
        elif isinstance(ip, list):
            [self.ips.remove(i) for i in ip]
        return self

    def __add__(self, ip):
        if isinstance(ip, str):
            self.ips.append(ip)
        elif isinstance(ip, list):
            self.ips += ip
        return self
