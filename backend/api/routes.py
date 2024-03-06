from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
import requests

# internal imports
from backend.models import Element, User, db, element_schema, elements_schema, element_table_schema

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
@jwt_required()
def get_periodic_table():
    # elements = Element()
    # elements_data = elements.api_call()
    # print(elements_data)
    # response = elements_schema.dump(elements_data)
    # return jsonify(response)

# THIS ONE WORKS TO GET ALL DATA
    # r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
    # if r.status_code == 200:
    #     data = r.json()
    #     elements = data['data']

    # return elements


# THIS ONE WORKS TO GET SPECIFIC DATA FOR THE PERIODIC TABLE
    listy = []
    r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
    if r.status_code == 200:
            data = r.json()
        
            for item in data['data']:
                element = {
                    'name': item['name'], 
                    'symbol': item['symbol'],
                    'atomic_number' : item['number'],
                    'xpos': item['xpos'],
                    'ypos': item['ypos'],
                    'category': item['category']
                }

                listy.append(element)
            return jsonify(listy)
    

    # table_elements = Element.query.all()
    # response = element_table_schema.dump(table_elements)
    # return jsonify(response)



# !!!---- for api can be a dictionary, but needs to be an object when adding to the database in routes due to ROM
@api.route('/study', methods=['GET'])
@jwt_required()
def get_info():
     
    all_elements = Element.query.all()
    response = elements_schema.dump(all_elements)
    return jsonify(response)



@api.route('/study/create/<user_id>', methods=['POST'])
@jwt_required()
def add_element(user_id):
    data = request.json
    name = data['name']
    notes = data['notes']
    print(name)
    ele = Element(name, notes)
    
    db.session.add(ele)
    db.session.commit()    
    return jsonify(element_schema.dump(ele))



@api.route('/study/delete/<element_id>', methods=['DELETE'])
@jwt_required()
def delete_element(element_id):

    # since delete, dont need to pass in data
    # data = request.json
    # element_id = data['element_id']
    element = Element.query.get(element_id)
    db.session.delete(element)
    db.session.commit()

    return {
          'status': 200,
          'message': 'Order was deleted successfully.'
     }



@api.route('/study/update/<element_id>', methods=['PUT'])
@jwt_required()
def update_notes(element_id):
     data = request.json
     notes = data['notes']

     new_notes = Element.query.get(element_id)
     new_notes.update_notes(notes)
     db.session.commit()

     return {
          'status': 200,
          'message': 'Notes updated!'
     }





# DIFFERENT TRY FOR GET ELEMENT ROUTE:
    # listy = []
    # r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
    # if r.status_code == 200:
    #     data = r.json()

    # for item in data['data']:
    #     # if name == item['name'].lower():
    #         element = {
    #             'name': item['name'], 
    #             'symbol': item['symbol'],
    #             'atomic number' : item['number'],
    #             'phase' : item['phase'],
    #             'atomic mass' : item['atomic_mass'],
    #             'summary': item['summary'],
    #             'boiling point': item['boil'],
    #             'melting point': item['melt']
                
    #         }

    #         listy.append(element)

    # return jsonify(listy)





# DIFFERENT TRYS FOR CREATE ELEMENT ROUTE:
    # data = request.json
    # element_list = data['name']

    # user = User.query.filter(User.user_id == user_id).first()
    # if not user:
    #      user = User()  # <---user_id inside?
    #      db.session.add(user)

    # element = Element()
    # db.session.add(element)

    # for ele in element_list:
    #     element = Element(ele['name'], ele['symbol'], ele['number'], ele['phase'], 
    #                       ele['atomic_mass'], ele['summary'], ele['boil'], ele['melt'])
        
    #     db.session.add(element)
    #     db.session.commit()
        
    # return {
    #          'status': 200,
    #          'message': 'New element added!'
    #     }



#  GETTING SOME INFO BACK, BUT GETTING ELEMENT_ID ERROR (Need to input info in insomnia tho)
    # element = Element(name = request.json['name'], symbol = request.json['symbol'], 
    #                   atomic_number = request.json['atomic number'], phase = request.json['phase'], 
    #                   atomic_mass = request.json['atomic mass'], summary = request.json['summary'], 
    #                   boil = request.json['boiling point'], melt = request.json['melting point'])
    # db.session.add(element)
    # db.session.commit()
    # return element
     

#  THIS ONE NEED ALL INPUTS IN INSOMIA THO
    # data = request.json
    # name = data['name']
    # symbol = data['symbol']
    # atomic_number = data['number']
    # phase = data['phase']
    # atomic_mass = data['atomic_mass']
    # summary = data['summary']
    # boil = data['boil']
    # melt = data['melt']

    # new_element = Element(name, symbol, atomic_number, phase, atomic_mass, summary, boil, melt)

    # db.session.add(new_element)
    # db.session.commit()

    # return jsonify(element_schema.dump(new_element))