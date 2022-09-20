# from apscheduler.scheduler import Scheduler
import threading

from customer import Customer
from data_base import DataBase
from hash_password import hash_check


def post_customer(db: DataBase, customer: Customer) -> Customer:
    db.add_customer(customer)
    return customer


# check if customer id already exist
def costumer_id_exists(customer_id, db: DataBase) -> bool:
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return True
        return False


def get_customer_from_id(customer_id, db: DataBase) -> Customer:
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return customer


# The password is checked with the given assumption that the id is already verified/ existing.
# There is only one password for a given attempted password so we check the passwords one to one
def check_password(customer: Customer, try_pswrd: str) -> bool:
    return hash_check(try_pswrd, customer.password, customer.salt)


def task(customer: Customer, i: int):
    actions = customer.actions
    steps = actions.steps
    next_step = steps[i]
    customer.add(float(next_step))
    i += 1
    timer = threading.Timer(float(actions.delay), task, args=(customer, i,))
    timer.start()
    if i == len(actions.steps):
        timer.cancel()
    # print(customer.customer_id, "----------", actions.delay, "----------", customer.value)


def is_number(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def check_delay(delay: str):
    if is_number(delay) and float(delay) >= 0:
        return True, float(delay)
    else:
        return False, -1


def check_steps(steps):
    for s in steps:
        if not is_number(s):
            return False, -1
        else:
            float(s)
    return True, steps
