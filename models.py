from app import db

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))

	def __init__(self, symbol, name):
		self.symbol = symbol
		self.name = name

# class History(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	date = db.Column(db.Date)
# 	open_price = db.Column(db.Float)
# 	high_price = db.Column(db.Float)
# 	low_price = db.Column(db.Float)
# 	close_price = db.Column(db.Float)
# 	volum = db.Column(db.Integer)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	username = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password


