
def post_customer(dataBase, customer):
    dataBase.add_customer(customer)
    return customer


# check if customer id already exist
def costumer_id_exists(customer_id, db):
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return True
        return False


def get_customer_from_id(customer_id, db):
    for customer in db.get_customers():
        if customer_id == customer.customer_id:
            return customer


# The password is checked with the given assumption that the id is already verified/ existing.
# There is only one password for a given attempted password so we check the passwords one to one
def check_password(customer, try_pswrd, hash):
    return hash.hash_check(try_pswrd, customer.password, customer.salt)


# TODO: method responsible to do the actions
# TODO: delay needs to be added here
def doAction(customer):
    actions = customer["actions"]
    steps = actions["steps"
]