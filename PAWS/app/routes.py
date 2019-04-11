from flask import render_template, jsonify, abort, make_response, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EnrollForm, DepartmentForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Course, EnrollList, Departments
import sqlite3 as sql
import requests

@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title='PAWS - Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))	
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, fname=form.fname.data, lname=form.lname.data, department=form.department.data, degree=form.degree.data, address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zip=form.zip.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user')
@login_required
def user():
	user = User.query.filter_by(username=current_user.username).first_or_404()
	return render_template('user.html', user=user)

@app.route('/enroll', methods=['GET', 'POST'])
@login_required
def enroll():
	sid = current_user.id
	dep = current_user.department
	courses = Course.query.filter_by(department=dep, year=2019).all()
	enroll_list=EnrollList.query.filter_by(sid=sid).all()
	cidd=[]
	cname=[]
	cdepartment=[]
	ctime1=[]
	ctime2=[]
	for i in courses:
		cidd.append(i.id)
		cname.append(str(i.name))
		cdepartment.append(str(i.department))
		ctime1.append(str(i.time1))
		ctime2.append(str(i.time2))	
	
	course_list = [(cidd[i], (cname[i]+" | "+cdepartment[i]+" | "+ctime1[i][0]+" "+ctime1[i][1]+ctime1[i][2]+":"+ctime1[i][3]+ctime1[i][4]+", "+ctime2[i][0]+" "+ctime2[i][1]+ctime2[i][2]+":"+ctime2[i][3]+ctime2[i][4])) for i in range(len(courses))]
	form=EnrollForm()
	form.course.choices = course_list
	msg="not get in"
	
	if request.method == 'POST':
		msg="get in onsubmit"
		try:
			cid=form.course.data
			with sql.connect("app.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO enroll_list(sid, cid) VALUES(?, ?)", (sid, cid))
				con.commit()
				msg="suc"
		except:
			con.rollback()
			msg="fail"
	cur=sql.connect("app.db").cursor()
	cur.execute("SELECT cid FROM enroll_list WHERE sid=?", (sid,))
	result = cur.fetchall()
	lr=[]
	for i in result:
		lr.append(i[0])
	result=lr
	enroll_courses=[]
	for i in result:
		cur.execute("SELECT name, department, time1, time2 FROM course WHERE id=?", (i,))
		enroll_courses.append(cur.fetchall())
	tl=[]
	for i in enroll_courses:
		tl.append(i[0])
	cname=[]
	cdepartment=[]
	ctime1=[]
	ctime2=[]
	for i in tl:
		cname.append(i[0])
		cdepartment.append(i[1])
		ctime1.append(str(i[2]))
		ctime2.append(str(i[3]))	
	
	return render_template('enroll.html', title='Enroll',tl=tl, form=form, cname=cname, cdepartment=cdepartment, ctime1=ctime1, ctime2=ctime2, sid=sid, cid=form.course.data, msg=msg, enroll_courses=enroll_courses)
	
@app.route('/department', methods=['GET', 'POST'])
def department():
	year=2019
	dep="Computer Science"
	sem="SP"
	departments = Departments.query.all()
	department_list = [(i.department, i.department) for i in departments]
	form=DepartmentForm()
	form.department.choices = department_list
	course_list=[]
	#if request.method == 'POST':
	dep = form.department.data
	sem = form.semester.data
	year = form.year.data
	cur=sql.connect("app.db").cursor()
	cur.execute("SELECT name, time1, time2, id FROM course WHERE department=? AND semester=? AND year=?", (dep,sem,year))
	course_list=cur.fetchall()
	cname=[]
	ctime1=[]
	ctime2=[]
	cid=[]
	cstudent=[]
	for i in course_list:
		cname.append(str(i[0]))
		ctime1.append(str(i[1]))
		ctime2.append(str(i[2]))
		cid.append(i[3])
	temp=[]
	for i in range(len(cid)):
		cur.execute("SELECT sid FROM enroll_list WHERE cid=?", (cid[i],))
		temp=cur.fetchall()
		for a in temp:
			cur.execute("SELECT fname, lname FROM user WHERE id=?", (a[0],))
			result = cur.fetchall()
			lr = []
			for k in result:
				lr.append(k[0]+" "+k[1])
			cstudent.append([cname[i], lr])
	return render_template('department.html', title='Check courses',cstudent=cstudent, t=type(course_list), cname=cname, ctime1=ctime1, ctime2=ctime2, form=form, dep=dep, course_list=course_list)

@app.route('/api/get_courses/<string:dep>', methods=['GET'])
def get_courses(dep):
	cur=sql.connect("app.db").cursor()
	cur.execute("SELECT name FROM course WHERE department=?", (dep,))	
	result=cur.fetchall()
	lr=[]
	for i in result:
		lr.append(i[0])
	result = lr
	return jsonify({'courses': result})

@app.route('/api/get_students/<string:dep>', methods=['GET'])
def get_students(dep):
	cur = sql.connect("app.db").cursor()
	cur.execute("SELECT fname, lname, email, degree FROM user WHERE department=?", (dep,))
	result=cur.fetchall()
	lr=[]
	for i in result:
		lr.append(i)
	result = lr
	return jsonify({'students': result})

@app.route('/api/get_enrollment/<string:dep>', methods=['GET'])
def get_enrollment(dep):
	cur = sql.connect("app.db").cursor()
	cur.execute("SELECT name, id FROM course WHERE department=?", (dep,))
	result=cur.fetchall()
	cid=[]
	cname=[]
	for i in result:
		cname.append(i[0])
		cid.append(i[1])
	temp=[]
	cstudent=[]
	for i in range(len(cid)):
		cur.execute("SELECT sid FROM enroll_list WHERE cid=?", (cid[i],))
		temp=cur.fetchall()
		for a in temp:
			cur.execute("SELECT fname, lname FROM user WHERE id=?", (a[0],))
			result = cur.fetchall()
			lr = []
			for k in result:
				lr.append(k[0]+" "+k[1])
			cstudent.append([cname[i], lr])	
	return jsonify({'enrollment information': cstudent})

@app.route('/accepted', methods=['GET', 'POST'])
def accepted():
	data=""
	if request.method=='POST':
		try:
			data=requests.get('http://tinman.cs.gsu.edu:5028/api/v1.0/new_accepted_applicants').json()
		except:
			data="Nothing"
	return render_template('accepted.html', data=data)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
	data=""
	if request.method=='POST':
		try:
			url = "http://tinman.cs.gsu.edu:5028/api/v1.0/statistics/university"
			payload = "{\n\t\"university\": \"GSU\",\n\t\"term\": \"FA\",\n\t\"year\": 2019\n}"
			headers = {
				'Content-Type': "application/json",
				'cache-control': "no-cache",
				'Postman-Token': "5dbd8ec5-67c8-483a-807e-60427e705a65"
			}
			response = requests.request("GET", url, data=payload, headers=headers)
			data=response.text
		except:
			data="Nothing"
	return render_template('statistics.html', data=data)
