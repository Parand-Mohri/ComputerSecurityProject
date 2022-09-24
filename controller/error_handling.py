from controller import data_base
from controller import hash_password
from information.customer import Customer

# TODO input the ip and port of the computer running
main_server_ip_address = "SERVER_IP"
main_server_port = "PORT"


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
    if is_number(delay) and float(delay) >= 0:
        return True, float(delay)
    else:
        return False, -1


# steps need to be numbers
def check_steps(steps):
    """return True if the steps given are numbers"""
    for s in steps:
        if not is_number(s):
            return False, -1
        else:
            float(s)
    return True, steps


def check_id(cust_id: str) -> bool:
    """"return True if given id is less than 20 characters"""
    if len(cust_id) < 20:
        return True
    else:
        return False


def check_pw(cust_pw: str) -> bool:
    """return True if given password is less than 120 characters"""
    if len(cust_pw) < 120:
        return True
    else:
        return False


def check_srvr(new_ip, new_port):
    """return True if given server is match the one specified"""
    if new_ip == main_server_ip_address and new_port == main_server_port:
        return True
    else:
        return False
