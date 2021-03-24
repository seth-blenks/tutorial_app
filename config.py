from os import path
class Basic:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join('.','data.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = 'secret'

class Test(Basic):
	WTF_CSRF_ENABLED = False