from passlib.hash import bcrypt 
import os 
import random
from string import ascii_letters,ascii_lowercase,digits

def hash_password(password:str):
    hashed = bcrypt.hash(password)
    return str(hash) 


def Init_Uploads():
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, 'uploads')
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)



def allowed_file(filename , ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS