from flask import jsonify, request, url_for, g
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User, Meal
from app.api import bp

@bp.route('/users/<int:id>/meals', methods=['GET'])
@token_auth.login_required
def get_meals(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Meal.to_collection_dict(Meal.query,
                                      g.current_user.id,
                                      page,
                                      per_page,
                                      'api.get_meals')
    return jsonify(data)

@bp.route('/users/<int:user_id>/meals/<int:id>', methods=['GET'])
@token_auth.login_required
def get_meal(user_id, id):
    # FIXME: only return meal if it belongs to user
    return jsonify(Meal.query.get_or_404(id).to_dict())

