# from Customer import Customer
# from dataBase import dataBase


from dataclasses import dataclass
from sqlite3 import DatabaseError
from Customer import Customer

from DataBase import DataBase


def post_customer(dataBase, customer):
    dataBase.add_customer(customer)
    return customer


# check if customer id already exist
def costumer_id_exists(customer_id, dataBase):
    for customer in dataBase.get_customers():
        if customer_id == customer['customer_id']:
            return True
        return False

def get_customer_from_id(customer_id, dataBase):
    for customer in dataBase.get_customers():
        if customer_id == customer['customer_id']:
            return customer

# The password is checked with the given assumption that the id is already verified/ existing.  
# There is only one password for a given attempted password so we check the passwords one to one 
def check_password(customer, try_pswrd):
    if try_pswrd == customer.password:
        return True
    return False