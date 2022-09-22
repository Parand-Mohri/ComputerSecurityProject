import logging

from flask import jsonify

from controller import data_base
from controller import hash_password
from information.action import Action
from information.customer import Customer
from information.server import Server


# TODO: do something about check actions inside another person loging it make error
def check_input(customer_input: dict, db: data_base):
    try_id = customer_input["id"]
    try_pswrd = customer_input["password"]
    if costumer_id_exists(try_id, db):
        existing_cust = get_customer_from_id(try_id, db)
        if check_password(existing_cust, try_pswrd):
            if existing_cust.last_instance >= 2:
                return jsonify("message: only two instances can be in same account")
            else:
                existing_cust.last_instance += 1
                # TODO: simultaneously actions for two people in same account
                check_s, steps = check_steps(customer_input["actions"]["steps"])
                check_d, delay = check_delay(customer_input["actions"]["delay"])
                if check_d and check_s:
                    existing_cust.add_steps(steps)
                    #existing_cust.do_steps(0)
                    existing_cust.do_steps()
                else:
                    return jsonify(message='Error - action is not valid', category='Fail')

                return jsonify(message='Password validated correctly!', category='Success',
                             # data=data,
                            status=200)
        else:
            return jsonify(message='Error - wrong password', category='Fail',
                           # data=data,
                           status=200)
    else:
        # if come here account doesnt already exist
        logging.info('new account')
        check_s, steps = check_steps(customer_input["actions"]["steps"])
        check_d, delay = check_delay(customer_input["actions"]["delay"])
        is_pw = check_pw(customer_input["password"])
        is_id = check_id(customer_input["id"])
        if is_id:
            if is_pw:
                if check_d and check_s and is_pw and is_id:
                    actions = Action(delay=delay, steps=steps)
                    try_pswrd, salt = hash_password.hash_salt_and_pepper(try_pswrd)
                    server = Server(customer_input["server"]["ip"], customer_input["server"]["port"])
                    customer = Customer(try_id, try_pswrd, server, actions, salt)
                    db.add_customer(customer)  # add customer to db
                    customer.do_steps(0)
                    data = customer.dictionary()
                    return jsonify(message='new customer',
                                   category='success',
                                   data=data,
                                   status=200)
                else:
                    return jsonify(message='Error - action is not valid', category='Fail')
            else:
                return jsonify(message='Error - password is not valid', category='Fail')
        else:
            return jsonify(message='Error - id is not valid', category='Fail')


# check if customer id already exist
def costumer_id_exists(customer_id, db: data_base) -> bool:
    for customer in db.customers:
        if customer_id == customer.customer_id:
            return True
    return False


# find the customer from db using its id
def get_customer_from_id(customer_id, db: data_base) -> Customer:
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return customer
    return None


# The password is checked with the given assumption that the id is already verified/ existing.
# There is only one password for a given attempted password so we check the passwords one to one
def check_password(customer: Customer, try_pswrd: str) -> bool:
    return hash_password.hash_check(try_pswrd, customer.password, customer.salt)


# check if the value in string is a number
def is_number(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


# delay should be a number
def check_delay(delay: str):
    if is_number(delay) and float(delay) >= 0:
        return True, float(delay)
    else:
        return False, -1


# steps need to be numbers
def check_steps(steps):
    for s in steps:
        if not is_number(s):
            return False, -1
        else:
            float(s)
    return True, steps


def check_id(cust_id: str) -> bool:
    if len(cust_id) < 20:
        return True
    else:
        return False


def check_pw(cust_pw: str) -> bool:
    if len(cust_pw) < 120:
        return True
    else:
        return False


def add_actions(customer, steps):
    customer.actions.add(steps)




def add_actions(customer, steps):
    customer.actions.add(steps)


