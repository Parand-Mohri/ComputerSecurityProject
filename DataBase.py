
# gonna be used as data base
class DataBase:
    def __init__(self):
        self.customers = []
        # self.actions = []

    def get_customers(self):
        return self.customers

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self, customer):
        self.customers.remove(customer)
