# from apscheduler.scheduler import Scheduler
import threading

from hash_password import hash_check


def post_customer(dataBase, customer):
    dataBase.add_customer(customer)
    return customer


# check if customer id already exist
def costumer_id_exists(customer_id, db):
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return True
        return False


def get_customer_from_id(customer_id, db):
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return customer


# The password is checked with the given assumption that the id is already verified/ existing.
# There is only one password for a given attempted password so we check the passwords one to one
def check_password(customer, try_pswrd):
    return hash_check(try_pswrd, customer.password, customer.salt)


def task(customer, i):
    actions = customer.actions
    steps = actions.steps
    first_step = steps[i]
    customer.add(int(first_step))
    i += 1
    timer = threading.Timer(int(actions.delay), task, args=(customer, i,))
    timer.start()
    if i == len(actions.steps):
        timer.cancel()
    print(customer.customer_id, "----------", actions.delay, "----------", customer.value)


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def check_delay(delay):
    if is_number(delay) and float(delay) >= 0:
        return True, float(delay)
    else:
        return False


def check_steps(steps):
    for s in steps:
        if is_number(s) == False:
            return False
        else:
            s = float(s)
    return True, steps
