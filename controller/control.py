import logging

from flask import jsonify

from controller import data_base, hash_password
import controller.error_handling as eh
from information.action import Action
from information.customer import Customer
from information.server import Server


def login(customer_input: dict, db: data_base):
    """return success if all the information given is correct"""
    try_id = customer_input["id"]
    try_pswrd = customer_input["password"]
    check_s, steps = eh.check_steps(customer_input["actions"]["steps"])
    check_d, delay = eh.check_delay(customer_input["actions"]["delay"])
    check_serv = eh.check_srvr(customer_input["server"]["ip"], customer_input["server"]["port"])
    if not check_serv:
        return jsonify(messag='Error - server is not valid', category='Fail')
    if not check_d or not check_s:
        return jsonify(message='Error - actions are not valid', category='Fail')
    if eh.costumer_id_exists(try_id, db):
        existing_cust = eh.get_customer_from_id(try_id, db)
        if not eh.check_password(existing_cust, try_pswrd):
            return jsonify(message='Error - wrong password', category='Fail')
        if existing_cust.last_instance >= 2:
            return jsonify(message='Error - only two instances can be in same account', category='Fail')
        if existing_cust.actions.delay != delay:
            return jsonify(message='Error - cannot change the delay', category='Fail')
        existing_cust.last_instance += 1
        msg = "New instance of customer:", str(existing_cust.customer_id),
        logging.info('%s : new instance', msg)
        if len(steps) > 0:
            existing_cust.add_steps(steps)
            if not existing_cust.inprocess:
                existing_cust.inprocess = True
                existing_cust.do_steps()
        return jsonify(message='Password validated correctly!', category='Success')
    else:
        if len(steps) < 1:
            return jsonify(message='You need to add steps as first instance!', category='Fail')
        is_pw = eh.check_pw(customer_input["password"])
        is_id = eh.check_id(customer_input["id"])
        if not is_pw:
            return jsonify(message='Error - password is not valid. Password should be between 1 and 120 characters.',
                           category='Fail')
        if not is_id:
            return jsonify(message='Error - id is not valid. Id should be between 1 and 20 characters.', category='Fail')
        actions = Action(delay=delay, steps=steps)
        try_pswrd, salt = hash_password.hash_salt_and_pepper(try_pswrd)
        server = Server(customer_input["server"]["ip"], customer_input["server"]["port"])
        customer = Customer(try_id, try_pswrd, server, actions, salt)
        db.add_customer(customer)  # add customer to db
        msg = "Customer:", str(customer.customer_id),
        logging.info('%s : logged in', msg)
        customer.do_steps()
        data = customer.dictionary()
        return jsonify(message='new customer',
                       category='success',
                       data=data)


def logout(customer_id, db:data_base):
    customer = eh.get_customer_from_id(customer_id, db)
    if customer is None:
        return jsonify(messag='Error - The account does not exist to log out', category='Fail')
    if customer.last_instance > 1:
        customer.last_instance -= 1
        return jsonify(messag='You logged out successfully & you NOT the last instance', category='Success')
    if customer.inprocess:
        return jsonify(messag='Error - cant logout when actions still happening', category='Fail')
    msg = "Customer:", str(customer.customer_id),
    logging.info('%s : logged out', msg)
    db.remove_customer(customer)
    return jsonify(messag='You logged out successfully', category='Success')
