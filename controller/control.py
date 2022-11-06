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
    if not check_d or not check_s:
        return jsonify(message='Error - actions are not valid', category='Fail')

    ########### For existing customer ###################

    if eh.costumer_id_exists(try_id, db):

        existing_cust = eh.get_customer_from_id(try_id, db)
        if existing_cust.account_frozen:
            return jsonify(message="You account has been frozen")

        log_in_legit, msg = eh.check_login_attempts(try_pswrd, existing_cust)

        if not log_in_legit:
            return jsonify(message=msg, category='Fail')

        else:  # if login successful
            if existing_cust.last_instance >= 2:
                return jsonify(message='Error - only two instances can be in same account', category='Fail')
            if existing_cust.actions.delay != delay:
                return jsonify(message='Error - cannot change the delay', category='Fail')

            existing_cust.server.append(Server(customer_input["server"]["ip"], customer_input["server"]["port"]))
            existing_cust.last_instance += 1
            msg = "New instance of customer:", str(existing_cust.customer_id),
            logging.info('%s : new instance', msg)
            if len(steps) > 0:
                existing_cust.add_steps(steps)
                if not existing_cust.inprocess:
                    existing_cust.inprocess = True
                    existing_cust.do_steps()
            return jsonify(message='Password validated correctly!', category='Success')


    ########### New customer ###################

    else:
        if len(steps) < 1:
            return jsonify(message='You need to add steps as first instance!', category='Fail')
        is_pw = eh.check_pw(customer_input["password"])
        is_id = eh.check_id(customer_input["id"])
        if not is_pw:
            return jsonify(message='Error - password is not valid. Password should be between 1 and 120 characters.',
                           category='Fail')
        if not is_id:
            return jsonify(message='Error - id is not valid. Id should be between 1 and 20 characters.',
                           category='Fail')
        # Check for common psw
        if not eh.common_pass(try_id, try_pswrd):
            return jsonify(messag='Error - Password is not secure, try another password', category='Fail')

        actions = Action(delay=delay, steps=steps)
        try_pswrd, salt = hash_password.hash_salt_and_pepper(try_pswrd)
        server = [Server(customer_input["server"]["ip"], customer_input["server"]["port"])]
        customer = Customer(try_id, try_pswrd, server, actions, salt)
        db.add_customer(customer)  # add customer to db
        msg = "Customer:", str(customer.customer_id),
        logging.info('%s : logged in', msg)
        customer.do_steps()
        return jsonify(message='new customer',
                       category='Success')


def logout(customer_input: dict, db: data_base):
    try_id = customer_input["id"]
    try_pswrd = customer_input["password"]
    customer = eh.get_customer_from_id(try_id, db)
    server = Server(customer_input["server"]["ip"], customer_input["server"]["port"])
    if customer is None:
        return jsonify(message='Error - Cannot log out', category='Fail')
    if not eh.check_password(customer, try_pswrd):
        return jsonify(message='Error - Cannot log out', category='Fail')
    if not eh.check_srvr(customer, server):
        return jsonify(message='Cant log out with this server', category='Fail')
    if customer.last_instance > 1:
        customer.last_instance -= 1
        customer.takeout_server(server)
        return jsonify(message='You logged out successfully & you NOT the last instance', category='Success')
    if customer.inprocess:
        return jsonify(message='Error - cant logout when actions still happening', category='Fail')
    msg = "Customer:", str(customer.customer_id),
    logging.info('%s : logged out', msg)
    db.remove_customer(customer)
    return jsonify(message='You logged out successfully', category='Success')
