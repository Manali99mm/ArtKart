from flask import Flask
from dotenv import load_dotenv
from config.config import ConfigClass
from flask_jwt_extended import JWTManager
import os
from pymongo import MongoClient
from routes.auth_bp import auth_bp
from routes.user_bp import user_bp
from models import User

load_dotenv()

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

try:
    client = MongoClient(os.environ.get('MONGO_URI'))
    db = client[os.environ.get('MONGO_DBNAME')]
    if 'users' not in db.list_collection_names():
        ConfigClass.create_collection('users', User.userSchema)
except Exception as ex:
    raise Exception(ex)

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def index():
    return 'Setup success!'

if __name__ == '__main__':
    app.run(debug=True)