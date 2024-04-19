from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid 
from flask_marshmallow import Marshmallow
import requests


# internal import
from .helpers import get_table


db = SQLAlchemy()
ma = Marshmallow()


class Element(db.Model):
    element_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10))
    atomic_number = db.Column(db.Integer)
    phase = db.Column(db.String(30))
    atomic_mass = db.Column(db.Numeric(precision=10, scale=5))  
    # atomic_mass = db.Column(db.String(30))    <-----correct new way with other api
    summary = db.Column(db.String)
    boil = db.Column(db.Numeric(precision=10, scale=5))   
    melt = db.Column(db.Numeric(precision=10, scale=5))   
    # boil = db.Column(db.String(50))    <-----correct new way with other api
    # melt = db.Column(db.String(50))    <-----correct new way with other api
    category = db.Column(db.String(50))
    notes = db.Column(db.String)
    date_added = db.Column(db.DateTime, default = datetime.utcnow())
    user_id = db.Column(db.String, nullable=False)

    def __init__(self, name, user_id, notes = ""):
        self.element_id = self.set_id()
        self.name = name
        self.user_id = user_id
        self.symbol = None
        self.atomic_number = None
        self.phase = None
        self.atomic_mass = None
        self.summary = None
        self.boil = None
        self.melt = None
        self.category = None
        self.notes = notes
        # self.api_call()     <----- if using old way with render api

        # data = get_table()
        # if data:
        #     for item in data:
        #         if item['name'] == self.name:
        #             self.name = item['name']
        #             self.symbol = item['symbol']
        #             self.atomic_number = item['atomicNumber']
        #             self.phase = item['standardState']
        #             self.atomic_mass = item['atomicMass']
        #             self.summary = item['history']
        #             self.boil = item['boilingPoint']
        #             self.melt = item['meltingPoint']
        #             self.category = item['groupBlock']
                
        # else:
        #     print("Failed to fetch data from the API")
        data = get_table()
        if data:
            for item in data['data']:
                if item['name'] == self.name:
                    self.name = item['name']
                    self.symbol = item['symbol']
                    self.atomic_number = item['number']
                    self.phase = item['phase']
                    self.atomic_mass = item['atomic_mass']
                    self.summary = item['summary']
                    self.boil = item['boil']
                    self.melt = item['melt']
                    self.category = item['category']
                
        else:
            print("Failed to fetch data from the API")


        
# !!!---- for api can be a dictionary, but needs to be an object when adding to the database in routes due to ROM
    # def api_call(self):          <-------correct old way getting data from render.com
    #     listy = []
    #     r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
    #     if r.status_code == 200:
    #         data = r.json()
    #         # print(data)
            
    #     else:
    #         print(f"Check name: {r.status_code}")

    #     for item in data['data']:
    #         if item['name'] == self.name:
    #             self.name = item['name']
    #             self.symbol = item['symbol']
    #             self.atomic_number = item['number']
    #             self.phase = item['phase']
    #             self.atomic_mass = item['atomic_mass']
    #             self.summary = item['summary']
    #             self.boil = item['boil']
    #             self.melt = item['melt']
    #             self.category = item['category']
                
    #             element = {
    #                 'name': self.name, 
    #                 'symbol': self.symbol,
    #                 'atomic_number' : self.atomic_number,
    #                 'phase' : self.phase,
    #                 'atomic_mass' : self.atomic_mass,
    #                 'summary': self.summary,
    #                 'boiling_point': self.boil,
    #                 'melting_point': self.melt,
    #                 'category': self.category
    #             }
    #             listy.append(element)
    #     return listy                <------end of old way
            

    def set_id(self):
        return str(uuid.uuid4())
    
    def update_notes(self, notes):
        self.notes = notes
        return notes
    

    def getInfo(self, name):
        # data = get_table()
        # if data:
        #     for item in data:
        #         if name == item['name'].lower():
        #             self.name = item['name']
        #             self.symbol = item['symbol']
        #             self.atomic_number = item['atomicNumber']
        #             self.phase = item['standardState']
        #             self.atomic_mass = item['atomicMass']
        #             self.summary = item['history']
        #             self.boil = item['boilingPoint']
        #             self.melt = item['meltingPoint']
        #             self.category = item['groupBlock']

        #             return {
        #                 'name': self.name, 
        #                 'symbol': self.symbol,
        #                 'atomic_number' : self.atomic_number,
        #                 'phase' : self.phase,
        #                 'atomic_mass' : self.atomic_mass,
        #                 'summary': self.summary,
        #                 'boiling_point': self.boil,
        #                 'melting_point': self.melt,
        #                 'category': self.category
        #             }
                
        # else:
        #     print("Failed to fetch data from the API")
        #     return None
        data = get_table()
        if data:
            for item in data['data']:
                if name == item['name'].lower():
                    self.name = item['name']
                    self.symbol = item['symbol']
                    self.atomic_number = item['number']
                    self.phase = item['phase']
                    self.atomic_mass = item['atomic_mass']
                    self.summary = item['summary']
                    self.boil = item['boil']
                    self.melt = item['melt']
                    self.category = item['category']

                    return {
                        'name': self.name, 
                        'symbol': self.symbol,
                        'atomic_number' : self.atomic_number,
                        'phase' : self.phase,
                        'atomic_mass' : self.atomic_mass,
                        'summary': self.summary,
                        'boiling_point': self.boil,
                        'melting_point': self.melt,
                        'category': self.category
                    }
                
        else:
            print("Failed to fetch data from the API")
            return None


    # def getInfo(self, name):        <-------correct old way getting data from render.com
    #     listy = []
    #     r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
    #     if r.status_code == 200:
    #         data = r.json()

    #     for item in data['data']:
    #         if name == item['name'].lower():
    #             self.name = item['name']
    #             self.symbol = item['symbol']
    #             self.atomic_number = item['number']
    #             self.phase = item['phase']
    #             self.atomic_mass = item['atomic_mass']
    #             self.summary = item['summary']
    #             self.boil = item['boil']
    #             self.melt = item['melt']
    #             self.category = item['category']
                
    #             element = {
    #                 'name': self.name, 
    #                 'symbol': self.symbol,
    #                 'atomic_number' : self.atomic_number,
    #                 'phase' : self.phase,
    #                 'atomic_mass' : self.atomic_mass,
    #                 'summary': self.summary,
    #                 'boiling_point': self.boil,
    #                 'melting_point': self.melt,
    #                 'category': self.category
    #             }

    #             listy.append(element)

    #     return listy             <------- end of old way
    #     # If not having to add to a list
    #     # return element
    

    def __repr__(self):
        return f"<Element: {self.name}>"
    


class ElementSchema(ma.Schema):
    class Meta:
        fields = ['element_id', 'name', 'symbol', 'atomic_number', 'phase', 'atomic_mass', 'summary', 'boil', 'melt', 'category', 'notes']

element_schema = ElementSchema()
elements_schema = ElementSchema(many=True)


class ElementTableSchema(ma.Schema):
    class Meta:
        fields = ['name', 'symbol', 'atomic_number']

element_table_schema = ElementSchema(many=True)

