from datetime import datetime

from flask import (
    Blueprint, render_template
)

from flaskr import db
from flaskr.models import Post, User

bp = Blueprint('stat', __name__)


@bp.route('/general', methods=('GET',))
def general():
    oldest_post_date = Post.query.order_by(Post.created.asc()).first().created
    days = (datetime.now() - oldest_post_date).days
    if days == 0:
        days = 1

    posts_count = Post.query.count()
    if posts_count == 0:
        posts_count = 1

    post_titles = list(map((lambda i: i[0]), db.session.query(Post.title).all()))
    posts_bodies = list(map((lambda i: i[0]), db.session.query(Post.body).all()))
    all_texts = " ".join(post_titles + posts_bodies)
    words_count = len(all_texts.split())
    if words_count == 0:
        words_count = 1

    chars_count = sum(db.session.execute("SELECT SUM(LENGTH(title) + LENGTH(body)) FROM Post").first())
    if chars_count == 0:
        chars_count = 1

    users_count = User.query.count()
    if users_count == 0:
        users_count = 1

    return render_template(
        'stats/general_stats.html',
        days=days,
        posts_count=posts_count,
        users_count=users_count,
        words_count=words_count,
        chars_count=chars_count
    )


@bp.route('/<int:user_id>', methods=('GET',))
def user(user_id):
    username = User.query.get_or_404(user_id).username

    user_created = User.query.get_or_404(user_id).created
    days = (datetime.now() - user_created).days
    if days == 0:
        days = 1

    user_posts_count = Post.query.filter(Post.author_id == user_id).count()
    if user_posts_count == 0:
        user_posts_count = 1

    post_titles = list(map((lambda i: i[0]), db.session.query(Post.title).filter(Post.author_id == user_id).all()))
    posts_bodies = list(map((lambda i: i[0]), db.session.query(Post.body).filter(Post.author_id == user_id).all()))
    all_user_texts = " ".join(post_titles + posts_bodies)
    user_words_count = len(all_user_texts.split())
    if user_words_count == 0:
        user_words_count = 1

    user_chars_count = db.session.execute(
        "SELECT SUM(LENGTH(title) + LENGTH(body)) FROM Post WHERE author_id = {0}".format(user_id)
    ).first()[0]
    if user_chars_count == 0:
        user_chars_count = 1

    return render_template(
        'stats/user_stats.html',
        username=username,
        user_created=user_created,
        days=days,
        posts_count=user_posts_count,
        words_count=user_words_count,
        chars_count=user_chars_count
    )
