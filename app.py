from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

from controller import error_handling
from controller.data_base import DataBase

app = Flask(__name__)
db = DataBase()
CORS(app)

# logging.basicConfig(filename="record.log", level=logging.DEBUG)

# log = logging.getLogger('werkzeug')
# log.disabled = True
# app.logger.disabled = True


# TODO: commenting
# TODO: connect GUI
# TODO: log all the actions

# Test
@app.route("/")
def get_name():
    return jsonify(message='Heyyy')


@app.route("/", methods=["POST"])
def login():
    return error_handling.check_input(request.json, db)


@app.route('/logout/<id>')
def logout(id):
    customer = error_handling.get_customer_from_id(id, db)
    if customer is not None:
        if customer.last_instance == 1:
            if not customer.inprocess:
                db.remove_customer(customer)
                return jsonify({'message': 'You logged out successfully'})
            else:
                return jsonify({'message': 'cant logout when actions still happening'})
        else:
            customer.last_instance -= 1
            return jsonify({'message': 'You logged out successfully & you NOT the last instance'})
    else:
        # we shouldn't get here but just to be sure
        return jsonify({'message': 'The account does not exist to log out'})
