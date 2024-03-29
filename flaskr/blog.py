from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.auth import login_required
from flaskr.models import Post

bp = Blueprint('blog', __name__)


def get_post(post_id, check_author=True):
    post = Post.query.get_or_404(post_id)

    if check_author and post.author != g.user:
        abort(403)

    return post


@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.session.add(Post(title=title, body=body, author=g.user))
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            post.modification = db.func.current_timestamp()
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    post = get_post(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
