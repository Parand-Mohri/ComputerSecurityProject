import logging
import threading


from information import action
from information import server


class Customer():
    def __init__(self, customer_id, password, server: server, actions: action, salt: str):
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

    # add the given step to value
    def add(self, value_amount: float):
        previous_value = self.value
        self.value = self.value + value_amount
        msg = "Customer:", str(self.customer_id), ": amount was: ", str(previous_value), ", and is now: ", str(
            self.value)
        logging.info('%s : Add', msg)

    # do the steps with the given delay
    def do_steps(self, i: int):
        steps = self.actions.steps
        next_step = steps[i]
        self.add(float(next_step))
        i += 1
        timer = threading.Timer(float(self.actions.delay), self.do_steps, args=(i,))
        timer.start()
        if i == len(self.actions.steps):
            timer.cancel()
        print(self.customer_id, "----------", self.actions.delay, "----------", self.value)

    def add_steps(self, new_steps, i: int):
        next_step = new_steps[i]
        self.add(float(next_step))
        i += 1
