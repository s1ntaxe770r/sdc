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
    PRIVATE_FOLDER =os.path.join(path, 'private')
    if not os.path.isdir(UPLOAD_FOLDER) and os.path.isdir(PRIVATE_FOLDER):
        os.makedir(UPLOAD_FOLDER)
        os.makedir(PRIVATE_FOLDER)


class Random_File:
 	@classmethod
 	def generate(cls,size=6):
 		characters = ascii_letters  +  digits + ascii_lowercase
 		choice = random.SystemRandom()
 		password =  "".join(choice.choice(characters)
                    for i in range(size))
 		return str(password)
def allowed_file(filename , ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS