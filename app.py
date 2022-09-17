from flask import Flask, jsonify, request
import logging

import hash_password
import post_customer
from Customer import Customer
from DataBase import DataBase

app = Flask(__name__)
db = DataBase()
logging.basicConfig(filename='record.log', level=logging.DEBUG)


#Test
@app.route("/", methods=["GET"])
def get_name():
    return jsonify(message='Heyyy')


@app.route("/", methods=["POST"])
def create_customer():
    # TODO: error handeling should happend here
    logging.info('logged in successfully') # logger test
    password = request.json["password"]
    password, salt = hash_password.hash_salt_and_pepper(password)
    customer = Customer(request.json["id"], password, request.json["server"], request.json["actions"], salt)
    customer = post_customer.post_customer(db, customer)
    data = customer.dictionary()
    return jsonify(message='Customer',
                   category='success',
                   data=data,
                   status=200)