from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Course, EnrollList, Departments
from app import app, db

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	department = SelectField('Department', choices=[('Computer Science','Computer Science'), ('Computer Information Systems', 'Computer Information Systems'), ('Physics', 'Physics')], validators=[DataRequired()])
	degree = SelectField('Degree', choices=[('MS', 'Master'), ('U', 'Undergraduate'), ('PHD', 'PHD')], validators=[DataRequired()])
	fname = StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	address1 = StringField('Address', validators=[DataRequired()])
	address2 = StringField('Address (additonal)')
	city = StringField('City', validators=[DataRequired()])
	state = SelectField('State', choices=[('AL','Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('GA','Georgia'),('CA','California')], validators=[DataRequired()])
	zip = StringField('Zip', validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class EnrollForm(FlaskForm):
	
	courses = Course.query.all()
	course_list = [(i.id, (i.name+i.department+str(i.time1)+str(i.time2))) for i in courses]
	course = SelectField('Course', choices=course_list, validators=[DataRequired()])
	submit = SubmitField('Enroll')

class DepartmentForm(FlaskForm):
	departments = Departments.query.all()
	department_list = [(i.id, i.department) for i in departments]
	department = SelectField('Department', choices = department_list, validators=[DataRequired()])
	semester = SelectField('Semester', choices = [('SP', 'Spring'), ('SU', 'Summer'), ('FA', 'Fall')])
	year = SelectField('Year', choices=[(2019, 2019), (2018, 2018), (2017, 2017)])
	submit = SubmitField('Check')

