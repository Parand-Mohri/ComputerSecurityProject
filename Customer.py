class Customer():
    def __init__(self, customer_id,password, server, actions, salt):
        self.customer_id = customer_id
        self.password = password
        self.server = server
        self.actions = actions
        self.salt = salt
        self.value = 0

    def dictionary(self):
        return {
            "customer_id": self.customer_id,
            "password": self.password,
            "server": self.server,
            "actions": self.actions,
            "value": self.value
        }