from flask import jsonify, request, url_for, g
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User, Store
from app.api import bp

@bp.route('/users/<int:id>/stores', methods=['GET'])
@token_auth.login_required
def get_stores(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Store.to_collection_dict(Store.query,
                                      g.current_user.id,
                                      page,
                                      per_page,
                                      'api.get_stores')
    return jsonify(data)

@bp.route('/users/<int:user_id>/stores/<int:id>', methods=['GET'])
@token_auth.login_required
def get_store(user_id, id):
    # FIXME: only return store if it belongs to user
    return jsonify(Store.query.get_or_404(id).to_dict())

