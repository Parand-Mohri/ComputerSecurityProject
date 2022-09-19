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


# TODO: method responsible to do the actions
# TODO: delay needs to be added here
def do_step():
    print("Hello, World!")
    # actions = customer.actions
    # steps = actions.steps
    # first_step = steps[0]
    # customer.add(int(first_step))


# def do_action(customer):
#
#     delaying_time(customer)


# target task function
# def task(message):
#     print(message)

def task(message, i):
    print(message)
    # actions = customer.actions
    # for i in range(len(actions.steps)):
    # i = 0
    # S = threading.Timer(int(actions.delay), task, args=('Hello world',)).start()
    # timer = threading.Timer(10, do_step(), args=(arg1, arg2))
    # while i < 5:
    i += 1
    timer = threading.Timer(5, task, args=('Hello world',i,))
    timer.start()
    # print(customer.customer_id , "-----------", actions.delay )

    if i == 5:
        timer.cancel()
    # actions = customer.actions
    # steps = actions.steps
    # first_step = steps[0]
    # customer.add(int(first_step))
    #     i+= 1





def doAction(customer):
    actions = customer["actions"]
    steps = actions["steps"
    ]

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

