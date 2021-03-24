from flask_login import LoginManager
from .blueprint import admin
from database import Users
from forms import LoginForm, RegisterForm
from flask import request, render_template, redirect, url_for, flash
from database import db
from flask_login import login_user, logout_user, current_user

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(user_id)

@admin.route('/login', methods=['POST','GET'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		email = form.email.data
		user = Users.query.filter_by(email=email).first()
		if not user:
			flash('Login failed')
			return redirect(url_for('client.login'))

		if user.check_password(form.password.data):
			user.is_authenticated = True
			db.session.add(user)
			db.session.commit()

			login_user(user)

			flash('Login successful')

			_next = request.args.get('next')
			if _next:
				return redirect(_next)

			return redirect(url_for('admin.homepage'))

	return render_template('login.html',form=form)

'''
@client.route('/register', methods=['POST','GET'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		email = form.email.data
		user = Users.query.filter_by(email=email).first()
		if user:
			flash('user with this email already exists')
			return redirect(url_for('client.login'))

		user = Users(username=form.username.data,email=email)
		user.password = form.password.data

		db.session.add(user)
		db.session.commit()
		flash("login successful")
		return redirect(url_for('client.login'))

	return render_template('register.html', form=form)
'''