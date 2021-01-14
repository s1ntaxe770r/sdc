import re
from flask import Flask,request
from flask import json
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import backref
from flask_marshmallow import Marshmallow , fields
from utils import Init_Uploads,allowed_file
from passlib.hash import bcrypt 
from tasks import upload_file
from redis import Redis
from rq import Queue



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg','webp'])
redis_conn= Redis()
q = Queue(connection=redis_conn)


Init_Uploads()



db = SQLAlchemy(app)
ma = Marshmallow(app)

db.drop_all()
db.create_all()
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    user_img = db.relationship('Images',backref='user_images')
  

    def __repr__(self):
        return '<User %r>' % self.username
    @classmethod
    def hash_password(cls,password:str):
        hashed = bcrypt.hash(password)
        return str(hashed) 
    @classmethod
    def pass_verify(cls,password:str,hash:str):
        verified = bcrypt.verify(password,hash)
        return verified


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_image_links = db.Column(db.String(230),nullable=False)
    private_image_links = db.Column(db.String(230),nullable=False)
    image_owner  = db.Column(db.Integer(),db.ForeignKey('users.id'))



@app.route("/users/create",methods=['POST'])
def create_user():
    form_data = request.json
    if form_data['username'] == '' and form_data['password'] == '':
        err_message = {'error':'password and username are required to create an account'}
        return jsonify(err_message)
    hash = Users.hash_password(form_data['password'])
    username =  form_data['username']
    new_user = Users(username=username,password=hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {
            'username': username,
            'account_created': 'true',
        }
    )
    
@app.route('/upload',methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        err_msg  = {'err':'no file found in request body'}
        return jsonify(err_msg)

    files = request.files.getlist('files[]')
    print('none here either')
    for file in files:
        if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
            print('files get qued')
            q.enqueue(upload_file,file)
            success_msg = 'your files would be uploaded shortly'
            print('json failing?')
            return jsonify({'uploaded':"True",'message':success_msg})
        print('prob return val')
        return jsonify({'err':'sorry one of the files is not allowed'})  
                
     

    
    


if __name__ == "__main__":
    app.run(debug=True)



