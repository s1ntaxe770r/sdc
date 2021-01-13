from flask import Flask,request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import backref
from flask_marshmallow import Marshmallow , fields
from passlib.hash import bcrypt 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


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
        return hash 
    @classmethod
    def pass_verify(cls,password:str,hash:str):
        verified = bcrypt.verify(password,hash)
        return verified


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_image_links = db.Column(db.String(230),nullable=False)
    private_image_links = db.Column(db.String(230),nullable=False)
    image_owner  = db.Column(db.Integer(),db.ForeignKey('users.id'))

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model= Users
        fields = ("username","password")

    username = ma.auto_field()
    password = ma.auto_field()




@app.route("/users/create",methods=['POST'])
def create_user():
    form_data = request.json
    errors = UserSchema.validate(form_data)
    if errors:
        return jsonify({ 'error':errors})
    hash = Users.hash_password(form_data['password'])
    username =  form_data['username']
    new_user = Users(username=username,password=hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {
            'username': username,
            'account_created': 'true',
            'date': datetime.time()
        }
    )
    

if __name__ == "__main__":
    app.run(debug=True)