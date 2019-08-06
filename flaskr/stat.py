from flask import (
    Blueprint, render_template
)

bp = Blueprint('stat', __name__)


@bp.route('/general', methods=('GET',))
def general():
    return render_template('stats/general_stats.html')


@bp.route('/<int:user_id>', methods=('GET',))
def user(user_id):
    return render_template('stats/user_stats.html')
