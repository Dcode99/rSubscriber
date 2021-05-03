from app import db

class User(db.Model):

	__tablename__ = 'auth_user'

	id 		= db.Column(db.Integer, primary_key=True)
	date_created 	= db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified 	= db.Column(db.DateTime, default=db.func.current_timestamp(),
						onupdate=db.func.current_timestamp())
	name 		= db.Column(db.String(256), nullable=False)
	password 	= db.Column(db.String(192), nullable=False)

	#Constructor
	def __init__(self, name, password):
		self.name = name
		self.password = password

	def __repr__(self):
		return '<User %r' % (self.name)
