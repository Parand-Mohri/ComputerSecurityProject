from controller import data_base
from controller import hash_password
from information.customer import Customer

# TODO input the ip and port of the computer running
main_server_ip_address = "SERVER_IP"
main_server_port = "PORT"


# check if customer id already exist
def costumer_id_exists(customer_id, db: data_base) -> bool:
    for customer in db.customers:
        if customer_id == customer.customer_id:
            return True
    return False


# find the customer from db using its id
def get_customer_from_id(customer_id, db: data_base) -> Customer:
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
    try:
        float(string)
        return True
    except ValueError:
        return False


# delay should be a number
def check_delay(delay: str):
    if is_number(delay) and float(delay) >= 0:
        return True, float(delay)
    else:
        return False, -1


# steps need to be numbers
def check_steps(steps):
    for s in steps:
        if not is_number(s):
            return False, -1
        else:
            float(s)
    return True, steps


def check_id(cust_id: str) -> bool:
    if len(cust_id) < 20:
        return True
    else:
        return False


def check_pw(cust_pw: str) -> bool:
    if len(cust_pw) < 120:
        return True
    else:
        return False


def add_actions(customer, steps):
    customer.actions.add(steps)


def check_srvr(new_ip, new_port):
    if new_ip == main_server_ip_address and new_port == main_server_port:
        return True
    else:
        return False
