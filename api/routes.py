from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import Element, elements_schema

# internal imports
from backend.models import Element, db, element_schema, elements_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/token', methods=['GET', 'POST'])
def token():
    data = request.json
    if data: 
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client ID.  Please try again.'
        }
    

@api.route('/periodictable', methods=['GET'])
def get_periodic_table():
    elements = Element()
    elements_data = elements.api_call()
    response = elements_schema.dump(elements_data)

    return jsonify(response)