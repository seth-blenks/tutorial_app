from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import event
from datetime import datetime
from datetime import datetime
import markdown

db = SQLAlchemy()

class Image(db.Model):
	__tablename__ = 'image'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(32),unique=True)


class Users(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(225))
	email = db.Column(db.String(225), unique = True)
	_password = db.Column(db.String(225))
	active = db.Column(db.Boolean, default= True)
	authenticated = db.Column(db.Boolean, default=False)

	@property
	def is_authenticated(self):
		return self.authenticated

	@is_authenticated.setter
	def is_authenticated(self, state):
		self.authenticated = state
		db.session.add(self)

	@property
	def is_active(self):
		return self.active

	@is_active.setter
	def is_active(self, state):
		self.active = state
		db.session.add(self)

	@property
	def password(self):
		raise AttributeError('Password not readable')

	@password.setter
	def password(self, password):
		self._password = generate_password_hash(password, salt_length=10)

	def check_password(self, password):
		return check_password_hash(self._password, password)


tags_posts = db.Table('tags_posts',
	db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
	db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'))
	)

class Tags(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(32), unique=True)

class Posts(db.Model):
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(32), unique=True)
	content = db.Column(db.Text)
	image_name = db.Column(db.String(225))
	date = db.Column(db.DateTime, default=datetime.now)
	description = db.Column(db.Text)
	tags = db.relationship('Tags',secondary=tags_posts, backref=db.backref('posts',lazy='dynamic'))
	author = db.relationship('Users',backref=db.backref('posts',lazy='dynamic'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def add_tag(self, tag_lists):
		tag_lists = tag_lists.split(',')
		tags = []
		for tag in tag_lists:
			_tag = Tags.query.filter_by(name=tag).first()
			if _tag:
				self.tags.append(_tag)

def process_content(target, value, oldvalue, initiator):
	content = markdown.markdown(value)
	return content
				
event.listen(Posts.content,'set',process_content,retval=True)