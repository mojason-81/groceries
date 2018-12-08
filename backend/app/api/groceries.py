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

# May have to POST to /groceries and include the user id as form data
@bp.route('/users/<int:id>/groceries', methods=['POST'])
@token_auth.login_required
def create_grocery(id):
    data = request.get_json() or {}
    # FIXME: it's failing.  find out why
    if 'name' not in data:
        return bad_request('must include name field.')
    grocery = Grocery()
    grocery.from_dict(data)
    g.current_user.add_grocery(grocery)
    response = jsonify(grocery.to_dict())
    response.status_code = 201
    # TODO: Will grocery here get an id after commit() or do
    # I need to look it up again?
    response.headers['Location'] = url_for('api.get_grocery',
                                           user_id=g.current_user.id,
                                           id=grocery.id)
    return response

