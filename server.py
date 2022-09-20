class Server():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def dictionary(self):
        return {
            "ip_address": self.ip_address,
            "port": self.port,
        }
