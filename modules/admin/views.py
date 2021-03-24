from flask import render_template, redirect, url_for, abort, flash, current_app
from pathlib import Path
from os import path
from .blueprint import admin
from forms import UploadPostForm, UploadImageForm, UploadTag
from database import Tags, Posts, db, Image
from flask_login import current_user, fresh_login_required
from uuid import uuid4

def save_file(doc, location):
	image_name = str(uuid4()) + '.jpg'

	with open(path.join(location, image_name), 'wb') as wfile:
		wfile.write(doc.read())

	return image_name

@admin.route('/')
@fresh_login_required
def homepage():
	return render_template('admin/homepage.html')


@admin.route('/upload/image', methods=['GET','POST'])
@fresh_login_required
def upload_image():
	form = UploadImageForm()

	if form.validate_on_submit():
		image = form.image.data

		current_app.logger.debug(image)

		image_name = save_file(image,Path(current_app.instance_path).parent.joinpath('static/img') )

		img = Image()
		img.name = image_name
		db.session.add(img)
		db.session.commit()

		current_app.logger.info(f'{image.name} saved to /static/images/')
		flash('image successfully uploaded', category='alert alert-success')
		return	 redirect(url_for('admin.homepage'))


	return render_template('admin/upload_image.html',form=form)


@admin.route('/upload/post', methods=['POST','GET'])
@fresh_login_required
def upload_post():
	form = UploadPostForm()
	if form.validate_on_submit():
		title = form.title.data.strip(' ')
		content = form.content.data.strip(' ')
		image_name = form.image_name.data.strip(' ')
		
		old = Posts.query.filter_by(title=title).first()
		if old:
			flash('post already collected')
			return redirect(url_for('admin.upload_post'))

		post = Posts(title=title, content=content)
		post.add_tag(form.tags.data)
		post.image_name = image_name
		post.description = form.description.data
		post.author = current_user

		db.session.add(post)
		db.session.commit()

		flash('upload successful')
		return redirect(url_for('admin.upload_post'))

	return render_template('admin/upload_post.html',form=form)

@admin.route('/upload/tag', methods=['POST','GET'])
@fresh_login_required
def upload_tag():
	form = UploadTag()

	if form.validate_on_submit():
		names = form.name.data.split(',')
		for name in names:
			tag = Tags.query.filter_by(name=name).first()
			if not tag:
				db.session.add(Tags(name=name))
				db.session.commit()

		flash('tags uploaded')

		return redirect(url_for('admin.upload_tag'))

	return render_template('admin/upload_tag.html', form=form)

from . import deletions
from . import json
from . import update
from . import login

