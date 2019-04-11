from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	department = db.Column(db.String(30))
	degree = db.Column(db.String(30))
	fname = db.Column(db.String(30), index=True)
	lname = db.Column(db.String(30), index=True)
	address1 = db.Column(db.String(50), index=True)
	address2 = db.Column(db.String(50), index=True)
	city = db.Column(db.String(30), index=True)
	state = db.Column(db.String(30), index=True)
	zip = db.Column(db.Integer, index=True)

	def __repr__(self):
		return '<User {}>'.format(self.username)
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), index=True)
	time1 = db.Column(db.Integer, index=True)
	time2 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
	department = db.Column(db.String(50), index=True)
	semester = db.Column(db.String(50), index=True)
	year = db.Column(db.Integer, index=True)
	def __repr__(self):
		return '<Course {}>'.format(self.name)

class Departments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	department = db.Column(db.String(100), index=True)
	def __repr__(self):
		return '<Department {}>'.format(self.department)

class EnrollList(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sid = db.Column(db.Integer, index=True)
	cid = db.Column(db.Integer, index=True)
	def __repr__(self):
		return '<EnrollList {}>'.format(self.id)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
