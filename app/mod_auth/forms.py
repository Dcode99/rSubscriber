from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required


#Login form

class LoginForm(Form):
	name = TextField('User ID', [Required(message='')])
	password = PasswordField('Password', [Required(message='')])
