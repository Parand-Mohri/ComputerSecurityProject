from flask import Flask, jsonify, request
import logging

import hash_password
import post_customer
from Customer import Customer
from DataBase import DataBase

app = Flask(__name__)
db = DataBase()
# logging.basicConfig(filename='record.log', level=logging.DEBUG)


#Test
@app.route("/", methods=["GET"])
def get_name():
    hash_password.hash_password("parand")
    return jsonify(message='Heyyy')


@app.route("/", methods=["POST"])
def create_customer():
    # error handeling should happend here
    logging.info('logged in successfully') # logger test
    customer = Customer(request.json["id"], request.json["password"], request.json["server"], request.json["actions"])
    customer = post_customer.post_customer(db, customer)
    data = customer.dictionary()
    return jsonify(message='Customer',
                   category='success',
                   data=data,
                   status=200)