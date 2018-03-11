from flask import jsonify, request, url_for, g
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User, Menu
from app.api import bp

@bp.route('/users/<int:id>/menus', methods=['GET'])
@token_auth.login_required
def get_menus(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Menu.to_collection_dict(Menu.query,
                                      g.current_user.id,
                                      page,
                                      per_page,
                                      'api.get_menus')
    return jsonify(data)

@bp.route('/users/<int:user_id>/menus/<int:id>', methods=['GET'])
@token_auth.login_required
def get_menu(user_id, id):
    # FIXME: only return menu if it belongs to user
    return jsonify(Menu.query.get_or_404(id).to_dict())
