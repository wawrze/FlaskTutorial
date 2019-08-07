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
    now = datetime.now()
    days = (now - oldest_post_date).days
    posts_count = Post.query.count()
    post_titles = list(map((lambda i: i[0]), db.session.query(Post.title).all()))
    posts_bodies = list(map((lambda i: i[0]), db.session.query(Post.body).all()))
    all_texts = " ".join(post_titles + posts_bodies)
    words_count = len(all_texts.split())
    chars_count = sum(db.session.execute("SELECT SUM(LENGTH(title) + LENGTH(body)) FROM Post").first())
    users_count = User.query.count()
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
    return render_template('stats/user_stats.html')
