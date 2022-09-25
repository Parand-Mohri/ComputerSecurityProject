from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

from controller import control
from controller.data_base import DataBase

app = Flask(__name__)
db = DataBase()
CORS(app)

logging.basicConfig(filename="record.log", level=logging.DEBUG)

log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True


# TODO: connect GUI

# Test
@app.route("/")
def get_name():
    return jsonify(message='Heyyy')


@app.route("/", methods=["POST"])
def login():
    return control.login(request.json, db)


@app.route('/logout/<customer_id>')
def logout(customer_id):
    return control.logout(customer_id, db)





