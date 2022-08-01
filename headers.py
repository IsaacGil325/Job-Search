from flask import Flask
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
bcrypt = Bcrypt(app)
proxied = FlaskBehindProxy(app)


app.config['SECRET_KEY'] = 'f8ab5567ef84a9ee5c1e3d86bb8b9ef9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobify.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"