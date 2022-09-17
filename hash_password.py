import hashlib
import random
import string


# source https://github.com/apscandy/database-hash-demo-python/blob/main/backend/hashing.py

# hash the password and return the hash password with used salt to be saved
def hash_salt_and_pepper(password: str):
    salt = salt_generator()
    password = pepper(password)
    password = password + salt
    password = hash_password(password)
    return password, salt


# hash the password using build in library
def hash_password(password):
    return hashlib.md5(str.encode(password)).hexdigest()

# generate random str with size 64 that added to password before hashing
def salt_generator():
    salt = ''
    for _ in range(0, 64):
        salt += random.choice(string.ascii_letters + string.digits)
    return str(salt)


# reverse the substring of password in a random location before hashing
def pepper(password):
    num1 = random.randint(0, len(password))
    password = password[0:num1] + password[num1::][::-1]
    return password


# TODO: check all combinations of the pepper to check the password
# check if the given password match the stored one
def hash_check(password: str, database_hash: str, database_salt: str) -> bool:
    password = pepper(password)
    password = hash_password(password + database_salt)
    if password == database_hash:
        return True
    else:
        return False
