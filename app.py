from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

from controller import control
from controller.data_base import DataBase

app = Flask(__name__)
db = DataBase()
CORS(app)
cors = CORS(app, resources={r"/": {"origins": "*"}})

# logging.basicConfig(filename="record.log", level=logging.DEBUG)
#
# log = logging.getLogger('werkzeug')
# log.disabled = True
# app.logger.disabled = True


# Test
@app.route("/")
def get_name():
    return jsonify(message='Heyyy')


@app.route("/", methods=["POST"])
def login():
    return control.login(request.json, db)


@app.route('/logout', methods=["POST"])
def logout():
    return control.logout(request.json, db)





