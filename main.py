import re
from flask import Flask,request
from flask import json
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import backref
from flask_marshmallow import Marshmallow , fields
from utils import Init_Uploads
from passlib.hash import bcrypt 
from celery import make_celery
from tasks import upload_file



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'

Init_Uploads()
celery  = make_celery(app)



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
async def upload():
     if request.method == 'POST':

        if 'files[]' not in request.files:
            err_msg  = {'err':'files not found'}
            return  jsonify(err_msg)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                err_msg  = f'file {file} is not allowed'
                err = {'err':err_msg}
                return jsonify(err)

        return "successfully uploaded file"

    
    


if __name__ == "__main__":
    app.run(debug=True)



