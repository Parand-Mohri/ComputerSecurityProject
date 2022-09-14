# from Customer import Customer
from dataBase import dataBase


def post_customer(dataBase, customer):
    dataBase.add_customer(dataBase, customer)
    return customer


# check if customer id already exist
def check_customer_id(customer_id):
    for customer in dataBase.get_customer():
        if customer_id == customer['customer_id']:
            return True
        return False

# TODO
# check if the password is correct
def check_password(customer):
    return False