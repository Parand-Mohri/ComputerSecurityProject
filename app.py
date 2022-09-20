from flask import Flask, jsonify, request
import logging

import hash_password as hash
import post_customer as post
from action import Action
from customer import Customer
from data_base import DataBase
from server import Server

app = Flask(__name__)
db = DataBase()


# TODO: test the log file in other classes
# TODO: fix the config of log
# logging.basicConfig(filename='record.log', level=logging.DEBUG)


# Test
@app.route("/", methods=["GET"])
def get_name():
    return jsonify(message='Heyyy')


# TODO:Logout
# TODO: add type of instance and putput to methods
# TODO: add limitation for id and password and server
# TODO: do something about check actions inside another person loging it make eroor
@app.route("/", methods=["POST"])
def login():
    try_id = request.json["id"]
    try_pswrd = request.json["password"]
    if post.costumer_id_exists(try_id, db):
        existing_cust = post.get_customer_from_id(try_id, db)
        if post.check_password(existing_cust, try_pswrd):
            # TODO: simultaneously actions for two people in same account
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
        check_s, steps = post.check_steps(request.json["actions"]["steps"])
        check_d, delay = post.check_delay(request.json["actions"]["delay"])
        if check_d and check_s:
            actions = Action(delay=delay, steps=steps)
            try_pswrd, salt = hash.hash_salt_and_pepper(try_pswrd)
            server = Server(request.json["server"]["ip"], request.json["server"]["port"])
            customer = Customer(try_id, try_pswrd, server, actions, salt)
            customer = post.post_customer(db, customer)
            post.task(customer, 0)
            data = customer.dictionary()
            return jsonify(message='new customer',
                           category='success',
                           data=data,
                           status=200)
        else:
            return jsonify(message='Error - action is not valid', category='Fail')
