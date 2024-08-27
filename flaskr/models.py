from . import db
from flask_login import LoginManager,UserMixin,login_user,logout_user

class user(UserMixin,db.Model):
        __tablename__="user"
        id=db.Column(db.Integer,primary_key=True)
        username=db.Column(db.string(250),unique=True,nullable=False)
        password=db.Column(db.string(250),nullable=False)
        def __repr__(self):
                return self.username