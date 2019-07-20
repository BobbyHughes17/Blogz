from app import db,app
import hashlib
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(120), unique = True,nullable = True)
    pw_hash = db.Column(db.String(120),nullable = False)
    blogz = db.relationship('Blog',backref='User')

    def __init__(self,user_name,password):

        self.user_name = user_name
        self.pw_hash = make_pw_hash(password)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False, unique = True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    owner = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.date_created = datetime.now()
        
def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexigest()

def check_pw_hash(password,hash):
    if make_pw_hash(password) == hash:
        return True
    return False

