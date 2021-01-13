from passlib.hash import bcrypt 


def hash_password(password:str):
    hashed = bcrypt.hash(password)
    return str(hash) 

print(hash_password('hi'))