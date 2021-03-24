from flask import jsonify
from database import Users, Posts, Image, Tags
from .blueprint import admin
from flask_login import fresh_login_required

@admin.route('/posts')
@fresh_login_required
def get_posts():
	posts = Posts.query.all()
	data = []
	for post in posts:
		data.append({
			'id': post.id,
			'title': post.title,
			'content': post.content,
			'image_name': post.image_name,
			'tags': [x.name for x in post.tags],
			'author': post.author.username
			})

	return jsonify(data)

@admin.route('/images')
@fresh_login_required
def get_images():
	images = Image.query.all()
	data = []
	for image in images:
		data.append({
			'name': image.name,
			})

	return jsonify(data)

@admin.route('/tags')
@fresh_login_required
def get_tags():
	tags = Tags.query.all()
	data = []
	for tag in tags:
		data.append({
			'name': tag.name,
			})

	return jsonify(data)
	