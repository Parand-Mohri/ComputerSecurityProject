import hashlib
import random
import string

# source https://github.com/apscandy/database-hash-demo-python/blob/main/backend/hashing.py


def hash_password(password):
    return hashlib.md5(str.encode(password)).hexdigest()


def salt_generator():
    salt = ''
    for _ in range(0, 64):
        salt += random.choice(string.ascii_letters + string.digits)
    return str(salt)