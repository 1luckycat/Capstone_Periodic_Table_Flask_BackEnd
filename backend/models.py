from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid 
from flask_marshmallow import Marshmallow
import requests


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    elements = db.relationship('Element', lazy=True, backref='user')


    def __init__(self, username, email, password):
        self.user_id = self.set_id()
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"
    


class Element(db.Model):
    element_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10))
    atomic_number = db.Column(db.Integer)
    phase = db.Column(db.String(30))
    atomic_mass = db.Column(db.Numeric(precision=10, scale=5))
    summary = db.Column(db.String)
    boil = db.Column(db.Numeric(precision=10, scale=5))
    melt = db.Column(db.Numeric(precision=10, scale=5))
    notes = db.Column(db.String)
    date_added = db.Column(db.DateTime, default = datetime.utcnow())
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))

    def __init__(self, name):
        self.element_id = self.set_id()
        self.name = name
        self.symbol = None
        self.atomic_number = None
        self.phase = None
        self.atomic_mass = None
        self.summary = None
        self.boil = None
        self.melt = None
        self.notes = None
        self.api_call()
        
# !!!---- for api can be a dictionary, but needs to be an object when adding to the database in routes due to ROM
    def api_call(self):
        listy = []
        r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
        if r.status_code == 200:
            data = r.json()
            # print(data)
            
        else:
            print(f"Check name: {r.status_code}")

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
                
                element = {
                    'name': self.name, 
                    'symbol': self.symbol,
                    'atomic number' : self.atomic_number,
                    'phase' : self.phase,
                    'atomic mass' : self.atomic_mass,
                    'summary': self.summary,
                    'boiling point': self.boil,
                    'melting point': self.melt
                }
                listy.append(element)
        return listy
            

    def set_id(self):
        return str(uuid.uuid4())
    
    def update_notes(self, notes):
        self.notes = notes
        return notes
    

    def getInfo(self, name):
        listy = []
        r = requests.get(f"https://kineticzephyr.onrender.com/periodictable")
        if r.status_code == 200:
            data = r.json()

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
                
                element = {
                    'name': self.name, 
                    'symbol': self.symbol,
                    'atomic number' : self.atomic_number,
                    'phase' : self.phase,
                    'atomic mass' : self.atomic_mass,
                    'summary': self.summary,
                    'boiling point': self.boil,
                    'melting point': self.melt
                }

                listy.append(element)

        return listy
        # If not having to add to a list
        # return element
    

    def __repr__(self):
        return f"<Element: {self.name}>"
    


class ElementSchema(ma.Schema):
    class Meta:
        fields = ['element_id', 'name', 'symbol', 'atomic_number', 'phase', 'atomic_mass', 'summary', 'boil', 'melt', 'notes']

element_schema = ElementSchema()
elements_schema = ElementSchema(many=True)


class ElementTableSchema(ma.Schema):
    class Meta:
        fields = ['name', 'symbol', 'atomic_number']

element_table_schema = ElementSchema(many=True)



# test = Element()
# print(test.api_call())
# print(test.getInfo('iron'))