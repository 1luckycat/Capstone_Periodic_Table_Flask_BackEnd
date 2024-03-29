from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# internal imports
from config import Config
from .models import db
from .helpers import JSONEncoder
from .api.routes import api


app = Flask(__name__)

app.config.from_object(Config)
jwt = JWTManager(app)


app.register_blueprint(api)


db.init_app(app)
migrate = Migrate(app, db)
app.json_encoder = JSONEncoder
cors = CORS(app)