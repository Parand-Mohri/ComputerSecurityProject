from flask import Flask, jsonify, request

from controller import error_handling
from controller.data_base import DataBase

app = Flask(__name__)
db = DataBase()


# TODO: test the log file in other classes
# TODO: fix the config of log
# TODO: Once a client (its last instance!) logs out, all information on that client is deleted
# TODO: If the registration was successful, the server sends an acknowledgement.
# logging.basicConfig(filename='record.log', level=logging.DEBUG)


# Test
@app.route("/", methods=["GET"])
def get_name():
    return jsonify(message='Heyyy')


# TODO:Logout
@app.route("/", methods=["POST"])
def login():
    return error_handling.check_input(request.json, db)




