import logging
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

    def increase(self, value_amount):
        previous_value = self.value
        self.value = self.value + value_amount
        logging.info('(INCREASE) Customer' + self.customer_id + ': amount was: ' + previous_value + ', and is now:'+ self.value)

    def decrease(self, value_amount):
        previous_value = self.value
        if self.value > -500:
            self.value = self.value - value_amount
            logging.info('(DECREASE) Customer' + self.customer_id + ': amount was: ' + previous_value + ', and is now:' + self.value)
        else:
            logging.info('(DECREASE) Customer' + self.customer_id + ': Failed')


