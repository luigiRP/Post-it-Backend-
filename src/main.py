 #flask
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, validation_username, validation_email, validation_name, validation_password, validation_date
from admin import setup_admin
from models import db, User, Post, Social, Multimedia
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['POST'])
def add_user():
    data_user = request.get_json()
    valid_username = validation_username(data_user)
    valid_email = validation_email(data_user)
    valid_name = validation_name(data_user)
    valid_password = validation_password(data_user)
    if valid_username == True and valid_email == True and valid_name == True and valid_password == True:
        User.post_user(data_user)
        return "Successful registration", 200
    else:
        return "Error", 303

@app.route('/socials', methods=['POST'])
def add_social():
    data_social = request.get_json()
    Social.post_social(data_social)
    return "Successful registration", 200

@app.route('/posts', methods=['POST'])
def add_post():
    posting = request.get_json()
    valid_date = validation_date(posting)
    if valid_date == True:
        Post.post_posts(posting)
        return "Successful registration", 200
    else:
        return "Error", 303
    
@app.route('/multimedias', methods=['POST'])
def add_multimedia():
    data_multimedia = request.get_json()
    Multimedia.post_multimedia(data_multimedia)
    return "Successful registration", 200
    
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)