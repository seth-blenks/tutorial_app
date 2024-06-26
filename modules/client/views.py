from flask import render_template, redirect, request, url_for, current_app, Response
from .blueprint import client
from database import Posts, Tags
from flask import abort

@client.route('/')
def homepage():
    return render_template('index.html')

@client.route('/favicon.ico')
def favicon():
    with current_app.open_resource('modules/client/assets/favicon.png') as wfile:
        content = wfile.read()
        return Response(content, mimetype='image/png')

@client.route('/contact')
def contact():
    return render_template('contact.html')

@client.route('/tutorials')
def tutorials():
    section_name = request.args.get('section')
    section = Tags.query.filter_by(name=section_name).first()

    page = request.args.get('page', 1, type=int)

    if not section:
        abort(404)

    pagination = Posts.query.filter(Posts.tags.any(name=section_name)).order_by(Posts.date.desc()).paginate(page=page, per_page=7, error_out=False)
    posts = pagination.items

    if not posts:
        abort(404)

    related_posts = []

    related_python = Posts.query.filter(Posts.tags.any(name='flask'))
    if related_python:
        related_posts.append(related_python.paginate(page=1, per_page=2).items)

    related_biology = Posts.query.filter(Posts.tags.any(name='biology'))
    if related_biology:
        related_posts.append(related_biology.paginate(page=1, per_page=2).items)

    tag_cloud = Tags.query.paginate(page=1, per_page=15, error_out=False).items

    return render_template('blog.html', posts=posts, others=related_posts, tag_cloud=tag_cloud)

@client.route('/tutorials/<title>')
def tutorials_read(title):
    post = Posts.query.filter_by(title=title).first()
    if not post:
        abort(404)

    related_posts = Posts.query.filter(Posts.tags.any(name=post.tags[0].name)).filter(Posts.id != post.id).paginate(page=1, per_page=4, error_out=False).items
    tag_cloud = Tags.query.paginate(page=1, per_page=15, error_out=False).items

    return render_template('blog-details.html', post=post, others=related_posts, tag_cloud=tag_cloud)

@client.app_errorhandler(404)
def file_not_found(e):
    return render_template('404.html'), 404
