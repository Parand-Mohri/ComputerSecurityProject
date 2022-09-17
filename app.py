from flask import Flask, jsonify, request
import logging

import hash_password as hash
import post_customer as post
from Customer import Customer
from DataBase import DataBase

app = Flask(__name__)
db = DataBase()
# logging.basicConfig(filename='record.log', level=logging.DEBUG)


#Test
@app.route("/", methods=["GET"])
def get_name():
    return jsonify(message='Heyyy')



@app.route("/", methods=["POST"])
def login():
    try_id = request.json["id"]
    try_pswrd = request.json["password"]
    if post.costumer_id_exists(try_id, db):
        existing_cust = post.get_customer_from_id(try_id)
        if post.check_password(existing_cust, try_pswrd,hash ) == False:
            return jsonify(message='Error - wrong password',
                   category='Fail',
                   data=data,
                   status=200)
        else:
            return jsonify(message='Password validated correctly!',
                   category='success',
                   data=data,
                   status=200)

    else:
        logging.info('logged in successfully') # logger test
        # if password
        try_pswrd, salt = hash_password.hash_salt_and_pepper(try_pswrd)
        customer = Customer(try_id, try_pswrd, request.json["server"], request.json["actions"], salt)
        customer = post.post_customer(db, customer)
        data = customer.dictionary()
        return jsonify(message='Customer',
                   category='success',
                   data=data,
                   status=200)




# @app.route("/", methods=["POST"])
# def create_customer():
#     # TODO: error handeling should happend here
#     logging.info('logged in successfully') # logger test
#     password = request.json["password"]
#     # if password
#     password, salt = hash_password.hash_salt_and_pepper(password)
#     customer = Customer(request.json["id"], password, request.json["server"], request.json["actions"], salt)
#     customer = post_customer.post_customer(db, customer)
#     data = customer.dictionary()
#     return jsonify(message='Customer',
#                    category='success',
#                    data=data,
#                    status=200)