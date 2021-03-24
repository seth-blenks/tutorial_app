from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields import FileField


class UploadPostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('content',validators=[DataRequired()])
	image_name = StringField('image_name', validators=[DataRequired()])
	tags = StringField('tags', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])

class UpdatePostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('content',validators=[DataRequired()])
	image_name = StringField('image_name', validators=[DataRequired()])
	tags = StringField('tags', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])

class LoginForm(FlaskForm):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class UploadImageForm(FlaskForm):
	image = FileField('image', validators=[DataRequired()])

class UploadTag(FlaskForm):
	name = StringField('tag', validators=[DataRequired()])

