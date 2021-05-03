from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


#Application object
app = Flask(__name__)

#Configurations
app.config.from_object('config')

#SQL Alchemy database object
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

from app.mod_auth.controllers import mod_auth as auth_module

app.register_blueprint(auth_module)

db.create_all()
