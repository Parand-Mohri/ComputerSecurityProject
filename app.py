from flask import Flask, jsonify, request
import logging

import hash_password as hash
import post_customer as post
from Action import Action
from Customer import Customer
from DataBase import DataBase
from Server import Server

app = Flask(__name__)
db = DataBase()
# TODO: test the log file in other classes
# TODO: fix the config of log
# logging.basicConfig(filename='record.log', level=logging.DEBUG)


#Test
@app.route("/", methods=["GET"])
def get_name():
    return jsonify(message='Heyyy')


# TODO: check if actions are vaild
@app.route("/", methods=["POST"])
def login():
    try_id = request.json["id"]
    try_pswrd = request.json["password"]
    if post.costumer_id_exists(try_id, db):
        existing_cust = post.get_customer_from_id(try_id,db)
        if post.check_password(existing_cust, try_pswrd, hash):
            # TODO: simultaneously actions for two people in same account
            return jsonify(message='Password validated correctly!', category='succes',
                   # data=data,
                   status=200)
        else:
            return jsonify(message='Error - wrong password', category='Fail',
                   # data=data,
                   status=200)

    else:
        # TODO: test the if else statement
        # if come here account doesnt exist
        logging.info('new account')
        if post.check_delay(request.json["delay"]) and post.check_steps(request.json["steps"]):
            return jsonify(message='action is valid!', category='succes',
            # data=data,
            status=200)
        else:
            return jsonify(message='Error - action is not valid', category='Fail',
                           # data=data,
                           status=200)
        actions = Action(request.json["delay"], request.json["steps"])
        try_pswrd, salt = hash.hash_salt_and_pepper(try_pswrd)
        server = Server(request.json["ip_address"], request.json["port"])
        customer = Customer(try_id, try_pswrd, server, actions, salt)
        customer = post.post_customer(db, customer)
        data = customer.dictionary()
        return jsonify(message='new customer',category='success',data=data,  status=200)