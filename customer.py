import logging

from action import Action
from server import Server


class Customer():
    def __init__(self, customer_id, password, server: Server, actions: Action, salt: str):
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
            "server": self.server.dictionary(),
            "actions": self.actions.dictionary(),
            "value": self.value
        }

    def add(self, value_amount: float):
        previous_value = self.value
        self.value = self.value + value_amount
        logging.info('Customer' , self.customer_id , ': amount was: ' , previous_value , ', and is now:', self.value)


