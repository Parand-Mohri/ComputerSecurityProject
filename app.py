from flask import Flask, jsonify, request

import post_customer
from Customer import Customer

app = Flask(__name__)

#Test
@app.route("/", methods=["GET"])
def get_name():
    return jsonify(message='Heyyy')


@app.route("/", methods=["POST"])
def create_customer():
    # error handeling should happend here
    customer = Customer(request.json["customer_id"], request.json["password"], request.json["server"], request.json["actions"])
    customer = post_customer.post_customer(customer)
    data = customer
    return jsonify(message='pizzas',
                   category='success',
                   data=data,
                   status=200)