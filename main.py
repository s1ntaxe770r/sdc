import re
from flask import Flask,request,g,send_from_directory
from flask import json
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from utils import Init_Uploads,allowed_file,Random_File
from passlib.hash import bcrypt 
import pathlib
from flask.globals import request
from werkzeug.utils import secure_filename
from itertools import chain
import os
from flask_httpauth import HTTPBasicAuth
import requests



app = Flask(__name__,static_url_path='/images',static_folder='uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PRIVATE_UPLOAD_FOLDER'] = 'private'
auth = HTTPBasicAuth()
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg','webp'])




Init_Uploads()

db = SQLAlchemy(app)


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
    public_image= db.Column(db.String(230))
    private_image= db.Column(db.String(230))
    image_owner  = db.Column(db.Integer(),db.ForeignKey('users.username'))


@auth.verify_password
def verify_password(username, password):
    user = Users.query.filter_by(username = username).first()
    if not user or not Users.pass_verify(password,user.password):
        return False
    g.user = user
    return True



# Create an account !!
@app.route("/users/create",methods=['POST'])
def create_user():
    form_data = request.json
    if form_data['username'] == '' and form_data['password'] == '':
        err_message = {'error':'password and username are required to create an account'}
        return jsonify(err_message)
    hash = Users.hash_password(form_data['password'])
    username =  form_data['username']
    if Users.query.filter_by(username = username).first() is not None:
        err_message  = {
            'message':'sorry that user already exists',
            'account_created':'false'
        }
        return jsonify(err_message)
    new_user = Users(username=username,password=hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {
            'username': username,
            'account_created': 'true',
        }
    )
 
@app.route('/public/upload',methods=['POST'])
@auth.login_required
def upload_public():
    if 'files[]' not in request.files:
        err_msg  = {'err':'no file found in request body'}
        return jsonify(err_msg)
    files = request.files.getlist('files[]')
    for file in files:
        if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
            uploaded_files = 0 
            secure_file , filext = os.path.splitext(secure_filename(file.filename))
            Random_Filename = Random_File.generate()
            newfilename = Random_Filename + filext
            if file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename)):
                uploaded_files +=1
                os.rename(secure_file,newfilename)
            usr_name = auth.current_user()
            user_img = Images(public_image=newfilename,image_owner=usr_name)
            db.session.add(user_img)
            db.session.commit()
            success_msg = 'uploaded file(s)'
            return jsonify({'uploaded':"True",'message':success_msg})
        
        return jsonify({'err':'sorry one of the files is not allowed'})


@app.route('/private/upload',methods=['POST'])
@auth.login_required
def upload_private():
    if 'files[]' not in request.files:
        err_msg  = {'err':'no file found in request body'}
        return jsonify(err_msg)
    files = request.files.getlist('files[]')
    print('none here either')
    for file in files:
        uploaded_files = []
        if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
            secure_file , filext = os.path.splitext(secure_filename(file.filename))
            Random_Filename = Random_File.generate()
            newfilename = Random_Filename + filext
            if file.save(os.path.join(app.config['PRIVATE_UPLOAD_FOLDER'], newfilename)):
                os.rename(secure_file,newfilename)
            usr_name = auth.current_user()
            user_img = Images(private_image=newfilename,image_owner=usr_name)
            uploaded_files.append(newfilename)
            db.session.add(user_img)
            db.session.commit()
            success_msg = f'uploaded {len(uploaded_files)} file(s)'
            return jsonify({'uploaded':"True",'message':success_msg,'uploaded_files':uploaded_files})
        
        return jsonify({'err':'sorry one of the files is not allowed'})








@app.route('/public/images')
def get_images():
   images  = db.session.query(Images.public_image).all()
   image_list = list(chain.from_iterable(images))
   public_images = {'Images':image_list} 
   return  jsonify(public_images)

@app.route('/private/images')
@auth.login_required
def get_private_images():
   username =  usr_name = auth.current_user()
   images  = db.session.query(Images.private_image).filter(Images.image_owner==username).all()
   image_list = list(chain.from_iterable(images))   
   public_images = {'Images':image_list} 
   return  jsonify(public_images)





@app.route('/image/<path:filename>')
def send_image(filename):
    return send_from_directory('uploads', filename)

    
    

if __name__ == "__main__":
    app.run(debug=True)



