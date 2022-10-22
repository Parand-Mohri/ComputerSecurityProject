from controller import data_base
from controller import hash_password
from information.customer import Customer
import time



def costumer_id_exists(customer_id, db: data_base) -> bool:
    """return True if customer id already exist"""
    for customer in db.customers:
        if customer_id == customer.customer_id:
            return True
    return False


def get_customer_from_id(customer_id, db: data_base) -> Customer:
    """return the customer with the given id"""
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return customer
    return None


# The password is checked with the given assumption that the id is already verified/ existing.
# There is only one password for a given attempted password so we check the passwords one to one
def check_password(customer: Customer, try_pswrd: str) -> bool:
    return hash_password.hash_check(try_pswrd, customer.password, customer.salt)


# check if the value in string is a number
def is_number(string: str) -> bool:
    """return true if the given string is a number"""
    try:
        float(string)
        return True
    except ValueError:
        return False


def check_delay(delay: str):
    """return True if the value given as delay is a number"""
    if len(delay) < 1:
        return False, -1
    if is_number(delay) and float(delay) >= 0:
        return True, float(delay)
    else:
        return False, -1


# steps need to be numbers
def check_steps(steps):
    """return True if the steps given are numbers"""
    for s in steps:
        num = float(s)
        if not is_number(s):
            return False, -1
    return True, steps


def check_id(cust_id: str) -> bool:
    """"return True if given id is less than 20 characters"""
    if 20 > len(cust_id) > 0:
        return True
    else:
        return False


def check_pw(cust_pw: str) -> bool:
    """return True if given password is less than 120 characters"""
    if 120 > len(cust_pw) > 0:
        return True
    else:
        return False


def check_srvr(customer: Customer, server) -> bool:
    """return True if given server is match with one of the servers that customer has"""
    for s in customer.server:
        if (s.ip_address == server.ip_address) & (s.port == server.port):
            return True
    return False

def check_login_attempts(cust_pwd : str, customer : Customer):
    return_msg = ''
    customer.attempt_count += 1
    print('cus ', customer.attempt_count)
    if customer.attempt_count <= 5:
        if check_password(customer, cust_pwd):
            return_msg = 'Password validated correctly!'
            customer.attempt_count = 0
            return True, return_msg
        else:
            remaining = 5 - customer.attempt_count
            return_msg = 'Error - wrong password or user name, you have ' + str(remaining) + ' attempts remaining'
            return False, return_msg

    elif customer.attempt_count == 6:    # if they failed login more than 5 times
        customer.account_frozen = True
        return_msg = 'Cannot login, user is blocked.'
        return False , return_msg
    