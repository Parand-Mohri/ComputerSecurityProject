import logging
import threading

from information import action
from information import server


class Customer:
    def __init__(self, customer_id, password, server: server, actions: action, salt: str):
        self.customer_id = customer_id
        self.password = password
        self.server = server
        self.actions = actions
        self.salt = salt
        self.value = 0
        self.last_instance = 1
        self.inprocess = True
        self.attempt_count = 0
        self.account_frozen = False

    def dictionary(self):
        return {
            "customer_id": self.customer_id,
            "password": self.password,
            # "server": self.server.dictionary(),
            "actions": self.actions.dictionary(),
            "value": self.value
        }

    def takeout_server(self, new_server: server):
        for s in server:
            if (s.ip_address == new_server.ip_address) & (s.port == new_server.port):
                server.remove()
                return

    def add(self, value_amount: float):
        """add the step to  value"""
        previous_value = self.value
        self.value = self.value + value_amount
        msg = "Customer:", str(self.customer_id), ": amount was: ", str(previous_value), ", and is now: ", str(
            self.value)
        logging.info('%s : Add', msg)

    def do_steps(self):
        """do the steps with given delay"""
        steps = self.actions.steps
        next_step = steps[self.actions.start_at]
        self.add(float(next_step))
        self.actions.start_at += 1
        timer = threading.Timer(float(self.actions.delay), self.do_steps)
        timer.start()
        if self.actions.start_at == len(self.actions.steps):
            self.inprocess = False
            timer.cancel()

    def add_steps(self, new_steps):
        """add new steps"""
        self.actions.steps = self.actions.steps + new_steps
