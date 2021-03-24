from flask import Flask
from database import db, Users, Tags
from modules.client.blueprint import client
from modules.admin.blueprint import admin
from modules.admin.login import login_manager
from config import Basic, Test

def create_app(config):
	app = Flask(__name__, static_folder='static')

	app.config.from_object(config)

	db.init_app(app)
	login_manager.init_app(app)

	app.register_blueprint(client)
	app.register_blueprint(admin)

	return app

app = create_app(Test)

@app.cli.command('setup')
def setup():
	db.drop_all()
	db.create_all()

	user = Users(username='seth',email='sethdad224@gmail.com')
	user.password = 'seth'

	db.session.add(Tags(name='flask'))
	db.session.add(Tags(name='biology'))
	db.session.add(user)
	
	db.session.commit()
	


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
