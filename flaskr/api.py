from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/demo', methods=['GET'])
def demo():
    return 'haha demo1'
