
# gonna be used as data base
class dataBase:

    def __init__(self):
        self.customers = []
        # self.actions = []

    def get_customer(self):
        return self.customer

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self, customer):
        self.customer.remove(customer)

    # def get_actions(self):
    #     return self.customer
    #
    # def add_actions(self, customer):
    #     self.customer.append(customer)
    #
    # def remove_actions(self, customer):
    #     self.customer.remove(customer)