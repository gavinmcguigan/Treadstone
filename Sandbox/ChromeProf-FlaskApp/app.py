from flask import Flask 
from flask_restful import Api 
from db import db
import os
from gevent.pywsgi import WSGIServer
import logging 
from resources.files import ProfileZip
from resources.email import Email, Emails
from gevent import monkey
monkey.patch_all()

# logging.basicConfig(filename="profiles.log", level=logging.DEBUG,
#                     format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///profiles.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'I am a secret key'

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)

api.add_resource(Email, '/email/<string:email>')
api.add_resource(Emails, '/emails')
api.add_resource(ProfileZip, '/profile')


if __name__ == '__main__':
    db.init_app(app)
    # app.debug = True
    #app.run(port=5002, debug=True, host="0.0.0.0")
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()