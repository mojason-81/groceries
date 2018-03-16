from flask import jsonify, request, url_for, g
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User, Grocery
from app.api import bp

@bp.route('/users/<int:id>/groceries', methods=['GET'])
@token_auth.login_required
def get_groceries(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Grocery.to_collection_dict(Grocery.query,
                                      g.current_user.id,
                                      page,
                                      per_page,
                                      'api.get_groceries')
    return jsonify(data)

@bp.route('/users/<int:user_id>/groceries/<int:id>', methods=['GET'])
@token_auth.login_required
def get_grocery(user_id, id):
    # FIXME: only return grocery if it belongs to user.
    return jsonify(Grocery.query.get_or_404(id).to_dict())
