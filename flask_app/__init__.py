import os
from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key= os.environ['secret_key']
bcrypt = Bcrypt(app)

from flask_app.config.custom_templating_features import custom_template_filters
app.register_blueprint(custom_template_filters)