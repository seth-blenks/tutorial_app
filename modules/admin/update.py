from flask import render_template, flash, redirect, url_for, current_app
from forms import UpdatePostForm
from database import Posts, db
from .blueprint import admin
from flask import request, abort
from flask_login import fresh_login_required


@admin.route('/update', methods=['GET','POST'])
@fresh_login_required
def update():
	form = UpdatePostForm()

	post_id = request.args.get('id')
	current_app.logger.debug(post_id)
	post = Posts.query.get(int(post_id))

	current_app.logger.debug(post)

	if not post:
		abort(400)

	tags = ",".join([x.name for x in post.tags])

	current_app.logger.debug(tags)


	if form.validate_on_submit():
		current_app.logger.info('form validated')

		title = form.title.data
		other_post = Posts.query.filter(Posts.title == title).filter(Posts.id != post.id).first()
		

		if other_post:
			flash('title already taken')
			current_app.logger.debug(f'other post id: {other_post.id} \n other post title: {other_post.title}')
			return redirect(url_for('admin.update',id=post.id))

		post.title = title
		post.content = form.content.data
		post.image_name = form.image_name.data
		post.add_tag(form.tags.data)

		db.session.add(post)
		db.session.commit()

		current_app.logger.debug('post updated successfully')

		flash('upload successful')
		return redirect(url_for('admin.homepage'))
	else:
		for field, errors in form.errors.items():
			for error in errors:
				current_app.logger.info(f'field name: {field.name}\n field error: {error}')

	return render_template('admin/update_post.html', post=post, form=form, tags=tags)