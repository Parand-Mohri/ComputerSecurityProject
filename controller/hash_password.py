import hashlib
import random
import string


# source: https://github.com/apscandy/database-hash-demo-python/blob/main/backend/hashing.py

def hash_salt_and_pepper(password: str):
    """hash the password and return the salt and new password"""
    salt = salt_generator()
    password = simple_pepper(password)
    password = password + salt
    password = hash_password(password)
    return password, salt


def hash_password(password):
    """use md5 to hash the password"""
    return hashlib.md5(str.encode(password)).hexdigest()


def salt_generator():
    """generate and return random str with size 64 that added to password before hashing"""
    salt = ''
    for _ in range(0, 64):
        salt += random.choice(string.ascii_letters + string.digits)
    return str(salt)


# reverse the substring of password in a random location before hashing
# TODO: find way to switch to this pepper
def pepper(password):
    num1 = random.randint(0, len(password))
    password = password[0:num1] + password[num1::][::-1]
    return password


# simpler peper
def simple_pepper(password):
    password = password[::-1]
    return password


def hash_check(password: str, database_hash: str, database_salt: str) -> bool:
    """return True if new password matches the stored one """
    password = simple_pepper(password)
    password = hash_password(password + database_salt)
    if password == database_hash:
        return True
    else:
        return False
